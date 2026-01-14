# 3.2 Cost Reduction Techniques

## 1. Prompt Caching
As discussed, this provides a ~90% discount on input tokens. Use it for:
- Large Contexts (Books, Codebases).
- Frequent System Prompts.
- Few-shot examples (10+ examples).

## 2. Model Selection
- Use **Haiku** for simple tasks.
- Use **Sonnet** for general intelligence.
- Use **Opus** only when reasoning depth requires it.

## 3. Token Truncation
- Don't send the entire conversation history if it's not needed.
- Summarize old turns.

## 4. Batch Processing
The **Message Batches API** (see next lesson) offers a **50% discount** on all tokens if you can wait up to 24 hours (usually much faster).

| Feature | Discount | Speed |
|---------|----------|-------|
| Prompt Caching | ~90% (Input) | Fast |
| Batch API | 50% (Total) | Slow (Async) |

## Next Steps
- Learn about [Batch Processing](./08_batch_processing.md).
