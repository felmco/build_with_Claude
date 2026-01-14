# 5.3 Optimización de Latencia

## El TTFT vs Tiempo Total
- **TTFT (Tiempo Hasta el Primer Token):** Qué tan rápido el usuario ve *algo*. Importante para UI.
- **Tiempo Total:** Cuánto tiempo hasta que la petición termina.

## Optimizando TTFT
1. **Reduce Entrada:** Los prompts más cortos se procesan más rápido.
2. **Caché:** Los aciertos de caché procesados son mucho más rápidos.
3. **Modelo:** Haiku tiene un TTFT mucho más bajo que Opus.

## Optimizando Tiempo Total
1. **Reduce Salida:** Pide respuestas más cortas.
2. **Paraleliza:** Ejecuta subtareas independientes en paralelo.

## Próximos Pasos
- [Streaming para Mejor UX](./11_streaming_ux.md).
