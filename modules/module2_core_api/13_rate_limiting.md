# 2.5 Understanding Rate Limits

Rate limits define how much you can use the API within a specific timeframe.

## Types of Limits

1. **RPM (Requests Per Minute):** Number of API calls.
2. **TPM (Tokens Per Minute):** Total tokens (Input + Output).
3. **Daily Limit:** Total spend or tokens per day (varies by tier).

## Tier System (Example)

| Tier | RPM | TPM |
|------|-----|-----|
| Free | 5 | 20k |
| Tier 1 | 50 | 50k |
| Tier 2 | 1000 | 1M |
| Tier 4 | 4000 | 400k+ |

*Check your specific limits in the Console.*

## Handling Rate Limits

### Headers
The API returns headers indicating your status:
- `anthropic-ratelimit-requests-limit`
- `anthropic-ratelimit-requests-remaining`
- `anthropic-ratelimit-requests-reset`
- `retry-after`: Seconds to wait.

### Strategies

1. **Throttling:** Track your usage locally and pause before sending if you are close to the limit.
2. **Queuing:** Put requests in a queue (Celery, Redis) and process them at a controlled rate.
3. **Batch API:** Use the Batch API (Module 3) for high-volume, non-time-sensitive tasks (50% cheaper and higher limits).

## Congratulations!
You have completed Module 2. You now understand the core API, vision, files, and reliability patterns.

## Next Module
Proceed to [Module 3: Advanced Features](../module3_advanced_features/README.md) to learn about Tools, Caching, and Batching.
