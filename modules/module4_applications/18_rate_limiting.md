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

## Libraries
- Python: `celery` or `rq`.
- Redis: For the queue.

## Next Steps
- [Logging & Monitoring](./19_logging_monitoring.md).
