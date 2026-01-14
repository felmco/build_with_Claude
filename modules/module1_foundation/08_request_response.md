# 1.3 Understanding Requests and Responses

The Claude API uses a JSON-based structure for inputs and outputs. Understanding this structure is key to effective development.

## The Message Object

When you call `client.messages.create()`, you are creating a **Message**.

### Request Structure (Input)

```python
{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, Claude!"}
    ]
}
```

**Key Fields:**
- `model`: (Required) The ID of the model to use.
- `max_tokens`: (Required) The maximum output length.
- `messages`: (Required) A list of message objects (`role` and `content`).
- `system`: (Optional) System-level instructions.
- `temperature`: (Optional) Controls randomness (0.0 to 1.0).

### Response Structure (Output)

The API returns a `Message` object. Here represents its JSON structure:

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello! How can I assist you today?"
    }
  ],
  "model": "claude-sonnet-4-5-20250929",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "output_tokens": 9
  }
}
```

**Key Fields:**
- `id`: Unique identifier for the request.
- `content`: An list of content blocks. Usually contains one text block.
- `role`: Always "assistant" for responses.
- `stop_reason`: Why the generation stopped.
  - `"end_turn"`: Natural completion.
  - `"max_tokens"`: Hit the limit.
- `usage`: Token counts for billing.

## Accessing Response Data in Python

The Python SDK wraps this JSON in an object.

```python
response = client.messages.create(...)

# Get the text content
text = response.content[0].text

# Get the ID
msg_id = response.id

# Get usage stats
input_tokens = response.usage.input_tokens
```

## Next Steps
- Learn how to handle potential issues in [Basic Error Handling](./09_error_handling.md).
