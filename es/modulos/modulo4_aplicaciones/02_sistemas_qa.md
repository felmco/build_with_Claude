# 4.1 Sistemas de Q&A (Preguntas y Respuestas)

Los sistemas de Q&A difieren de los chatbots en que a menudo son de un solo turno y se centran en la precisión más que en el flujo de conversación.

## Arquitectura

1. **Entrada:** Pregunta del usuario.
2. **Recuperación:** Obtener conocimiento (RAG).
3. **Síntesis:** Claude genera respuesta basada *solo* en el contexto recuperado.
4. **Cita:** Claude enlaza fuentes.

## Patrón de Prompt: "Responder usando Contexto"

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

## Manejando "No lo sé"
Es crucial instruir a Claude para rechazar responder si faltan datos, en lugar de alucinar.

## Estructura de Salida
- **Respuesta:** La respuesta directa.
- **Citas:** Citas textuales usadas.
- **Fuentes:** Metadatos (números de página, URLs).

## Próximos Pasos
- [Pipelines de Generación de Contenido](03_generacion_contenido.md).
