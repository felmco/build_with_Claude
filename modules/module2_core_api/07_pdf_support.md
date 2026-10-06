# 2.3 PDF Support

Claude can natively read and analyze PDF documents. This is part of its multimodal capabilities.

## How It Works

Claude extracts the text of each page and also sees each page as an image, so it can read charts, tables and scanned content.

### Requirements
- **Format:** Standard PDF (no passwords/encryption).
- **Size:** Max 32MB per request (the whole payload, not just the PDF).
- **Pages:** Max 600 pages per request on models with a 1M-token context window (100 pages on Haiku 4.5, which has 200K).
- **Cost:** Each page costs text tokens plus image tokens, so long PDFs add up quickly; use `client.messages.count_tokens` to check.

## Sending a PDF via API

You send PDFs similarly to images, using a `document` block with a base64, `url` or Files API (`file`) source.

```python
import anthropic
import base64

client = anthropic.Anthropic()

# Encode PDF
with open("report.pdf", "rb") as f:
    pdf_data = base64.b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-5-5",
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

For a PDF at a public URL, use `"source": {"type": "url", "url": "https://example.com/report.pdf"}` instead. For a PDF you will query many times, upload it once with the [Files API](./09_files_api.md) and reference it by `file_id`.

## Optimizing PDF Performance

1. **Text Selection:** Ensure the PDF has selectable text if possible (Claude also uses vision, but text layers help).
2. **Chunking:** For documents over the page limit, split the PDF into smaller chunks or multiple requests.
3. **Prompting:** Ask specific questions. "Find the table on page 3 and extract the revenue figures."

## Next Steps
- Learn more about [Document Analysis Strategies](./08_document_analysis.md).
