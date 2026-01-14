# 2.5 Error Handling Types

Building production apps requires robust error handling. The Anthropic SDK throws specific exceptions for different failure modes.

## Hierarchy of Exceptions

All exceptions inherit from `anthropic.APIError`.

- `APIConnectionError`: Network issues (DNS, Timeout, Connection refused).
- `APIStatusError`: The server returned a non-200 status code.
  - `BadRequestError` (400): Malformed request.
  - `AuthenticationError` (401): Bad API key.
  - `PermissionError` (403): Unauthorized access.
  - `NotFoundError` (404): Resource/Model not found.
  - `RateLimitError` (429): Too many requests.
  - `InternalServerError` (500): Issue on Anthropic's side.
  - `OverloadedError` (529): API is overloaded.

## Handling Strategy

1. **Retriable Errors:** `RateLimitError`, `InternalServerError`, `OverloadedError`, `APIConnectionError`.
2. **Non-Retriable:** `BadRequestError`, `AuthenticationError`, `PermissionError`, `NotFoundError`.

### Code Example

```python
import anthropic
import time

client = anthropic.Anthropic()

def safe_call(prompt):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response
    except anthropic.RateLimitError:
        print("Rate limited. Waiting...")
        # Implement backoff
    except anthropic.APIStatusError as e:
        if e.status_code == 529:
            print("Overloaded. Retry later.")
        else:
            print(f"API Error: {e}")
    except anthropic.APIConnectionError:
        print("Network error.")
```

## Next Steps
- Implement [Retry Logic](./12_retry_logic.md).
