# 5.5 Lógica de Reintento Avanzada

## El SDK ya reintenta
El SDK oficial `anthropic` reintenta los errores de conexión y las respuestas 408, 409, 429 y 5xx con retroceso exponencial y jitter, respetando el encabezado `retry-after`. El valor por defecto es `max_retries=2`. Ajústalo en lugar de escribir tu propio bucle:

```python
client = anthropic.Anthropic(max_retries=5)
# or per request
client.with_options(max_retries=0).messages.create(...)  # when you do your own retries
```

Envolver las llamadas del SDK en otro bucle de reintentos multiplica los intentos (3 x 3 = 9 peticiones) y empeora la limitación de velocidad. Si escribes tu propia capa, define `max_retries=0` en el cliente.

## Retroceso Exponencial con Jitter (Exponential Backoff with Jitter)
El estándar de oro, y lo que el SDK hace por ti:
- Intento 1: Esperar 0s.
- Intento 2: Esperar 1s + rand(0, 0.1).
- Intento 3: Esperar 2s + rand(0, 0.1).
- Intento 4: Esperar 4s + rand(0, 0.1).

## Qué reintentar
Reintenta solo los fallos transitorios: 429, 5xx (incluido 529 por sobrecarga) y errores de red. Nunca reintentes 400, 401, 403, 404 o 413; fallarán de la misma manera.

## Idempotencia
Asegúrate de que reintentar una petición no cause efectos secundarios (como cobrar a un usuario dos veces).
- **Peticiones de solo lectura:** Seguro reintentar.
- **Peticiones de acción:** Ten cuidado.

## Próximos Pasos
- [Observabilidad](20_observabilidad.md).
