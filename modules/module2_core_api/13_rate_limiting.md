# 2.5 Understanding Rate Limits

Rate limits define how much you can use the API within a specific timeframe.

## Types of Limits

1. **RPM (Requests Per Minute):** Number of API calls.
2. **ITPM / OTPM (Input / Output Tokens Per Minute):** Input and output tokens are limited separately. On most models, cached input tokens that were read from the prompt cache do not count toward ITPM.
3. **Monthly spend limit:** Maximum spend per month (varies by tier).

## Tier System

Limits depend on your usage tier (Tier 1 through Tier 4, plus custom enterprise limits) and are set **per model class**, with separate input-token and output-token limits (ITPM and OTPM). Tiers rise automatically as your spend grows. The numbers change over time, so do not hard-code them: check your own limits in the [Claude Console](https://platform.claude.com/settings/limits) and the [Rate limits docs](https://platform.claude.com/docs/en/api/rate-limits).

## Handling Rate Limits

### Headers
The API returns headers indicating your status:
- `anthropic-ratelimit-requests-limit`
- `anthropic-ratelimit-requests-remaining`
- `anthropic-ratelimit-requests-reset`
- `anthropic-ratelimit-input-tokens-*` and `anthropic-ratelimit-output-tokens-*` (same `limit` / `remaining` / `reset` suffixes)
- `retry-after`: Seconds to wait (sent with 429 responses).

```python
import anthropic

client = anthropic.Anthropic()
raw = client.messages.with_raw_response.create(
    model="claude-sonnet-5-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hi"}],
)
print(raw.headers.get("anthropic-ratelimit-requests-remaining"))
message = raw.parse()  # the usual Message object
```

### Strategies

1. **Throttling:** Track your usage locally and pause before sending if you are close to the limit.
2. **Queuing:** Put requests in a queue (Celery, Redis) and process them at a controlled rate.
3. **Batch API:** Use the Batch API (Module 3) for high-volume, non-time-sensitive tasks (50% cheaper, and batches have their own separate limits).

## Congratulations!
You have completed Module 2. You now understand the core API, vision, files, and reliability patterns.

## Next Module
Proceed to [Module 3: Advanced Features](../module3_advanced_features/README.md) to learn about Tools, Caching, and Batching.
