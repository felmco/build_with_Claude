# 2.4 File Management Code Examples

*Note: The Files API is in beta. You must use the appropriate beta headers.*

## 1. Uploading a File

```python
import httpx

api_key = "your-api-key"
file_path = "large_document.pdf"

url = "https://api.anthropic.com/v1/files"
headers = {
    "x-api-key": api_key,
    "anthropic-version": "2023-06-01",
    "anthropic-beta": "files-api-2025-04-14" # Check documentation for latest beta string
}

files = {
    "file": open(file_path, "rb")
}
data = {
    "purpose": "assistants" # or appropriate purpose
}

response = httpx.post(url, headers=headers, files=files, data=data)
file_id = response.json()["id"]
print(f"Uploaded file ID: {file_id}")
```

## 2. Using a File in a Message

```python
import anthropic

client = anthropic.Anthropic(
    api_key=api_key,
)

# Note: Beta support might require raw HTTP requests or specific client configuration
# depending on SDK version support for the beta Files API.
# Below implies SDK support or wrapping the call.

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": file_id
                    }
                },
                {
                    "type": "text",
                    "text": "Analyze this file."
                }
            ]
        }
    ],
    extra_headers={"anthropic-beta": "files-api-2025-04-14"}
)
```

## 3. Listing and Deleting

**List Files:**
```bash
curl https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: files-api-2025-04-14"
```

**Delete File:**
```bash
curl -X DELETE https://api.anthropic.com/v1/files/file_id_here \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: files-api-2025-04-14"
```

## Next Steps
- Move on to [Reliability and Error Handling](./11_error_handling.md).
