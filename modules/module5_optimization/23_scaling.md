# 5.6 Horizontal Scaling

## Statelessness
Claude API is stateless. Your app should be too.
- Store session state in Redis, not Python memory.
- Run multiple instances of your app (Docker/K8s).

## Rate Limit Sharing
Rate limits apply per organization (and per workspace, if you set limits) and per model, not per server or per key. If you have 10 servers they all draw from the same limits.
- **Centralized Rate Limiter:** Use Redis to count requests and tokens globally across all servers.
- Handle `429` responses (the SDK retries them and honors `retry-after`) and read the `anthropic-ratelimit-*` response headers to see your remaining budget.

## Next Steps
- [Load Balancing](./24_load_balancing.md).
