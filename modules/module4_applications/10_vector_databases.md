# 4.3 Vector Databases

Vector databases store data as high-dimensional numbers (embeddings), allowing for "Semantic Search" (search by meaning, not just keywords).

## Popular Options
- **Pinecone:** Managed, fast.
- **Chroma:** Open source, local/server.
- **Weaviate:** Open source, strong hybrid search.
- **Postgres (pgvector):** Good if you already use Postgres.

## Integration Pattern

```python
# Pseudo-code
import chromadb

client = chromadb.Client()
collection = client.create_collection("docs")

# Add docs
collection.add(
    documents=["This is a doc about cats", "This is about dogs"],
    ids=["id1", "id2"]
)

# Search
results = collection.query(
    query_texts=["feline"],
    n_results=1
)
# Returns "This is a doc about cats"
```

## Next Steps
- Understand [Embeddings](./11_embeddings.md).
