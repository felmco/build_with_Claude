"""Usage tracking and the per-run budget guard.

Every API response carries ``response.usage``. We accumulate it per model so the
final cost line is accurate even though the lead, workers and synthesizer use
different models (Module 1.3 pricing, Module 5.6 token optimization).
"""
from __future__ import annotations

from dataclasses import dataclass, field

# Estimated USD per million tokens (input, output). Prices change: check the
# pricing page. Unknown models fall back to the Sonnet 5.5 row.
PRICES = {
    "claude-sonnet-5-5": (2.0, 10.0),
    "claude-haiku-4-5": (1.0, 5.0),
    "claude-opus-5-5": (4.0, 20.0),
}
DEFAULT_PRICE = PRICES["claude-sonnet-5-5"]
CACHE_READ_MULT = 0.10   # cache reads ~10% of the input price
CACHE_WRITE_MULT = 1.25  # 5-minute cache writes ~1.25x
WEB_SEARCH_USD = 0.01    # $10 per 1,000 searches, on top of tokens


class BudgetExceeded(RuntimeError):
    """Raised when a run would go past its token, cost or tool-use limit."""


def _get(obj, name, default=0):
    """Read a field from an SDK object or a plain dict/namespace; None -> default."""
    val = obj.get(name) if isinstance(obj, dict) else getattr(obj, name, None)
    return default if val is None else val


@dataclass
class Budget:
    max_tokens: int = 400_000      # input + output, all agents combined
    max_cost_usd: float = 1.00     # estimated
    max_tool_uses: int = 40        # web searches + fetches, all workers combined
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    tool_uses: int = 0
    searches: int = 0
    cost_usd: float = 0.0
    calls: int = 0
    by_model: dict = field(default_factory=dict)

    def record(self, model: str, usage) -> None:
        """Add one response's usage. Call it for EVERY response, including pause_turn ones."""
        inp = _get(usage, "input_tokens")
        out = _get(usage, "output_tokens")
        cr = _get(usage, "cache_read_input_tokens")
        cw = _get(usage, "cache_creation_input_tokens")
        stu = _get(usage, "server_tool_use", None)
        searches = _get(stu, "web_search_requests") if stu is not None else 0
        fetches = _get(stu, "web_fetch_requests") if stu is not None else 0
        pin, pout = PRICES.get(model, DEFAULT_PRICE)
        cost = (inp * pin + out * pout + cr * pin * CACHE_READ_MULT
                + cw * pin * CACHE_WRITE_MULT) / 1_000_000 + searches * WEB_SEARCH_USD
        self.input_tokens += inp
        self.output_tokens += out
        self.cache_read_tokens += cr
        self.cache_write_tokens += cw
        self.searches += searches
        self.tool_uses += searches + fetches
        self.cost_usd += cost
        self.calls += 1
        m = self.by_model.setdefault(model, {"in": 0, "out": 0, "cost": 0.0})
        m["in"] += inp
        m["out"] += out
        m["cost"] += cost

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def check(self) -> None:
        """Raise BudgetExceeded if any limit is reached. Call BEFORE each API request.

        Requests already in flight can still overshoot a little: the guard stops
        new work, it cannot cancel tokens the API is already generating.
        """
        if self.total_tokens >= self.max_tokens:
            raise BudgetExceeded(f"token budget reached ({self.total_tokens:,}/{self.max_tokens:,})")
        if self.cost_usd >= self.max_cost_usd:
            raise BudgetExceeded(f"cost budget reached (~${self.cost_usd:.3f}/${self.max_cost_usd:.2f})")
        if self.tool_uses >= self.max_tool_uses:
            raise BudgetExceeded(f"tool-use budget reached ({self.tool_uses}/{self.max_tool_uses})")

    def summary(self) -> str:
        models = ", ".join(f"{m}: {v['in']:,} in/{v['out']:,} out" for m, v in self.by_model.items())
        return (f"Usage: {self.calls} API calls, {self.input_tokens:,} in / {self.output_tokens:,} out "
                f"(+{self.cache_read_tokens:,} cache read, {self.cache_write_tokens:,} cache write), "
                f"{self.tool_uses} tool uses ({self.searches} searches); "
                f"estimated cost ~${self.cost_usd:.4f} [{models}] (estimate, check your Console)")
