# 5.2 Token Optimization

Reducing tokens = Reducing Cost + Improving Latency.

## Techniques

1. **Be Concise:** Ask Claude to "Be concise" in the system prompt.
2. **Remove Fluff:** Strip unnecessary HTML, JSON keys, or verbose text from input data.
3. **Limit Output:** Use `max_tokens`.
4. **Stop Sequences:** Stop generation early.

## Measure, don't guess
Count tokens with the API (never a third-party tokenizer such as tiktoken, which does not match Claude's tokenizer):

```python
import anthropic

client = anthropic.Anthropic()
count = client.messages.count_tokens(
    model="claude-sonnet-5-5",
    messages=[{"role": "user", "content": document_text}],
)
print(count.input_tokens)
```

Newer models use a newer tokenizer that can produce roughly 1x to 1.35x more tokens for the same text than older ones, so re-measure after a model change.

## Input Sanitization
Stripping markup, boilerplate and repeated whitespace from large inputs can save a meaningful share of tokens. Check the saving with `count_tokens` before and after; for ordinary prose the gain is small, and renaming variables in code rarely helps and hurts readability.

## Bigger levers
Prompt caching (10% or less of the normal input price for cached reads), batching (50% off) and `effort` usually save far more than trimming words.

## Next Steps
- [Model Selection Strategy](./07_model_selection.md).
