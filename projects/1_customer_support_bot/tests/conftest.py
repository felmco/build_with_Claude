"""Shared fakes: a scripted client that mimics anthropic.Anthropic().messages.stream(...)."""
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from support_bot.analytics import AnalyticsLog  # noqa: E402
from support_bot.bot import SupportBot  # noqa: E402
from support_bot.tools import SupportTools  # noqa: E402

KB = Path(__file__).resolve().parents[1] / "data" / "kb.json"


def text(t):
    return NS(type="text", text=t)


def tool_use(id, name, **inp):
    return NS(type="tool_use", id=id, name=name, input=inp)


def response(content, stop_reason="end_turn", inp=10, out=5, cache_read=0, cache_write=0):
    usage = NS(input_tokens=inp, output_tokens=out, cache_read_input_tokens=cache_read,
               cache_creation_input_tokens=cache_write)
    return NS(content=content, stop_reason=stop_reason, usage=usage)


class FakeStream:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    @property
    def text_stream(self):
        for b in self.message.content:
            if b.type == "text":
                yield b.text

    def get_final_message(self):
        return self.message


class FakeClient:
    """Returns the scripted responses in order and records a deep-ish copy of each request."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []
        self.messages = self

    def stream(self, **params):
        snapshot = dict(params)
        snapshot["messages"] = [dict(m) for m in params["messages"]]
        self.calls.append(snapshot)
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return FakeStream(item)


@pytest.fixture
def paths(tmp_path):
    return NS(tickets=tmp_path / "tickets.jsonl", log=tmp_path / "analytics.jsonl")


@pytest.fixture
def make_bot(paths):
    def _make(responses, **kw):
        client = FakeClient(responses)
        tools = SupportTools(KB, paths.tickets)
        bot = SupportBot(client, tools, analytics=AnalyticsLog(paths.log), **kw)
        return bot, client
    return _make
