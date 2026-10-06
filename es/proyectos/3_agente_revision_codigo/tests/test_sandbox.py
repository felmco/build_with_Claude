import os

import pytest

from reviewer.sandbox import Sandbox, SandboxError
from reviewer.diffparse import parse_diff


def test_read_file_with_line_range(repo):
    out = Sandbox(repo).read_file("app/a.py", 3, 5)
    assert "lines 3-5 of 10" in out and "    3| line3" in out and "line6" not in out


@pytest.mark.parametrize("bad", ["../etc/passwd", "app/../../x", "/etc/passwd", "~/x", "", "a\x00b"])
def test_path_traversal_and_absolute_rejected(repo, bad):
    with pytest.raises(SandboxError):
        Sandbox(repo).read_file(bad)


def test_symlink_escape_rejected(repo, tmp_path_factory):
    outside = tmp_path_factory.mktemp("outside") / "secret.txt"
    outside.write_text("top secret")
    os.symlink(outside, repo / "app" / "link.txt")
    os.symlink(outside.parent, repo / "linkdir")
    sb = Sandbox(repo)
    with pytest.raises(SandboxError, match="escapes"):
        sb.read_file("app/link.txt")
    with pytest.raises(SandboxError, match="escapes"):
        sb.read_file("linkdir/secret.txt")
    assert "link.txt" not in sb.list_files() and "top secret" not in sb.grep("secret")


def test_size_limit_and_binary(repo):
    (repo / "big.txt").write_text("x" * 500)
    (repo / "bin.dat").write_bytes(b"\x00\x01\x02")
    sb = Sandbox(repo, max_file_bytes=100)
    with pytest.raises(SandboxError, match="larger"):
        sb.read_file("big.txt")
    with pytest.raises(SandboxError, match="binary"):
        Sandbox(repo).read_file("bin.dat")


def test_read_lines_capped(repo):
    (repo / "long.txt").write_text("\n".join(str(i) for i in range(1000)))
    out = Sandbox(repo, max_read_lines=20).read_file("long.txt")
    assert "lines 1-20 of 1000" in out


def test_secret_files_denied_and_hidden(repo):
    sb = Sandbox(repo)
    with pytest.raises(SandboxError, match="denied"):
        sb.read_file(".env")
    assert ".env" not in sb.list_files() and ".git" not in sb.list_files()
    assert "SECRET" not in sb.grep("SECRET")


def test_grep_finds_caps_and_rejects_bad_regex(repo):
    sb = Sandbox(repo)
    assert "app/b.txt:1: hello needle" in sb.grep("needle")   # .git/config skipped
    assert ".git" not in sb.grep("needle")
    assert sb.grep("NEEDLE", ignore_case=True).startswith("app/b.txt")
    assert sb.grep("zzz") == "(no matches)"
    with pytest.raises(SandboxError, match="invalid regex"):
        sb.grep("(")
    with pytest.raises(SandboxError):
        sb.grep("a" * 300)
    assert "stopped at 3 matches" in Sandbox(repo, max_grep_matches=3).grep("line")


def test_list_files_capped(repo):
    for i in range(10):
        (repo / f"f{i}.txt").write_text("x")
    assert "capped at 5" in Sandbox(repo, max_list_entries=5).list_files()


def test_run_tool_dispatch_and_unknown(repo):
    sb = Sandbox(repo)
    assert "line1" in sb.run_tool("read_file", {"path": "app/a.py"})
    for name, args in [("rm_rf", {}), ("read_file", {"bogus": 1}), ("read_file", {})]:
        with pytest.raises(SandboxError):
            sb.run_tool(name, args)


def test_get_diff_hunk(sample_sandbox):
    out = sample_sandbox.get_diff_hunk("app/db.py", 15)
    assert "search_users" in out
    with pytest.raises(SandboxError):
        sample_sandbox.get_diff_hunk("app/other.py")
    with pytest.raises(SandboxError):
        sample_sandbox.get_diff_hunk("app/db.py", 999)


def test_parse_diff_visible_lines(sample_diff):
    files = parse_diff(sample_diff)
    assert set(files) == {"app/db.py", "app/pagination.py"}
    assert {14, 15, 16}.issubset(files["app/db.py"].visible_lines())
    assert 7 in files["app/pagination.py"].visible_lines()
