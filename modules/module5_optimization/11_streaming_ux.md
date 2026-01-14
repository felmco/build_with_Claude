# 5.3 Streaming for Better UX

We covered streaming basics in Module 2. In optimization, we focus on the **Frontend Experience**.

## Smoothing
Raw tokens arrive at irregular intervals. "Jitter" looks bad.
- **Technique:** Buffer incoming tokens for 50ms and display them at a constant character-per-second rate.

## Parsing while Streaming
If you request JSON, don't wait for the full response to parse.
- **Incremental Parsing:** Use a library that can parse partial JSON strings to show UI elements (like lists) as they generate.

## Next Steps
- [Async and Concurrency](./12_async_concurrency.md).
