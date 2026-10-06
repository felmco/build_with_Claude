# 5.2 Batch Processing for Cost Reduction

## The 50% Rule
The Message Batches API costs 50% less than standard calls. Anything that doesn't need an answer right away should go to Batch. Most batches finish within an hour, but allow up to 24 hours.

## Architecture
1. **Queue:** Accumulate non-urgent requests in a DB table.
2. **Cron Job:** Every 5 minutes, query the table.
3. **Submit:** If > 100 requests (or if oldest is > 1 hour), submit a batch.
4. **Retrieve:** Poll for results and update the DB.

## Cost Savings Example
- **Scenario:** Processing 1M documents/month with Sonnet 5.5, assuming 2K input and 500 output tokens each (2,000 MTok in, 500 MTok out).
- **Standard:** $2 input + $10 output / MTok = $4,000 + $5,000 = $9,000.
- **Batch:** $1 input + $5 output / MTok = $4,500.
- **Savings:** about $4,500 per month. Check current prices before budgeting.

## Minimal example
```python
import anthropic

client = anthropic.Anthropic()
batch = client.messages.batches.create(requests=[
    {
        "custom_id": f"doc-{i}",
        "params": {
            "model": "claude-sonnet-5-5",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": f"Summarize: {doc}"}],
        },
    }
    for i, doc in enumerate(docs)
])
# Later: poll client.messages.batches.retrieve(batch.id) until processing_status == "ended",
# then iterate client.messages.batches.results(batch.id) and match on custom_id
# (results are not returned in request order).
```

Message Batches is not available on Amazon Bedrock or Vertex AI; use the first-party API (or Claude Platform on AWS) for it.

## Next Steps
- Move to [Latency Optimization](./10_latency.md).
