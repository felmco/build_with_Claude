"""Shared fakes: a scripted stand-in for anthropic.Anthropic (no network)."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reviewer.diffparse import parse_diff  # noqa: E402
from reviewer.sandbox import Sandbox  # noqa: E402

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def usage(i=100, o=50, cr=0, cw=0):
    return NS(input_tokens=i, output_tokens=o, cache_read_input_tokens=cr, cache_creation_input_tokens=cw)


def text_resp(text, stop="end_turn", **u):
    return NS(content=[NS(type="text", text=text)], stop_reason=stop, usage=usage(**u))


def json_resp(findings=(), summary="ok", **u):
    return text_resp(json.dumps({"summary": summary, "findings": list(findings)}), **u)


def tool_resp(*calls, **u):
    """calls: (id, name, input) tuples. A thinking block comes first, as with adaptive thinking."""
    blocks = [NS(type="thinking", thinking="", signature="x")]
    blocks += [NS(type="tool_use", id=i, name=n, input=inp) for i, n, inp in calls]
    return NS(content=blocks, stop_reason="tool_use", usage=usage(**u))


def stop_resp(stop, **u):
    return NS(content=[], stop_reason=stop, usage=usage(**u))


def finding(**kw):
    base = dict(file="app/db.py", line=15, severity="high", category="security",
                message="SQL injection", suggestion="use ? placeholders")
    base.update(kw)
    return base


class FakeClient:
    """client.messages.create(**kw) pops scripted responses and records each call."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []
        self.messages = self

    def create(self, **kw):
        # deep-ish snapshot: the agent mutates `messages` after the call
        kw["messages"] = [dict(m, content=list(m["content"]) if isinstance(m["content"], list) else m["content"])
                          for m in kw["messages"]]
        self.calls.append(kw)
        if not self.responses:
            raise AssertionError("FakeClient ran out of scripted responses")
        return self.responses.pop(0)


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "a.py").write_text("\n".join(f"line{i}" for i in range(1, 11)) + "\n")
    (tmp_path / "app" / "b.txt").write_text("hello needle\nworld\n")
    (tmp_path / ".env").write_text("SECRET=1\n")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("needle")
    return tmp_path


@pytest.fixture
def sample_diff():
    return (EXAMPLES / "sample.diff").read_text()


@pytest.fixture
def sample_sandbox(sample_diff):
    return Sandbox(EXAMPLES / "sample_repo", parse_diff(sample_diff))
