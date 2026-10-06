# 2.1 Managing Conversations

The Messages API is stateless, meaning Claude doesn't "remember" past requests automatically. You must manage the conversation history yourself.

## How Context Works

To have a multi-turn conversation, you append each new message to a list and send the *entire* list back to the API with each new request.

### The Conversation Loop

```python
import anthropic

client = anthropic.Anthropic()
conversation_history = []

def chat_turn(user_input):
    # 1. Add user message to history
    conversation_history.append({"role": "user", "content": user_input})

    # 2. Send history to API
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=conversation_history
    )

    # 3. Get assistant response (join the text blocks; content can also hold thinking blocks)
    assistant_reply = "".join(b.text for b in response.content if b.type == "text")
    print(f"Claude: {assistant_reply}")

    # 4. Add assistant response to history
    conversation_history.append({"role": "assistant", "content": assistant_reply})

# Example usage
chat_turn("Hi, my name is Alex.")
chat_turn("What is my name?")
```

## Managing Context Window

Claude has a large context window (200K to 1M tokens depending on the model), but it's not infinite.

### Strategies for Long Conversations

1. **Truncation:** Remove the oldest messages when the limit is reached.
2. **Summarization:** Ask Claude to summarize the conversation so far, and replace old messages with the summary.
3. **Filtering:** Remove less important messages (e.g., "Okay", "Thanks").

### Example: Simple Truncation

```python
MAX_HISTORY = 10  # Keep last 10 messages

def truncate(history, max_messages=MAX_HISTORY):
    """Keep the last N messages; the system prompt is a separate parameter, so it is unaffected."""
    trimmed = history[-max_messages:]
    # The list must start with a user message
    while trimmed and trimmed[0]["role"] != "user":
        trimmed = trimmed[1:]
    return trimmed

conversation_history = truncate(conversation_history)
```

## User vs. Assistant Roles

- **User**: The human input.
- **Assistant**: Claude's output.

**Rules:**
- Roles should alternate (User -> Assistant -> User).
- The list must start with a `user` message.

### Controlling the Output Format (Prefill Is Removed)
Older tutorials "put words in Claude's mouth" by ending the list with an `assistant` message (for example `{`). **That prefill returns a 400 error on current models** (Fable 5.1, Opus 5.5, Sonnet 5.5, and the 4.6+ family). Use one of these instead:

- **Structured outputs**: constrain the response to a JSON schema with `output_config.format`.
- **Clear instructions** in the system prompt ("Respond with a single JSON object and nothing else").

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Describe a car as JSON."}],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "make": {"type": "string"},
                    "model": {"type": "string"},
                    "year": {"type": "integer"},
                },
                "required": ["make", "model", "year"],
                "additionalProperties": False,
            },
        }
    },
)
print(response.content[0].text)  # valid JSON matching the schema (check stop_reason != "refusal" first)
```

Check the [Structured outputs docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) for the SDK helper `client.messages.parse()`.

## Next Steps
- Learn about [Streaming Responses](./04_streaming_basics.md) for real-time feedback.
