# 5.3 Monitorización de Respuesta

No puedes optimizar lo que no mides.

## Métricas para Rastrear
1. **Latencia (P50, P90, P99):** ¿Qué tan rápido es usualmente? ¿Qué tan lento es en el peor caso?
2. **Uso de Tokens:** ¿Están algunos prompts consumiendo mucho más de lo esperado?
3. **Tasa de Error:** 429s, 500s.
4. **Tasa de Aciertos de Caché:** ¿Están funcionando tus breakpoints? Compara `usage.cache_read_input_tokens` con `usage.input_tokens` en cada respuesta.

```python
import time

start = time.perf_counter()
response = client.messages.create(...)
latency = time.perf_counter() - start
u = response.usage
metrics = {
    "latency_s": latency,
    "input_tokens": u.input_tokens,
    "output_tokens": u.output_tokens,
    "cache_read": u.cache_read_input_tokens,
    "stop_reason": response.stop_reason,
    "request_id": response._request_id,
}
```

## Tableros (Dashboarding)
Envía estas métricas a Datadog/Grafana/CloudWatch usando instrumentación estándar.

## Próximos Pasos
- Muévete a [Evaluación y Pruebas](14_evaluacion.md).
