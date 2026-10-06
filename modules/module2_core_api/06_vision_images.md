# 2.3 Vision and Images

Current Claude models are multimodal, meaning they can understand and analyze images alongside text.

## Supported Formats
- **Formats:** JPEG, PNG, GIF, WebP
- **Count:** Up to 600 images per API request (100 on Haiku 4.5, which has a 200K context window); 20 per message on claude.ai.
- **Size:** Max 10 MB per image (base64-encoded) on the Claude API, max 8000x8000 px. If a request has more than 20 images, each image must fit within 2000x2000 px. The overall request limit is 32 MB.
- **Resizing:** Images are processed in 28x28 px patches (one visual token each). Larger images are downscaled (long edge 1568 px on most models, 2576 px on Claude 4.7 and later), so pre-resizing saves latency and tokens.

## How to Send Images

You can send images as **Base64** strings (`"type": "base64"`), as **URLs** (`"type": "url"`), or as a **`file_id`** from the Files API (`"type": "file"`, see [Files API](./09_files_api.md)). Base64 works everywhere, including Amazon Bedrock and Google Cloud, which only accept base64 sources.

### Base64 Example

```python
import anthropic
import base64
import httpx

# 1. Get image data
image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image_media_type = "image/jpeg"
response = httpx.get(image_url, follow_redirects=True, timeout=30)
response.raise_for_status()
image_data = base64.b64encode(response.content).decode("utf-8")

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)
print(message.content[0].text)
```

### URL Example

```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "url", "url": image_url}},
                {"type": "text", "text": "Describe this image."},
            ],
        }
    ],
)
```

Only send URLs you trust, and note that the image must be publicly reachable.

## Best Practices for Vision

1. **Image Quality:** Ensure text in images is legible. Claude reads text well but struggles with very blurry or small text.
2. **Placement:** Put images *before* the questions about them.
   - ✅ Image -> "What is this?"
   - ❌ "What is this?" -> Image
3. **Multiple Images:** You can include multiple image blocks in the `content` list to ask for comparisons. Label each one with a short text block ("Image 1:", "Image 2:") so you can refer to them.

## Limitations

- **People:** Claude will refuse to identify (name) real people in images.
- **Medical:** Not for diagnostic use (not designed for complex scans such as CTs or MRIs).
- **Spatial:** Approximate location of objects, not pixel-perfect coordinates.
- **Counting:** Counts of many small objects are approximate.
- **Generation:** Claude analyzes images; it cannot generate or edit them.

## Next Steps
- Learn about [PDF Support](./07_pdf_support.md).
