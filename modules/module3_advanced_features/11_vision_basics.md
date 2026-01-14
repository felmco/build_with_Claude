# 3.4 Vision Basics

We covered the basics in Module 2. Here we go deeper.

## Image Sizing and Tokens

- **Max Edge:** 1568px (for optimal processing).
- **Resizing:** If larger, the API resizes it automatically, but you pay latency for the upload. Resize *client-side* for speed.
- **Cost:** ~1600 tokens max for high-res images.

## Example: Client-Side Resizing (Python)

```python
from PIL import Image
import io

def resize_image(image_path, max_size=1568):
    with Image.open(image_path) as img:
        ratio = min(max_size / img.width, max_size / img.height)
        if ratio < 1:
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        return buffer.getvalue()
```

## Next Steps
- [Advanced Vision Techniques](./12_vision_advanced.md).
