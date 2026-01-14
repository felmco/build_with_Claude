# 5.2 Caching Strategies

## The "Cache Everything Static" Rule
If text appears in more than one request, cache it.

## Common Candidates
1. **System Prompts:** If lengthy (>1024 tokens).
2. **Few-Shot Examples:** If you provide 50 examples, cache them.
3. **Reference Documents:** Policy docs, API specs.
4. **Conversation History:** In chatbots, cache the history up to the last turn.

## Breakpoint Management
Place breakpoints at the *end* of the static section.

`[Static System Prompt] -> [CACHE] -> [Dynamic User Input]`

## Next Steps
- [Batch Processing for Cost](./09_batch_cost.md).
