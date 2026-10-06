"""Offline pieces: response builders shaped like the SDK's, and a FakeClient with canned data.

``FakeClient`` mimics ``AsyncAnthropic().messages.create`` so the whole pipeline (plan ->
parallel workers with a pause_turn -> synthesis) runs with no key and no network.
The content it returns is FICTIONAL demo data, not research.
"""
from __future__ import annotations

import json
import re
from types import SimpleNamespace as NS

NS_USAGE = dict(input_tokens=1200, output_tokens=400, cache_read_input_tokens=0, cache_creation_input_tokens=0)


def usage(searches=0, fetches=0, **over):
    u = {**NS_USAGE, **over}
    return NS(**u, server_tool_use=NS(web_search_requests=searches, web_fetch_requests=fetches))


def text_block(text, citations=None):
    return NS(type="text", text=text, citations=citations)


def citation(url, title):
    return NS(type="web_search_result_location", url=url, title=title, cited_text="...")


def server_tool_use(name="web_search", tid="srvtoolu_1", **inp):
    return NS(type="server_tool_use", id=tid, name=name, input=inp)


def search_result(results, tid="srvtoolu_1"):
    """results: [(url, title)] -> success block (content is a LIST)."""
    return NS(type="web_search_tool_result", tool_use_id=tid,
              content=[NS(type="web_search_result", url=u, title=t) for u, t in results])


def tool_error(code="max_uses_exceeded", kind="web_search", tid="srvtoolu_1"):
    """Server-tool failure: HTTP 200, content is an error OBJECT, not a list."""
    return NS(type=f"{kind}_tool_result", tool_use_id=tid,
              content=NS(type=f"{kind}_tool_result_error", error_code=code))


def make_response(content, stop_reason="end_turn", usage_=None):
    return NS(id="msg_fake", role="assistant", content=content, stop_reason=stop_reason,
              stop_details=None, usage=usage_ or usage())


class _Messages:
    def __init__(self, handler):
        self._handler = handler
        self.calls: list[dict] = []

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        return self._handler(kwargs)


class ScriptedClient:
    """Test double: returns queued responses (or raises queued exceptions) in order."""

    def __init__(self, responses):
        self.queue = list(responses)
        self.messages = _Messages(self._next)

    def _next(self, kwargs):
        item = self.queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item(kwargs) if callable(item) else item


DEMO_SOURCES = [
    ("https://example.org/demo/overview", "Demo overview (fictional)"),
    ("https://example.org/demo/study-a", "Demo study A (fictional)"),
    ("https://example.net/demo/study-b", "Demo study B (fictional)"),
    ("https://example.com/demo/critique", "Demo critique (fictional)"),
]


class FakeClient:
    """Canned research run. Detects the role from the request: structured output = lead,
    tools = worker, otherwise = synthesizer."""

    def __init__(self):
        self._worker_calls: dict[str, int] = {}
        self.messages = _Messages(self._handle)

    def _handle(self, kw):
        if (kw.get("output_config") or {}) and kw["output_config"].get("format"):
            return self._plan(kw)
        if kw.get("tools"):
            return self._worker(kw)
        return self._synth(kw)

    def _plan(self, kw):
        q = kw["messages"][0]["content"]
        subs = [{"question": f"Background: what is the context behind {q!r}?", "rationale": "orient"},
                {"question": f"Evidence: what do studies and data say about {q!r}?", "rationale": "evidence"},
                {"question": f"Critique: what are the risks or disagreements around {q!r}?", "rationale": "balance"}]
        return make_response([text_block(json.dumps({"sub_questions": subs}))])

    def _worker(self, kw):
        sub = kw["messages"][0]["content"].split("Sub-question:", 1)[1].strip()
        n = self._worker_calls[sub] = self._worker_calls.get(sub, 0) + 1
        idx = 0 if sub.startswith("Background") else 1 if sub.startswith("Evidence") else 2
        (u1, t1), (u2, t2) = DEMO_SOURCES[idx], DEMO_SOURCES[(idx + 1) % 4]
        if n == 1:  # first call: server loop hits its iteration cap -> pause_turn
            return make_response(
                [text_block("Searching..."), server_tool_use(query=sub[:40], tid=f"srvtoolu_{idx}"),
                 search_result([(u1, t1), (u2, t2)], tid=f"srvtoolu_{idx}")],
                stop_reason="pause_turn", usage_=usage(searches=1))
        extra = [tool_error("url_not_accessible", "web_fetch")] if idx == 2 else []
        claim = ["- Demo claim A: the effect is large (source: %s)\n" % u1,
                 "- Demo claim B: the effect is small (source: %s)\n" % u2,
                 "- Demo claim C: the effect is contested (source: %s)\n" % DEMO_SOURCES[3][0]][idx]
        return make_response(
            extra + [text_block(claim + "Confidence: medium (fictional demo data).",
                                citations=[citation(u1, t1)])],
            usage_=usage(searches=1, fetches=1))

    def _synth(self, kw):
        prompt = kw["messages"][0]["content"]
        nums = [int(n) for n in re.findall(r"^\[(\d+)\] ", prompt, flags=re.M)]
        c = lambda i: f"[{nums[i % len(nums)]}]" if nums else ""  # noqa: E731
        md = (f"# Research report (OFFLINE DEMO)\n\n> Canned, fictional data from FakeClient. Not real research.\n\n"
              f"## Summary\n\nThe demo sources disagree on how large the effect is {c(0)}{c(1)}.\n\n"
              f"## Findings\n\n- Background is covered by an overview {c(0)}.\n- One study reports a large effect {c(1)}; "
              f"another reports a small one {c(2)}.\n\n"
              f"## Conflicts and low-confidence claims\n\n- Studies A and B conflict on effect size {c(1)}{c(2)}.\n"
              f"- The critique rests on a single source {c(3)}; one fetch failed, so it is low confidence.\n"
              f"- (Deliberately bogus citation to show validation: [99])\n")
        return make_response([text_block(md)], usage_=usage())
