# 3.3 Batch Monitoring Code

**monitor_batch.py**:

```python
import anthropic
import time
import requests

client = anthropic.Anthropic()

def wait_for_batch(batch_id):
    print(f"Monitoring batch {batch_id}...")

    while True:
        batch = client.messages.batches.retrieve(batch_id)
        status = batch.processing_status

        print(f"Status: {status}")

        if status == "ended":
            return batch
        elif status == "canceling" or status == "canceled":
            print("Batch canceled.")
            return batch
        elif status == "expired":
            print("Batch expired.")
            return batch

        time.sleep(30) # Check every 30s

def download_results(batch):
    if not batch.results_url:
        print("No results URL found.")
        return

    print("Downloading results...")
    response = requests.get(batch.results_url)

    # Save to file
    with open("batch_results.jsonl", "w") as f:
        f.write(response.text)
    print("Saved to batch_results.jsonl")

# Usage (Assuming you have a batch_id)
# batch = wait_for_batch("msgbatch_123...")
# download_results(batch)
```

## Next Steps
- Move to [Vision Basics](./11_vision_basics.md).
