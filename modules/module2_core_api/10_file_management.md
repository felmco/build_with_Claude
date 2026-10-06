# 2.4 File Management Code Examples

*Note: The Files API is generally available: no beta header is needed, and the SDK exposes it as `client.files`. See the [Files API docs](https://platform.claude.com/docs/en/build-with-claude/files).*

## 1. Uploading a File

```python
import anthropic

client = anthropic.Anthropic()

with open("large_document.pdf", "rb") as f:
    uploaded = client.files.upload(file=("large_document.pdf", f, "application/pdf"))

file_id = uploaded.id
print(f"Uploaded file ID: {file_id}")
```

## 2. Using a File in a Message

```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "file", "file_id": file_id}},
                {"type": "text", "text": "Analyze this file."},
            ],
        }
    ],
)
print(message.content[0].text)
```

The content block type must match the file: `document` for PDF/text, `image` for images.

## 3. Listing and Deleting

**List Files:**
```bash
curl https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

**Delete File:**
```bash
curl -X DELETE https://api.anthropic.com/v1/files/file_id_here \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

Or with the SDK: `client.files.list()` and `client.files.delete(file_id)`.

## Next Steps
- Move on to [Reliability and Error Handling](./11_error_handling.md).
