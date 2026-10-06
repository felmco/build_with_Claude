"""Token usage and cost estimate. Prices are USD per million tokens (MTok)."""
from __future__ import annotations

from dataclasses import dataclass

# Check https://platform.claude.com/docs/en/about-claude/pricing; these go stale.
PRICES = {
    "claude-sonnet-5-5": {"in": 2.0, "out": 10.0},
    "claude-haiku-4-5": {"in": 1.0, "out": 5.0},
    "claude-opus-5-5": {"in": 4.0, "out": 20.0},
}
CACHE_READ_MULT = 0.10    # cache reads cost ~10% of base input (less on some models)
CACHE_WRITE_MULT = 1.25   # 5-minute cache writes cost 1.25x base input


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read: int = 0
    cache_write: int = 0
    requests: int = 0

    def add(self, u) -> None:
        """Accumulate an SDK `response.usage` (cache fields may be None)."""
        self.input_tokens += getattr(u, "input_tokens", 0) or 0
        self.output_tokens += getattr(u, "output_tokens", 0) or 0
        self.cache_read += getattr(u, "cache_read_input_tokens", 0) or 0
        self.cache_write += getattr(u, "cache_creation_input_tokens", 0) or 0
        self.requests += 1

    def cost(self, model: str) -> float | None:
        p = PRICES.get(model)
        if p is None:
            return None
        return (self.input_tokens * p["in"]
                + self.cache_read * p["in"] * CACHE_READ_MULT
                + self.cache_write * p["in"] * CACHE_WRITE_MULT
                + self.output_tokens * p["out"]) / 1_000_000

    def summary(self, model: str) -> str:
        c = self.cost(model)
        cost = f"~${c:.4f} (estimate)" if c is not None else "cost unknown for this model"
        return (f"usage: {self.requests} request(s), in={self.input_tokens} out={self.output_tokens} "
                f"cache_read={self.cache_read} cache_write={self.cache_write} | {cost}")
