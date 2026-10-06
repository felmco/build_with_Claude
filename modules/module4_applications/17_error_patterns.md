# 4.5 Production Error Patterns

In production, you must handle more than just exceptions.

## 1. The "Refusal" Loop
Claude refuses a request ("I cannot help with that").
- **Detect:** Check `response.stop_reason == "refusal"` before reading `response.content`; `response.stop_details` explains the refusal. Do not rely on keyword matching.
- **Fix:** Adjust the system prompt or fall back to a human.

## 2. The "Hallucination" Check
- **Pattern:** Use a second, smaller model to verify the output of the first model.
- **Prompt:** "Does this response contradict the context provided?"

## 3. The "Output Parsing" Fail
- **Pattern:** Claude returns invalid JSON.
- **Better:** Use structured outputs (`output_config={"format": {...}}`, or `client.messages.parse`) so the response matches your JSON schema.
- **Fallback:** Use a retry loop (max 3 tries) passing the error message back to Claude. "You returned invalid JSON here: [Error]. Please fix."

## 4. API Errors
Catch `anthropic.RateLimitError`, `anthropic.APIConnectionError` and `anthropic.APIStatusError` (most specific first). The SDK already retries transient errors (`max_retries=2` by default), so add your own retries only on top of that.

## Next Steps
- [Rate Limiting Strategies](./18_rate_limiting.md).
