# 3.1 Multi-Tool Orchestration

Claude can choose from multiple tools in a single turn, or use tools sequentially.

## Providing Multiple Tools

Just add them to the `tools` list.

```python
tools = [weather_tool, stock_tool, calculator_tool]

response = client.messages.create(
    ...,
    tools=tools,
    messages=[{"role": "user", "content": "What is the stock price of Apple + Google?"}]
)
```

## Parallel Tool Use

Claude might try to call multiple tools at once (e.g., getting stock price for AAPL and GOOGL simultaneously).

The API returns a list of `content` blocks. You might see multiple `tool_use` blocks.

**Handling Loop:**
1. Iterate through `response.content`.
2. Collect all `tool_use` blocks.
3. Execute them (sequentially or in parallel using `asyncio`).
4. Append *all* `tool_result` blocks to the next user message.

```python
tool_results = []
for block in response.content:
    if block.type == "tool_use":
        result = execute(block)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": str(result)
        })

# Send back all results
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": tool_results})
```

## Sequential Orchestration (Chaining)

Sometimes tool B needs the output of tool A.
- Claude handles this automatically!
- It calls Tool A.
- You return result.
- Claude sees result, then calls Tool B.

## Next Steps
- Review [Tool Best Practices](./04_tool_best_practices.md).
