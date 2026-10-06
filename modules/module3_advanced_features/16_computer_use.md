# 3.6 Computer Use

Claude can control a computer desktop (mouse, keyboard, screenshots).

## Prerequisites
- **Docker:** Run the Anthropic reference container (or your own sandboxed VM).
- **No beta header:** `computer_toolset_20260801` is generally available on the Claude API and Google Cloud.

## The Tool Definition

Unlike standard tools, the computer toolset is built into the model and schema-less. It exposes 17 member tools (`screenshot`, `zoom`, `left_click`, `type`, `key`, `scroll`, `wait`, ...).

```python
tools = [
    {"type": "computer_toolset_20260801"},
    # Optional per-member settings:
    # {"type": "computer_toolset_20260801", "configs": {"zoom": {"enabled": False}}},
]
```

> **Migrating?** The older `computer_20251124` tool (with `display_width_px` and a beta header) is deprecated on the Claude 5.5 models and returns a 400 on the Claude API and Google Cloud for Opus 5.5 / Sonnet 5.5. The two cannot be mixed in one request. See the [Computer use docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool).

## How It Works
1. Claude sends a tool use request (e.g., `screenshot`, `left_click`, `type`).
2. Your "Agent Loop" executes this on the VM/Container.
3. You send the result back with `"toolset_name": "computer"` on the `tool_result` (an image block for `screenshot` and `zoom`, text otherwise).

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01...",
  "toolset_name": "computer",
  "content": [{ "type": "text", "text": "OK" }]
}
```

*Note: This requires a specialized, sandboxed environment. See the Reference Implementation, and keep a human in the loop for sensitive actions.*

## Next Steps
- [Computer Automation](./17_computer_automation.md).
