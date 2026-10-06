# 3.3 Batch Monitoring Code

**monitor_batch.py**:

```python
import time

import anthropic

client = anthropic.Anthropic()

def wait_for_batch(batch_id, poll_seconds=30):
    print(f"Monitoring batch {batch_id}...")

    while True:
        batch = client.messages.batches.retrieve(batch_id)
        counts = batch.request_counts
        print(f"Status: {batch.processing_status} "
              f"(processing={counts.processing}, succeeded={counts.succeeded}, "
              f"errored={counts.errored}, canceled={counts.canceled}, expired={counts.expired})")

        # processing_status is one of: in_progress, canceling, ended.
        # Individual requests can still end as canceled or expired.
        if batch.processing_status == "ended":
            return batch

        time.sleep(poll_seconds)

def save_results(batch_id, path="batch_results.jsonl"):
    # The results endpoint needs your API key, so use the SDK rather than a bare HTTP GET on results_url
    print("Downloading results...")
    with open(path, "w") as f:
        for entry in client.messages.batches.results(batch_id):
            f.write(entry.model_dump_json() + "\n")
    print(f"Saved to {path}")

# Usage (assuming you have a batch_id)
# batch = wait_for_batch("msgbatch_123...")
# save_results(batch.id)
```

Each line of the saved file has a `custom_id` and a `result` whose `type` is `succeeded`, `errored`, `canceled`, or `expired`. Retry `errored` (server errors) and `expired` requests in a new batch.

## Next Steps
- Move to [Vision Basics](./11_vision_basics.md).
