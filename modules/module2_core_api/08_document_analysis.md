# 2.3 Document Analysis Strategies

Once you can send PDFs or images, how do you get the best analysis?

## 1. Extraction
Claude excels at converting unstructured document data into structured JSON.

**Prompt:**
> "Extract the invoice number, date, and total amount from this document. Return JSON."

For output that must always match a schema, use structured outputs (`output_config={"format": {"type": "json_schema", ...}}`, see [Managing Conversations](./03_conversations.md)).

## 2. Summarization
For long documents, ask for tiered summaries.

**Prompt:**
> "Provide a 1-sentence executive summary, followed by a bulleted list of the top 3 risks mentioned in this contract."

## 3. Visual Analysis (Charts & Graphs)
Claude can interpret charts in PDFs/Images.

**Technique:**
- Isolate the chart if possible (crop image).
- Ask specifically: "Analyze the trend in the bar chart on page 5."

## 4. Comparisons
Send two documents (e.g., Contract V1 and Contract V2) and ask for a diff.

```python
# doc_v1 / doc_v2: base64 PDF strings (or use {"type": "file", "file_id": ...} sources)
messages = [
    {"role": "user", "content": [
        {"type": "text", "text": "Version 1:"},
        {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": doc_v1}},
        {"type": "text", "text": "Version 2:"},
        {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": doc_v2}},
        {"type": "text", "text": "Highlight the changes in the liability clause."},
    ]}
]
```

## Handling Complex Layouts
PDFs with multiple columns or complex tables can be tricky.
- **Tip:** Ask Claude to read the table row by row, or raise `output_config.effort`, if it misreads a table.
- **Tip:** Use `text` mode extraction tools (Python `pypdf`) alongside Claude's vision for verification.

## Next Steps
- Learn about the [Files API](./09_files_api.md) for easier management.
