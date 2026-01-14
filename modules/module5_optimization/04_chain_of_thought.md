# 5.1 Chain of Thought (CoT)

CoT is a technique where the model is encouraged to produce intermediate reasoning steps.

## How to implement
1. **Explicit Instruction:** "Think step-by-step."
2. **XML Tags:** Instruct Claude to output reasoning inside `<thinking>` tags.

```python
system = "You are a math tutor. Always output your thinking in <thinking> tags before your final answer."
```

## Benefits
- **Debugging:** You can see *why* Claude got an answer wrong.
- **Accuracy:** Breaking problems down reduces logic errors.

## Next Steps
- [Prompt Templates](./05_prompt_templates.md).
