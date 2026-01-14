# 5.5 Observability

## Tracing
Follow a request from User -> API -> Claude -> DB -> User.
- **OpenTelemetry:** Standard for tracing.

## Logging Costs
Log `input_tokens` and `output_tokens` for *every* request.
- Calculate cost per user.
- Identify "Whales" (users costing you a fortune).

## Quality Monitoring
Log "Refusal Rate".
- If Claude starts refusing 50% of requests, your system prompt might have broken.

## Next Steps
- Move to [Security & Compliance](./21_security.md).
