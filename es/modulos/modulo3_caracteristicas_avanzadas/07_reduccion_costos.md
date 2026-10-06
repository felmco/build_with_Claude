# 3.2 Técnicas de Reducción de Costes

## 1. Almacenamiento en Caché de Prompts
Como se discutió, las lecturas de caché cuestan cerca del 10% del precio base de entrada (5% en Opus 5.5, 2.5% en Fable 5.1), mientras que las escrituras cuestan 1.25x. Úsalo para:
- Contextos Grandes (Libros, Bases de código).
- Prompts del Sistema Frecuentes.
- Ejemplos few-shot (10+ ejemplos).

## 2. Selección de Modelo
- Usa **Haiku 4.5** para tareas simples y de alto volumen.
- Usa **Sonnet 5.5** para inteligencia general.
- Usa **Opus 5.5** o **Fable 5.1** solo cuando la profundidad de razonamiento lo requiera.
- Configura un valor más bajo del parámetro `effort` para peticiones simples; los tokens de pensamiento se facturan como salida.

Consulta los IDs de modelo y precios vigentes en la [descripción general de modelos](https://platform.claude.com/docs/en/about-claude/models/overview).

## 3. Truncamiento de Tokens
- No envíes el historial de conversación completo si no es necesario.
- Resume turnos antiguos.
- Cuenta los tokens antes de enviar con `client.messages.count_tokens(...)` en lugar de adivinar.

## 4. Procesamiento por Lotes
La **API de Lotes de Mensajes** (ver siguiente lección) ofrece un **50% de descuento** en todos los tokens si puedes esperar hasta 24 horas (usualmente mucho más rápido).

| Característica | Descuento | Velocidad |
|----------------|-----------|-----------|
| Caché de Prompts | ~90% menos en lecturas de entrada cacheadas | Más rápido |
| API por Lotes | 50% (entrada y salida) | Async, hasta 24 horas |

Ambas se pueden combinar, pero los aciertos de caché dentro de un lote son de mejor esfuerzo porque las peticiones del lote pueden ejecutarse en cualquier orden.

## Próximos Pasos
- Aprende sobre [Procesamiento por Lotes](08_procesamiento_lotes.md).
