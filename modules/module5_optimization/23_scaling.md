# 5.6 Horizontal Scaling

## Statelessness
Claude API is stateless. Your app should be too.
- Store session state in Redis, not Python memory.
- Run multiple instances of your app (Docker/K8s).

## Rate Limit Sharing
If you have 10 servers, they share ONE Anthropic API Key limit.
- **Centralized Rate Limiter:** Use Redis to count tokens globally across all servers.

## Next Steps
- [Load Balancing](./24_load_balancing.md).
