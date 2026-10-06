"""Token accounting and a rough USD estimate (labelled as an estimate)."""
from __future__ import annotations

from dataclasses import dataclass

# USD per million tokens (input, output). Estimates; check the pricing page.
PRICES = {
    "claude-sonnet-5-5": (2.0, 10.0),
    "claude-haiku-4-5": (1.0, 5.0),
    "claude-opus-5-5": (4.0, 20.0),
}
CACHE_READ_MULT = 0.10   # approx; actual discount varies by model
CACHE_WRITE_MULT = 1.25


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    calls: int = 0

    def add(self, u) -> None:
        # fields can be None/absent depending on features used; treat as 0
        self.input_tokens += getattr(u, "input_tokens", 0) or 0
        self.output_tokens += getattr(u, "output_tokens", 0) or 0
        self.cache_read_tokens += getattr(u, "cache_read_input_tokens", 0) or 0
        self.cache_write_tokens += getattr(u, "cache_creation_input_tokens", 0) or 0
        self.calls += 1

    @property
    def total_tokens(self) -> int:
        return (self.input_tokens + self.output_tokens
                + self.cache_read_tokens + self.cache_write_tokens)

    def cost_usd(self, model: str) -> float | None:
        if model not in PRICES:
            return None
        pin, pout = PRICES[model]
        return (self.input_tokens * pin + self.output_tokens * pout
                + self.cache_read_tokens * pin * CACHE_READ_MULT
                + self.cache_write_tokens * pin * CACHE_WRITE_MULT) / 1e6

    def summary(self, model: str) -> str:
        c = self.cost_usd(model)
        cost = f"~${c:.4f} (estimate)" if c is not None else "cost unknown for this model"
        return (f"usage: {self.calls} calls, in={self.input_tokens} out={self.output_tokens} "
                f"cache_read={self.cache_read_tokens} cache_write={self.cache_write_tokens} | {cost}")
