# 4.2 Agent Loops

The "Loop" is the runtime code that keeps the agent running until the task is complete.

## The Loop Algorithm

```python
def run_agent(goal, tools):
    messages = [{"role": "user", "content": goal}]

    while True:
        # 1. Ask Claude
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # 2. Check stop condition
        if response.stop_reason == "end_turn":
            return response.content[0].text

        # 3. Handle Tool Use
        if response.stop_reason == "tool_use":
            tool_use = ... # Get tool block
            result = execute_tool(tool_use)

            # 4. Update History
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": str(result)
                }]
            })
```

## Safeguards
- **Max Loops:** Prevent infinite loops (e.g., `if loop_count > 10: break`).
- **Timeout:** Stop after X seconds.
- **Budget:** Stop after X tokens spent.

## Next Steps
- [Multi-Agent Systems](./07_multi_agent.md).
