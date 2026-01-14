# 3.2 Técnicas de Reducción de Costes

## 1. Almacenamiento en Caché de Prompts
Como se discutió, esto proporciona un descuento de ~90% en tokens de entrada. Úsalo para:
- Contextos Grandes (Libros, Bases de código).
- Prompts del Sistema Frecuentes.
- Ejemplos few-shot (10+ ejemplos).

## 2. Selección de Modelo
- Usa **Haiku** para tareas simples.
- Usa **Sonnet** para inteligencia general.
- Usa **Opus** solo cuando la profundidad de razonamiento lo requiera.

## 3. Truncamiento de Tokens
- No envíes el historial de conversación completo si no es necesario.
- Resume turnos antiguos.

## 4. Procesamiento por Lotes
La **API de Lotes de Mensajes** (ver siguiente lección) ofrece un **50% de descuento** en todos los tokens si puedes esperar hasta 24 horas (usualmente mucho más rápido).

| Característica | Descuento | Velocidad |
|----------------|-----------|-----------|
| Caché de Prompts | ~90% (Entrada) | Rápido |
| API por Lotes | 50% (Total) | Lento (Async) |

## Próximos Pasos
- Aprende sobre [Procesamiento por Lotes](./08_batch_processing.md).
