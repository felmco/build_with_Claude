# 2.4 Streaming Basics

## Introduction
Streaming allows you to receive Claude's response in real-time as it's generated, rather than waiting for the entire response. This creates a better user experience, especially for long responses.

## Why Use Streaming?

### Benefits
✅ **Better UX**: Users see responses immediately
✅ **Perceived Speed**: Feels faster even if total time is same
✅ **Real-time Feedback**: Users can interrupt if needed
✅ **Progressive Loading**: Display content as it arrives

### When to Use Streaming
- Chatbots and conversational interfaces
- Long-form content generation
- Real-time applications
- Interactive tools

### When NOT to Use Streaming
- Batch processing
- Automated testing
- When you need the complete response before processing
- Logging or storing full responses

## Basic Streaming Example

### Simple Streaming
```python
from anthropic import Anthropic

client = Anthropic()

# Enable streaming with stream=True
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Tell me a short story about a robot"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()  # New line at end
```

**Output** (appears progressively):
```
Once upon a time, there was a small robot named Bolt...
```

### Complete Streaming Example with All Events
```python
from anthropic import Anthropic

client = Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain Python in 3 sentences"}
    ]
) as stream:
    # Get each text chunk as it arrives
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Access final message after streaming completes
final_message = stream.get_final_message()
print(f"\n\nTokens used: {final_message.usage.output_tokens}")
```

## Stream Events

### Understanding Stream Events
Streaming provides several event types:

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for event in stream:
        # Event types:
        # - message_start: Beginning of response
        # - content_block_start: Start of content block
        # - content_block_delta: New content chunk
        # - content_block_stop: End of content block
        # - message_delta: Message metadata update
        # - message_stop: End of response

        print(f"Event type: {event.type}")
```

### Handling Different Event Types
```python
from anthropic import Anthropic
from anthropic.types import (
    MessageStartEvent,
    ContentBlockStartEvent,
    ContentBlockDeltaEvent,
    ContentBlockStopEvent,
    MessageDeltaEvent,
    MessageStopEvent
)

client = Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Count to 5"}]
) as stream:
    for event in stream:
        if isinstance(event, MessageStartEvent):
            print("🟢 Message started")
            print(f"   Model: {event.message.model}")

        elif isinstance(event, ContentBlockStartEvent):
            print("📝 Content block started")

        elif isinstance(event, ContentBlockDeltaEvent):
            # This is where the actual text comes through
            if hasattr(event.delta, 'text'):
                print(event.delta.text, end="", flush=True)

        elif isinstance(event, ContentBlockStopEvent):
            print("\n📝 Content block ended")

        elif isinstance(event, MessageDeltaEvent):
            print(f"🔄 Message delta: {event.delta.stop_reason}")

        elif isinstance(event, MessageStopEvent):
            print("🔴 Message stopped")
```

## Stream Helpers

### text_stream (Simplest)
Get only the text content:

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a haiku"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### get_final_message()
Access complete message after streaming:

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Get final message with metadata
message = stream.get_final_message()
print(f"\n\nInput tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")
print(f"Stop reason: {message.stop_reason}")
```

### get_final_text()
Get complete text after streaming:

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Say hello"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Get complete text
full_text = stream.get_final_text()
print(f"\n\nFull response: {full_text}")
```

## Practical Streaming Patterns

### Pattern 1: Console Output with Typing Effect
```python
import sys
import time

def stream_with_typing_effect(prompt: str, delay: float = 0.01):
    """Stream with typing effect"""
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            sys.stdout.write(text)
            sys.stdout.flush()
            time.sleep(delay)  # Small delay for typing effect
    print()

# Usage
stream_with_typing_effect("Tell me a joke")
```

### Pattern 2: Streaming with Progress Indicator
```python
import sys

def stream_with_progress(prompt: str):
    """Stream with character count progress"""
    char_count = 0

    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            char_count += len(text)

    print(f"\n\n📊 Generated {char_count} characters")

# Usage
stream_with_progress("Write a paragraph about AI")
```

### Pattern 3: Collecting Streamed Content
```python
def stream_and_collect(prompt: str) -> tuple[str, dict]:
    """Stream text and collect full response"""
    collected_text = []

    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            collected_text.append(text)

        # Get final message
        final_message = stream.get_final_message()

    full_text = "".join(collected_text)
    metadata = {
        "tokens": final_message.usage.output_tokens,
        "stop_reason": final_message.stop_reason
    }

    return full_text, metadata

# Usage
text, meta = stream_and_collect("Explain quantum computing")
print(f"\n\nTokens: {meta['tokens']}")
```

### Pattern 4: Streaming to File
```python
def stream_to_file(prompt: str, filename: str):
    """Stream response directly to file"""
    with open(filename, 'w') as f:
        with client.messages.stream(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                f.write(text)
                f.flush()  # Ensure immediate write
                print(text, end="", flush=True)  # Also show on screen

    print(f"\n\n✅ Saved to {filename}")

# Usage
stream_to_file("Write a long article about Python", "article.txt")
```

### Pattern 5: Streaming with Error Handling
```python
from anthropic import APIError, APIConnectionError

def safe_stream(prompt: str):
    """Stream with comprehensive error handling"""
    try:
        with client.messages.stream(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)

    except APIConnectionError as e:
        print(f"\n❌ Connection error: {e}")
        print("Check your internet connection")

    except APIError as e:
        print(f"\n❌ API error: {e}")
        print("Try again in a moment")

    except KeyboardInterrupt:
        print("\n\n⚠️  Streaming interrupted by user")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

# Usage
safe_stream("Tell me about the solar system")
```

## Async Streaming

### Basic Async Streaming
```python
import asyncio
from anthropic import AsyncAnthropic

async def async_stream_example():
    """Async streaming example"""
    client = AsyncAnthropic()

    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Count to 10"}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

    print()

# Run async function
asyncio.run(async_stream_example())
```

### Concurrent Async Streams
```python
import asyncio
from anthropic import AsyncAnthropic

async def stream_response(client, prompt: str, label: str):
    """Stream a single response"""
    print(f"\n{label}:")
    print("-" * 40)

    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

    print()

async def concurrent_streams():
    """Run multiple streams concurrently"""
    client = AsyncAnthropic()

    # Create multiple streaming tasks
    tasks = [
        stream_response(client, "Count to 5", "Stream 1"),
        stream_response(client, "List 3 colors", "Stream 2"),
        stream_response(client, "Name 3 animals", "Stream 3")
    ]

    # Run all streams concurrently
    await asyncio.gather(*tasks)

# Run concurrent streams
asyncio.run(concurrent_streams())
```

## Building a Streaming Chatbot

**streaming_chatbot.py**:
```python
#!/usr/bin/env python3
"""Interactive streaming chatbot"""

from anthropic import Anthropic
from typing import List, Dict

class StreamingChatbot:
    """Simple streaming chatbot"""

    def __init__(self):
        self.client = Anthropic()
        self.conversation: List[Dict] = []
        self.model = "claude-sonnet-4-5-20250929"

    def chat(self, user_message: str):
        """Send message and stream response"""
        # Add user message to conversation
        self.conversation.append({
            "role": "user",
            "content": user_message
        })

        print("Claude: ", end="", flush=True)

        # Stream response
        with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            messages=self.conversation
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)

            # Get complete response
            final_message = stream.get_final_message()
            assistant_message = final_message.content[0].text

        # Add assistant response to conversation
        self.conversation.append({
            "role": "assistant",
            "content": assistant_message
        })

        print()  # New line after response

def main():
    """Run chatbot"""
    bot = StreamingChatbot()

    print("Streaming Chatbot (type 'quit' to exit)")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            bot.chat(user_input)
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
```

## Performance Considerations

### Time to First Token (TTFT)
```python
import time

def measure_streaming_performance(prompt: str):
    """Measure streaming performance metrics"""
    start_time = time.time()
    first_token_time = None
    token_count = 0

    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            if first_token_time is None:
                first_token_time = time.time()
                ttft = first_token_time - start_time
                print(f"⏱️  Time to first token: {ttft:.2f}s\n")

            print(text, end="", flush=True)
            token_count += 1

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n\n📊 Performance:")
    print(f"   TTFT: {ttft:.2f}s")
    print(f"   Total time: {total_time:.2f}s")
    print(f"   Chunks received: {token_count}")

# Usage
measure_streaming_performance("Explain neural networks")
```

## Common Issues and Solutions

### Issue 1: Buffering Problems
```python
# ❌ Without flush - may buffer
for text in stream.text_stream:
    print(text)  # May not appear immediately

# ✅ With flush - immediate display
for text in stream.text_stream:
    print(text, end="", flush=True)  # Appears immediately
```

### Issue 2: Unicode/Emoji Issues
```python
import sys

# Ensure proper encoding
sys.stdout.reconfigure(encoding='utf-8')

with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Use emojis to describe weather"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Issue 3: Interrupted Streams
```python
def handle_interrupted_stream(prompt: str):
    """Handle stream interruption gracefully"""
    try:
        with client.messages.stream(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)

    except KeyboardInterrupt:
        print("\n\n⚠️  Stream interrupted")
        # Can still access partial response if needed
        try:
            partial = stream.get_final_text()
            print(f"Partial response: {partial}")
        except:
            pass

# Usage
handle_interrupted_stream("Write a long story")
```

## Best Practices

1. **Always use `flush=True`** for immediate output
2. **Handle interruptions** gracefully with try/except
3. **Use async streaming** for concurrent requests
4. **Consider buffering** for very fast output
5. **Monitor performance** (TTFT, throughput)
6. **Test with slow connections** to verify UX
7. **Provide feedback** to users during streaming

## Quick Reference

```python
# Basic streaming
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Get final message
final_message = stream.get_final_message()
print(f"Tokens: {final_message.usage.output_tokens}")
```

## Next Steps
- Learn [Advanced Streaming Patterns](./05_streaming_advanced.md)
- Explore [Vision and Images](./06_vision_images.md)
- Build a [Conversational Interface](./03_conversations.md)

## Additional Resources
- [Streaming API Documentation](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Server-Sent Events (SSE) Spec](https://html.spec.whatwg.org/multipage/server-sent-events.html)
