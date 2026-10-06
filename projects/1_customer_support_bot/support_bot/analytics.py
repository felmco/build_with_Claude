"""JSONL analytics: one line per user turn, plus a /stats summary.

Course links: usage and cost (module 1, lesson 3), logging and monitoring
(module 4, lesson 19).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

# Estimated USD per million tokens (input, output). Check the pricing page; prices change.
PRICES = {
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-opus-5-5": (4.00, 20.00),
}
DEFAULT_PRICE = PRICES["claude-sonnet-5-5"]  # used for unknown models
CACHE_READ_MULT = 0.10   # cache reads cost ~10% of the input price
CACHE_WRITE_MULT = 1.25  # 5-minute cache writes cost 1.25x the input price


def estimate_cost(model: str, input_tokens: int, output_tokens: int,
                  cache_read: int = 0, cache_write: int = 0) -> float:
    """Estimated USD. `input_tokens` excludes cached tokens (as in response.usage)."""
    p_in, p_out = PRICES.get(model, DEFAULT_PRICE)
    return (input_tokens * p_in + cache_write * p_in * CACHE_WRITE_MULT
            + cache_read * p_in * CACHE_READ_MULT + output_tokens * p_out) / 1_000_000


class UsageTotals:
    """Accumulates response.usage across the API calls of one turn or session."""

    def __init__(self) -> None:
        self.input = self.output = self.cache_read = self.cache_write = self.calls = 0

    def add(self, usage) -> None:
        # Cache fields can be None/absent when caching is not used.
        self.input += getattr(usage, "input_tokens", 0) or 0
        self.output += getattr(usage, "output_tokens", 0) or 0
        self.cache_read += getattr(usage, "cache_read_input_tokens", 0) or 0
        self.cache_write += getattr(usage, "cache_creation_input_tokens", 0) or 0
        self.calls += 1

    def merge(self, other: "UsageTotals") -> None:
        self.input += other.input
        self.output += other.output
        self.cache_read += other.cache_read
        self.cache_write += other.cache_write
        self.calls += other.calls

    def cost(self, model: str) -> float:
        return estimate_cost(model, self.input, self.output, self.cache_read, self.cache_write)


class AnalyticsLog:
    def __init__(self, path: str | Path | None, session: str | None = None):
        self.path = Path(path) if path else None
        self.session = session  # tag rows so /stats can separate "this session" from history

    def record(self, **fields) -> dict:
        row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "session": self.session, **fields}
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return row

    def rows(self) -> list[dict]:
        if not self.path or not self.path.exists():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # tolerate a half-written line
        return out


def summarize(rows: list[dict]) -> dict:
    """Aggregate log rows into the numbers /stats prints."""
    n = len(rows)
    tools: dict[str, int] = {}
    for r in rows:
        for t in r.get("tools", []):
            tools[t] = tools.get(t, 0) + 1
    lat = sorted(r.get("latency_s", 0) for r in rows)
    in_all = sum(r.get("input_tokens", 0) + r.get("cache_read_tokens", 0)
                 + r.get("cache_write_tokens", 0) for r in rows)
    cached = sum(r.get("cache_read_tokens", 0) for r in rows)
    return {
        "turns": n,
        "errors": sum(1 for r in rows if r.get("error")),
        "input_tokens": sum(r.get("input_tokens", 0) for r in rows),
        "output_tokens": sum(r.get("output_tokens", 0) for r in rows),
        "cache_read_tokens": cached,
        "cache_write_tokens": sum(r.get("cache_write_tokens", 0) for r in rows),
        "cache_hit_rate": (cached / in_all) if in_all else 0.0,
        "avg_latency_s": (sum(lat) / n) if n else 0.0,
        "p95_latency_s": lat[min(n - 1, int(0.95 * n))] if n else 0.0,
        "cost_usd": sum(r.get("cost_usd", 0) for r in rows),
        "tools": tools,
    }


def format_stats(title: str, s: dict) -> str:
    tools = ", ".join(f"{k}={v}" for k, v in sorted(s["tools"].items())) or "none"
    return (f"{title}: {s['turns']} turns, {s['errors']} errors | "
            f"tokens in={s['input_tokens']} out={s['output_tokens']} "
            f"cache_read={s['cache_read_tokens']} cache_write={s['cache_write_tokens']} "
            f"(hit rate {s['cache_hit_rate']:.0%}) | latency avg={s['avg_latency_s']:.2f}s "
            f"p95={s['p95_latency_s']:.2f}s | tools: {tools} | est. cost ${s['cost_usd']:.4f}")
