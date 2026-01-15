# 3.3 API de Lotes de Mensajes (Message Batches API)

La API de Lotes de Mensajes te permite enviar un grupo grande de peticiones a la vez.

## Características Clave
- **Asíncrono:** Envías un lote, y Claude lo procesa en segundo plano.
- **50% Más Barato:** Tanto tokens de entrada como de salida tienen un 50% de descuento sobre el precio estándar.
- **SLA:** Resultados dentro de 24 horas (a menudo < 1 hora).
- **Límite:** Hasta 100,000 peticiones por lote (o 256MB).

## Creando un Lote

**1. Preparar Archivo JSONL**
Crea una lista de peticiones.

```json
{"custom_id": "req1", "params": {"model": "claude-sonnet-4-5-20250929", "max_tokens": 1024, "messages": [...]}}
{"custom_id": "req2", "params": {"model": "claude-sonnet-4-5-20250929", "max_tokens": 1024, "messages": [...]}}
```

**2. Enviar Lote**

```python
import anthropic

client = anthropic.Anthropic()

batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "my-first-request",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hello world"}]
            }
        }
    ]
)
print(f"ID de Lote: {batch.id}")
```

## Recuperando Resultados

1. **Sondea (Poll)** el estado del lote (`in_progress` -> `ended`).
2. **Descarga** la URL de resultados.

```python
import time

while True:
    batch = client.messages.batches.retrieve(batch.id)
    if batch.processing_status == "ended":
        break
    time.sleep(60)

# Obtener resultados
results_url = batch.results_url
# (Obtener contenido de URL para ver resultados JSONL)
```

## Próximos Pasos
- Ver [Casos de Uso de Lotes](09_casos_uso_lotes.md).
