# 3.4 Document Vision

This is distinct from the "PDF Support" feature. This refers to converting document *pages* to images yourself for fine-grained control.

## Why convert to images?
- **Annotations:** You can draw red boxes on the image to highlight areas before sending to Claude.
- **Specific crops:** Send only a specific chart.
- **Legacy formats:** TIFF, BMP, etc. The API accepts only JPEG, PNG, GIF, and WebP, so convert other formats first.

## Strategy: Visual Q&A
1. Convert PDF page to PNG.
2. Send to Claude.
3. Keep the page within the image limits for your model (see [Vision Basics](./11_vision_basics.md)); text must stay legible after resizing.
4. Ask: "Is there a signature in the bottom right corner?"

For plain PDFs, you can also send the file directly as a `document` content block (base64, URL, or Files API `file_id`) and skip the conversion.

## Next Steps
- Learn about [Extended Thinking](./14_extended_thinking.md).
