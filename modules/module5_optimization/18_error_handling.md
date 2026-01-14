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
Anthropic requests can take 30s+.
- Set client timeouts (`timeout=60.0`).
- Don't let your web server worker hang forever.

## Next Steps
- [Retry Logic](./19_retry_logic.md).
