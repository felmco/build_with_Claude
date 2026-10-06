"""OfflineClient: a tiny stand-in for anthropic.Anthropic used by --dry-run.

It is NOT an LLM. For each user message it asks for a knowledge-base search (a tool_use), then
quotes the first article it got back. This lets you try the REPL, tools, history and /stats
without an API key, and shows the exact object shapes the bot expects from the SDK.
"""
from __future__ import annotations

import re
from types import SimpleNamespace as NS


class _Stream:
    def __init__(self, message):
        self._m = message

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    @property
    def text_stream(self):
        for b in self._m.content:
            if b.type == "text":
                yield b.text

    def get_final_message(self):
        return self._m


class _Messages:
    def __init__(self):
        self._n = 0

    def stream(self, **params):
        usage = NS(input_tokens=0, output_tokens=0, cache_read_input_tokens=0, cache_creation_input_tokens=0)
        last = params["messages"][-1]
        if isinstance(last["content"], str):  # fresh user question -> ask for a KB search
            self._n += 1
            block = NS(type="tool_use", id=f"toolu_offline_{self._n}", name="search_knowledge_base",
                       input={"query": last["content"][:200]})
            return _Stream(NS(content=[block], stop_reason="tool_use", usage=usage))
        data = last["content"][0]["content"]  # tool_result text
        m = re.search(r'<kb_document id="([^"]+)" title="([^"]+)">\n(.*?)\n</kb_document>', data, re.S)
        text = (f"[offline demo] Closest article {m.group(1)} ({m.group(2)}): {m.group(3)}" if m
                else "[offline demo] I found no matching article. In a real run I would offer to open a ticket.")
        return _Stream(NS(content=[NS(type="text", text=text)], stop_reason="end_turn", usage=usage))


class OfflineClient:
    def __init__(self):
        self.messages = _Messages()
