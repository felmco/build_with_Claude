# 3.5 Thinking Use Cases

## When to use Extended Thinking?

1. **Complex Math & Logic:** "Solve this riddle." "Calculate the trajectory..."
2. **Coding:** "Refactor this legacy codebase." (Thinking allows planning the structure first).
3. **Creative Writing:** "Write a mystery novel outline." (Planning characters and plot twists).
4. **Safety & Policy:** "Analyze if this content violates our complex TOS."

## When NOT to use it?
- Simple greetings ("Hi").
- Fact retrieval ("Capital of France").
- Low-latency applications (Chatbots for simple queries). Lower the effort level, or on Sonnet 5.5 use `{"type": "between_tools"}`.

## Controlling Depth
On Fable 5.1, Opus 5.5, and Sonnet 5.5 you do not set a token budget (`budget_tokens` returns a 400). Claude decides how much to think, and you steer it with `output_config={"effort": ...}`:
- **low / medium:** Quick checks and routine tasks.
- **high:** Standard coding and analysis.
- **xhigh / max:** Deep research and the hardest problems. Expect more cost and latency; use streaming and a large `max_tokens`.

Only Claude Haiku 4.5 still uses a manual budget (`{"type": "enabled", "budget_tokens": N}`, minimum 1024, below `max_tokens`). Thinking tokens are billed as output tokens.

## Next Steps
- Learn about the beta feature [Computer Use](./16_computer_use.md).
