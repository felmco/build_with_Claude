# 3.3 Código de Monitorización de Lotes

**monitor_batch.py**:

```python
import time

import anthropic

client = anthropic.Anthropic()

def wait_for_batch(batch_id, poll_seconds=30):
    print(f"Monitorizando lote {batch_id}...")

    while True:
        batch = client.messages.batches.retrieve(batch_id)
        counts = batch.request_counts
        print(f"Estado: {batch.processing_status} "
              f"(processing={counts.processing}, succeeded={counts.succeeded}, "
              f"errored={counts.errored}, canceled={counts.canceled}, expired={counts.expired})")

        # processing_status es uno de: in_progress, canceling, ended.
        # Las peticiones individuales aún pueden terminar como canceled o expired.
        if batch.processing_status == "ended":
            return batch

        time.sleep(poll_seconds)

def save_results(batch_id, path="batch_results.jsonl"):
    # El endpoint de resultados requiere tu API key, así que usa el SDK en lugar de un GET HTTP simple a results_url
    print("Descargando resultados...")
    with open(path, "w") as f:
        for entry in client.messages.batches.results(batch_id):
            f.write(entry.model_dump_json() + "\n")
    print(f"Guardado en {path}")

# Uso (Asumiendo que tienes un batch_id)
# batch = wait_for_batch("msgbatch_123...")
# save_results(batch.id)
```

Cada línea del archivo guardado tiene un `custom_id` y un `result` cuyo `type` es `succeeded`, `errored`, `canceled` o `expired`. Reintenta las peticiones `errored` (errores de servidor) y `expired` en un nuevo lote.

## Próximos Pasos
- Muévete a [Fundamentos de Visión](11_conceptos_basicos_vision.md).
