# 3.4 Document Vision

This is distinct from the "PDF Support" feature. This refers to converting document *pages* to images yourself for fine-grained control.

## Why convert to images?
- **Annotations:** You can draw red boxes on the image to highlight areas before sending to Claude.
- **Specific crops:** Send only a specific chart.
- **Legacy formats:** TIFF, BMP, etc.

## Strategy: Visual Q&A
1. Convert PDF page to PNG.
2. Send to Claude.
3. Ask: "Is there a signature in the bottom right corner?"

## Next Steps
- Learn about [Extended Thinking](./14_extended_thinking.md).
