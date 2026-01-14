# 3.3 Message Batches API

The Message Batches API allows you to send a large group of requests at once.

## Key Features
- **Asynchronous:** You submit a batch, and Claude processes it in the background.
- **50% Cheaper:** Both input and output tokens are 50% off standard pricing.
- **SLA:** Results within 24 hours (often < 1 hour).
- **Limit:** Up to 100,000 requests per batch (or 256MB).

## Creating a Batch

**1. Prepare JSONL File**
Create a list of requests.

```json
{"custom_id": "req1", "params": {"model": "claude-sonnet-4-5-20250929", "max_tokens": 1024, "messages": [...]}}
{"custom_id": "req2", "params": {"model": "claude-sonnet-4-5-20250929", "max_tokens": 1024, "messages": [...]}}
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
                "model": "claude-sonnet-4-5-20250929",
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
2. **Download** the results URL.

```python
import time

while True:
    batch = client.messages.batches.retrieve(batch.id)
    if batch.processing_status == "ended":
        break
    time.sleep(60)

# Get results
results_url = batch.results_url
# (Fetch URL content to see JSONL results)
```

## Next Steps
- See [Batch Use Cases](./09_batch_use_cases.md).
