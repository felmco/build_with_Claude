# 3.6 Computer Use (Beta)

Claude can control a computer desktop (mouse, keyboard, screenshots).

## Prerequisites
- **Docker:** Run the Anthropic reference container.
- **Beta Header:** `computer-use-2025-01-24` (or latest).

## The Tool Definition

Unlike standard tools, "computer" is a built-in tool type.

```python
tools = [
    {
        "type": "computer_20250124",
        "name": "computer",
        "display_width_px": 1024,
        "display_height_px": 768,
        "display_number": 1
    }
]
```

## How It Works
1. Claude sends a tool use request (e.g., `screenshot`, `mouse_move`, `type`).
2. Your "Agent Loop" executes this on the VM/Container.
3. You send the result (image or status) back to Claude.

*Note: This requires a specialized environment. See the Reference Implementation.*

## Next Steps
- [Computer Automation](./17_computer_automation.md).
