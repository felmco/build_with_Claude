# 2.5 Implementando Lógica de Reintento

Para errores reintentables (500s, 429s, problemas de red), debes implementar una estrategia de **Backoff Exponencial**.

## ¿Qué es el Backoff Exponencial?

En lugar de reintentar inmediatamente (lo cual podría empeorar el problema), esperas intervalos progresivamente más largos: 1s, 2s, 4s, 8s...

### Reintentos Incorporados en el SDK

El SDK de Python de Anthropic tiene lógica de reintento incorporada habilitada por defecto (usualmente 2 reintentos).

```python
client = anthropic.Anthropic(
    max_retries=5  # Aumentar reintentos por defecto
)
```

### Decorador de Reintento Personalizado

Si necesitas más control (ej. usando la librería `tenacity`):

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import anthropic

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((anthropic.RateLimitError, anthropic.APIConnectionError))
)
def call_claude():
    return client.messages.create(...)
```

## Jitter (Fluctuación)

Añade "jitter" (aleatoriedad) a tu tiempo de espera para prevenir problemas de "manada atronadora" (thundering herd) donde muchos clientes reintentan en el mismo milisegundo exacto.

## Próximos Pasos
- Entiende el [Límite de Velocidad (Rate Limiting)](13_limite_velocidad.md) para evitar errores 429.
