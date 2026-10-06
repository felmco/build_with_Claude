# 5.1 Chain of Thought (CoT)

CoT is a technique where the model is encouraged to produce intermediate reasoning steps.

## How to implement
1. **Explicit Instruction:** "Think step-by-step."
2. **XML Tags:** Instruct Claude to output reasoning inside `<thinking>` tags.

```python
system = "You are a math tutor. Reason inside <reasoning> tags, then give the final answer inside <answer> tags."
```

Parse the `<answer>` block in your code and discard the rest.

## Native thinking
Claude's built-in thinking is often better than prompted reasoning. On `claude-sonnet-5-5`, `claude-opus-5-5` and `claude-fable-5-1`, use adaptive thinking and control depth with `effort`:

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "summarized"},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "A train leaves at 3pm going 60 mph..."}],
)
for block in response.content:
    if block.type == "thinking":
        print("Reasoning summary:", block.thinking)
    elif block.type == "text":
        print(block.text)
```

`budget_tokens` is rejected on these models; only `claude-haiku-4-5` still uses `thinking={"type": "enabled", "budget_tokens": N}`. Thinking is hidden by default (`display: "omitted"`), so request `"summarized"` if you want to show it.

## Benefits
- **Debugging:** You can see *why* Claude got an answer wrong.
- **Accuracy:** Breaking problems down reduces logic errors.

## Next Steps
- [Prompt Templates](./05_prompt_templates.md).
