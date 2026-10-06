"""Where the diff comes from: a file, `git diff <range>`, or a GitHub PR.

Everything here treats its inputs as hostile: git is run WITHOUT a shell
(argument list), the range is validated first, and every source has a hard
byte cap so a huge diff cannot blow up memory or the token budget.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import httpx

MAX_DIFF_BYTES = 200_000  # ~50k tokens; bigger diffs should be reviewed in pieces
GITHUB_API = "https://api.github.com"
GITHUB_TIMEOUT = httpx.Timeout(20.0, connect=10.0)

# one side of a range: refs, SHAs, HEAD~2, v1.0, feature/x ... never leading "-"
_REF = r"[A-Za-z0-9_][A-Za-z0-9_./~^@{}:+-]{0,199}"
_REF_RE = re.compile(_REF)
_PR_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9-]{0,38})/([A-Za-z0-9_.-]{1,100})#(\d{1,9})$")


class SourceError(Exception):
    """Bad input or failed fetch; reported to the user (exit code 2)."""


def validate_git_range(rng: str) -> str:
    """Accept `a`, `a..b` or `a...b` where each side is a plain ref-like token."""
    ok = isinstance(rng, str)
    if ok:
        sep = "..." if "..." in rng else (".." if ".." in rng else None)
        parts = rng.split(sep) if sep else [rng]
        ok = len(parts) <= 2 and all(_REF_RE.fullmatch(x) and ".." not in x for x in parts)
    if not ok:
        raise SourceError(f"invalid git range: {rng!r} (expected e.g. main..HEAD)")
    return rng


def parse_pr_ref(ref: str) -> tuple[str, str, int]:
    m = _PR_RE.match(ref or "")
    if not m or m.group(2) in (".", ".."):
        raise SourceError(f"invalid PR reference: {ref!r} (expected owner/repo#123)")
    return m.group(1), m.group(2), int(m.group(3))


def _cap(data: bytes, limit: int) -> str:
    if len(data) > limit:
        raise SourceError(f"diff is larger than {limit} bytes; review a smaller range")
    return data.decode("utf-8", errors="replace")


def read_diff_file(path: str, limit: int = MAX_DIFF_BYTES) -> str:
    p = Path(path)
    try:
        if p.stat().st_size > limit:
            raise SourceError(f"diff file is larger than {limit} bytes")
        return _cap(p.read_bytes(), limit)
    except OSError as e:
        raise SourceError(f"cannot read diff file: {e.strerror}") from None


def git_range_diff(rng: str, repo: str = ".", limit: int = MAX_DIFF_BYTES) -> str:
    rng = validate_git_range(rng)
    # list form + no shell: the range can never be interpreted by a shell.
    cmd = ["git", "-C", repo, "diff", "--no-color", "--no-ext-diff", rng, "--"]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=30, check=False,
                              env={**os.environ, "GIT_PAGER": "cat"})
    except (OSError, subprocess.TimeoutExpired) as e:
        raise SourceError(f"git failed: {e.__class__.__name__}") from None
    if proc.returncode != 0:
        raise SourceError("git diff failed: " + proc.stderr.decode("utf-8", "replace").strip()[:300])
    return _cap(proc.stdout, limit)


def _gh_headers(accept: str, token: str | None) -> dict:
    h = {"Accept": accept, "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "code-review-agent"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def fetch_pr(owner: str, repo: str, number: int, token: str | None = None,
             client: httpx.Client | None = None, limit: int = MAX_DIFF_BYTES) -> tuple[str, str | None]:
    """Return (diff_text, head_sha). Works without a token for public repos."""
    own = client is None
    client = client or httpx.Client(timeout=GITHUB_TIMEOUT, follow_redirects=False)
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}"
    try:
        buf = bytearray()
        with client.stream("GET", url, headers=_gh_headers("application/vnd.github.diff", token)) as r:
            if r.status_code != 200:
                raise SourceError(f"GitHub returned HTTP {r.status_code} for {owner}/{repo}#{number}")
            for chunk in r.iter_bytes():
                buf += chunk
                if len(buf) > limit:  # stop downloading, do not buffer a giant body
                    raise SourceError(f"PR diff is larger than {limit} bytes")
        diff = _cap(bytes(buf), limit)
        head_sha = None
        meta = client.get(url, headers=_gh_headers("application/vnd.github+json", token))
        if meta.status_code == 200:
            head_sha = (meta.json().get("head") or {}).get("sha")
        return diff, head_sha
    except httpx.HTTPError as e:
        raise SourceError(f"GitHub request failed: {e.__class__.__name__}") from None
    finally:
        if own:
            client.close()
