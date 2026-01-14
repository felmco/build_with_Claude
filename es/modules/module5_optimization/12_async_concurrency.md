# 5.3 Async y Concurrencia

Para escalar aplicaciones de alto rendimiento, debes usar AsyncIO.

## Cliente Asíncrono de Python

```python
from anthropic import AsyncAnthropic
import asyncio

client = AsyncAnthropic()

async def worker(task_id):
    await client.messages.create(...)
    print(f"Hecho {task_id}")

async def main():
    tasks = [worker(i) for i in range(100)]
    await asyncio.gather(*tasks)
```

## Patrón Semáforo
Limita la concurrencia para evitar Límites de Velocidad.

```python
sem = asyncio.Semaphore(10) # Máx 10 peticiones concurrentes

async def worker(task_id):
    async with sem:
        await client.messages.create(...)
```

## Próximos Pasos
- [Monitorización de Respuesta](./13_response_monitoring.md).
