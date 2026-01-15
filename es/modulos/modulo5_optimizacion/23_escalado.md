# 5.6 Escalado Horizontal

## Apatridia (Statelessness)
La API de Claude es sin estado. Tu aplicación también debería serlo.
- Almacena el estado de la sesión en Redis, no en la memoria de Python.
- Ejecuta múltiples instancias de tu aplicación (Docker/K8s).

## Compartir Límites de Velocidad
Si tienes 10 servidores, comparten UN límite de clave API de Anthropic.
- **Limitador de Velocidad Centralizado:** Usa Redis para contar tokens globalmente a través de todos los servidores.

## Próximos Pasos
- [Balanceo de Carga](24_balanceo_carga.md).
