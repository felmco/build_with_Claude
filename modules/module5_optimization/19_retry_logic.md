# 5.5 Advanced Retry Logic

## Exponential Backoff with Jitter
The gold standard.
- Attempt 1: Wait 0s.
- Attempt 2: Wait 1s + rand(0, 0.1).
- Attempt 3: Wait 2s + rand(0, 0.1).
- Attempt 4: Wait 4s + rand(0, 0.1).

## Idempotency
Ensure retrying a request doesn't cause side effects (like charging a user twice).
- **Read-only requests:** Safe to retry.
- **Action requests:** Be careful.

## Next Steps
- [Observability](./20_observability.md).
