# 2.4 Files API Overview

The **Files API** (beta) allows you to upload files once and reuse them across multiple message requests. This saves bandwidth and simplifies code for repeated assets.

## Supported Models
- **Images:** All Claude 3+ models.
- **PDFs:** All Claude 3.5+ models.
- **CSV/Text:** Supported for specific tools (Code Execution), generally use text blocks for these in standard messages.

## Usage Flow

1. **Upload** a file to Anthropic's storage.
2. **Receive** a `file_id`.
3. **Reference** the `file_id` in your messages.

## Benefits
- **Efficiency:** Don't re-upload Base64 strings every call.
- **Cost:** No repeated network upload overhead (token costs still apply for processing).
- **Scale:** Easier management of assets.

## Important Note
Files uploaded via the API are **not** persistent forever by default in all contexts (lifecycle policies apply), and standard token usage limits still apply when the file content is processed by the model.

## Next Steps
- See the code for [File Management](./10_file_management.md).
