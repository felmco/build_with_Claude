# 3.3 API de Lotes de Mensajes (Message Batches API)

La API de Lotes de Mensajes te permite enviar un grupo grande de peticiones a la vez.

## Características Clave
- **Asíncrono:** Envías un lote, y Claude lo procesa en segundo plano.
- **50% Más Barato:** Tanto tokens de entrada como de salida tienen un 50% de descuento sobre el precio estándar.
- **SLA:** La mayoría de los lotes terminan en menos de 1 hora; el máximo es 24 horas, tras las cuales las peticiones sin terminar expiran.
- **Retención:** Los resultados siguen disponibles durante 29 días tras la creación.
- **Conjunto completo de funciones:** Visión, herramientas, pensamiento y caché funcionan dentro de un lote.
- **Límite:** Hasta 100,000 peticiones por lote (o 256MB).

## Creando un Lote

**1. Preparar las peticiones**
Cada petición tiene un `custom_id` único y un objeto `params` que es el mismo cuerpo que enviarías a `messages.create`. El SDK las recibe como una lista de Python (la API REST recibe la misma lista como JSON; no hay subida de archivos).

```json
{"custom_id": "req1", "params": {"model": "claude-sonnet-5-5", "max_tokens": 1024, "messages": [{"role": "user", "content": "..."}]}}
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
                "model": "claude-sonnet-5-5",
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
2. **Recorre los resultados** con el SDK. Los resultados pueden llegar en cualquier orden, así que empárejalos con tus entradas mediante `custom_id`.

```python
import time

while True:
    batch = client.messages.batches.retrieve(batch.id)
    if batch.processing_status == "ended":
        break
    time.sleep(60)

for entry in client.messages.batches.results(batch.id):
    result = entry.result
    if result.type == "succeeded":
        text = next((b.text for b in result.message.content if b.type == "text"), "")
        print(f"[{entry.custom_id}] {text[:100]}")
    elif result.type == "errored":
        print(f"[{entry.custom_id}] error: {result.error}")
    else:  # "canceled" or "expired"
        print(f"[{entry.custom_id}] {result.type}")
```

## Notas
- Algunos modelos (Claude Fable 5.1, Opus 5.5, Sonnet 5.5) rechazan `tool_choice` forzado (`any`/`tool`), también en lotes.
- Un lote se puede cancelar con `client.messages.batches.cancel(batch.id)`; las peticiones que ya se están ejecutando terminan igualmente y se facturan.

## Próximos Pasos
- Ver [Casos de Uso de Lotes](09_casos_uso_lotes.md).
