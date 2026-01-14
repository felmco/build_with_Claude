# 3.2 Cache Optimization Strategies

Prompt caching reduces costs and latency, but only if used correctly.

## How Caching Works (Review)
- **Structure:** `[Tools] -> [System] -> [Messages]`
- **Breakpoint:** You mark the *last* block you want to cache.
- **Lifetime:** 5 minutes (default). Refreshed on every hit.

## Strategy 1: Static Prefixing
Put all static content at the *very top* of your system prompt or message list.

```python
system_content = [
    {
        "type": "text",
        "text": "You are a helpful assistant..."
    },
    {
        "type": "text",
        "text": "<huge_document>...</huge_document>",
        "cache_control": {"type": "ephemeral"} # CACHE HERE
    }
]
```

## Strategy 2: Tool Definitions
Tools are often static. Cache them!
*Note: Tool caching usually happens automatically or via specific placement depending on API updates. Check current docs.*

## Strategy 3: Multi-Turn Caching
In a long conversation, cache the *last* message periodically (e.g., every 5 turns) to create checkpoints.

```python
# Pseudo-code
messages = [...]
if len(messages) % 5 == 0:
    messages[-1]["content"][0]["cache_control"] = {"type": "ephemeral"}
```

## Monitoring Hit Rate
Check `usage` stats in the response.
- `cache_creation_input_tokens`: Miss (Written to cache).
- `cache_read_input_tokens`: Hit (Read from cache).

**Goal:** Maximize Read, Minimize Creation.

## Next Steps
- Learn more about [Cost Reduction](./07_cost_reduction.md).
