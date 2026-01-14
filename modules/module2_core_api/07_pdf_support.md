# 2.3 PDF Support

Claude can natively read and analyze PDF documents. This is part of its multimodal capabilities.

## How It Works

The PDF is converted into image/text representations internally. Claude "sees" the document pages.

### Requirements
- **Format:** Standard PDF (no passwords/encryption).
- **Size:** Max 32MB per request.
- **Pages:** Max 100 pages per request (recommended).

## Sending a PDF via API

You send PDFs similarly to images, using a `document` block with Base64 encoding.

```python
import anthropic
import base64

client = anthropic.Anthropic()

# Encode PDF
with open("report.pdf", "rb") as f:
    pdf_data = base64.b64encode(f.read()).decode("utf-8")

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
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {
                    "type": "text",
                    "text": "Summarize the key findings in this report."
                }
            ]
        }
    ]
)
print(message.content[0].text)
```

## Optimizing PDF Performance

1. **Text Selection:** Ensure the PDF has selectable text if possible (though Claude uses vision, text layers help).
2. **Chunking:** For very large documents (>100 pages), split the PDF into smaller chunks or multiple requests.
3. **Prompting:** Ask specific questions. "Find the table on page 3 and extract the revenue figures."

## Next Steps
- Learn more about [Document Analysis Strategies](./08_document_analysis.md).
