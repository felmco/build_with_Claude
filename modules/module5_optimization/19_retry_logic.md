# 5.5 Advanced Retry Logic

## The SDK already retries
The official `anthropic` SDK retries connection errors, 408, 409, 429 and 5xx responses with exponential backoff and jitter, honoring the `retry-after` header. The default is `max_retries=2`. Tune it instead of writing your own loop:

```python
client = anthropic.Anthropic(max_retries=5)
# or per request
client.with_options(max_retries=0).messages.create(...)  # when you do your own retries
```

Wrapping SDK calls in another retry loop multiplies attempts (3 x 3 = 9 requests) and worsens rate limiting. If you write your own layer, set `max_retries=0` on the client.

## Exponential Backoff with Jitter
The gold standard, and what the SDK does for you:
- Attempt 1: Wait 0s.
- Attempt 2: Wait 1s + rand(0, 0.1).
- Attempt 3: Wait 2s + rand(0, 0.1).
- Attempt 4: Wait 4s + rand(0, 0.1).

## What to retry
Retry only transient failures: 429, 5xx (including 529 overloaded) and network errors. Never retry 400, 401, 403, 404 or 413; they will fail the same way.

## Idempotency
Ensure retrying a request doesn't cause side effects (like charging a user twice).
- **Read-only requests:** Safe to retry.
- **Action requests:** Be careful.

## Next Steps
- [Observability](./20_observability.md).
