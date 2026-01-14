# 4.3 RAG Fundamentals

**Retrieval Augmented Generation (RAG)** is the technique of fetching external data and passing it to the model to ground its response.

## Why RAG?
- **Knowledge Cutoff:** Models don't know recent news.
- **Private Data:** Models don't know your company emails.
- **Hallucinations:** Reduces made-up facts.

## The Workflow
1. **Ingest:** Convert docs to text -> Chunk -> Embed -> Store in Vector DB.
2. **Retrieve:** User Query -> Embed -> Search Vector DB -> Get Top K chunks.
3. **Generate:** System Prompt + Top K Chunks + User Query -> Claude.

## Simple Implementation (No DB)
For small datasets, you don't need a Vector DB. Just load text into memory.

```python
docs = ["Doc 1 content...", "Doc 2 content..."]

def retrieve(query):
    # Keyword search (TF-IDF) or just return all for tiny sets
    return "\n\n".join(docs)

context = retrieve("question")
prompt = f"Context:\n{context}\n\nQuestion: {query}"
```

## Next Steps
- Learn about [Vector Databases](./10_vector_databases.md).
