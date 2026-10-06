# 5.5 Estrategias de Manejo de Errores

Cubrimos tipos básicos en el Módulo 2. Aquí, cubrimos **Resiliencia**.

## Cortocircuitos (Circuit Breakers)
Si Anthropic devuelve 500s para el 10% de las peticiones, deja de llamarlo por 1 minuto.
- **¿Por qué?** Previene fallos en cascada en tu sistema.

## Alternativas (Fallbacks)
Si Claude está caído, ¿qué pasa?
1. **Caché:** ¿Devolver una respuesta cacheada?
2. **Modo Degradado:** ¿"Características de IA no disponibles"?
3. **Otro Proveedor:** Recurrir a un modelo diferente (si es compatible).

## Gestión de Tiempo de Espera (Timeout)
Las generaciones largas pueden tardar un minuto o más.
- Establece tiempos de espera del cliente, p. ej. `anthropic.Anthropic(timeout=60.0)` o por petición con `client.with_options(timeout=60.0)`. El valor por defecto del SDK es de 10 minutos.
- Para `max_tokens` grandes usa streaming (`client.messages.stream(...)`); el SDK rechaza las peticiones sin streaming que espera que sean demasiado largas.
- No dejes que el trabajador de tu servidor web se cuelgue para siempre.

## Captura de errores
El SDK ya reintenta los errores 429, 5xx y de conexión (consulta [Lógica de Reintento](19_logica_reintentos.md)). Maneja lo que quede, empezando por lo más específico:

```python
try:
    response = client.messages.create(...)
except anthropic.RateLimitError:
    ...  # still rate limited after SDK retries: queue or shed load
except anthropic.APIConnectionError:
    ...  # network problem
except anthropic.APIStatusError as e:
    ...  # other HTTP errors; e.status_code, e.response
```

Comprueba también `response.stop_reason` antes de usar el contenido: `"refusal"` y `"max_tokens"` no son errores, pero requieren manejo.

## Próximos Pasos
- [Lógica de Reintento](19_logica_reintentos.md).
