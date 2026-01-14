# 4.5 Logging & Monitoring

## What to Log?
1. **Inputs/Outputs:** The full prompt and response (Be careful with PII/Privacy).
2. **Metadata:** Model ID, Latency, Token Usage, Cost.
3. **User Feedback:** Thumbs up/down.

## Tools
- **LangSmith:** specialized for LLM traces.
- **Arize / Phoenix:** LLM observability.
- **Standard:** Datadog, Prometheus.

## Alerting
- Alert on **Error Rate > 1%**.
- Alert on **Cost > Budget**.
- Alert on **Latency > 5s**.

## Next Steps
- [Testing](./20_testing.md).
