# 5.3 Latency Optimization

## The TTFT vs Total Time
- **TTFT (Time To First Token):** How fast the user sees *something*. Important for UI.
- **Total Time:** How long until the request finishes.

## Optimizing TTFT
1. **Reduce Input:** Shorter prompts process faster.
2. **Cache:** Processed cache hits are much faster.
3. **Model:** Haiku has much lower TTFT than Opus.

## Optimizing Total Time
1. **Reduce Output:** Ask for shorter answers.
2. **Parallelize:** Run independent sub-tasks in parallel.

## Next Steps
- [Streaming for Better UX](./11_streaming_ux.md).
