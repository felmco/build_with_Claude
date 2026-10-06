# 5.3 Async and Concurrency

To scale high-throughput apps, you must use AsyncIO.

## Python Async Client

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
    print(f"Done {task_id}")
    return response.content[0].text

async def main():
    tasks = [worker(i) for i in range(100)]
    return await asyncio.gather(*tasks)

asyncio.run(main())
```

Every `client.messages.create(...)` on `AsyncAnthropic` returns a coroutine, so it must be awaited.

## Semaphore Pattern
Limit concurrency to avoid Rate Limits. The SDK already retries 429 and 5xx responses (`max_retries=2` by default), but a semaphore keeps you from hitting the limit in the first place.

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

For very large offline jobs, the Batches API is cheaper than any amount of concurrency.

## Next Steps
- [Response Monitoring](./13_response_monitoring.md).
