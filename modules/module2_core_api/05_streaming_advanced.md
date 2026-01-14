# 2.2 Advanced Streaming Patterns

Building on the basics, let's explore advanced streaming techniques for production applications.

## Handling Stream Events

The `client.messages.stream()` context manager handles a lot of complexity for you. Sometimes you need raw access to events.

### Async Streaming

For high-performance web apps (FastAPI, Django, etc.), use the `AsyncAnthropic` client.

```python
import asyncio
from anthropic import AsyncAnthropic

async def stream_chat():
    client = AsyncAnthropic()

    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Tell me a joke"}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(stream_chat())
```

## Streaming with Tool Use

When using tools (function calling) with streaming, you need to handle tool events.

```python
# (Simplified concept)
async with client.messages.stream(..., tools=[...]) as stream:
    for event in stream:
        if event.type == "tool_use":
            # Handle tool call
            pass
        elif event.type == "text_delta":
            # Handle text
            pass
```

*Note: The helper `stream` object simplifies this. It accumulates tool inputs automatically.*

## Error Handling in Streams

Errors can occur mid-stream (e.g., network disconnect).

```python
try:
    with client.messages.stream(...) as stream:
        for text in stream.text_stream:
            print(text)
except anthropic.APIConnectionError:
    print("Stream disconnected. Implement retry logic here.")
```

## Optimizing Perceived Latency

1. **Flush output immediately:** Don't buffer text on your server; send it to the frontend client via WebSockets or SSE (Server-Sent Events) immediately.
2. **Small chunks:** Processing smaller chunks updates the UI faster.

## Example: SSE (Server-Sent Events) Adapter

If you are building a web server, you'll often convert the Anthropic stream into an SSE stream for the browser.

```python
# Pseudo-code for a Flask/FastAPI endpoint
def generate_sse():
    with client.messages.stream(...) as stream:
        for text in stream.text_stream:
            # SSE format: "data: <content>\n\n"
            yield f"data: {text}\n\n"
    yield "data: [DONE]\n\n"
```

## Next Steps
- Explore multimodal capabilities in [Vision and Images](./06_vision_images.md).
