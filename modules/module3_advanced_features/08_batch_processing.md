# 3.3 Message Batches API

The Message Batches API allows you to send a large group of requests at once.

## Key Features
- **Asynchronous:** You submit a batch, and Claude processes it in the background.
- **50% Cheaper:** Both input and output tokens are 50% off standard pricing.
- **SLA:** Most batches finish within 1 hour; the maximum is 24 hours, after which unfinished requests expire.
- **Retention:** Results stay available for 29 days after creation.
- **Full feature set:** Vision, tools, thinking, and caching all work inside a batch.
- **Limit:** Up to 100,000 requests per batch (or 256MB).

## Creating a Batch

**1. Prepare the requests**
Each request has a unique `custom_id` and a `params` object that is the same body you would send to `messages.create`. The SDK takes them as a Python list (the REST API takes the same list as JSON; there is no file upload).

```json
{"custom_id": "req1", "params": {"model": "claude-sonnet-5-5", "max_tokens": 1024, "messages": [{"role": "user", "content": "..."}]}}
```

**2. Submit Batch**

```python
import anthropic

client = anthropic.Anthropic()

batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "my-first-request",
            "params": {
                "model": "claude-sonnet-5-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hello world"}]
            }
        }
    ]
)
print(f"Batch ID: {batch.id}")
```

## Retrieving Results

1. **Poll** the batch status (`in_progress` -> `ended`).
2. **Stream the results** with the SDK. Results can come back in any order, so match them to your inputs by `custom_id`.

```python
import time

while True:
    batch = client.messages.batches.retrieve(batch.id)
    if batch.processing_status == "ended":
        break
    time.sleep(60)

for entry in client.messages.batches.results(batch.id):
    result = entry.result
    if result.type == "succeeded":
        text = next((b.text for b in result.message.content if b.type == "text"), "")
        print(f"[{entry.custom_id}] {text[:100]}")
    elif result.type == "errored":
        print(f"[{entry.custom_id}] error: {result.error}")
    else:  # "canceled" or "expired"
        print(f"[{entry.custom_id}] {result.type}")
```

## Notes
- Some models (Claude Fable 5.1, Opus 5.5, Sonnet 5.5) reject forced `tool_choice` (`any`/`tool`), in batches too.
- A batch can be cancelled with `client.messages.batches.cancel(batch.id)`; requests already running still finish and are billed.

## Next Steps
- See [Batch Use Cases](./09_batch_use_cases.md).
