# 2.5 Implementing Retry Logic

For retriable errors (500s, 429s, network issues), you should implement an **Exponential Backoff** strategy.

## What is Exponential Backoff?

Instead of retrying immediately (which might worsen the problem), you wait for progressively longer intervals: 1s, 2s, 4s, 8s...

### Built-in SDK Retries

The Anthropic Python SDK has built-in retry logic enabled by default (usually 2 retries).

```python
client = anthropic.Anthropic(
    max_retries=5  # Increase default retries
)
```

### Custom Retry Decorator

If you need more control (e.g., using `tenacity` library):

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import anthropic

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((anthropic.RateLimitError, anthropic.APIConnectionError))
)
def call_claude():
    return client.messages.create(...)
```

## Jitter

Add "jitter" (randomness) to your wait time to prevent "thundering herd" problems where many clients retry at the exact same millisecond.

## Next Steps
- Understand [Rate Limiting](./13_rate_limiting.md) to avoid 429s.
