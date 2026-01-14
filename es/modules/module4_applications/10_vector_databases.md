# 4.3 Bases de Datos Vectoriales

Las bases de datos vectoriales almacenan datos como números de alta dimensión (embeddings), permitiendo la "Búsqueda Semántica" (búsqueda por significado, no solo palabras clave).

## Opciones Populares
- **Pinecone:** Gestionado, rápido.
- **Chroma:** Código abierto, local/servidor.
- **Weaviate:** Código abierto, búsqueda híbrida fuerte.
- **Postgres (pgvector):** Bueno si ya usas Postgres.

## Patrón de Integración

```python
# Pseudo-código
import chromadb

client = chromadb.Client()
collection = client.create_collection("docs")

# Añadir documentos
collection.add(
    documents=["This is a doc about cats", "This is about dogs"],
    ids=["id1", "id2"]
)

# Buscar
results = collection.query(
    query_texts=["feline"],
    n_results=1
)
# Devuelve "This is a doc about cats"
```

## Próximos Pasos
- Entiende los [Embeddings](./11_embeddings.md).
