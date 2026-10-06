# 6.5 The Claude Agent SDK

In Module 4 you built an agent loop by hand. The **Claude Agent SDK** gives you the loop that powers Claude Code as a library: built-in tools, permissions, hooks, subagents, MCP and sessions, ready to embed in your own Python or TypeScript process.

## Four Ways to Build an Agent

| You want to... | Use | Who runs the loop? |
|---|---|---|
| Call the Claude API and own every step | Messages API (Module 2-4) | You |
| Same, but let the SDK drive the tool loop | Tool Runner (beta): `@beta_tool` + `client.beta.messages.tool_runner(...)` | The client SDK, in your process |
| Embed Claude Code's agent (files, shell, search) in your app | **Agent SDK** | The Claude Code binary, in a process you operate |
| Have Anthropic host the agent in a cloud sandbox | Managed Agents (see [6.6](./06_managed_agents.md)) | Anthropic |

Rule of thumb: pick the Agent SDK when the agent needs a real filesystem and shell on **your** infrastructure and you want Claude Code's behavior without rebuilding it. Pick the Messages API when you need full control of a narrow task.

## Install and Authenticate

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install claude-agent-sdk          # TypeScript: npm install @anthropic-ai/claude-agent-sdk
export ANTHROPIC_API_KEY="..."        # use API-key auth, never hard-code the key
```

Anthropic does not allow third-party products to offer claude.ai login for agents built on the SDK. Use API-key authentication.

## query(): One Task, Streamed Messages

`query()` is an async generator. You pass a prompt and `ClaudeAgentOptions`, and iterate over messages as the agent works.

```python
import asyncio
from claude_agent_sdk import (
    query, ClaudeAgentOptions, AssistantMessage, ResultMessage, TextBlock,
)

async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep"],  # pre-approved, read-only
        max_turns=10,                            # hard stop on the loop
        max_budget_usd=0.50,                     # hard stop on spend
        cwd=".",
    )
    async for message in query(prompt="Summarize what this repo does", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            # Final message: status, cost, usage, session id
            print(message.subtype, message.num_turns, message.total_cost_usd)
            print("session:", message.session_id)

asyncio.run(main())
```

`ResultMessage.total_cost_usd` and `ResultMessage.usage` give per-run accounting (see [6.7](./07_admin_usage_and_cost.md)).

## Built-in Tools

The agent ships with the same tools as Claude Code: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `WebFetch`, and more. You do not write the tool loop or the executors. `allowed_tools` lists tools that run without asking; `disallowed_tools` removes them.

## Permissions

`permission_mode` sets the baseline:

| Mode | Behavior |
|---|---|
| `"default"` | Standard permission behavior |
| `"acceptEdits"` | Auto-accept file edits |
| `"plan"` | Explore without editing |
| `"dontAsk"` | Deny anything not pre-approved (good for unattended jobs) |
| `"auto"` | A model classifier reviews actions |
| `"bypassPermissions"` | No checks: only inside a throwaway sandbox |

For unattended runs combine a narrow `allowed_tools` with `permission_mode="dontAsk"`.

## Hooks

Hooks are Python callbacks that run at lifecycle points. Python supports `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `UserPromptSubmit`, `Stop`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PermissionRequest` and `Notification`. A matcher filters by tool name. Returning `{}` allows; a `deny` decision blocks.

```python
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

async def protect_env_files(input_data, tool_use_id, context):
    file_path = input_data["tool_input"].get("file_path", "")
    if file_path.split("/")[-1] == ".env":
        return {
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "deny",
                "permissionDecisionReason": "Cannot modify .env files",
            }
        }
    return {}  # empty dict = allow

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="Write|Edit", hooks=[protect_env_files])]}
)
```

Matchers match tool names only, not paths: check `tool_input` inside the callback. `SessionStart` and `SessionEnd` are TypeScript-only callbacks.

## Subagents

Define specialists with `AgentDefinition`. The main agent delegates to them and only their report returns to its context.

```python
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Agent"],  # the parent needs the Agent tool to delegate
    agents={
        "code-reviewer": AgentDefinition(
            description="Reviews code changes for bugs. Use after edits.",
            prompt="You are a code reviewer. Report concrete issues with file and line.",
            tools=["Read", "Grep"],   # least privilege
            maxTurns=5,
        )
    },
)
```

Claude invokes subagents through the `Agent` tool. Older SDK versions named it `Task`, so match both when detecting delegation in `tool_use` blocks. Subagent output counts toward the query's `total_cost_usd`; `max_budget_usd` caps it.

## Custom Tools and MCP

Add your own tools in-process with `@tool` and `create_sdk_mcp_server`, or connect external servers through `mcp_servers`. MCP tools are named `mcp__<server>__<tool>`.

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions

@tool("add", "Add two numbers", {"a": float, "b": float})
async def add(args):
    return {"content": [{"type": "text", "text": f"Sum: {args['a'] + args['b']}"}]}

calculator = create_sdk_mcp_server(name="calculator", version="1.0.0", tools=[add])

options = ClaudeAgentOptions(
    mcp_servers={"calc": calculator},
    allowed_tools=["mcp__calc__add"],
)
```

## Sessions: Continue, Resume, Fork

A session is the conversation history, saved to disk automatically. For multi-turn chat in one process use `ClaudeSDKClient`; to come back later, capture `session_id` and pass `resume`.

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, query, ResultMessage

async def chat():
    async with ClaudeSDKClient(options=ClaudeAgentOptions(allowed_tools=["Read", "Grep"])) as client:
        await client.query("Analyze the auth module")
        async for message in client.receive_response():
            pass  # handle messages
        await client.query("Now list the risks you found")   # same session, full context
        async for message in client.receive_response():
            print(message)

async def resume_later(session_id: str):
    options = ClaudeAgentOptions(resume=session_id)          # fork_session=True to branch instead
    async for message in query(prompt="Implement your suggestions", options=options):
        if isinstance(message, ResultMessage):
            print(message.subtype)
```

Sessions persist the conversation, not the filesystem. Resuming works on the same machine unless you add a session store adapter.

## Common Pitfalls

- **Treating it like the Messages API.** The SDK launches the Claude Code binary; it needs a runtime where that can run, and it acts on a real filesystem.
- **`bypassPermissions` outside a sandbox.** Use `dontAsk` plus a tight `allowed_tools` list.
- **No limits.** Always set `max_turns` and `max_budget_usd` for unattended runs.
- **Hooks that raise or block on slow I/O.** Catch errors inside the hook and run blocking calls in a thread.
- **Expecting `SessionStart` hooks in Python.** They are TypeScript-only callbacks.
- **Assuming a stored transcript moves between hosts.** Use a session store or pass results as state.

## Next Steps
- Compare with the hosted option in [Managed Agents](./06_managed_agents.md).
- Track what runs cost in [Admin API, Usage and Cost](./07_admin_usage_and_cost.md).

## Additional Resources
- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Python SDK reference](https://code.claude.com/docs/en/agent-sdk/python)
- [Hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions)
- [Permissions](https://code.claude.com/docs/en/agent-sdk/permissions)
- [Subagents](https://code.claude.com/docs/en/agent-sdk/subagents)
- [MCP in the SDK](https://code.claude.com/docs/en/agent-sdk/mcp)
