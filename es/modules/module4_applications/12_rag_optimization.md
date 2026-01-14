# 4.3 Optimización de RAG

El RAG básico a menudo falla ("No puedo encontrar esa información"). La optimización arregla esto.

## 1. Búsqueda Híbrida
Combina **Búsqueda por Palabras Clave** (BM25) con **Búsqueda Semántica** (Embeddings).
- Las palabras clave captan coincidencias exactas ("Error 503").
- La semántica capta conceptos ("Fallo del servidor").

## 2. Re-clasificación (Reranking)
1. Recupera los top 50 resultados (rápido).
2. Usa un modelo **Reranker** (Cohere Rerank) para ordenarlos por relevancia a la consulta.
3. Pasa los top 5 a Claude.

## 3. Expansión de Consulta
Pide a Claude que genere sinónimos o sub-preguntas.
- Usuario: "Compara X e Y."
- Agente: "Buscando X", "Buscando Y".

## 4. Recuperación Contextual
En lugar de incrustar solo un fragmento crudo, pide a Claude que añada contexto *antes* de incrustar.
- **Fragmento:** "Costaba 50 dólares." (Ambiguo)
- **Fragmento Enriquecido:** "El precio del Widget X mencionado en el informe de 2024 era de 50 dólares." (Incrusta esto).

## Próximos Pasos
- Introducción a [MCP](./13_mcp_intro.md).
