import json

import httpx
import pytest

import main as cli
from reviewer.diffparse import parse_diff
from reviewer.ghpost import post_review
from reviewer.report import (FINDINGS_SCHEMA, Finding, Report, build_review_payload, exit_code,
                             parse_report, render_json, render_markdown)
from reviewer.sources import SourceError
from conftest import EXAMPLES, FakeClient, finding, json_resp


def rep(*sevs):
    return Report("sum", [Finding("a.py", 1, s, "bug", "m", "s") for s in sevs])


def test_schema_enums_match_spec():
    item = FINDINGS_SCHEMA["properties"]["findings"]["items"]
    assert item["properties"]["category"]["enum"] == ["bug", "security", "performance", "style", "test"]
    assert set(item["required"]) == set(item["properties"]) and item["additionalProperties"] is False
    assert {"file", "line", "severity", "category", "message", "suggestion"} == set(item["properties"])


@pytest.mark.parametrize("sevs,fail_on,code", [
    ([], "high", 0), (["low", "medium"], "high", 0), (["high"], "high", 1), (["critical"], "high", 1),
    (["low"], "low", 1), (["critical"], "none", 0), (["info"], "critical", 0)])
def test_exit_codes(sevs, fail_on, code):
    assert exit_code(rep(*sevs), fail_on) == code


def test_markdown_sorted_by_severity_and_clean():
    r = parse_report(json.dumps({"summary": "s", "findings": [
        finding(severity="low", message="minor", line=3),
        finding(severity="critical", message="\x1b[31mevil\x1b[0m"),
        finding(severity="medium", line=0, suggestion="")]}))
    md = render_markdown(r)
    assert md.index("CRITICAL") < md.index("MEDIUM") < md.index("LOW")
    assert "\x1b" not in md and "`app/db.py:15`" in md and "`app/db.py`" in md
    assert "1 critical" in md and render_markdown(Report("none", [])).endswith("No findings.")
    assert json.loads(render_json(r))["findings"][0]["severity"] == "critical"


def test_review_payload_inline_vs_body(sample_diff):
    r = Report("sum", [Finding("app/db.py", 15, "high", "security", "SQLi", "fix"),
                       Finding("app/db.py", 1, "low", "style", "outside diff", ""),
                       Finding("missing.py", 2, "low", "style", "nofile", "")])
    p = build_review_payload(r, parse_diff(sample_diff), "sha1")
    assert p["event"] == "COMMENT" and p["commit_id"] == "sha1"
    assert [(c["path"], c["line"], c["side"]) for c in p["comments"]] == [("app/db.py", 15, "RIGHT")]
    assert "outside diff" in p["body"] and "nofile" in p["body"]


def test_post_review_requires_token_and_posts():
    with pytest.raises(SourceError, match="GITHUB_TOKEN"):
        post_review("o", "r", 1, {}, None)
    seen = {}

    def handler(req):
        seen["req"] = req
        return httpx.Response(200, json={"html_url": "https://x/y"})

    url = post_review("o", "r", 7, {"event": "COMMENT"}, "tok",
                      client=httpx.Client(transport=httpx.MockTransport(handler)))
    assert url == "https://x/y" and seen["req"].url.path == "/repos/o/r/pulls/7/reviews"
    assert json.loads(seen["req"].content) == {"event": "COMMENT"}


def run_cli(args, client=None, capsys=None):
    code = cli.main(args, client=client)
    return code, capsys.readouterr()


def base_args(*extra):
    return ["--diff", str(EXAMPLES / "sample.diff"), "--repo", str(EXAMPLES / "sample_repo"), *extra]


def test_cli_end_to_end_exit_1_on_high(capsys):
    client = FakeClient(json_resp([finding()]))
    code, io = run_cli(base_args(), client, capsys)
    assert code == 1 and "SQL injection" in io.out and "usage:" in io.err and "estimate" in io.err


def test_cli_exit_0_when_below_threshold_and_json(capsys):
    client = FakeClient(json_resp([finding(severity="low")]))
    code, io = run_cli(base_args("--format", "json"), client, capsys)
    assert code == 0 and json.loads(io.out)["findings"][0]["severity"] == "low"


def test_cli_dry_run_makes_no_call(capsys):
    client = FakeClient()
    code, io = run_cli(base_args("--dry-run"), client, capsys)
    assert code == 0 and "no API call" in io.out and client.calls == []


def test_cli_errors(capsys, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert run_cli(base_args(), None, capsys)[0] == 2                       # no key
    assert run_cli(["--git-range=--output=x"], FakeClient(), capsys)[0] == 2
    assert run_cli(["--diff", "/nonexistent.diff"], FakeClient(), capsys)[0] == 2
    assert run_cli(base_args("--post"), FakeClient(), capsys)[0] == 2       # --post needs --pr
    from conftest import stop_resp
    assert run_cli(base_args(), FakeClient(stop_resp("refusal")), capsys)[0] == 3


def test_cli_pr_defaults_to_dry_run_and_never_posts(monkeypatch, capsys):
    monkeypatch.setattr(cli, "fetch_pr", lambda *a, **k: ((EXAMPLES / "sample.diff").read_text(), "sha9"))
    called = []
    monkeypatch.setattr(cli, "post_review", lambda *a, **k: called.append(1))
    code, io = run_cli(["--pr", "o/r#5", "--repo", str(EXAMPLES / "sample_repo")],
                       FakeClient(json_resp([finding()])), capsys)
    assert code == 1 and not called and "DRY RUN" in io.err and '"commit_id": "sha9"' in io.err
    code, io = run_cli(["--pr", "o/r#5", "--post", "--repo", str(EXAMPLES / "sample_repo")],
                       FakeClient(json_resp([finding()])), capsys)
    assert called == [1]
