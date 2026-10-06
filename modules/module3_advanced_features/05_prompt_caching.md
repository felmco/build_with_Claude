# 3.2 Understanding Prompt Caching

## Introduction
Prompt caching allows you to reuse large portions of your prompt across multiple requests, dramatically reducing costs (cache reads cost about 10% of the normal input price) and latency for repeated content.

## Why Prompt Caching?

### Without Caching
Every API call processes the entire prompt from scratch:
```
Request 1: Process 10,000 tokens → Full cost
Request 2: Process 10,000 tokens → Full cost (same content!)
Request 3: Process 10,000 tokens → Full cost (same content!)
```

### With Caching
Reuse cached portions:
```
Request 1: Process 10,000 tokens → Cache them → Full cost + 25% write premium
Request 2: Read from cache → 90% cost reduction!
Request 3: Read from cache → 90% cost reduction!
```

## Cost Comparison

### Pricing (multipliers of the base input price)
- **Cache write (5-minute TTL)**: 1.25x base input price
- **Cache write (1-hour TTL)**: 2x base input price
- **Cache read**: about 0.1x base input price (even less on some models, for example 0.05x on Claude Opus 5.5)

Prices change, so check the [pricing page](https://claude.com/pricing). The example below uses Claude Sonnet 5.5 at $2 per million input tokens: $2.50 per MTok for a 5-minute cache write and $0.20 per MTok for a cache read.

### Example Calculation
10,000 token prompt, used 100 times (within the cache lifetime):

**Without caching**:
```
100 requests × 10,000 tokens × $2/MTok = $2.00
```

**With caching**:
```
Write: 1 × 10,000 × $2.50/MTok = $0.025
Reads: 99 × 10,000 × $0.20/MTok = $0.198
Total: $0.025 + $0.198 = $0.223
Savings: $2.00 - $0.223 = $1.777 (about 89% reduction)
```

Because a write costs 1.25x and a read 0.1x, caching pays off after as few as two requests that share the prefix.

## How Prompt Caching Works

### Cache Breakpoints
Mark content to be cached using `cache_control`:

```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an AI assistant with access to the following documentation...",
        },
        {
            "type": "text",
            "text": "<long documentation content here>",
            "cache_control": {"type": "ephemeral"}  # Cache this!
        }
    ],
    messages=[
        {"role": "user", "content": "Based on the docs, explain feature X"}
    ]
)
```

### Cache Duration
- **Default duration**: 5 minutes (`{"type": "ephemeral"}`)
- **Refresh**: Each cache hit resets the timer at no extra cost, so a prefix that is used at least every 5 minutes stays warm
- **1-hour option**: `{"type": "ephemeral", "ttl": "1h"}` costs more to write (2x) but survives longer gaps between requests
- **Limits**: at most 4 `cache_control` breakpoints per request. Caches are scoped to your workspace and to the model.
- **Minimum size**: the prefix must reach a model-dependent minimum (512 to 4096 tokens, see Troubleshooting) or it is silently not cached.

## Basic Caching Example

**simple_caching.py**:
```python
#!/usr/bin/env python3
"""Basic prompt caching example"""

from anthropic import Anthropic
import time

client = Anthropic()

# Large knowledge base to cache
KNOWLEDGE_BASE = """
Python Programming Guide:
=========================

1. Variables and Data Types:
   - Strings: text data enclosed in quotes
   - Integers: whole numbers
   - Floats: decimal numbers
   - Lists: ordered collections [1, 2, 3]
   - Dictionaries: key-value pairs {"key": "value"}

2. Control Flow:
   - if/elif/else: conditional execution
   - for loops: iterate over sequences
   - while loops: repeat while condition is true

3. Functions:
   - def function_name(parameters):
   - return values
   - *args and **kwargs for flexible parameters

4. Classes:
   - class ClassName:
   - __init__ method for initialization
   - self parameter for instance reference

[... imagine this is several thousand tokens of documentation ...]
"""

def ask_with_caching(question: str):
    """Ask question with cached knowledge base"""

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": "You are a Python programming expert. Use the following documentation to answer questions:"
            },
            {
                "type": "text",
                "text": KNOWLEDGE_BASE,
                "cache_control": {"type": "ephemeral"}  # Cache this block
            }
        ],
        messages=[
            {"role": "user", "content": question}
        ]
    )

    # Check cache usage
    usage = response.usage
    print(f"""
📊 Token Usage:
   Input tokens (uncached): {usage.input_tokens}
   Cache creation: {getattr(usage, 'cache_creation_input_tokens', 0)}
   Cache read: {getattr(usage, 'cache_read_input_tokens', 0)}
   Output tokens: {usage.output_tokens}
    """)

    return next(b.text for b in response.content if b.type == "text")

def main():
    """Test caching with multiple requests"""

    questions = [
        "What are Python data types?",
        "Explain Python functions",
        "How do classes work in Python?",
        "What are control flow statements?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"Request #{i}: {question}")
        print('='*60)

        answer = ask_with_caching(question)
        print(f"\n💬 Answer: {answer}")

        if i < len(questions):
            print("\n⏳ Waiting 1 second...")
            time.sleep(1)  # Small delay between requests

if __name__ == "__main__":
    main()
```

**Expected Output**:
```
Request #1: What are Python data types?
📊 Token Usage:
   Input tokens: 150
   Cache creation: 2500  ← Created cache (first time)
   Cache read: 0
   Output tokens: 120

Request #2: Explain Python functions
📊 Token Usage:
   Input tokens: 150
   Cache creation: 0
   Cache read: 2500  ← Read from cache! (90% savings)
   Output tokens: 115
```

## Caching System Prompts

### Single System Prompt
```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Very long system instructions...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Question"}]
)
```

### Multiple System Blocks
```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "General instructions (not cached)",
        },
        {
            "type": "text",
            "text": "Large knowledge base part 1...",
            "cache_control": {"type": "ephemeral"}  # Cache point 1
        },
        {
            "type": "text",
            "text": "Large knowledge base part 2...",
            "cache_control": {"type": "ephemeral"}  # Cache point 2
        }
    ],
    messages=[{"role": "user", "content": "Question"}]
)
```

## Caching Conversation History

### Caching Long Conversations

Put a breakpoint on the last block of the most recent turn. Each new request then reads the whole earlier conversation from the cache. (If you do not need to control placement, you can instead pass a top-level `cache_control={"type": "ephemeral"}` to `messages.create()`, which places the breakpoint on the last cacheable block automatically.)

```python
def chat_with_caching(messages: list, new_message: str):
    """Chat with cached conversation history"""

    # Add new user message
    messages.append({
        "role": "user",
        "content": new_message
    })

    # Mark last few turns for caching (conversation context)
    # Clone messages to avoid modifying original
    cached_messages = messages[:-1]  # All but last message
    if cached_messages:
        # Add cache control to the last message before current
        last_msg = cached_messages[-1].copy()
        if isinstance(last_msg["content"], str):
            last_msg["content"] = [
                {
                    "type": "text",
                    "text": last_msg["content"],
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        cached_messages[-1] = last_msg

    # Add current message without cache control
    cached_messages.append(messages[-1])

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=cached_messages
    )

    # Add assistant response to history (text only; in tool-use loops
    # append response.content unchanged so thinking blocks are preserved)
    messages.append({
        "role": "assistant",
        "content": next(b.text for b in response.content if b.type == "text")
    })

    return response
```

## Caching with Tools

**tools_with_caching.py**:
```python
#!/usr/bin/env python3
"""Caching with tool definitions"""

from anthropic import Anthropic

client = Anthropic()

# Large tool definitions (cache these!)
TOOLS = [
    {
        "name": "search_database",
        "description": "Searches a large database with complex query capabilities...",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "filters": {"type": "object", "description": "Filter criteria"},
                "limit": {"type": "integer", "description": "Result limit"}
            },
            "required": ["query"]
        }
    },
    # ... imagine 50 more tool definitions ...
]

def query_with_tools_cached(question: str):
    """Query with cached tool definitions"""

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        tools=TOOLS,
        system=[
            {
                "type": "text",
                "text": "You are a helpful assistant with access to various tools.",
                "cache_control": {"type": "ephemeral"}  # Cache system + tools
            }
        ],
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return response
```

## Caching Best Practices

### 1. Cache Large, Reused Content
✅ **Good candidates for caching**:
- Large documentation
- System instructions
- Few-shot examples
- Tool definitions
- Knowledge bases
- Conversation history

❌ **Poor candidates**:
- Prompts below the model's minimum cacheable size (512 to 4096 tokens depending on the model)
- Unique, one-time content
- Frequently changing content

### 2. Position Cached Content Strategically
```python
# ❌ Bad: Variable content at the end of cache
system = [
    {
        "type": "text",
        "text": f"Large docs... User preferences: {user_prefs}",  # Changes per user!
        "cache_control": {"type": "ephemeral"}
    }
]

# ✅ Good: Stable content in cache
system = [
    {
        "type": "text",
        "text": "Large docs...",  # Stable content
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": f"User preferences: {user_prefs}"  # Variable, not cached
    }
]
```

### 3. Cache at Natural Breakpoints
```python
system = [
    {
        "type": "text",
        "text": "Core instructions...",
    },
    {
        "type": "text",
        "text": "Documentation section 1...",
        "cache_control": {"type": "ephemeral"}  # Breakpoint 1
    },
    {
        "type": "text",
        "text": "Documentation section 2...",
        "cache_control": {"type": "ephemeral"}  # Breakpoint 2
    }
]
```

### 4. Monitor Cache Performance
```python
def monitor_cache_usage(response):
    """Monitor cache hit rate and savings"""
    usage = response.usage

    cache_creation = getattr(usage, 'cache_creation_input_tokens', 0)
    cache_read = getattr(usage, 'cache_read_input_tokens', 0)
    input_tokens = usage.input_tokens

    if cache_read > 0:
        # Cache hit!
        savings_percent = (cache_read / (cache_read + input_tokens)) * 100
        print(f"✅ Cache hit! {savings_percent:.1f}% of input from cache")
    elif cache_creation > 0:
        # Created cache
        print(f"📝 Created cache: {cache_creation} tokens")
    else:
        # No caching
        print("❌ No caching used")

    return {
        "cache_creation": cache_creation,
        "cache_read": cache_read,
        "input_tokens": input_tokens,
        "cache_hit_rate": cache_read / (cache_read + input_tokens) if cache_read > 0 else 0
    }
```

## Advanced: Multi-Level Caching

```python
#!/usr/bin/env python3
"""Multi-level caching strategy"""

from anthropic import Anthropic

client = Anthropic()

def multi_level_cache(project_id: str, user_query: str):
    """
    Level 1: Global documentation (cache for all users)
    Level 2: Project-specific context (cache per project)
    Level 3: User-specific data (not cached, changes frequently)
    """

    # Level 1: Global (least frequently changes)
    global_docs = "Global API documentation..."

    # Level 2: Project-specific (changes per project)
    project_context = f"Project {project_id} specific information..."

    # Level 3: User-specific (changes every request)
    user_context = f"Current query: {user_query}"

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": global_docs,
                "cache_control": {"type": "ephemeral"}  # Level 1 cache
            },
            {
                "type": "text",
                "text": project_context,
                "cache_control": {"type": "ephemeral"}  # Level 2 cache
            },
            {
                "type": "text",
                "text": "You are a helpful assistant."  # Not cached
            }
        ],
        messages=[
            {"role": "user", "content": user_context}  # Not cached
        ]
    )

    return response
```

## Caching with Images

```python
import base64

# Cache image data for repeated analysis
with open("diagram.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    },
                    "cache_control": {"type": "ephemeral"}  # Cache image
                },
                {
                    "type": "text",
                    "text": "Analyze this diagram"
                }
            ]
        }
    ]
)
```

## Real-World Example: RAG with Caching

**rag_with_caching.py**:
```python
#!/usr/bin/env python3
"""RAG (Retrieval Augmented Generation) with caching"""

from anthropic import Anthropic
from typing import List

client = Anthropic()

class CachedRAG:
    """RAG system with prompt caching"""

    def __init__(self, knowledge_base: str):
        self.knowledge_base = knowledge_base
        self.client = Anthropic()

    def query(self, question: str, context_docs: List[str] = None):
        """
        Query with cached knowledge base and optional fresh context
        """
        system_parts = [
            {
                "type": "text",
                "text": "You are a helpful assistant. Answer questions based on the provided knowledge base."
            },
            {
                "type": "text",
                "text": f"Knowledge Base:\n{self.knowledge_base}",
                "cache_control": {"type": "ephemeral"}  # Cache main KB
            }
        ]

        # Add fresh context documents (not cached)
        if context_docs:
            context_text = "\n\n".join(context_docs)
            system_parts.append({
                "type": "text",
                "text": f"Additional Context:\n{context_text}"
            })

        response = self.client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            system=system_parts,
            messages=[
                {"role": "user", "content": question}
            ]
        )

        return next(b.text for b in response.content if b.type == "text")

def main():
    """Test RAG with caching"""

    # Large knowledge base (cached)
    kb = """
    Product Documentation:
    - Product A: Features, pricing, specifications...
    - Product B: Features, pricing, specifications...
    [... imagine 10,000 tokens of documentation ...]
    """

    rag = CachedRAG(kb)

    # First query - creates cache
    print("Query 1:")
    answer1 = rag.query("What are the features of Product A?")
    print(answer1)

    # Second query - uses cache
    print("\nQuery 2:")
    answer2 = rag.query("How much does Product B cost?")
    print(answer2)

    # Query with additional context
    print("\nQuery 3 with fresh context:")
    fresh_context = ["Product A is currently on sale for 20% off"]
    answer3 = rag.query("Is Product A on sale?", context_docs=fresh_context)
    print(answer3)

if __name__ == "__main__":
    main()
```

## Troubleshooting

### Cache Not Being Used
**Problem**: `cache_read_input_tokens` is always 0

**Solutions**:
1. Check the minimum cacheable prefix. It depends on the model: 512 tokens on Claude Sonnet 5.5, Opus 5.5, and Fable 5.1; 1024 on several earlier Sonnet/Opus models; 4096 on Claude Haiku 4.5. Shorter prefixes are silently not cached (no error, `cache_creation_input_tokens` is 0). Confirm the current value in the docs.
2. Verify the cache hasn't expired (5 minutes by default, measured from the start of the last request that wrote or read it)
3. Ensure the prefix is byte-identical. The cache is a prefix match in the order tools, system, messages, so a timestamp, a changed tool list, or unsorted JSON keys early in the prompt invalidates everything after it.
4. Confirm `cache_control` is set on the last block of the stable prefix, and that you use the same model and workspace

### High Cache Creation Costs
**Problem**: Creating too many caches

**Solutions**:
1. Consolidate cacheable content
2. Use fewer cache breakpoints
3. Cache only frequently reused content
4. Make sure the prefix is stable, so entries are read instead of rewritten

## Quick Reference

```python
# Cache system prompt
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Large content to cache...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Question"}]
)

# Check cache usage
usage = message.usage
print(f"Cache created: {usage.cache_creation_input_tokens}")
print(f"Cache read: {usage.cache_read_input_tokens}")
```

## Next Steps
- Learn about [Cache Optimization Strategies](./06_cache_optimization.md)
- Explore [Cost Reduction Techniques](./07_cost_reduction.md)
- Try [Batch Processing](./08_batch_processing.md)

## Additional Resources
- [Official Prompt Caching Documentation](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Prompt Caching Announcement](https://www.anthropic.com/news/prompt-caching)
- [Caching Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#best-practices)
