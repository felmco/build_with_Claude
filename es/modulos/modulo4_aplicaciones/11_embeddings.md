# 4.3 Embeddings

Un **embedding** es un vector (lista de números) que representa el significado semántico del texto.

## Eligiendo un Proveedor
Anthropic no produce embeddings directamente. Usa:
- **Voyage AI:** El proveedor de embeddings recomendado por Anthropic (`pip install voyageai`, requiere `VOYAGE_API_KEY`).
- **OpenAI:** `text-embedding-3-small`.
- **HuggingFace:** `sentence-transformers` (Local).

## Usando Voyage AI

```python
import voyageai

vo = voyageai.Client()
text = "Hello world"
# Los nombres de modelos cambian: consulta la documentación de Voyage AI para el modelo recomendado actual
vector = vo.embed([text], model="voyage-3-large").embeddings[0]
print(vector[:5]) # [0.012, -0.04, ...]
```

## Mejores Prácticas
- **Fragmentación (Chunking):** No incrustes un libro entero como un solo vector. Divide en párrafos (tamaño de fragmento ~512 tokens).
- **Superposición (Overlap):** Incluye superposición entre fragmentos (ej. 50 tokens) para preservar los límites del contexto.

## Próximos Pasos
- [Optimización de RAG](12_optimizacion_rag.md).
