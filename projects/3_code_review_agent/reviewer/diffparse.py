"""Minimal unified-diff parser.

We need it for two things: the get_diff_hunk tool, and deciding which
(file, line) pairs GitHub will accept for inline review comments (only lines
visible in the diff on the RIGHT/new side).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


@dataclass
class Hunk:
    new_start: int
    new_count: int
    lines: list[str] = field(default_factory=list)
    visible_new_lines: set[int] = field(default_factory=set)  # added + context
    path: str = ""

    @property
    def text(self) -> str:
        return f"--- {self.path} (hunk starting at new line {self.new_start})\n" + "\n".join(self.lines)


@dataclass
class DiffFile:
    path: str
    hunks: list[Hunk] = field(default_factory=list)

    def visible_lines(self) -> set[int]:
        out: set[int] = set()
        for h in self.hunks:
            out |= h.visible_new_lines
        return out


def hunks_for(df: DiffFile, line=None) -> list[Hunk]:
    if line is None:
        return df.hunks
    try:
        n = int(line)
    except (TypeError, ValueError):
        return []
    return [h for h in df.hunks if h.new_start <= n < h.new_start + max(h.new_count, 1)]


def parse_diff(text: str) -> dict[str, DiffFile]:
    files: dict[str, DiffFile] = {}
    cur: DiffFile | None = None
    hunk: Hunk | None = None
    old_left = new_left = 0
    new_no = 0
    for raw in text.splitlines():
        if hunk is not None and (old_left > 0 or new_left > 0):
            # inside a hunk: the counts decide where it ends, so lines such as
            # "--- foo" (a removed line starting with "-- ") are not misread as headers
            tag = raw[:1]
            if tag == "\\":
                continue
            hunk.lines.append(raw)
            if tag == "+":
                hunk.visible_new_lines.add(new_no); new_no += 1; new_left -= 1
            elif tag == "-":
                old_left -= 1
            else:
                hunk.visible_new_lines.add(new_no); new_no += 1; new_left -= 1; old_left -= 1
            continue
        if raw.startswith("diff --git "):
            cur, hunk = None, None
        elif raw.startswith("+++ "):
            name = raw[4:].split("\t")[0].strip()
            if name != "/dev/null":
                path = name[2:] if name.startswith("b/") else name
                cur = files.setdefault(path, DiffFile(path))
        else:
            m = HUNK_RE.match(raw)
            if m and cur is not None:
                old_left = int(m.group(2) or 1)
                new_count = int(m.group(4) or 1)
                new_left, new_no = new_count, int(m.group(3))
                hunk = Hunk(new_no, new_count, [raw], path=cur.path)
                cur.hunks.append(hunk)
    return files
