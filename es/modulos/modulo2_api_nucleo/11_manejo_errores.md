# 2.5 Tipos de Manejo de Errores

Construir aplicaciones de producción requiere un manejo de errores robusto. El SDK de Anthropic lanza excepciones específicas para diferentes modos de fallo.

## Jerarquía de Excepciones

Todas las excepciones heredan de `anthropic.APIError`.

- `APIConnectionError`: Problemas de red (DNS, Tiempo de espera, Conexión rechazada).
- `APIStatusError`: El servidor devolvió un código de estado distinto de 200.
  - `BadRequestError` (400): Petición mal formada.
  - `AuthenticationError` (401): Clave API incorrecta.
  - `PermissionError` (403): Acceso no autorizado.
  - `NotFoundError` (404): Recurso/Modelo no encontrado.
  - `RateLimitError` (429): Demasiadas peticiones.
  - `InternalServerError` (500): Problema en el lado de Anthropic.
  - `OverloadedError` (529): La API está sobrecargada.

## Estrategia de Manejo

1. **Errores Reintentables:** `RateLimitError`, `InternalServerError`, `OverloadedError`, `APIConnectionError`.
2. **No Reintentables:** `BadRequestError`, `AuthenticationError`, `PermissionError`, `NotFoundError`.

### Ejemplo de Código

```python
import anthropic
import time

client = anthropic.Anthropic()

def safe_call(prompt):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response
    except anthropic.RateLimitError:
        print("Límite de velocidad alcanzado. Esperando...")
        # Implementar backoff (espera exponencial)
    except anthropic.APIStatusError as e:
        if e.status_code == 529:
            print("Sobrecargado. Reintentar más tarde.")
        else:
            print(f"Error de API: {e}")
    except anthropic.APIConnectionError:
        print("Error de red.")
```

## Próximos Pasos
- Implementar [Lógica de Reintento](12_logica_reintentos.md).
