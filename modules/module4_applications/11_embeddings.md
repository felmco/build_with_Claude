# 4.3 Embeddings

An **embedding** is a vector (list of numbers) representing the semantic meaning of text.

## Choosing a Provider
Anthropic does not produce embeddings directly. Use:
- **Voyage AI:** Highly recommended for Claude.
- **OpenAI:** `text-embedding-3-small`.
- **HuggingFace:** `sentence-transformers` (Local).

## Using Voyage AI

```python
import voyageai

vo = voyageai.Client()
text = "Hello world"
vector = vo.embed([text], model="voyage-3-large").embeddings[0]
print(vector[:5]) # [0.012, -0.04, ...]
```

## Best Practices
- **Chunking:** Don't embed a whole book as one vector. Split into paragraphs (chunk size ~512 tokens).
- **Overlap:** Include overlap between chunks (e.g., 50 tokens) to preserve context boundaries.

## Next Steps
- [RAG Optimization](./12_rag_optimization.md).
