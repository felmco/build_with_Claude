# 5.5 Observabilidad

## Rastreo (Tracing)
Sigue una petición de Usuario -> API -> Claude -> DB -> Usuario.
- **OpenTelemetry:** Estándar para rastreo.

## Registro de Costes
Registra `usage.input_tokens`, `usage.output_tokens` y los campos de caché (`cache_creation_input_tokens`, `cache_read_input_tokens`) para *cada* petición, además del ID de la petición (`response._request_id`) para los tickets de soporte.
- Calcula coste por usuario.
- Identifica "Ballenas" (usuarios que te cuestan una fortuna).

## Monitorización de Calidad
Registra la "Tasa de Rechazo" (respuestas con `stop_reason == "refusal"`) y la proporción que termina en `"max_tokens"`.
- Si Claude empieza a rechazar el 50% de las peticiones, tu prompt del sistema podría haberse roto.

## Próximos Pasos
- Muévete a [Seguridad y Cumplimiento](21_seguridad.md).
