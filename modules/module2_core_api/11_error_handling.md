# 2.5 Error Handling Types

Building production apps requires robust error handling. The Anthropic SDK throws specific exceptions for different failure modes.

## Hierarchy of Exceptions

All exceptions inherit from `anthropic.APIError`.

- `APIConnectionError`: Network issues (DNS, Timeout, Connection refused).
- `APIStatusError`: The server returned a non-2xx status code.
  - `BadRequestError` (400): Malformed request.
  - `AuthenticationError` (401): Bad API key.
  - `PermissionDeniedError` (403): Unauthorized access (not Python's built-in `PermissionError`).
  - `NotFoundError` (404): Resource/Model not found.
  - `RequestTooLargeError` (413): Request exceeds the size limit (32 MB).
  - `RateLimitError` (429): Too many requests.
  - `InternalServerError` (500): Issue on Anthropic's side.
  - `OverloadedError` (529): API is overloaded.

## Handling Strategy

The SDK already retries 429, 5xx and connection errors twice (`max_retries=2`) before raising, so the errors below reach your code only after those retries are used up.

1. **Retriable Errors:** `RateLimitError`, `InternalServerError`, `OverloadedError`, `APIConnectionError`.
2. **Non-Retriable:** `BadRequestError`, `AuthenticationError`, `PermissionDeniedError`, `NotFoundError`, `RequestTooLargeError`.

### Code Example

```python
import anthropic
import time

client = anthropic.Anthropic()

def safe_call(prompt):
    try:
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response
    except anthropic.RateLimitError:
        print("Rate limited. Waiting...")
        # Implement backoff
    except anthropic.APIConnectionError:
        print("Network error.")
    except anthropic.APIStatusError as e:  # base class for HTTP errors, so it goes last
        if e.status_code == 529:
            print("Overloaded. Retry later.")
        else:
            print(f"API Error {e.status_code}: {e}")
            print(f"Request ID: {e.response.headers.get('request-id')}")  # include when contacting support
```

## Next Steps
- Implement [Retry Logic](./12_retry_logic.md).
