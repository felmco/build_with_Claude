# 3.2 Cost Reduction Techniques

## 1. Prompt Caching
As discussed, cache reads cost about 10% of the base input price (5% on Opus 5.5, 2.5% on Fable 5.1), while writes cost 1.25x. Use it for:
- Large Contexts (Books, Codebases).
- Frequent System Prompts.
- Few-shot examples (10+ examples).

## 2. Model Selection
- Use **Haiku 4.5** for simple, high-volume tasks.
- Use **Sonnet 5.5** for general intelligence.
- Use **Opus 5.5** or **Fable 5.1** only when reasoning depth requires it.
- Set the `effort` parameter lower for simple requests; thinking tokens are billed as output.

Check current model IDs and prices on the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview).

## 3. Token Truncation
- Don't send the entire conversation history if it's not needed.
- Summarize old turns.
- Count tokens before sending with `client.messages.count_tokens(...)` instead of guessing.

## 4. Batch Processing
The **Message Batches API** (see next lesson) offers a **50% discount** on all tokens if you can wait up to 24 hours (usually much faster).

| Feature | Discount | Speed |
|---------|----------|-------|
| Prompt Caching | ~90% off cached input reads | Faster |
| Batch API | 50% (input and output) | Async, up to 24 hours |

The two can be combined, but cache hits inside a batch are best-effort because batch requests may run in any order.

## Next Steps
- Learn about [Batch Processing](./08_batch_processing.md).
