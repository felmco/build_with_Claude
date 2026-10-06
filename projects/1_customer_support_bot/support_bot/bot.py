"""SupportBot: streaming conversation + manual tool-use loop + caching + analytics.

Course links: streaming (module 2, lessons 4-5), agent loops (module 4, lesson 6),
prompt caching (module 3, lesson 5), refusals (module 6, lesson 2).
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Callable

import anthropic

from .analytics import AnalyticsLog, UsageTotals
from .history import trim_history
from .prompts import SYSTEM_PROMPT
from .tools import TOOLS, SupportTools

MAX_INPUT_CHARS = 2000
MAX_TOOL_ROUNDS = 6  # safety net against endless tool loops
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


class InputRejected(ValueError):
    """User input failed validation (empty or too long)."""


def sanitize_input(text: str, limit: int = MAX_INPUT_CHARS) -> str:
    """Basic hygiene: strip control chars, reject empty/oversized input (we never silently truncate)."""
    text = _CONTROL.sub("", text).strip()
    if not text:
        raise InputRejected("Please type a message.")
    if len(text) > limit:
        raise InputRejected(f"Message too long ({len(text)} chars, limit {limit}). Please shorten it.")
    return text


def block_to_param(block) -> dict:
    """Convert a response content block to a request param (what we store in history)."""
    if block.type == "text":
        return {"type": "text", "text": block.text}
    if block.type == "tool_use":
        return {"type": "tool_use", "id": block.id, "name": block.name, "input": block.input}
    # thinking / redacted_thinking etc.: must be passed back unchanged, so use the SDK's own dump
    return block.model_dump(exclude_none=True)


@dataclass
class TurnResult:
    text: str = ""
    stop_reason: str | None = None
    tools_used: list[str] = field(default_factory=list)
    error: str | None = None
    notice: str | None = None  # refusal / truncation message for the UI
    latency_s: float = 0.0
    cost_usd: float = 0.0


class SupportBot:
    def __init__(self, client, tools: SupportTools, model: str = "claude-sonnet-5-5",
                 max_tokens: int = 1024, effort: str | None = None,
                 analytics: AnalyticsLog | None = None, max_history_messages: int = 40,
                 max_history_chars: int = 40_000):
        self.client = client  # injected so tests can pass a fake
        self.tools = tools
        self.model = model
        self.max_tokens = max_tokens
        self.effort = effort
        self.analytics = analytics or AnalyticsLog(None)
        self.max_history_messages = max_history_messages
        self.max_history_chars = max_history_chars
        self.messages: list[dict] = []
        self.session_usage = UsageTotals()

    def reset(self) -> None:
        self.messages = []
        self.tools.escalated = False

    def _request_params(self) -> dict:
        params = dict(
            model=self.model, max_tokens=self.max_tokens, tools=TOOLS, messages=self.messages,
            # Stable system prompt as a content block with a cache breakpoint. Together with the
            # cache_control on the last tool, tools + system are cached as one prefix.
            system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        )
        if self.effort:  # not supported on Haiku 4.5
            params["output_config"] = {"effort": self.effort}
        return params

    def ask(self, user_text: str, on_text: Callable[[str], None] | None = None) -> TurnResult:
        """Run one user turn (possibly several API calls) and log it. Raises InputRejected only."""
        user_text = sanitize_input(user_text)
        on_text = on_text or (lambda s: None)
        result, usage = TurnResult(), UsageTotals()
        t0 = time.perf_counter()
        self.messages.append({"role": "user", "content": user_text})
        self.messages = trim_history(self.messages, self.max_history_messages, self.max_history_chars)
        turn_start = max(0, len(self.messages) - 1)  # index of this turn's user message after trimming
        try:
            self._run_loop(result, usage, on_text, turn_start)
        except anthropic.RateLimitError:
            result.error = "rate_limited"
        except anthropic.APIConnectionError:  # includes timeouts
            result.error = "connection_error"
        except anthropic.APIStatusError as e:
            result.error = f"api_error_{e.status_code}"
        if result.error:
            del self.messages[turn_start:]  # roll back so history stays valid
            result.notice = {"rate_limited": "The service is busy, please try again in a moment.",
                             "connection_error": "Network problem reaching the AI service. Please retry."
                             }.get(result.error, "Sorry, something went wrong on our side. Please retry.")
        result.latency_s = time.perf_counter() - t0
        result.cost_usd = usage.cost(self.model)
        self.session_usage.merge(usage)
        self.analytics.record(
            model=self.model, user_chars=len(user_text), latency_s=round(result.latency_s, 3),
            api_calls=usage.calls, input_tokens=usage.input, output_tokens=usage.output,
            cache_read_tokens=usage.cache_read, cache_write_tokens=usage.cache_write,
            tools=result.tools_used, stop_reason=result.stop_reason, error=result.error,
            cost_usd=round(result.cost_usd, 6))
        return result

    def _run_loop(self, result: TurnResult, usage: UsageTotals, on_text, turn_start: int) -> None:
        texts: list[str] = []
        for _ in range(MAX_TOOL_ROUNDS):
            # Stream tokens to the user as they arrive, then fetch the complete Message.
            with self.client.messages.stream(**self._request_params()) as stream:
                for chunk in stream.text_stream:
                    on_text(chunk)
                response = stream.get_final_message()
            usage.add(response.usage)
            result.stop_reason = response.stop_reason
            round_text = "".join(b.text for b in response.content if b.type == "text")

            if response.stop_reason == "refusal":
                # Safety classifier declined. Roll the turn back so the refusal does not poison history.
                del self.messages[turn_start:]
                result.text = ""
                result.notice = "I can't help with that request. Is there something else about your order or account?"
                return
            if response.stop_reason == "max_tokens" and any(b.type == "tool_use" for b in response.content):
                del self.messages[turn_start:]  # tool input may be cut off: never execute it
                result.notice = "My answer got cut off. Please try rephrasing or ask a shorter question."
                return

            self.messages.append({"role": "assistant", "content": [block_to_param(b) for b in response.content]})
            texts.append(round_text)

            if response.stop_reason == "tool_use":
                # ALL tool_results for this assistant message go in ONE user message.
                results = []
                for b in response.content:
                    if b.type != "tool_use":
                        continue
                    content, is_error = self.tools.execute(b.name, b.input)
                    result.tools_used.append(b.name)
                    item = {"type": "tool_result", "tool_use_id": b.id, "content": content}
                    if is_error:
                        item["is_error"] = True
                    results.append(item)
                self.messages.append({"role": "user", "content": results})
                continue
            if response.stop_reason == "pause_turn":
                continue  # only happens with server tools; re-send to let Claude continue
            if response.stop_reason == "max_tokens":
                result.notice = "(Answer truncated at the token limit.)"
            break
        else:
            result.notice = "Too many tool steps; stopping. Please try again."
            # history currently ends with a tool_result user message, which is valid; close the turn:
            self.messages.append({"role": "assistant", "content": [{"type": "text", "text": "(stopped)"}]})
        result.text = "\n".join(t for t in texts if t)
