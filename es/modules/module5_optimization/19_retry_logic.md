# 5.5 Lógica de Reintento Avanzada

## Retroceso Exponencial con Jitter (Exponential Backoff with Jitter)
El estándar de oro.
- Intento 1: Esperar 0s.
- Intento 2: Esperar 1s + rand(0, 0.1).
- Intento 3: Esperar 2s + rand(0, 0.1).
- Intento 4: Esperar 4s + rand(0, 0.1).

## Idempotencia
Asegúrate de que reintentar una petición no cause efectos secundarios (como cobrar a un usuario dos veces).
- **Peticiones de solo lectura:** Seguro reintentar.
- **Peticiones de acción:** Ten cuidado.

## Próximos Pasos
- [Observabilidad](./20_observability.md).
