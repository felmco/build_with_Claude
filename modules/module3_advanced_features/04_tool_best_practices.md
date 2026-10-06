# 3.1 Tool Use Best Practices

## 1. Clear Descriptions are Key
Claude chooses tools based on their `description`.
- ❌ "Calculate stuff"
- ✅ "Calculates the square root of a number. Returns an error for negative inputs."

## 2. Use Enums for Strict Inputs
If a parameter has a fixed set of valid values, use `enum` in the schema. This constrains Claude to valid options. Add `"strict": true` to the tool definition to guarantee that inputs match the schema exactly, and still validate inputs in your code.

```json
"unit": {
    "type": "string",
    "enum": ["celsius", "fahrenheit"]
}
```

## 3. Handle Errors Gracefully
If a tool fails (e.g., API down, invalid ID), return a **Tool Result** with the error message, rather than crashing.

**Return to Claude:**
```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01...",
  "is_error": true,
  "content": "Error: User ID 123 not found."
}
```
Claude can often self-correct (e.g., "Oh, I apologize. Let me search by name instead.").

## 4. Keep Tool Output Concise
Claude has to read the tool output. If your tool returns a 5MB JSON dump, it burns tokens and context.
- **Filter** data before returning it.
- **Summarize** large text files.

## 5. Security (Prompt Injection)
Be careful with tools that execute code or SQL.
- **Sandbox** execution environments.
- **Read-only** database access where possible.
- **Treat inputs and outputs as untrusted.** Never pass model-written text to `eval`, `exec`, or a shell, and use parameterized SQL. Tool results (web pages, documents) can contain injected instructions.
- **Human-in-the-loop** for sensitive actions (sending emails, deleting files).

## Next Steps
- Optimize costs with [Prompt Caching](./05_prompt_caching.md).
