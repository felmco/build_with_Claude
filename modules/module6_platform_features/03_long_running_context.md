# 6.3 Long-Running Context: Budgets, Compaction and Context Editing

## Introduction
Agents that run for dozens of tool calls hit three problems: they can spend more tokens than you intended, their context fills with stale tool output, and they eventually approach the context window. The platform has a feature for each. This lesson covers **task budgets**, **compaction**, **context editing**, and two cache-friendly ways to steer a conversation mid-flight (**mid-conversation system messages** and **per-message effort**). It ends with a table for choosing between them.

## Task Budgets: Pacing the Whole Loop
A task budget tells Claude how many tokens it may spend across an entire agentic loop (thinking, tool calls, tool results and output). The model sees a running countdown and wraps up gracefully as it shrinks.

```python
import anthropic

client = anthropic.Anthropic()

# Beta: task-budgets-2026-03-13. Minimum total is 20,000 tokens (smaller returns a 400).
with client.beta.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=64000,  # hard per-request ceiling, independent of the budget
    betas=["task-budgets-2026-03-13"],
    output_config={
        "effort": "high",
        "task_budget": {"type": "tokens", "total": 64000},
    },
    messages=[{"role": "user", "content": "Review the repo and propose a refactor plan."}],
) as stream:
    response = stream.get_final_message()

print(response.usage)
```

- The budget is **advisory**, not a hard cap. `max_tokens` is still the enforced per-request limit, so use both.
- A budget that is too small for the task can cause refusal-like behavior (declining, scoping down, stopping early). Measure real token use first and size the budget from your own distribution.
- The countdown is only visible to the model. The response has no remaining-budget field.
- If your own code rewrites or compacts history, pass `"remaining"` in `task_budget` so the countdown continues rather than resetting. For loops that resend full history, omit it.
- Changing the value between requests invalidates cached prefixes that contain it. Set it once.
- Not supported on Haiku 4.5 or Sonnet 5.

## Compaction: Server-Side Summaries
Compaction summarizes older turns on the server when input reaches a trigger. The API returns a `compaction` block, and on later requests it ignores everything before that block. **You must append the full `response.content`**, not just the text, or the summary is lost.

```python
messages = []

def chat(user_message: str) -> str:
    messages.append({"role": "user", "content": user_message})

    response = client.beta.messages.create(
        betas=["compact-2026-01-12"],
        model="claude-sonnet-5-5",
        max_tokens=4096,
        messages=messages,
        context_management={
            "edits": [{
                "type": "compact_20260112",
                "trigger": {"type": "input_tokens", "value": 150000},  # default; minimum 50000
                # "instructions": "Keep file paths and open TODOs.",  # replaces the default summary prompt
                # "pause_after_compaction": True,  # stop with stop_reason "compaction" to inspect the summary
            }]
        },
    )

    # Preserve compaction blocks: append blocks, not response.content[0].text
    messages.append({"role": "assistant", "content": response.content})
    return "".join(b.text for b in response.content if b.type == "text")
```

Billing note: top-level `usage` covers only the final message. Sum `usage.iterations` to see the cost of the summarization step too. A newer on-demand compaction variant (beta `compact-2026-09-04`) exists, where you decide when to compact. See the compaction overview for when to prefer it.

## Context Editing: Pruning by Rule
Context editing deletes stale tool results (or thinking blocks) instead of summarizing them. The conversation structure stays, the cleared content is removed.

```python
response = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    betas=["context-management-2025-06-27"],
    tools=tools,  # your tools
    messages=messages,
    context_management={
        "edits": [{
            "type": "clear_tool_uses_20250919",
            "trigger": {"type": "input_tokens", "value": 30000},  # default 100,000
            "keep": {"type": "tool_uses", "value": 3},  # keep the 3 most recent results
            "clear_at_least": {"type": "input_tokens", "value": 5000},  # make each clear worth a cache miss
            "exclude_tools": ["search_docs"],  # never clear these
        }]
    },
)

print(response.context_management.applied_edits)  # what was cleared this turn
```

Clearing tool results invalidates the cached prefix from that point, so use `clear_at_least` to ensure each clear saves enough to be worth it. `clear_thinking_20251015` handles thinking blocks, and when combining both strategies list it first. Pair context editing with the memory tool so Claude can save important results before they are cleared.

## Mid-Conversation System Messages
To change instructions mid-conversation ("switch to terse mode"), append a `role: "system"` message instead of editing top-level `system`. The cached prefix stays intact, and the instruction carries operator authority, so it is harder to spoof than text inside a user turn.

```python
response = client.messages.create(  # no beta header needed
    model="claude-sonnet-5-5",
    max_tokens=2048,
    system=[{"type": "text", "text": "You are a support assistant.",
             "cache_control": {"type": "ephemeral"}}],
    messages=history + [
        {"role": "user", "content": user_message},
        {"role": "system", "content": "Terse mode enabled - keep responses under 40 words."},
    ],
)
```

Rules: it must follow a user message, be last in `messages` or be followed by an assistant turn, and cannot be `messages[0]`. Content is text-only. Supported on Opus 5/5.5, Fable 5/5.1 and Sonnet 5.5 but not Sonnet 5, where it returns a 400, so catch `anthropic.BadRequestError` and fall back to a reminder inside the user turn.

## Per-Message Effort
Changing top-level `effort` between requests invalidates the prompt cache. A `role: "system"` message with empty content and an `output_config` changes effort from that point on without invalidating it. It is a beta (`mid-conversation-output-config-2026-07-01`) and needs thinking enabled.

```python
response = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    betas=["mid-conversation-output-config-2026-07-01"],
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[
        {"role": "user", "content": "Plan the database migration."},
        {"role": "assistant", "content": "Here is the plan: ..."},
        {"role": "system", "content": [], "output_config": {"effort": "low"}},
        {"role": "user", "content": "Now rename the config file."},
    ],
)
```

The new level applies from the next user turn until a later system message changes it. Lowering effort is reliable, and raising works best for big jumps (for example `low` to `xhigh`).

## Choosing Between Them

| Need | Use |
|------|-----|
| Stop an agent from overspending tokens | Task budget (plus `max_tokens` as the hard cap) |
| Keep a very long conversation inside the window | Compaction |
| Drop bulky old tool output but keep the transcript | Context editing |
| Change instructions without breaking the cache | Mid-conversation system message |
| Spend more or less thinking on one step | Per-message effort |
| Remember facts across separate conversations | Memory tool |

### Memory Tool
Compaction and context editing manage *one* conversation. The memory tool (`{"type": "memory_20250818", "name": "memory"}`) is a client-side tool that lets Claude read and write files in a `/memories` directory so knowledge survives across sessions. You implement the storage. The SDK provides a `BetaAbstractMemoryTool` helper. Never store secrets in memory files, and add per-user isolation in multi-user systems.

## Common Pitfalls
- Appending only the text of a compacting response (the summary is lost and context re-grows).
- Treating a task budget as a hard limit, or setting it far below the task's real cost.
- Decrementing `task_budget.remaining` on every request (it breaks caching and makes Claude wrap up early).
- Clearing tool results without `clear_at_least` (repeated cache misses for small savings).
- Putting a mid-conversation system message first in `messages` or after an assistant turn.
- Using per-message effort with thinking disabled, or on a model that does not support it (400).

## Next Steps
- Continue to [Agent Skills and the MCP Connector](./04_skills_and_mcp_connector.md)
- Revisit [Prompt Caching](../module3_advanced_features/05_prompt_caching.md)

## Additional Resources
- [Task Budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets)
- [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)
- [Context Editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)
- [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
