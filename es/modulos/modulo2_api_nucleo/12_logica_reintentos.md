# 2.5 Implementando Lógica de Reintento

Para errores reintentables (500s, 429s, problemas de red), debes implementar una estrategia de **Backoff Exponencial**.

## ¿Qué es el Backoff Exponencial?

En lugar de reintentar inmediatamente (lo cual podría empeorar el problema), esperas intervalos progresivamente más largos: 1s, 2s, 4s, 8s...

### Reintentos Incorporados en el SDK

El SDK de Python de Anthropic tiene lógica de reintento incorporada habilitada por defecto (2 reintentos, `max_retries=2`). Reintenta errores de conexión y respuestas 408, 409, 429 y 5xx con espera exponencial, y respeta la cabecera `retry-after`.

```python
import anthropic

client = anthropic.Anthropic(
    max_retries=5,  # Aumentar reintentos por defecto (pon 0 para desactivar los reintentos del SDK)
    timeout=60.0,   # Segundos; el timeout por defecto es de 10 minutos
)
```

### Decorador de Reintento Personalizado

Si necesitas más control (ej. usando la librería `tenacity`):

```python
# pip install tenacity
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type
import anthropic

client = anthropic.Anthropic(max_retries=0)  # deja que tenacity se encargue de los reintentos

@retry(
    stop=stop_after_attempt(4),
    wait=wait_random_exponential(multiplier=1, max=30),  # espera exponencial con jitter
    retry=retry_if_exception_type((
        anthropic.RateLimitError,
        anthropic.InternalServerError,
        anthropic.OverloadedError,
        anthropic.APIConnectionError,
    )),
    reraise=True,
)
def call_claude(prompt: str):
    return client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
```

## Jitter (Fluctuación)

Añade "jitter" (aleatoriedad) a tu tiempo de espera (`wait_random_exponential` arriba ya lo hace) para prevenir problemas de "manada atronadora" (thundering herd) donde muchos clientes reintentan en el mismo milisegundo exacto.

## Próximos Pasos
- Entiende el [Límite de Velocidad (Rate Limiting)](13_limite_velocidad.md) para evitar errores 429.
