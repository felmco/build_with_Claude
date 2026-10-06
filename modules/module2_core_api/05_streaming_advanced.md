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
        model="claude-sonnet-5-5",
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
import anthropic

client = anthropic.Anthropic()

# Define `tools` as in the tool use lesson
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
) as stream:
    for event in stream:
        if event.type == "content_block_start" and event.content_block.type == "tool_use":
            print(f"Tool call started: {event.content_block.name}")
        elif event.type == "text":
            print(event.text, end="", flush=True)  # helper event with the text chunk

    # The helper accumulates streamed tool inputs for you
    final = stream.get_final_message()

for block in final.content:
    if block.type == "tool_use":
        print(block.name, block.input)  # complete, parsed input
```

*Note: Tool inputs arrive as partial JSON (`input_json` events). Read the complete input from `get_final_message()` instead of parsing the fragments yourself.*

## Error Handling in Streams

Errors can occur mid-stream (e.g., network disconnect).

```python
import anthropic

client = anthropic.Anthropic()

try:
    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Tell me a story"}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
except anthropic.APIConnectionError:
    # The SDK does not resume a stream that breaks mid-way. Discard the partial
    # output and retry the whole request (see the retry lesson).
    print("Stream disconnected. Implement retry logic here.")
```

## Optimizing Perceived Latency

1. **Flush output immediately:** Don't buffer text on your server; send it to the frontend client via WebSockets or SSE (Server-Sent Events) immediately.
2. **Small chunks:** Processing smaller chunks updates the UI faster.

## Example: SSE (Server-Sent Events) Adapter

If you are building a web server, you'll often convert the Anthropic stream into an SSE stream for the browser.

```python
import json

# Sketch for a Flask/FastAPI endpoint (wrap the generator in a streaming response
# with media_type "text/event-stream")
def generate_sse(prompt: str):
    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            # SSE format: "data: <content>\n\n". JSON-encode the chunk so newlines
            # inside the text cannot break the framing.
            yield f"data: {json.dumps(text)}\n\n"
    yield "data: [DONE]\n\n"
```

## Next Steps
- Explore multimodal capabilities in [Vision and Images](./06_vision_images.md).
