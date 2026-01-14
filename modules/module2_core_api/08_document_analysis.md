# 2.3 Document Analysis Strategies

Once you can send PDFs or images, how do you get the best analysis?

## 1. Extraction
Claude excels at converting unstructured document data into structured JSON.

**Prompt:**
> "Extract the invoice number, date, and total amount from this document. Return JSON."

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
messages=[
    {"role": "user", "content": [
        {"type": "document", "source": {...data_v1...}}, # Doc 1
        {"type": "text", "text": "Here is Version 1."},
        {"type": "document", "source": {...data_v2...}}, # Doc 2
        {"type": "text", "text": "Here is Version 2. Highlight the changes in the liability clause."}
    ]}
]
```

## Handling Complex Layouts
PDFs with multiple columns or complex tables can be tricky.
- **Tip:** Ask Claude to "Think step-by-step about the layout" if it misreads a table.
- **Tip:** Use `text` mode extraction tools (Python `pypdf`) alongside Claude's vision for verification.

## Next Steps
- Learn about the [Files API](./09_files_api.md) for easier management.
