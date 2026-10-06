# 4.5 Rate Limiting & Queuing

## The Problem
Your app goes viral. 10,000 users hit "Send". You hit Anthropic rate limits immediately.

## The Solution: Token Bucket Queue

1. **Client:** Sends request -> API Gateway.
2. **Gateway:** Pushes job to **Redis Queue**.
3. **Worker:**
   - Checks "Token Bucket" (Available tokens / minute).
   - If available: Process job.
   - If not: Sleep / Retry later.

Note: the SDK retries 429s automatically (`max_retries`, honoring `retry-after`). A queue is for smoothing bursts beyond that. For non-urgent bulk work, the Message Batches API runs at a 50% discount without consuming real-time rate limits.

## Libraries
- Python: `celery` or `rq`.
- Redis: For the queue.

## Next Steps
- [Logging & Monitoring](./19_logging_monitoring.md).
