# 5.3 Async y Concurrencia

Para escalar aplicaciones de alto rendimiento, debes usar AsyncIO.

## Cliente Asíncrono de Python

```python
from anthropic import AsyncAnthropic
import asyncio

client = AsyncAnthropic()

async def worker(task_id):
    response = await client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        messages=[{"role": "user", "content": f"Task {task_id}: say hello"}],
    )
    print(f"Hecho {task_id}")
    return response.content[0].text

async def main():
    tasks = [worker(i) for i in range(100)]
    return await asyncio.gather(*tasks)

asyncio.run(main())
```

Cada `client.messages.create(...)` en `AsyncAnthropic` devuelve una corrutina, así que debe esperarse con `await`.

## Patrón Semáforo
Limita la concurrencia para evitar Límites de Velocidad. El SDK ya reintenta las respuestas 429 y 5xx (`max_retries=2` por defecto), pero un semáforo evita que llegues al límite desde el principio.

```python
sem = asyncio.Semaphore(10)  # Max 10 concurrent requests

async def worker(task_id):
    async with sem:
        response = await client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=256,
            messages=[{"role": "user", "content": f"Task {task_id}: say hello"}],
        )
        return response.content[0].text
```

Para trabajos offline muy grandes, la API de Batches es más barata que cualquier cantidad de concurrencia.

## Próximos Pasos
- [Monitorización de Respuesta](13_monitoreo_respuestas.md).
