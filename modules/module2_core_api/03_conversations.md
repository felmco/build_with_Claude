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
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=conversation_history
    )

    # 3. Get assistant response
    assistant_reply = response.content[0].text
    print(f"Claude: {assistant_reply}")

    # 4. Add assistant response to history
    conversation_history.append({"role": "assistant", "content": assistant_reply})

# Example usage
chat_turn("Hi, my name is Alex.")
chat_turn("What is my name?")
```

## Managing Context Window

Claude has a large context window (200K tokens), but it's not infinite.

### Strategies for Long Conversations

1. **Truncation:** Remove the oldest messages when the limit is reached.
2. **Summarization:** Ask Claude to summarize the conversation so far, and replace old messages with the summary.
3. **Filtering:** Remove less important messages (e.g., "Okay", "Thanks").

### Example: Simple Truncation

```python
MAX_HISTORY = 10  # Keep last 10 messages

if len(conversation_history) > MAX_HISTORY:
    # Keep the system prompt or first message if crucial?
    # Here we just slice the last N messages
    conversation_history = conversation_history[-MAX_HISTORY:]
```

## User vs. Assistant Roles

- **User**: The human input.
- **Assistant**: Claude's output.

**Rules:**
- Roles must alternate (User -> Assistant -> User).
- The list must start with a `user` message.

### Prefilling the Assistant Response
You can "put words in Claude's mouth" by adding an `assistant` message as the last message in the list *without* a corresponding user message following it. This is useful for:
- Forcing a specific format (e.g., `{`).
- Guiding the tone.

*Note: This feature is handled differently in the API. You supply the prefill as the last message with role `assistant`.*

```python
messages = [
    {"role": "user", "content": "Write a JSON object describing a car."},
    {"role": "assistant", "content": "{"} # Prefill
]

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=messages
)
# Claude continues from "{":  "make": "Toyota", ...
```

## Next Steps
- Learn about [Streaming Responses](./04_streaming_basics.md) for real-time feedback.
