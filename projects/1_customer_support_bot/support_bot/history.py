"""Conversation history trimming.

The Messages API is stateless: we resend the whole history every call. To bound
cost we drop old turns, but two rules must hold or the API returns a 400:
  1. every tool_use needs its tool_result in the very next user message;
  2. the first message must be a user message.
So we only ever cut at a "real" user message (plain text, not a tool_result).

Course links: conversations (module 2, lesson 3), token optimization (module 5, lesson 6).
"""
from __future__ import annotations

import json


def is_real_user_message(msg: dict) -> bool:
    """A user message that starts a turn (not one that only carries tool_results)."""
    if msg.get("role") != "user":
        return False
    content = msg.get("content")
    if isinstance(content, str):
        return True
    return not any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content)


def _size(msg: dict) -> int:
    return len(json.dumps(msg, default=str))


def trim_history(messages: list[dict], max_messages: int = 40, max_chars: int = 40_000) -> list[dict]:
    """Return a trimmed copy of `messages` (oldest turns dropped).

    Always keeps the most recent turn, even if it alone exceeds the limits
    (cutting inside a turn would orphan tool blocks).
    """
    starts = [i for i, m in enumerate(messages) if is_real_user_message(m)]
    if not starts:
        return list(messages)
    for start in starts:
        tail = messages[start:]
        if len(tail) <= max_messages and sum(_size(m) for m in tail) <= max_chars:
            return tail
    return messages[starts[-1]:]  # last turn only
