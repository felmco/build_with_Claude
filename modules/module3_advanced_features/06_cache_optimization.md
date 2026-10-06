# 3.2 Cache Optimization Strategies

Prompt caching reduces costs and latency, but only if used correctly.

## How Caching Works (Review)
- **Structure:** `[Tools] -> [System] -> [Messages]`
- **Breakpoint:** You mark the *last* block you want to cache.
- **Lifetime:** 5 minutes (default), refreshed on every hit. Add `"ttl": "1h"` to `cache_control` for a 1-hour entry (2x write cost).
- **Limits:** at most 4 breakpoints per request; the prefix must meet a model-dependent minimum (512 to 4096 tokens) or nothing is cached.
- **Prefix match:** any change before a breakpoint (a timestamp, a different tool list, reordered JSON keys) invalidates that breakpoint and everything after it.

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
Tools are rendered first, before the system prompt. A `cache_control` marker on the last system block therefore caches the tools and the system prompt together. You can also put the marker on the last tool definition. Keep the tool list identical (same tools, same order) between requests, because changing it invalidates the whole cache.

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    tools=TOOLS,  # rendered first
    system=[{"type": "text", "text": LONG_INSTRUCTIONS, "cache_control": {"type": "ephemeral"}}],
    messages=messages,
)
```

## Strategy 3: Multi-Turn Caching
In a long conversation, put a breakpoint on the last block of the newest turn so each request reads the earlier history from the cache. The simplest way is a top-level `cache_control`, which the API places on the last cacheable block for you:

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},  # automatic breakpoint on the last cacheable block
    messages=messages,
)
```

To place it yourself, convert the content of the last message to a block list first (string content has no place for `cache_control`):

```python
last = messages[-1]
if isinstance(last["content"], str):
    last["content"] = [{"type": "text", "text": last["content"]}]
last["content"][-1]["cache_control"] = {"type": "ephemeral"}
```

Earlier breakpoints stay valid read points, but remember the limit of 4 per request; remove old markers as you add new ones.

## Monitoring Hit Rate
Check `usage` stats in the response.
- `cache_creation_input_tokens`: Written to cache (billed at the write rate).
- `cache_read_input_tokens`: Read from cache (a hit).
- `input_tokens`: only the tokens after the last breakpoint, not the total.

**Goal:** Maximize Read, Minimize Creation.

## Next Steps
- Learn more about [Cost Reduction](./07_cost_reduction.md).
