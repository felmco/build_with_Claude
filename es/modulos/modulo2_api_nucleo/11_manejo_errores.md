# 2.5 Tipos de Manejo de Errores

Construir aplicaciones de producción requiere un manejo de errores robusto. El SDK de Anthropic lanza excepciones específicas para diferentes modos de fallo.

## Jerarquía de Excepciones

Todas las excepciones heredan de `anthropic.APIError`.

- `APIConnectionError`: Problemas de red (DNS, Tiempo de espera, Conexión rechazada).
- `APIStatusError`: El servidor devolvió un código de estado distinto de 200.
  - `BadRequestError` (400): Petición mal formada.
  - `AuthenticationError` (401): Clave API incorrecta.
  - `PermissionDeniedError` (403): Acceso no autorizado (no es el `PermissionError` incorporado de Python).
  - `NotFoundError` (404): Recurso/Modelo no encontrado.
  - `RequestTooLargeError` (413): La petición supera el límite de tamaño (32 MB).
  - `RateLimitError` (429): Demasiadas peticiones.
  - `InternalServerError` (500): Problema en el lado de Anthropic.
  - `OverloadedError` (529): La API está sobrecargada.

## Estrategia de Manejo

El SDK ya reintenta dos veces los errores 429, 5xx y de conexión (`max_retries=2`) antes de lanzar la excepción, así que los errores siguientes llegan a tu código solo cuando esos reintentos se han agotado.

1. **Errores Reintentables:** `RateLimitError`, `InternalServerError`, `OverloadedError`, `APIConnectionError`.
2. **No Reintentables:** `BadRequestError`, `AuthenticationError`, `PermissionDeniedError`, `NotFoundError`, `RequestTooLargeError`.

### Ejemplo de Código

```python
import anthropic
import time

client = anthropic.Anthropic()

def safe_call(prompt):
    try:
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response
    except anthropic.RateLimitError:
        print("Límite de velocidad alcanzado. Esperando...")
        # Implementar backoff (espera exponencial)
    except anthropic.APIConnectionError:
        print("Error de red.")
    except anthropic.APIStatusError as e:  # clase base de los errores HTTP, por eso va al final
        if e.status_code == 529:
            print("Sobrecargado. Reintentar más tarde.")
        else:
            print(f"Error de API {e.status_code}: {e}")
            print(f"Request ID: {e.response.headers.get('request-id')}")  # inclúyelo al contactar con soporte
```

## Próximos Pasos
- Implementar [Lógica de Reintento](12_logica_reintentos.md).
