"""Server-tool definitions and helpers for reading their result blocks.

web_search / web_fetch are SERVER tools: Anthropic runs them, so we never send
back a tool_result for them (Module 6.1). The ``_20260209`` versions add dynamic
filtering (the API runs code to trim pages before they reach context) but need
Sonnet 4.6+/Opus 4.6+ class models. Haiku 4.5 gets the basic versions.
"""
from __future__ import annotations

from urllib.parse import urlparse

DYNAMIC_FILTER_PREFIXES = ("claude-sonnet-5", "claude-opus-5", "claude-opus-4-6",
                           "claude-opus-4-7", "claude-opus-4-8", "claude-sonnet-4-6",
                           "claude-fable-5")


def supports_dynamic_filtering(model: str) -> bool:
    return model.startswith(DYNAMIC_FILTER_PREFIXES)


def supports_effort(model: str) -> bool:
    """output_config.effort is not accepted by Haiku 4.5."""
    return supports_dynamic_filtering(model)


def build_tools(model: str, max_searches: int = 4, max_fetches: int = 3,
                allowed_domains=None, blocked_domains=None) -> list[dict]:
    """Pick tool versions that match the worker model. max_uses is a hard per-request cap."""
    if allowed_domains and blocked_domains:
        raise ValueError("use allowed_domains OR blocked_domains, not both (the API returns 400)")
    dyn = supports_dynamic_filtering(model)
    search = {"type": "web_search_20260209" if dyn else "web_search_20250305",
              "name": "web_search", "max_uses": max_searches}
    fetch = {"type": "web_fetch_20260209" if dyn else "web_fetch_20250910",
             "name": "web_fetch", "max_uses": max_fetches, "max_content_tokens": 30_000}
    for tool in (search, fetch):
        if allowed_domains:
            tool["allowed_domains"] = list(allowed_domains)
        if blocked_domains:
            tool["blocked_domains"] = list(blocked_domains)
    return [search, fetch]


def _g(obj, name, default=None):
    return obj.get(name, default) if isinstance(obj, dict) else getattr(obj, name, default)


def safe_url(url) -> bool:
    """Only http(s) URLs with a host may appear in a report (blocks javascript:, data:, file:)."""
    try:
        p = urlparse(str(url))
    except ValueError:
        return False
    return p.scheme in ("http", "https") and bool(p.netloc)


def extract_text(content) -> str:
    """Join text blocks only. content may also hold thinking / server_tool_use / result blocks."""
    return "".join(_g(b, "text", "") or "" for b in content if _g(b, "type") == "text")


def extract_sources(content) -> list[dict]:
    """Collect {url, title} from search results, fetch results and text citations (deduped)."""
    found: dict[str, str] = {}

    def add(url, title):
        if url and safe_url(url) and url not in found:
            found[url] = title or url

    for b in content:
        t = _g(b, "type")
        body = _g(b, "content")
        if t == "web_search_tool_result" and isinstance(body, list):  # success = list
            for r in body:
                add(_g(r, "url"), _g(r, "title"))
        elif t == "web_fetch_tool_result" and body is not None and not _is_error(body):
            doc = _g(body, "content")
            add(_g(body, "url"), _g(doc, "title") if doc is not None else None)
        elif t == "text":
            for c in _g(b, "citations") or []:
                add(_g(c, "url"), _g(c, "title"))
    return [{"url": u, "title": t} for u, t in found.items()]


def _is_error(body) -> bool:
    return str(_g(body, "type", "")).endswith("_error")


def server_tool_errors(content) -> list[str]:
    """Server-tool failures arrive as HTTP 200 with an error object inside the result block."""
    errors = []
    for b in content:
        t = _g(b, "type")
        if t in ("web_search_tool_result", "web_fetch_tool_result"):
            body = _g(b, "content")
            if body is not None and not isinstance(body, list) and _is_error(body):
                errors.append(f"{t.removesuffix('_tool_result')}: {_g(body, 'error_code')}")
    return errors
