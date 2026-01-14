# 5.5 Estrategias de Manejo de Errores

Cubrimos tipos básicos en el Módulo 2. Aquí, cubrimos **Resiliencia**.

## Cortocircuitos (Circuit Breakers)
Si Anthropic devuelve 500s para el 10% de las peticiones, deja de llamarlo por 1 minuto.
- **¿Por qué?** Previene fallos en cascada en tu sistema.

## Alternativas (Fallbacks)
Si Claude está caído, ¿qué pasa?
1. **Caché:** ¿Devolver una respuesta cacheada?
2. **Modo Degradado:** ¿"Características de IA no disponibles"?
3. **Otro Proveedor:** Recurrir a un modelo diferente (si es compatible).

## Gestión de Tiempo de Espera (Timeout)
Las peticiones de Anthropic pueden tardar 30s+.
- Establece tiempos de espera del cliente (`timeout=60.0`).
- No dejes que el trabajador de tu servidor web se cuelgue para siempre.

## Próximos Pasos
- [Lógica de Reintento](./19_retry_logic.md).
