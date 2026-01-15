# 5.5 Observabilidad

## Rastreo (Tracing)
Sigue una petición de Usuario -> API -> Claude -> DB -> Usuario.
- **OpenTelemetry:** Estándar para rastreo.

## Registro de Costes
Registra `input_tokens` y `output_tokens` para *cada* petición.
- Calcula coste por usuario.
- Identifica "Ballenas" (usuarios que te cuestan una fortuna).

## Monitorización de Calidad
Registra "Tasa de Rechazo".
- Si Claude empieza a rechazar el 50% de las peticiones, tu prompt del sistema podría haberse roto.

## Próximos Pasos
- Muévete a [Seguridad y Cumplimiento](21_seguridad.md).
