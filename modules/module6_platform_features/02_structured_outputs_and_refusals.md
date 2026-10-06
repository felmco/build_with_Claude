# 6.2 Structured Outputs, Stop Reasons and Refusal Fallbacks

## Introduction
Production code needs two guarantees: the output has the shape your program expects, and your program knows *why* generation stopped. Structured outputs give you the first. Checking `stop_reason` gives you the second, including the `refusal` case that current models can return when a safety classifier declines a request. This lesson also shows the server-side fallback that retries a refused request on another model.

## Structured Outputs
Structured outputs constrain Claude's response to a JSON Schema. Because Claude 5.x models reject assistant prefill (a 400), this is the supported way to force a JSON shape.

### With Pydantic: `client.messages.parse`
```python
import anthropic
from pydantic import BaseModel

client = anthropic.Anthropic()

class ContactInfo(BaseModel):
    name: str
    email: str
    plan: str
    demo_requested: bool

response = client.messages.parse(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Extract: Jane Doe (jane@co.com) wants Enterprise and asked for a demo.",
    }],
    output_format=ContactInfo,  # SDK helper: converts the model to a schema and validates the reply
)

# Always check why generation stopped before trusting the parsed object
if response.stop_reason == "end_turn":
    contact = response.parsed_output  # a validated ContactInfo instance
    print(contact.name, contact.demo_requested)
```

`output_format` is a convenience accepted by `.parse()`. The API-level parameter is `output_config.format`, shown next.

### Raw schema: `output_config.format`
```python
import json

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Extract: John Smith (john@example.com) wants Enterprise."}],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "plan": {"type": "string"},
                },
                "required": ["name", "email", "plan"],
                "additionalProperties": False,  # required on every object
            },
        }
    },
)

if response.stop_reason == "end_turn":
    text = next(b.text for b in response.content if b.type == "text")
    data = json.loads(text)
```

Schema limits: no recursive schemas, no numeric constraints (`minimum`, `maximum`) and no string length constraints. The Python SDK strips unsupported constraints from the schema it sends and validates them client-side. The first request with a new schema pays a one-time compile cost, and structured outputs cannot be combined with citations (400). String `enum` values may come back with different capitalization, so compare case-insensitively.

### Strict tool use
Add `"strict": True` to a tool to guarantee `input` matches its schema. It also replaces forced `tool_choice` on current models: `{"type": "any"}` and `{"type": "tool", ...}` return a 400 on Fable 5.1, Opus 5.5 and Sonnet 5.5, so keep `auto`, instruct Claude to use the tool, and check for a `tool_use` block.

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    tools=[{
        "name": "book_flight",
        "description": "Book a flight to a destination",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "date": {"type": "string", "format": "date"},
                "passengers": {"type": "integer"},
            },
            "required": ["destination", "date", "passengers"],
            "additionalProperties": False,
        },
    }],
    messages=[{"role": "user", "content": "Use the book_flight tool: Tokyo, 2 passengers, March 15."}],
)
calls = [b for b in response.content if b.type == "tool_use"]
if not calls:
    ...  # auto does not guarantee a call: re-prompt or handle the text reply
```

## Always Check `stop_reason`

| `stop_reason` | Meaning | What to do |
|---------------|---------|------------|
| `end_turn` | Finished naturally | Use the output |
| `max_tokens` | Hit your `max_tokens` | Output may be cut off and invalid JSON. Raise `max_tokens` or stream |
| `tool_use` | Claude wants a client tool run | Execute and reply with `tool_result` |
| `pause_turn` | Server-tool turn paused | Re-send to resume (see 6.1) |
| `refusal` | A classifier or the model declined | Do not read `content` as a normal answer |

```python
def handle(response):
    if response.stop_reason == "refusal":
        # A refusal is HTTP 200, not an exception. Content is empty or partial.
        details = response.stop_details  # only present on refusals
        category = details.category if details else None  # e.g. "cyber", "bio", or None
        raise RuntimeError(f"Request declined (category={category})")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("Output truncated: increase max_tokens")
    return next(b.text for b in response.content if b.type == "text")
```

Branch on `stop_reason`, never on `stop_details`: it is informational and `category` can be `None`. With structured outputs a refusal takes precedence over the schema, so the output may not match it. Refusals still count against rate limits even if no output was produced. Asking a model to reproduce its internal reasoning in the reply can trigger a `reasoning_extraction` refusal. Use thinking `display: "summarized"` instead.

## Server-Side Refusal Fallbacks
Classifier refusals can hit benign requests (security tooling and life-science work are common cases). Without a fallback, a refused request just stops. With the beta `fallbacks` parameter, the API re-runs the declined request on another model inside the same call:

```python
response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    betas=["server-side-fallback-2026-07-01"],
    fallbacks="default",  # Anthropic picks the recommended fallback for the refusal category
    messages=[{"role": "user", "content": "Review this nginx config for hardening issues: ..."}],
)

print("served by:", response.model)
if response.stop_reason == "refusal":
    # The whole chain refused. recommended_model, when set, is a hint for a direct retry.
    print(response.stop_details)
```

Key facts:
- Header and form go together. `fallbacks: "default"` needs `server-side-fallback-2026-07-01`. The older array form `fallbacks=[{"model": "..."}]` needs `server-side-fallback-2026-06-01`. Mixing them returns a 400.
- It triggers only on policy declines, not on rate limits, overloads or server errors.
- A mid-stream decline is billed at normal rates, and the rescue is billed at the fallback model's own rates. Check `usage.iterations` for the per-attempt breakdown.
- Once a conversation falls back, later requests with `fallbacks` can be served by the fallback model directly for about an hour.
- Available on the Claude API and Claude Platform on AWS. Rejected on the Batches API and unavailable on Bedrock, Vertex AI and Foundry, where you use the SDK's client-side `BetaRefusalFallbackMiddleware` or your own retry.
- `reasoning_extraction` declines are not retried on a fallback model.

## Common Pitfalls
- Reading `response.content[0].text` without checking `stop_reason` (a refusal has empty or partial content).
- Treating `max_tokens` output as valid JSON. Truncated JSON fails to parse.
- Branching on `stop_details.category`, which can be `None`.
- Using prefill or forced `tool_choice` to get JSON. Both return a 400 on current models.
- Forgetting `additionalProperties: False` on schema objects and strict tool schemas.
- Combining the `fallbacks` array form with the `2026-07-01` header (or the reverse).
- Sending `fallbacks` through the Batches API or to Bedrock, Vertex or Foundry.

## Next Steps
- Continue to [Long-Running Context Management](./03_long_running_context.md)
- Review [Server Tools](./01_server_tools.md) for `pause_turn`

## Additional Resources
- [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Refusals and Fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)
- [Handling Stop Reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
- [Strict Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)
