import subprocess

import httpx
import pytest

from reviewer import sources
from reviewer.sources import SourceError, fetch_pr, git_range_diff, parse_pr_ref, validate_git_range


@pytest.mark.parametrize("ok", ["main..HEAD", "HEAD~3", "origin/main...feature/x", "abc1234..def5678", "v1.0"])
def test_valid_ranges(ok):
    assert validate_git_range(ok) == ok


@pytest.mark.parametrize("bad", ["--output=/tmp/x", "-p", "main..--exec=x", "a;rm -rf /", "a b", "$(id)..HEAD",
                                 "a`id`", "", "a..b..c", "main..", "a|b"])
def test_invalid_ranges(bad):
    with pytest.raises(SourceError):
        validate_git_range(bad)


def test_git_called_without_shell(monkeypatch):
    seen = {}

    def fake_run(cmd, **kw):
        seen.update(cmd=cmd, kw=kw)
        return subprocess.CompletedProcess(cmd, 0, b"diff --git a/x b/x\n", b"")

    monkeypatch.setattr(sources.subprocess, "run", fake_run)
    git_range_diff("main..HEAD", "/tmp")
    assert isinstance(seen["cmd"], list) and "shell" not in seen["kw"] and seen["kw"]["timeout"]
    assert seen["cmd"][-2:] == ["main..HEAD", "--"]


def test_git_range_real_repo(tmp_path):
    def git(*a):
        subprocess.run(["git", "-C", str(tmp_path), "-c", "user.email=a@b", "-c", "user.name=n", *a],
                       check=True, capture_output=True)
    git("init", "-q")
    (tmp_path / "f.txt").write_text("a\n")
    git("add", "."); git("commit", "-qm", "1")
    (tmp_path / "f.txt").write_text("a\nb\n")
    git("commit", "-qam", "2")
    assert "+b" in git_range_diff("HEAD~1..HEAD", str(tmp_path))
    with pytest.raises(SourceError, match="git diff failed"):
        git_range_diff("nope..HEAD", str(tmp_path))


def test_parse_pr_ref():
    assert parse_pr_ref("octo/repo-x#12") == ("octo", "repo-x", 12)
    for bad in ["octo/repo", "octo/repo#x", "a/../b#1", "http://x/y#1", "octo/repo#1; ls"]:
        with pytest.raises(SourceError):
            parse_pr_ref(bad)


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_fetch_pr_ok_sends_token_and_accept():
    seen = []

    def handler(req):
        seen.append(req)
        if "diff" in req.headers["accept"]:
            return httpx.Response(200, text="diff --git a/x b/x\n")
        return httpx.Response(200, json={"head": {"sha": "abc"}})

    diff, sha = fetch_pr("o", "r", 1, token="tok", client=_client(handler))
    assert diff.startswith("diff --git") and sha == "abc"
    assert seen[0].headers["authorization"] == "Bearer tok"
    assert str(seen[0].url) == "https://api.github.com/repos/o/r/pulls/1"


def test_fetch_pr_size_cap_and_http_error():
    big = lambda req: httpx.Response(200, content=b"x" * 5000)  # noqa: E731
    with pytest.raises(SourceError, match="larger"):
        fetch_pr("o", "r", 1, client=_client(big), limit=1000)
    with pytest.raises(SourceError, match="404"):
        fetch_pr("o", "r", 1, client=_client(lambda r: httpx.Response(404)))
