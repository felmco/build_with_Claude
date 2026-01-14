# 3.2 Understanding Prompt Caching

## Introduction
Prompt caching allows you to reuse large portions of your prompt across multiple requests, dramatically reducing costs (up to 90%) and latency (up to 80%) for repeated content.

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
Request 1: Process 10,000 tokens → Cache them → Full cost
Request 2: Read from cache → 90% cost reduction!
Request 3: Read from cache → 90% cost reduction!
```

## Cost Comparison

### Pricing (Approximate)
- **Regular input tokens**: $3 per million tokens
- **Cache write**: $3.75 per million tokens (25% more)
- **Cache read**: $0.30 per million tokens (90% less!)

### Example Calculation
10,000 token prompt, used 100 times:

**Without caching**:
```
100 requests × 10,000 tokens × $3/MTok = $3.00
```

**With caching**:
```
Write: 1 × 10,000 × $3.75/MTok = $0.0375
Reads: 99 × 10,000 × $0.30/MTok = $0.297
Total: $0.0375 + $0.297 = $0.3345
Savings: $3.00 - $0.33 = $2.67 (89% reduction!)
```

## How Prompt Caching Works

### Cache Breakpoints
Mark content to be cached using `cache_control`:

```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
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
- **Duration**: 5 minutes
- **Refresh**: Each cache hit extends duration by 5 minutes
- **Maximum**: Caches last as long as they're used within 5-minute windows

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

[... imagine this is 10,000+ tokens of documentation ...]
"""

def ask_with_caching(question: str):
    """Ask question with cached knowledge base"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
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
   Input tokens: {usage.input_tokens}
   Cache creation: {getattr(usage, 'cache_creation_input_tokens', 0)}
   Cache read: {getattr(usage, 'cache_read_input_tokens', 0)}
   Output tokens: {usage.output_tokens}
    """)

    return response.content[0].text

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
    model="claude-sonnet-4-5-20250929",
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
    model="claude-sonnet-4-5-20250929",
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
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=cached_messages
    )

    # Add assistant response to history
    messages.append({
        "role": "assistant",
        "content": response.content[0].text
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
        model="claude-sonnet-4-5-20250929",
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
- Small prompts (< 1000 tokens)
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
        model="claude-sonnet-4-5-20250929",
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
    model="claude-sonnet-4-5-20250929",
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
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            system=system_parts,
            messages=[
                {"role": "user", "content": question}
            ]
        )

        return response.content[0].text

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
1. Check minimum cache size (must be substantial)
2. Verify cache duration hasn't expired (5 minutes)
3. Ensure exact same content is being sent
4. Confirm `cache_control` is properly set

### High Cache Creation Costs
**Problem**: Creating too many caches

**Solutions**:
1. Consolidate cacheable content
2. Use fewer cache breakpoints
3. Cache only frequently reused content
4. Consider batch processing

## Quick Reference

```python
# Cache system prompt
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
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
