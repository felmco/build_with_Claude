# 4.5 Production Error Patterns

In production, you must handle more than just exceptions.

## 1. The "Refusal" Loop
Claude refuses a request ("I cannot help with that").
- **Fix:** Adjust System Prompt. Detect refusal keywords and fallback to a human.

## 2. The "Hallucination" Check
- **Pattern:** Use a second, smaller model to verify the output of the first model.
- **Prompt:** "Does this response contradicts the context provided?"

## 3. The "Output Parsing" Fail
- **Pattern:** Claude returns invalid JSON.
- **Fix:** Use a retry loop (max 3 tries) passing the error message back to Claude. "You returned invalid JSON here: [Error]. Please fix."

## Next Steps
- [Rate Limiting Strategies](./18_rate_limiting.md).
