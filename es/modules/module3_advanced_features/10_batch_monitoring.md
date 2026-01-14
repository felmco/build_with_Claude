# 3.3 Código de Monitorización de Lotes

**monitor_batch.py**:

```python
import anthropic
import time
import requests

client = anthropic.Anthropic()

def wait_for_batch(batch_id):
    print(f"Monitorizando lote {batch_id}...")

    while True:
        batch = client.messages.batches.retrieve(batch_id)
        status = batch.processing_status

        print(f"Estado: {status}")

        if status == "ended":
            return batch
        elif status == "canceling" or status == "canceled":
            print("Lote cancelado.")
            return batch
        elif status == "expired":
            print("Lote expirado.")
            return batch

        time.sleep(30) # Comprobar cada 30s

def download_results(batch):
    if not batch.results_url:
        print("No se encontró URL de resultados.")
        return

    print("Descargando resultados...")
    response = requests.get(batch.results_url)

    # Guardar en archivo
    with open("batch_results.jsonl", "w") as f:
        f.write(response.text)
    print("Guardado en batch_results.jsonl")

# Uso (Asumiendo que tienes un batch_id)
# batch = wait_for_batch("msgbatch_123...")
# download_results(batch)
```

## Próximos Pasos
- Muévete a [Fundamentos de Visión](./11_vision_basics.md).
