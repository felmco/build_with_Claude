# 3.5 Extended and Adaptive Thinking Overview

Thinking lets Claude reason before it answers, which improves performance on complex tasks. On current models you do not set a token budget: Claude decides how much to think (**adaptive thinking**) and you steer depth with the **`effort`** parameter.

## Supported Models and Modes

| Model | How to use thinking |
|-------|---------------------|
| **Claude Fable 5.1** | Always on. Omit `thinking` (or send `{"type": "adaptive"}`). Control depth with `effort`. |
| **Claude Opus 5.5** | Always on, adaptive. `{"type": "disabled"}` and `budget_tokens` return a 400. Default effort is `medium`. |
| **Claude Sonnet 5.5** | Adaptive by default. `{"type": "disabled"}` returns a 400; send `{"type": "between_tools"}` to turn thinking off (effort `high` or lower). |
| **Claude Haiku 4.5** | Manual *extended thinking*: `{"type": "enabled", "budget_tokens": N}` (minimum 1024, below `max_tokens`). |

> `budget_tokens` is deprecated on Opus 4.6 / Sonnet 4.6 and rejected on the 5.x models. See [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) and the [Effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort).

## How It Works
When thinking runs, the response contains `thinking` blocks before the `text` block.

```python
import anthropic

client = anthropic.Anthropic()

# Streaming is recommended for long, high-effort requests
with client.messages.stream(
    model="claude-opus-5-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "summarized"},
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": "Solve this complex logic puzzle..."}],
) as stream:
    response = stream.get_final_message()

for block in response.content:
    if block.type == "thinking":
        print("THINKING:", block.thinking)
    elif block.type == "text":
        print(block.text)
```

Haiku 4.5 (manual budget):

```python
client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=4096,
    thinking={"type": "enabled", "budget_tokens": 2048},
    messages=[{"role": "user", "content": "Solve this complex logic puzzle..."}],
)
```

## The "Thinking" Block
- **Visibility:** `display` defaults to `"omitted"` on the 5.x models (the block arrives with empty text). Set `"summarized"` to get a readable summary; the raw chain of thought is never returned. Thinking is billed the same whatever you display.
- **Depth:** Control it with `output_config.effort`: `low`, `medium`, `high`, `xhigh`, `max`. Higher effort means deeper thought and more cost and latency.
- **Replay:** When you continue a conversation, send thinking blocks back unchanged (append `response.content`, not just the text).

## Benefits
- Reduced hallucinations.
- Better planning.
- Self-correction during the thinking phase.

## Next Steps
- [Thinking Use Cases](./15_thinking_use_cases.md).
