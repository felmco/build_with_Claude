# 2.3 Vision and Images

Claude models (Claude 3 family and later) are multimodal, meaning they can understand and analyze images alongside text.

## Supported Formats
- **Formats:** JPEG, PNG, GIF, WebP
- **Limit:** Up to 100 images per request (API), 20 (Claude.ai).
- **Size:** Recommended < 1.15 MP for speed. Max 8000x8000px.

## How to Send Images

You can send images as **Base64** encoded strings or via **URLs** (depending on SDK version/feature support). The most robust way in the API is Base64.

### Base64 Example

```python
import anthropic
import base64
import httpx

# 1. Get image data
image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image_media_type = "image/jpeg"
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
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

## Best Practices for Vision

1. **Image Quality:** Ensure text in images is legible. Claude reads text well but struggles with very blurry or small text.
2. **Placement:** Put images *before* the questions about them.
   - ✅ Image -> "What is this?"
   - ❌ "What is this?" -> Image
3. **Multiple Images:** You can include multiple image blocks in the `content` list to ask for comparisons.

## Limitations

- **People:** Claude will refuse to identify (name) real people in images.
- **Medical:** Not for diagnostic use.
- **Spatial:** Approximate location of objects, not pixel-perfect coordinates.

## Next Steps
- Learn about [PDF Support](./07_pdf_support.md).
