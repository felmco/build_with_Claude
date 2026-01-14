# 4.3 Fundamentos de RAG

**Generación Aumentada por Recuperación (RAG)** es la técnica de obtener datos externos y pasarlos al modelo para fundamentar su respuesta.

## ¿Por qué RAG?
- **Corte de Conocimiento:** Los modelos no conocen noticias recientes.
- **Datos Privados:** Los modelos no conocen los correos de tu empresa.
- **Alucinaciones:** Reduce hechos inventados.

## El Flujo de Trabajo
1. **Ingestar:** Convertir documentos a texto -> Fragmentar (Chunk) -> Embed (Integrar) -> Almacenar en DB Vectorial.
2. **Recuperar:** Consulta de Usuario -> Embed -> Buscar en DB Vectorial -> Obtener Top K fragmentos.
3. **Generar:** Prompt del Sistema + Top K Fragmentos + Consulta de Usuario -> Claude.

## Implementación Simple (Sin DB)
Para conjuntos de datos pequeños, no necesitas una DB Vectorial. Simplemente carga el texto en memoria.

```python
docs = ["Doc 1 content...", "Doc 2 content..."]

def retrieve(query):
    # Búsqueda por palabras clave (TF-IDF) o simplemente devolver todo para conjuntos diminutos
    return "\n\n".join(docs)

context = retrieve("question")
prompt = f"Context:\n{context}\n\nQuestion: {query}"
```

## Próximos Pasos
- Aprende sobre [Bases de Datos Vectoriales](./10_vector_databases.md).
