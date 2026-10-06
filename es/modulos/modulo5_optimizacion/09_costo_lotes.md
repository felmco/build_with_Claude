# 5.2 Procesamiento por Lotes para Reducción de Costes

## La Regla del 50%
La API de Message Batches cuesta 50% menos que las llamadas estándar. Cualquier cosa que no necesite respuesta inmediata debería ir a Lotes (Batch). La mayoría de los lotes terminan en una hora, pero cuenta con hasta 24 horas.

## Arquitectura
1. **Cola:** Acumula peticiones no urgentes en una tabla de DB.
2. **Trabajo Cron:** Cada 5 minutos, consulta la tabla.
3. **Enviar:** Si > 100 peticiones (o si la más antigua es > 1 hora), envía un lote.
4. **Recuperar:** Sondea resultados y actualiza la DB.

## Ejemplo de Ahorro de Costes
- **Escenario:** Procesando 1M documentos/mes con Sonnet 5.5, suponiendo 2K tokens de entrada y 500 de salida cada uno (2,000 MTok de entrada, 500 MTok de salida).
- **Estándar:** $2 entrada + $10 salida / MTok = $4,000 + $5,000 = $9,000.
- **Lote:** $1 entrada + $5 salida / MTok = $4,500.
- **Ahorro:** unos $4,500 al mes. Consulta los precios vigentes antes de presupuestar.

## Ejemplo mínimo
```python
import anthropic

client = anthropic.Anthropic()
batch = client.messages.batches.create(requests=[
    {
        "custom_id": f"doc-{i}",
        "params": {
            "model": "claude-sonnet-5-5",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": f"Summarize: {doc}"}],
        },
    }
    for i, doc in enumerate(docs)
])
# Later: poll client.messages.batches.retrieve(batch.id) until processing_status == "ended",
# then iterate client.messages.batches.results(batch.id) and match on custom_id
# (results are not returned in request order).
```

Message Batches no está disponible en Amazon Bedrock ni en Vertex AI; usa la API de primera parte (o Claude Platform en AWS) para ello.

## Próximos Pasos
- Muévete a [Optimización de Latencia](10_latencia.md).
