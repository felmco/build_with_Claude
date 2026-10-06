"""Read-only tools sandboxed to a repository root.

Lesson link: modules/module3_advanced_features/04_tool_best_practices.md
(tool design) and modules/module5_optimization/21_security.md.

The model decides *which* files to read, so every path it sends is untrusted
input. Rules enforced here:
  * paths are resolved with Path.resolve() (follows symlinks) and must stay
    inside the root -> blocks "../" traversal AND symlinks that point outside;
  * absolute paths and NUL bytes are rejected;
  * secrets-looking files (.env, keys) and VCS/vendor dirs are never served;
  * file size, line counts, output size and grep matches are all capped;
  * nothing here can write, delete, or execute anything.
Limits: grep uses Python `re`, so a hostile pattern can still backtrack badly;
we cap pattern and line length but do not time-limit it.
"""
from __future__ import annotations

import fnmatch
import os
import re
from pathlib import Path

from .diffparse import DiffFile, hunks_for


class SandboxError(Exception):
    """Raised for any refused or failed tool call (reported to the model)."""


SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv", ".tox"}
DENY_PATTERNS = (".env", ".env.*", "*.pem", "*.key", "id_rsa*", "id_ed25519*", "*.p12", ".netrc")


class Sandbox:
    def __init__(self, root, diff_files: dict[str, DiffFile] | None = None, *,
                 max_file_bytes=200_000, max_read_lines=300, max_output_chars=20_000,
                 max_grep_matches=50, max_list_entries=200, max_walk_files=5000):
        self.root = Path(root).resolve()
        if not self.root.is_dir():
            raise SandboxError(f"repo root is not a directory: {root}")
        self.diff_files = diff_files or {}
        self.max_file_bytes = max_file_bytes
        self.max_read_lines = max_read_lines
        self.max_output_chars = max_output_chars
        self.max_grep_matches = max_grep_matches
        self.max_list_entries = max_list_entries
        self.max_walk_files = max_walk_files

    # ---- path safety -------------------------------------------------
    def resolve(self, path) -> Path:
        if not isinstance(path, str) or not path.strip():
            raise SandboxError("path must be a non-empty string")
        if "\x00" in path:
            raise SandboxError("path contains NUL byte")
        if os.path.isabs(path) or path.startswith(("~", "\\")):
            raise SandboxError("absolute paths are not allowed; use a repo-relative path")
        candidate = (self.root / path).resolve()  # resolves symlinks and ".."
        try:
            candidate.relative_to(self.root)
        except ValueError:
            raise SandboxError("path escapes the repository root") from None
        return candidate

    def _denied(self, p: Path) -> bool:
        return any(fnmatch.fnmatch(p.name, pat) for pat in DENY_PATTERNS)

    def _rel(self, p: Path) -> str:
        return p.relative_to(self.root).as_posix()

    def _clip(self, text: str) -> str:
        if len(text) > self.max_output_chars:
            return text[: self.max_output_chars] + "\n...[output truncated]"
        return text

    def _readable_text(self, p: Path) -> str:
        if self._denied(p):
            raise SandboxError("access to this file type is denied")
        if not p.is_file():
            raise SandboxError("not a regular file")
        if p.stat().st_size > self.max_file_bytes:
            raise SandboxError(f"file larger than {self.max_file_bytes} bytes; use grep or a smaller range")
        data = p.read_bytes()
        if b"\x00" in data[:2048]:
            raise SandboxError("binary file")
        return data.decode("utf-8", errors="replace")

    def _walk(self, base: Path):
        n = 0
        for dirpath, dirnames, filenames in os.walk(base, followlinks=False):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS
                                 and not os.path.islink(os.path.join(dirpath, d)))
            for name in sorted(filenames):
                fp = Path(dirpath) / name
                if fp.is_symlink() or self._denied(fp):
                    continue
                n += 1
                if n > self.max_walk_files:
                    return
                yield fp

    # ---- tools ---------------------------------------------------------
    def read_file(self, path, start_line=1, end_line=None) -> str:
        p = self.resolve(path)
        lines = self._readable_text(p).splitlines()
        try:
            start = max(1, int(start_line))
            end = len(lines) if end_line is None else int(end_line)
        except (TypeError, ValueError):
            raise SandboxError("start_line/end_line must be integers") from None
        end = min(end, len(lines), start + self.max_read_lines - 1)
        if start > max(len(lines), 1) or end < start:
            raise SandboxError(f"line range out of bounds (file has {len(lines)} lines)")
        body = "\n".join(f"{i:>5}| {lines[i - 1]}" for i in range(start, end + 1))
        return self._clip(f"{self._rel(p)} lines {start}-{end} of {len(lines)}\n{body}")

    def list_files(self, directory=".") -> str:
        base = self.resolve(directory)
        if not base.is_dir():
            raise SandboxError("not a directory")
        out = []
        for fp in self._walk(base):
            out.append(self._rel(fp))
            if len(out) >= self.max_list_entries:
                out.append(f"...[listing capped at {self.max_list_entries} entries]")
                break
        return "\n".join(out) or "(no files)"

    def grep(self, pattern, path=".", glob=None, ignore_case=False) -> str:
        if not isinstance(pattern, str) or not pattern or len(pattern) > 200:
            raise SandboxError("pattern must be a string of 1-200 characters")
        try:
            rx = re.compile(pattern, re.IGNORECASE if ignore_case else 0)
        except re.error as e:
            raise SandboxError(f"invalid regex: {e}") from None
        base = self.resolve(path)
        files = [base] if base.is_file() else self._walk(base)
        hits: list[str] = []
        for fp in files:
            if glob and not fnmatch.fnmatch(fp.name, glob):
                continue
            try:
                text = self._readable_text(fp)
            except SandboxError:
                continue  # skip binary / huge / denied files silently
            for no, line in enumerate(text.splitlines(), 1):
                if rx.search(line[:500]):
                    hits.append(f"{self._rel(fp)}:{no}: {line[:200]}")
                    if len(hits) >= self.max_grep_matches:
                        hits.append(f"...[stopped at {self.max_grep_matches} matches]")
                        return self._clip("\n".join(hits))
        return self._clip("\n".join(hits)) or "(no matches)"

    def get_diff_hunk(self, path, line=None) -> str:
        if not isinstance(path, str):
            raise SandboxError("path must be a string")
        df = self.diff_files.get(path[2:] if path.startswith("./") else path)
        if df is None:
            raise SandboxError("file is not part of the diff under review")
        hunks = hunks_for(df, line)
        if not hunks:
            raise SandboxError("no hunk contains that line")
        return self._clip("\n\n".join(h.text for h in hunks))

    # ---- dispatch ------------------------------------------------------
    def run_tool(self, name: str, args: dict) -> str:
        """Execute one model-requested tool. Only these four names exist."""
        if not isinstance(args, dict):
            raise SandboxError("tool input must be an object")
        table = {"read_file": self.read_file, "list_files": self.list_files,
                 "grep": self.grep, "get_diff_hunk": self.get_diff_hunk}
        fn = table.get(name)
        if fn is None:
            raise SandboxError(f"unknown tool: {name}")
        try:
            return fn(**args)
        except TypeError as e:  # unexpected / missing argument names
            raise SandboxError(f"bad arguments: {e}") from None
        except OSError as e:
            raise SandboxError(f"I/O error: {e.__class__.__name__}") from None


TOOL_DEFS = [
    {"name": "read_file",
     "description": "Read a repo file (read-only) with line numbers. Use start_line/end_line to page; max 300 lines per call.",
     "input_schema": {"type": "object", "properties": {
         "path": {"type": "string", "description": "repo-relative path"},
         "start_line": {"type": "integer"}, "end_line": {"type": "integer"}},
         "required": ["path"], "additionalProperties": False}},
    {"name": "list_files",
     "description": "List files under a repo-relative directory (recursive, capped).",
     "input_schema": {"type": "object", "properties": {"directory": {"type": "string"}},
                      "additionalProperties": False}},
    {"name": "grep",
     "description": "Regex search (Python re syntax) over repo files. Returns path:line: text, capped at 50 matches.",
     "input_schema": {"type": "object", "properties": {
         "pattern": {"type": "string"}, "path": {"type": "string"},
         "glob": {"type": "string", "description": "filename glob, e.g. *.py"},
         "ignore_case": {"type": "boolean"}},
         "required": ["pattern"], "additionalProperties": False}},
    {"name": "get_diff_hunk",
     "description": "Return the diff hunk(s) of a changed file, optionally only the hunk containing a new-file line.",
     "input_schema": {"type": "object", "properties": {
         "path": {"type": "string"}, "line": {"type": "integer"}},
         "required": ["path"], "additionalProperties": False}},
]
