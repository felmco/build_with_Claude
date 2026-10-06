# 5.2 Caching Strategies

## The "Cache Everything Static" Rule
If text appears in more than one request, cache it.

## Common Candidates
1. **System Prompts:** If lengthy. The minimum cacheable prefix depends on the model (512 to 4096 tokens); shorter prefixes silently do not cache.
2. **Few-Shot Examples:** If you provide 50 examples, cache them.
3. **Reference Documents:** Policy docs, API specs.
4. **Conversation History:** In chatbots, cache the history up to the last turn.

## Breakpoint Management
Place breakpoints at the *end* of the static section.

`[Static System Prompt] -> [CACHE] -> [Dynamic User Input]`

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": LONG_STATIC_INSTRUCTIONS,
        "cache_control": {"type": "ephemeral"},
    }],
    messages=[{"role": "user", "content": user_input}],
)
print(response.usage.cache_creation_input_tokens, response.usage.cache_read_input_tokens)
```

## Economics
- Cache writes cost 1.25x the base input price (5-minute TTL) or 2x (1-hour TTL, `"ttl": "1h"`).
- Cache reads cost about 0.1x the base input price (less on some models, e.g. 0.05x on Opus 5.5).
- With the 5-minute TTL, two requests already break even. Every read refreshes the timer.

## Verify it works
A broken cache fails silently: requests succeed, the bill is just higher. Check `usage.cache_read_input_tokens > 0` on the second identical request, and monitor it in production. Anything that changes the prefix (a timestamp in the system prompt, non-deterministic tool ordering) causes a miss.

On Amazon Bedrock's older integrations, top-level automatic `cache_control` is not supported; use explicit breakpoints on content blocks.

## Next Steps
- [Batch Processing for Cost](./09_batch_cost.md).
