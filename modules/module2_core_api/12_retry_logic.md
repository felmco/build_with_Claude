# 2.5 Implementing Retry Logic

For retriable errors (500s, 429s, network issues), you should implement an **Exponential Backoff** strategy.

## What is Exponential Backoff?

Instead of retrying immediately (which might worsen the problem), you wait for progressively longer intervals: 1s, 2s, 4s, 8s...

### Built-in SDK Retries

The Anthropic Python SDK has built-in retry logic enabled by default (2 retries by default, `max_retries=2`). It retries connection errors, 408, 409, 429 and 5xx responses with exponential backoff, and honors the `retry-after` header..

```python
import anthropic

client = anthropic.Anthropic(
    max_retries=5,  # Increase default retries (set 0 to turn SDK retries off)
    timeout=60.0,   # Seconds; the default timeout is 10 minutes
)
```

### Custom Retry Decorator

If you need more control (e.g., using `tenacity` library):

```python
# pip install tenacity
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type
import anthropic

client = anthropic.Anthropic(max_retries=0)  # let tenacity own the retries

@retry(
    stop=stop_after_attempt(4),
    wait=wait_random_exponential(multiplier=1, max=30),  # exponential backoff with jitter
    retry=retry_if_exception_type((
        anthropic.RateLimitError,
        anthropic.InternalServerError,
        anthropic.OverloadedError,
        anthropic.APIConnectionError,
    )),
    reraise=True,
)
def call_claude(prompt: str):
    return client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
```

## Jitter

Add "jitter" (randomness) to your wait time (`wait_random_exponential` above does this) to prevent "thundering herd" problems where many clients retry at the exact same millisecond.

## Next Steps
- Understand [Rate Limiting](./13_rate_limiting.md) to avoid 429s.
