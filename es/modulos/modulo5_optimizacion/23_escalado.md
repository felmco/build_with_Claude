# 5.6 Escalado Horizontal

## Apatridia (Statelessness)
La API de Claude es sin estado. Tu aplicación también debería serlo.
- Almacena el estado de la sesión en Redis, no en la memoria de Python.
- Ejecuta múltiples instancias de tu aplicación (Docker/K8s).

## Compartir Límites de Velocidad
Los límites de velocidad se aplican por organización (y por workspace, si defines límites) y por modelo, no por servidor ni por clave. Si tienes 10 servidores, todos consumen de los mismos límites.
- **Limitador de Velocidad Centralizado:** Usa Redis para contar peticiones y tokens globalmente a través de todos los servidores.
- Maneja las respuestas `429` (el SDK las reintenta y respeta `retry-after`) y lee los encabezados de respuesta `anthropic-ratelimit-*` para ver tu presupuesto restante.

## Próximos Pasos
- [Balanceo de Carga](24_balanceo_carga.md).
