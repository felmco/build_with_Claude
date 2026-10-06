# 4.5 Limitación de Velocidad y Colas

## El Problema
Tu app se hace viral. 10,000 usuarios pulsan "Enviar". Golpeas los límites de velocidad de Anthropic inmediatamente.

## La Solución: Cola de Token Bucket

1. **Cliente:** Envía petición -> Gateway API.
2. **Gateway:** Empuja trabajo a **Cola Redis**.
3. **Trabajador:**
   - Comprueba "Token Bucket" (Tokens disponibles / minuto).
   - Si hay disponibles: Procesa trabajo.
   - Si no: Duerme / Reintenta más tarde.

Nota: el SDK reintenta los 429 automáticamente (`max_retries`, respetando `retry-after`). Una cola sirve para suavizar ráfagas más allá de eso. Para trabajo masivo no urgente, la API de Message Batches funciona con un 50% de descuento y sin consumir los límites de tiempo real.

## Librerías
- Python: `celery` o `rq`.
- Redis: Para la cola.

## Próximos Pasos
- [Logging y Monitorización](19_registro_monitoreo.md).
