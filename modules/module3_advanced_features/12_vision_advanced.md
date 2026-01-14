# 3.4 Advanced Vision Techniques

## 1. Multiple Images
Send a series of images (frames of a video, or pages of a comic) to tell a story.

```python
content = []
for img_data in images:
    content.append({"type": "image", "source": {...}})
content.append({"type": "text", "text": "What is the sequence of events?"})
```

## 2. Transcribing Text (OCR)
Claude is excellent at OCR (Optical Character Recognition), especially for handwritten notes.

**Prompt:**
> "Transcribe this handwritten note verbatim. Maintain line breaks."

## 3. JSON Extraction from UI
Show Claude a screenshot of a website and ask for a JSON representation of the fields.

**Prompt:**
> "Extract the product name, price, and rating from this screenshot into JSON."

## Next Steps
- [Document Vision](./13_document_vision.md).
