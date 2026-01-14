# 5.2 Token Optimization

Reducing tokens = Reducing Cost + Improving Latency.

## Techniques

1. **Be Concise:** Ask Claude to "Be concise" in the system prompt.
2. **Remove Fluff:** Strip unnecessary HTML, JSON keys, or verbose text from input data.
3. **Limit Output:** Use `max_tokens`.
4. **Stop Sequences:** Stop generation early.

## Input Sanitization
Removing whitespaces or using shorter variable names in code snippets can save hundreds of tokens in large contexts.

## Next Steps
- [Model Selection Strategy](./07_model_selection.md).
