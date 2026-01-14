# 3.6 Computer Automation Strategies

## The Agent Loop

```python
while True:
    response = client.beta.messages.create(...)

    if response.stop_reason == "tool_use":
        # Execute action (click, type, screenshot)
        # Send result
    else:
        # Task done
        break
```

## Best Practices
1. **Screen Resolution:** Lower is cheaper/faster (e.g., 1024x768).
2. **Screenshots:** Send a screenshot *after* every action so Claude sees the result.
3. **Safety:** Run in a sandboxed container. Do not give it access to your personal banking!

## Limitations
- **Latency:** It's slow (screenshot -> upload -> process -> respond -> action).
- **Video:** No real-time video stream yet.

## Congratulations!
You have completed Module 3. You are now an advanced user of the Claude API.

## Next Module
Proceed to [Module 4: Building Applications](../module4_applications/README.md) to put it all together.
