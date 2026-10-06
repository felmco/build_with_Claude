# 5.3 Response Monitoring

You can't optimize what you don't measure.

## Metrics to Track
1. **Latency (P50, P90, P99):** How fast is it usually? How slow is it at worst?
2. **Token Usage:** Are some prompts consuming way more than expected?
3. **Error Rate:** 429s, 500s.
4. **Cache Hit Rate:** Are your breakpoints working? Compare `usage.cache_read_input_tokens` with `usage.input_tokens` on each response.

```python
import time

start = time.perf_counter()
response = client.messages.create(...)
latency = time.perf_counter() - start
u = response.usage
metrics = {
    "latency_s": latency,
    "input_tokens": u.input_tokens,
    "output_tokens": u.output_tokens,
    "cache_read": u.cache_read_input_tokens,
    "stop_reason": response.stop_reason,
    "request_id": response._request_id,
}
```

## Dashboarding
Send these metrics to Datadog/Grafana/CloudWatch using standard instrumentation.

## Next Steps
- Move to [Evaluation & Testing](./14_evaluation.md).
