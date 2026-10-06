# 1.3 Basic Error Handling

When working with APIs, things can go wrong. The Anthropic SDK provides specific exceptions to help you handle errors gracefully.

## Common Error Types

| Error Code | Exception Class | Cause | Solution |
|------------|-----------------|-------|----------|
| 400 | `BadRequestError` | Invalid JSON, malformed parameters | Check your request structure and parameters. |
| 401 | `AuthenticationError` | Invalid or missing API key | Verify your `ANTHROPIC_API_KEY` environment variable. |
| 403 | `PermissionDeniedError` | Key doesn't have access to resource | Check account permissions. |
| 404 | `NotFoundError` | Model or resource not found | Check your model name spelling (e.g. `claude-sonnet-5-5`). |
| 413 | `RequestTooLargeError` | Request too big | Reduce input size (e.g. fewer images or text). Max is ~32MB. |
| 429 | `RateLimitError` | Too many requests or tokens | Implement retries with backoff. Request a limit increase. |
| 500 | `InternalServerError` | Internal server error | Retry the request later. |
| 529 | `OverloadedError` | API is overloaded | Retry with exponential backoff. |

## Implementing Try-Except Blocks

Always wrap your API calls in a `try-except` block.

```python
import anthropic
import os

client = anthropic.Anthropic()

try:
    message = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(next(b.text for b in message.content if b.type == "text"))

except anthropic.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # Underlying exception

except anthropic.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")

except anthropic.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(f"Status code: {e.status_code}")
    print(e.response)
```

## Handling Overloaded Errors (529)

The `OverloadedError` specifically means Anthropic's systems are busy. The SDK already retries 429, 5xx and connection errors twice by default (`max_retries=2`), so extra retry code is only needed if you want more attempts or custom backoff.

```python
import time
import anthropic

client = anthropic.Anthropic()

max_retries = 3
for attempt in range(max_retries):
    try:
        message = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
        )
        break
    except (anthropic.OverloadedError, anthropic.InternalServerError) as e:
        if attempt == max_retries - 1:
            raise
        time.sleep(2 ** attempt)  # Exponential backoff
```

## Next Steps
Congratulations! You have completed Module 1. You are now ready to move to [Module 2: Core API Features](../module2_core_api/README.md).
