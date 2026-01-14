# 2.5 Entendiendo los Límites de Velocidad (Rate Limits)

Los límites de velocidad definen cuánto puedes usar la API dentro de un marco de tiempo específico.

## Tipos de Límites

1. **RPM (Requests Per Minute):** Número de llamadas a la API (Peticiones Por Minuto).
2. **TPM (Tokens Per Minute):** Tokens totales (Entrada + Salida) (Tokens Por Minuto).
3. **Límite Diario:** Gasto total o tokens por día (varía según el nivel).

## Sistema de Niveles (Ejemplo)

| Nivel | RPM | TPM |
|-------|-----|-----|
| Gratuito | 5 | 20k |
| Nivel 1 | 50 | 50k |
| Nivel 2 | 1000 | 1M |
| Nivel 4 | 4000 | 400k+ |

*Consulta tus límites específicos en la Consola.*

## Manejando Límites de Velocidad

### Encabezados
La API devuelve encabezados indicando tu estado:
- `anthropic-ratelimit-requests-limit`
- `anthropic-ratelimit-requests-remaining`
- `anthropic-ratelimit-requests-reset`
- `retry-after`: Segundos para esperar.

### Estrategias

1. **Throttling (Regulación):** Rastrea tu uso localmente y pausa antes de enviar si estás cerca del límite.
2. **Queuing (Colas):** Pon las peticiones en una cola (Celery, Redis) y procésalas a una velocidad controlada.
3. **API por Lotes (Batch API):** Usa la API por Lotes (Módulo 3) para tareas de alto volumen y no sensibles al tiempo (50% más barato y límites más altos).

## ¡Felicidades!
Has completado el Módulo 2. Ahora entiendes la API principal, visión, archivos y patrones de fiabilidad.

## Siguiente Módulo
Procede al [Módulo 3: Características Avanzadas](../module3_advanced_features/README.md) para aprender sobre Herramientas, Caché y Procesamiento por Lotes.
