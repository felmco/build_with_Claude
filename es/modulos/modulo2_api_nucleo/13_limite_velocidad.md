# 2.5 Entendiendo los Límites de Velocidad (Rate Limits)

Los límites de velocidad definen cuánto puedes usar la API dentro de un marco de tiempo específico.

## Tipos de Límites

1. **RPM (Requests Per Minute):** Número de llamadas a la API (Peticiones Por Minuto).
2. **ITPM / OTPM (Tokens de Entrada / Salida Por Minuto):** Los tokens de entrada y de salida se limitan por separado. En la mayoría de los modelos, los tokens de entrada en caché leídos de la caché de prompts no cuentan para el ITPM.
3. **Límite de gasto mensual:** Gasto máximo por mes (varía según el nivel).

## Sistema de Niveles

Los límites dependen de tu nivel de uso (Nivel 1 a Nivel 4, más límites personalizados para empresas) y se fijan **por clase de modelo**, con límites separados de tokens de entrada y de salida (ITPM y OTPM). Los niveles suben automáticamente a medida que crece tu gasto. Las cifras cambian con el tiempo, así que no las codifiques en tu código: consulta tus propios límites en la [Consola de Claude](https://platform.claude.com/settings/limits) y en la [documentación de límites](https://platform.claude.com/docs/en/api/rate-limits).

## Manejando Límites de Velocidad

### Encabezados
La API devuelve encabezados indicando tu estado:
- `anthropic-ratelimit-requests-limit`
- `anthropic-ratelimit-requests-remaining`
- `anthropic-ratelimit-requests-reset`
- `anthropic-ratelimit-input-tokens-*` y `anthropic-ratelimit-output-tokens-*` (mismos sufijos `limit` / `remaining` / `reset`)
- `retry-after`: Segundos para esperar (se envía con las respuestas 429).

```python
import anthropic

client = anthropic.Anthropic()
raw = client.messages.with_raw_response.create(
    model="claude-sonnet-5-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hi"}],
)
print(raw.headers.get("anthropic-ratelimit-requests-remaining"))
message = raw.parse()  # el objeto Message habitual
```

### Estrategias

1. **Throttling (Regulación):** Rastrea tu uso localmente y pausa antes de enviar si estás cerca del límite.
2. **Queuing (Colas):** Pon las peticiones en una cola (Celery, Redis) y procésalas a una velocidad controlada.
3. **API por Lotes (Batch API):** Usa la API por Lotes (Módulo 3) para tareas de alto volumen y no sensibles al tiempo (50% más barato, y los lotes tienen sus propios límites independientes).

## ¡Felicidades!
Has completado el Módulo 2. Ahora entiendes la API principal, visión, archivos y patrones de fiabilidad.

## Siguiente Módulo
Procede al [Módulo 3: Características Avanzadas](../modulo3_caracteristicas_avanzadas/README.md) para aprender sobre Herramientas, Caché y Procesamiento por Lotes.
