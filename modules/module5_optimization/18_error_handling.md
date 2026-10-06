# 5.5 Error Handling Strategies

We covered basic types in Module 2. Here, we cover **Resiliency**.

## Circuit Breakers
If Anthropic returns 500s for 10% of requests, stop calling it for 1 minute.
- **Why?** Prevents cascading failures in your system.

## Fallbacks
If Claude is down, what happens?
1. **Cache:** Return a cached answer?
2. **Degraded Mode:** "AI features unavailable"?
3. **Another Provider:** Fallback to a different model (if compatible).

## Timeout Management
Long generations can take a minute or more.
- Set client timeouts, e.g. `anthropic.Anthropic(timeout=60.0)` or per request with `client.with_options(timeout=60.0)`. The SDK default is 10 minutes.
- For large `max_tokens` use streaming (`client.messages.stream(...)`); the SDK refuses non-streaming requests it expects to be too long.
- Don't let your web server worker hang forever.

## Catching errors
The SDK already retries 429, 5xx and connection errors (see [Retry Logic](./19_retry_logic.md)). Handle what is left, most specific first:

```python
try:
    response = client.messages.create(...)
except anthropic.RateLimitError:
    ...  # still rate limited after SDK retries: queue or shed load
except anthropic.APIConnectionError:
    ...  # network problem
except anthropic.APIStatusError as e:
    ...  # other HTTP errors; e.status_code, e.response
```

Also check `response.stop_reason` before using the content: `"refusal"` and `"max_tokens"` are not errors but need handling.

## Next Steps
- [Retry Logic](./19_retry_logic.md).
