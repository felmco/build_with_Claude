# 1.3 Manejo Básico de Errores

Cuando trabajas con APIs, las cosas pueden salir mal. El SDK de Anthropic proporciona excepciones específicas para ayudarte a manejar errores con elegancia.

## Tipos de Errores Comunes

| Código de Error | Clase de Excepción | Causa | Solución |
|------------|-----------------|-------|----------|
| 400 | `BadRequestError` | JSON inválido, parámetros malformados | Comprueba tu estructura de solicitud y parámetros. |
| 401 | `AuthenticationError` | Clave API inválida o faltante | Verifica tu variable de entorno `ANTHROPIC_API_KEY`. |
| 403 | `PermissionError` | La clave no tiene acceso al recurso | Comprueba los permisos de la cuenta. |
| 404 | `NotFoundError` | Modelo o recurso no encontrado | Comprueba la ortografía del nombre del modelo (ej. `claude-sonnet-4-5...`). |
| 413 | `RequestTooLarge` | Solicitud demasiado grande | Reduce el tamaño de entrada (ej. menos imágenes o texto). El máx es ~32MB. |
| 429 | `RateLimitError` | Demasiadas solicitudes o tokens | Implementa reintentos con espera (backoff). Solicita un aumento de límite. |
| 500 | `APIError` | Error interno del servidor | Reintenta la solicitud más tarde. |
| 529 | `OverloadedError` | La API está sobrecargada | Reintenta con espera exponencial (exponential backoff). |

## Implementando Bloques Try-Except

Siempre envuelve tus llamadas a la API en un bloque `try-except`.

```python
import anthropic
import os

client = anthropic.Anthropic()

try:
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hola"}]
    )
    print(message.content[0].text)

except anthropic.APIConnectionError as e:
    print("No se pudo contactar con el servidor")
    print(e.__cause__)  # Excepción subyacente

except anthropic.RateLimitError as e:
    print("Se recibió un código de estado 429; deberíamos esperar un poco.")

except anthropic.APIStatusError as e:
    print("Se recibió otro código de estado fuera del rango 200")
    print(f"Código de estado: {e.status_code}")
    print(e.response)
```

## Manejando Errores de Sobrecarga (529)

El `OverloadedError` significa específicamente que los sistemas de Anthropic están ocupados. El SDK maneja algunos reintentos automáticamente, pero deberías manejar esto en código de producción esperando antes de reintentar.

```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        # Hacer llamada a API
        break
    except anthropic.InternalServerError as e:
        if attempt == max_retries - 1:
            raise
        time.sleep(2 ** attempt)  # Espera exponencial
```

## Próximos Pasos
¡Felicidades! Has completado el Módulo 1. Ahora estás listo para pasar al [Módulo 2: Características de la API Principal](../modulo2_api_nucleo/README.md).
