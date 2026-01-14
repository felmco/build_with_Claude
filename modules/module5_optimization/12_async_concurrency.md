# 5.3 Async and Concurrency

To scale high-throughput apps, you must use AsyncIO.

## Python Async Client

```python
from anthropic import AsyncAnthropic
import asyncio

client = AsyncAnthropic()

async def worker(task_id):
    await client.messages.create(...)
    print(f"Done {task_id}")

async def main():
    tasks = [worker(i) for i in range(100)]
    await asyncio.gather(*tasks)
```

## Semaphore Pattern
Limit concurrency to avoid Rate Limits.

```python
sem = asyncio.Semaphore(10) # Max 10 concurrent requests

async def worker(task_id):
    async with sem:
        await client.messages.create(...)
```

## Next Steps
- [Response Monitoring](./13_response_monitoring.md).
