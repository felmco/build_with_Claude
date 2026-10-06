# 5.5 Observability

## Tracing
Follow a request from User -> API -> Claude -> DB -> User.
- **OpenTelemetry:** Standard for tracing.

## Logging Costs
Log `usage.input_tokens`, `usage.output_tokens` and the cache fields (`cache_creation_input_tokens`, `cache_read_input_tokens`) for *every* request, plus the request ID (`response._request_id`) for support tickets.
- Calculate cost per user.
- Identify "Whales" (users costing you a fortune).

## Quality Monitoring
Log "Refusal Rate" (responses with `stop_reason == "refusal"`) and the share ending in `"max_tokens"`.
- If Claude starts refusing 50% of requests, your system prompt might have broken.

## Next Steps
- Move to [Security & Compliance](./21_security.md).
