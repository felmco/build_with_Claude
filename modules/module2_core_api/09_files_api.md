# 2.4 Files API Overview

The **Files API** (generally available; no beta header needed) allows you to upload files once and reuse them across multiple message requests. This saves bandwidth and simplifies code for repeated assets.

## Supported Models
- **Images:** All current Claude models (`image` blocks with a `file` source).
- **PDFs and plain text:** All current Claude models (`document` blocks with a `file` source).
- **CSV and other data files:** Used with the code execution tool; for plain text in a normal message, a text block is usually simpler.
- **Platforms:** Available on the Claude API; not on Amazon Bedrock or Google Vertex AI (use base64 there).

## Usage Flow

1. **Upload** a file to Anthropic's storage.
2. **Receive** a `file_id`.
3. **Reference** the `file_id` in your messages.

## Benefits
- **Efficiency:** Don't re-upload Base64 strings every call.
- **Cost:** No repeated network upload overhead (token costs still apply for processing).
- **Scale:** Easier management of assets.

## Limits and Billing
- Max file size: 500 MB; total storage: 100 GB per organization.
- Files persist until you delete them, so clean up files you no longer need.
- Upload, list and delete operations are free. File content used in a message is billed as input tokens like any other content, and the request still counts toward rate limits.
- You can only download files that were created by tools (such as code execution), not files you uploaded.

## Next Steps
- See the code for [File Management](./10_file_management.md).
