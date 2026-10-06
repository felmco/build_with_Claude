import pytest

from reviewer.agent import Agent, ReviewError
from conftest import FakeClient, finding, json_resp, stop_resp, text_resp, tool_resp


def make(client, sandbox, **kw):
    return Agent(client, sandbox, **kw)


def test_direct_answer_no_tools(sample_sandbox):
    c = FakeClient(json_resp([finding()]))
    ag = make(c, sample_sandbox)
    rep = ag.review("DIFF")
    assert rep.findings[0].category == "security"
    kw = c.calls[0]
    assert kw["model"] == "claude-sonnet-5-5"
    assert kw["output_config"]["format"]["type"] == "json_schema"
    assert "temperature" not in kw and "tool_choice" not in kw
    assert "UNTRUSTED" in kw["system"]
    assert {t["name"] for t in kw["tools"]} == {"read_file", "list_files", "grep", "get_diff_hunk"}


def test_tool_loop_runs_tools_and_returns_one_user_message(sample_sandbox):
    c = FakeClient(
        tool_resp(("t1", "read_file", {"path": "app/db.py"}), ("t2", "grep", {"pattern": "paginate"})),
        json_resp([finding()]))
    ag = make(c, sample_sandbox)
    ag.review("DIFF")
    second = c.calls[1]["messages"]
    assert second[1]["role"] == "assistant" and second[2]["role"] == "user"
    results = second[2]["content"]
    assert [r["tool_use_id"] for r in results] == ["t1", "t2"]      # both results, one message
    assert "search_users" in results[0]["content"] and "<repo_data>" in results[0]["content"]
    assert [n for n, _ in ag.tool_calls] == ["read_file", "grep"]
    assert any(b.type == "thinking" for b in second[1]["content"])   # response.content passed back verbatim


def test_tool_error_is_reported_not_raised(sample_sandbox):
    c = FakeClient(tool_resp(("t1", "read_file", {"path": "../../etc/passwd"})), json_resp())
    make(c, sample_sandbox).review("D")
    r = c.calls[1]["messages"][2]["content"][0]
    assert r["is_error"] is True and "escapes" in r["content"]


def test_injected_unknown_tool_is_rejected(sample_sandbox):
    c = FakeClient(tool_resp(("t1", "bash", {"cmd": "rm -rf /"})), json_resp())
    make(c, sample_sandbox).review("D")
    assert c.calls[1]["messages"][2]["content"][0]["is_error"] is True


def test_refusal_and_max_tokens_raise(sample_sandbox):
    with pytest.raises(ReviewError, match="declined"):
        make(FakeClient(stop_resp("refusal")), sample_sandbox).review("D")
    with pytest.raises(ReviewError, match="truncated"):
        make(FakeClient(text_resp('{"summ', stop="max_tokens")), sample_sandbox).review("D")


def test_bad_json_and_bad_enum_raise(sample_sandbox):
    with pytest.raises(ReviewError, match="schema"):
        make(FakeClient(text_resp("not json")), sample_sandbox).review("D")
    with pytest.raises(ReviewError, match="schema"):
        make(FakeClient(json_resp([finding(severity="catastrophic")])), sample_sandbox).review("D")


def test_pause_turn_continues(sample_sandbox):
    c = FakeClient(stop_resp("pause_turn"), json_resp())
    make(c, sample_sandbox).review("D")
    assert len(c.calls) == 2


def test_iteration_cap_forces_wrap_up_with_tool_choice_none(sample_sandbox):
    c = FakeClient(tool_resp(("a", "list_files", {})), tool_resp(("b", "list_files", {})), json_resp())
    ag = make(c, sample_sandbox, max_iterations=3)
    ag.review("D")
    assert "tool_choice" not in c.calls[0] and "tool_choice" not in c.calls[1]
    assert c.calls[2]["tool_choice"] == {"type": "none"}
    last_user = c.calls[2]["messages"][-1]["content"]
    assert last_user[0]["type"] == "tool_result" and "Budget reached" in last_user[-1]["text"]


def test_model_ignoring_wrap_up_is_an_error(sample_sandbox):
    c = FakeClient(tool_resp(("a", "list_files", {})), tool_resp(("b", "list_files", {})))
    with pytest.raises(ReviewError, match="after the budget"):
        make(c, sample_sandbox, max_iterations=2).review("D")
    assert len(c.calls) == 2


def test_token_budget_triggers_wrap_up_and_usage_accumulates(sample_sandbox):
    c = FakeClient(tool_resp(("a", "list_files", {}), i=1500, o=600, cr=10, cw=5), json_resp(i=10, o=10))
    ag = make(c, sample_sandbox, max_total_tokens=2000, max_iterations=10)
    ag.review("D")
    assert c.calls[1]["tool_choice"] == {"type": "none"}
    u = ag.usage
    assert (u.input_tokens, u.output_tokens, u.cache_read_tokens, u.cache_write_tokens, u.calls) == (1510, 610, 10, 5, 2)
    assert u.cost_usd("claude-sonnet-5-5") > 0 and "estimate" in u.summary("claude-sonnet-5-5")
    assert "unknown" in u.summary("mystery-model")


def test_single_iteration_wraps_up_immediately(sample_sandbox):
    c = FakeClient(json_resp())
    make(c, sample_sandbox, max_iterations=1).review("D")
    assert c.calls[0]["tool_choice"] == {"type": "none"}
    assert "Budget reached" in c.calls[0]["messages"][0]["content"][-1]["text"]
