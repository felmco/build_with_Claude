# 4.2 Agent Loops

The "Loop" is the runtime code that keeps the agent running until the task is complete.

## The Loop Algorithm

```python
import anthropic

client = anthropic.Anthropic()

def run_agent(goal, tools, max_loops=10):
    messages = [{"role": "user", "content": goal}]

    for _ in range(max_loops):
        # 1. Ask Claude
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )

        # 2. Check stop condition
        if response.stop_reason == "tool_use":
            # 3. Run EVERY tool_use block (Claude may call several in parallel)
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    try:
                        result = execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result),
                        })
                    except Exception as e:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"Error: {e}",
                            "is_error": True,
                        })

            # 4. Update history: echo the assistant turn, then ALL results
            #    in a single user message
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        elif response.stop_reason == "max_tokens":
            raise RuntimeError("Response truncated; raise max_tokens")
        elif response.stop_reason == "refusal":
            raise RuntimeError("Claude declined the request")
        else:  # "end_turn" (or "pause_turn": resend to continue)
            return "".join(b.text for b in response.content if b.type == "text")

    raise RuntimeError("Agent exceeded max_loops")
```

`execute_tool(name, input)` is your own dispatcher. Return all `tool_result` blocks for one assistant turn together in one user message, and put them first in the content list.

## Safeguards
- **Max Loops:** Prevent infinite loops (the `max_loops` argument above).
- **Timeout:** Stop after X seconds.
- **Budget:** Stop after X tokens spent.

## Next Steps
- [Multi-Agent Systems](./07_multi_agent.md).
