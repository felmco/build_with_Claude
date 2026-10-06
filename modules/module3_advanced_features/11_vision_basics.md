# 3.4 Vision Basics

We covered the basics in Module 2. Here we go deeper.

## Supported Formats and Limits

- **Formats:** JPEG, PNG, GIF, and WebP only (animated GIFs use the first frame). Convert TIFF, BMP, etc. first.
- **Size:** up to 10 MB per image (base64-encoded) on the Claude API; 5 MB on Amazon Bedrock and Google Cloud.
- **Count:** up to 600 images per API request (100 for models with a 200K context, such as Haiku 4.5), subject to the 32 MB request size limit. Above 20 images per request, each image must be at most 2000 px per side.
- **Dimensions:** up to 8000x8000 px per image.
- **Sources:** `base64`, `url`, or a `file_id` from the Files API (upload once, reuse many times).

## Image Sizing and Tokens

Claude sees an image as 28x28 pixel patches, so an image costs about `ceil(width/28) x ceil(height/28)` tokens.

| Tier | Models | Max long edge | Max tokens per image |
|------|--------|---------------|----------------------|
| High-resolution | Claude 4.7 and later (Fable 5.1, Opus 5.5, Sonnet 5.5) | 2576 px | 4784 |
| Standard | Others (e.g. Haiku 4.5) | 1568 px | 1568 |

- **Resizing:** Larger images are downscaled automatically, so you pay upload time and latency for pixels that are thrown away. Resize *client-side* to the tier's limit, or lower if you do not need the detail (a 1000x1000 image is about 1300 tokens).
- **Order:** Put images before the text question when you can.
- **Cost control:** High-resolution models can use about 3x more tokens per large image than standard ones. Downsample if you do not need fine detail.

## Example: Client-Side Resizing (Python)

```python
import base64
import io

from PIL import Image

def prepare_image(image_path, max_size=1568):
    """Downscale an image and return a base64 JPEG ready for the API."""
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # JPEG cannot store alpha/palette modes
        ratio = min(max_size / img.width, max_size / img.height)
        if ratio < 1:
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")

# Usage
# image_block = {
#     "type": "image",
#     "source": {"type": "base64", "media_type": "image/jpeg", "data": prepare_image("photo.png")},
# }
```

Heavy JPEG compression can make small text hard to read, so keep the quality high for documents and screenshots.

## Next Steps
- [Advanced Vision Techniques](./12_vision_advanced.md).
