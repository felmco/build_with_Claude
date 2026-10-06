# 3.4 Advanced Vision Techniques

## 1. Multiple Images
Send a series of images (frames of a video, or pages of a comic) to tell a story.

```python
content = []
for i, img_data in enumerate(images, 1):  # images: list of base64 strings
    content.append({"type": "text", "text": f"Image {i}:"})  # label each image
    content.append({
        "type": "image",
        "source": {"type": "base64", "media_type": "image/jpeg", "data": img_data},
    })
content.append({"type": "text", "text": "What is the sequence of events?"})

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": content}],
)
```

Claude keeps access to images from earlier turns, but every request resends them. For many images or long conversations, upload them once with the Files API (`client.files.upload(...)`) and reference them with `{"type": "file", "file_id": ...}` as the image source.

## 2. Transcribing Text (OCR)
Claude is good at OCR (Optical Character Recognition), including many handwritten notes. Check important transcriptions, since small or low-quality text can be misread.

**Prompt:**
> "Transcribe this handwritten note verbatim. Maintain line breaks."

## 3. JSON Extraction from UI
Show Claude a screenshot of a website and ask for a JSON representation of the fields.

**Prompt:**
> "Extract the product name, price, and rating from this screenshot into JSON."

## Limitations
- Claude cannot identify people from their faces, and it cannot generate or edit images.
- Counts, spatial positions, and bounding boxes are approximate. Verify them for high-stakes work.
- Very small (under about 200 px), rotated, or blurry images are more error-prone.

## Next Steps
- [Document Vision](./13_document_vision.md).
