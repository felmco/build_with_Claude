# 3.6 Computer Automation Strategies

## The Agent Loop

```python
tools = [{"type": "computer_toolset_20260801"}]
messages = [{"role": "user", "content": "Open the settings page and enable dark mode"}]

MAX_STEPS = 50  # always cap the loop

for _ in range(MAX_STEPS):
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=4096,
        tools=tools,
        messages=messages,
    )
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason != "tool_use":
        break  # task done (or stopped for another reason)

    results = []
    for block in response.content:
        if block.type != "tool_use":
            continue
        # The action is the block's name (screenshot, left_click, type, ...)
        output = execute_on_vm(block.name, block.input)  # your sandbox code
        content = (
            [{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": output}}]
            if block.name in ("screenshot", "zoom")
            else [{"type": "text", "text": "OK"}]
        )
        results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "toolset_name": "computer",  # required on every result
            "content": content,
        })

    # Return one tool_result per tool_use, all in a single user message
    messages.append({"role": "user", "content": results})
```

`execute_on_vm` is your own code that performs the action in the sandbox (and, for `screenshot` and `zoom`, returns a base64 PNG). Claude may request several actions in one turn, so handle every `tool_use` block.

## Best Practices
1. **Screen Resolution:** Lower is cheaper/faster (e.g., 1024x768 to 1080p). Screenshots you return must already fit the model's image limits; the API rejects oversized `tool_result` images instead of downscaling them, so resize them yourself.
2. **Screenshots:** Claude requests a `screenshot` when it needs to see the screen; return the image for `screenshot` and `zoom` calls and a short text result for other actions. Keep screenshots small, since they accumulate in the conversation.
3. **Safety:** Run in a sandboxed container with minimal privileges. Do not give it access to your personal banking! Web pages and documents on screen can contain prompt injection, so keep a human in the loop for sensitive actions.

## Limitations
- **Latency:** It's slow (screenshot -> upload -> process -> respond -> action).
- **Video:** No real-time video stream; Claude works from discrete screenshots.

## Congratulations!
You have completed Module 3. You are now an advanced user of the Claude API.

## Next Module
Proceed to [Module 4: Building Applications](../module4_applications/README.md) to put it all together.
