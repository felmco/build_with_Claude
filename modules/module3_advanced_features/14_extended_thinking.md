# 3.5 Extended Thinking Overview

Extended Thinking allows Claude to "think" before responding, making its reasoning visible and improving performance on complex tasks.

## Supported Models
- **Claude Sonnet 3.7+**
- **Claude 4+** (Future)

## How It Works
When enabled, Claude generates a `thinking` block before the `text` block.

```python
client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    thinking={
        "type": "enabled",
        "budget_tokens": 1024
    },
    messages=[{"role": "user", "content": "Solve this complex logic puzzle..."}]
)
```

## The "Thinking" Block
- **Visibility:** You can choose to show this to the user or hide it.
- **Budget:** You set a token budget for thinking. Higher budget = deeper thought (and higher cost/latency).

## Benefits
- Reduced hallucinations.
- Better planning.
- Self-correction during the thinking phase.

## Next Steps
- [Thinking Use Cases](./15_thinking_use_cases.md).
