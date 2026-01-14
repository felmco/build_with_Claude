# 4.1 Q&A Systems

Q&A systems differ from chatbots in that they are often single-turn and focused on accuracy over conversation flow.

## Architecture

1. **Input:** User question.
2. **Retrieval:** Fetch knowledge (RAG).
3. **Synthesis:** Claude generates answer based *only* on retrieved context.
4. **Citation:** Claude links sources.

## Prompt Pattern: "Answer using Context"

```python
system_prompt = """
You are a helpful assistant. Answer the user's question using ONLY the provided context.
If the answer is not in the context, say "I don't know".
Cite the Document ID for every statement.

<context>
{retrieved_documents}
</context>
"""
```

## Handling "I don't know"
It is crucial to instruct Claude to refuse answering if the data is missing, rather than hallucinating.

## Output Structure
- **Answer:** The direct answer.
- **Quotes:** Verbatim quotes used.
- **Sources:** Metadata (page numbers, URLs).

## Next Steps
- [Content Generation Pipelines](./03_content_generation.md).
