# 6.6 Managed Agents (Beta)

Managed Agents is a hosted agent harness. You define a persistent **agent** (model, system prompt, tools), an **environment** (a cloud container template), and then start **sessions**. The agent loop runs on Anthropic's orchestration layer; the container is where its tools (bash, files, code) execute. You send events in and stream events out.

## When to Choose It

| Situation | Better fit |
|---|---|
| Short request/response, a few tools you control | Messages API loop ([4.3](../module4_applications/06_agent_loops.md)) |
| Agent needs files and a shell on your own machines | [Agent SDK](./05_agent_sdk.md) |
| Long-running, multi-step work in a sandbox you do not want to operate; scheduled runs; graded deliverables | **Managed Agents** |

You trade control of the loop for not having to host it: no container fleet, no loop code, built-in compaction and prompt caching.

## The Flow: Agent (once) -> Environment -> Session (every run)

Managed Agents is in beta. The SDK sets the `managed-agents-2026-04-01` beta header for you on `client.beta.{agents,environments,sessions,vaults,deployments}.*` calls. Do not add it by hand.

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

# 1. Environment: the container template (setup step, not the hot path)
environment = client.beta.environments.create(
    name="my-dev-env",
    config={
        "type": "cloud",
        "networking": {"type": "limited", "allow_package_managers": True, "allow_mcp_servers": True},
    },
)

# 2. Agent: persistent and versioned. Create ONCE, store agent.id and agent.version.
agent = client.beta.agents.create(
    name="Coding Assistant",
    model="claude-opus-5-5",
    tools=[
        {
            "type": "agent_toolset_20260401",
            "default_config": {"enabled": True, "permission_policy": {"type": "auto"}},
            "configs": [
                {"name": "web_fetch", "enabled": False},   # web off unless the job needs it
                {"name": "web_search", "enabled": False},
            ],
        },
    ],
)

# 3. Session: a pointer to the agent. model/system/tools live on the AGENT, never here.
session = client.beta.sessions.create(
    agent={"type": "agent", "id": agent.id, "version": agent.version},
    environment_id=environment.id,
)
print(session.id, session.status)
```

Updating an agent creates a new immutable version; running sessions keep the version they pinned. Do not call `agents.create()` on every request.

## Events: Send and Stream

Open the stream first, then send, so you do not miss early events.

```python
with client.beta.sessions.events.stream(session_id=session.id) as stream:
    client.beta.sessions.events.send(
        session_id=session.id,
        events=[{"type": "user.message", "content": [{"type": "text", "text": "Review the auth module"}]}],
    )
    for event in stream:
        if event.type == "agent.message":
            for block in event.content:
                if block.type == "text":
                    print(block.text, end="", flush=True)
        elif event.type == "session.status_idle":
            if event.stop_reason.type != "requires_action":  # requires_action: waiting on you
                break
        elif event.type == "session.status_terminated":
            break
```

If the stream drops while a tool call awaits your answer, the session stalls. On reconnect, list events (`client.beta.sessions.events.list(session_id=...)`), de-duplicate by event ID, then resume streaming.

## Custom Tools

Declare a `{"type": "custom", ...}` tool on the agent. When the agent calls it you get an `agent.custom_tool_use` event and answer with `user.custom_tool_result`:

```python
client.beta.sessions.events.send(
    session_id=session.id,
    events=[{
        "type": "user.custom_tool_result",
        "custom_tool_use_id": event.id,           # id of the agent.custom_tool_use event
        "content": [{"type": "text", "text": "All 42 tests passed."}],
    }],
)
```

## Permission Policies

Set a `permission_policy` on the toolset `default_config` or on one tool in `configs`:

| Policy | Behavior |
|---|---|
| `always_allow` | Runs automatically (default for the agent toolset) |
| `always_ask` | Pauses with `requires_action` until you send `user.tool_confirmation` (default for MCP toolsets) |
| `auto` | The server decides per call: run, deny, or pause for you |

`auto` is not a human checkpoint: a call it judges safe runs before anyone looks. Put `always_ask` on tools a person must review, and answer paused calls with `deny` when nobody is watching.

```python
for event in stream:  # inside the stream loop from above
    if (event.type == "agent.tool_use" or event.type == "agent.mcp_tool_use") and event.evaluated_permission == "ask":
        client.beta.sessions.events.send(
            session_id=session.id,
            events=[{
                "type": "user.tool_confirmation",
                "tool_use_id": event.id,              # the event ID (sevt_...), not a toolu_ ID
                "result": "allow" if approve(event) else "deny",   # approve() is your own policy
            }],
        )
```

## Vault Credentials

The agent's `mcp_servers` entry holds only `{type, name, url}`. Secrets live in a **vault** attached to the session at creation (`vault_ids` cannot be added later). MCP OAuth credentials auto-refresh; `environment_variable` credentials are substituted at egress, so the sandbox only sees a placeholder.

```python
agent = client.beta.agents.create(
    name="MCP Agent",
    model="claude-opus-5-5",
    mcp_servers=[{"type": "url", "name": "my-tools", "url": "https://my-mcp-server.example.com/sse"}],
    tools=[
        {"type": "agent_toolset_20260401",
         "default_config": {"enabled": True, "permission_policy": {"type": "auto"}}},
        {"type": "mcp_toolset", "mcp_server_name": "my-tools"},
    ],
)

session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    vault_ids=[vault.id],   # vault created with client.beta.vaults.create(...) + credentials.create(...)
)
```

Credential shapes (`mcp_oauth`, `static_bearer`, `environment_variable`) are in the vaults section of the managed-agents tools docs. Keep credentials minimal in scope and never put them in memory stores or prompts.

## Outcomes: Grade Against a Rubric

For work with a checkable deliverable, start with `user.define_outcome` instead of `user.message` (never both). A separate grader scores each iteration against your rubric and the agent revises until it passes or hits `max_iterations`.

```python
RUBRIC = """# Report rubric (starter, tune the criteria)
- Output is a single report.md in /mnt/session/outputs/
- Every claim cites a source URL
- Includes a summary table with one row per competitor
- No placeholder text, TODOs, or empty sections remain
"""

client.beta.sessions.events.send(
    session_id=session.id,
    events=[{
        "type": "user.define_outcome",
        "description": "Write a competitor-pricing report as report.md",
        "rubric": {"type": "text", "content": RUBRIC},
        "max_iterations": 5,   # optional; default 3, max 20
    }],
)
```

The stream carries `span.outcome_evaluation_end` events with a `result` of `satisfied`, `needs_revision`, `max_iterations_reached`, `failed` or `interrupted`. Write explicit, independently gradeable criteria; vague ones make noisy loops. The example needs `web_search` and `web_fetch` enabled on the agent.

## Scheduled Deployments

A deployment fires a session on a cron schedule. It needs an agent, an environment, `initial_events` and a `schedule`.

```python
deployment = client.beta.deployments.create(
    name="Weekly compliance scan",
    agent=agent.id,
    environment_id=environment.id,
    initial_events=[{"type": "user.message", "content": [{"type": "text", "text": "Run the weekly compliance scan."}]}],
    schedule={"type": "cron", "expression": "0 20 * * 5", "timezone": "America/New_York"},
)

for run in client.beta.deployment_runs.list(deployment_id=deployment.id, has_error=True):
    print(run.created_at, run.error.type, run.error.message)
```

Runs can fire up to a few minutes late (jitter), no client is attached when they fire, and paused tool calls wait until answered (use webhooks, or avoid `always_ask`). Pause with `client.beta.deployments.pause(id)`.

## Multiagent and Memory Stores

**Multiagent:** add a top-level `multiagent` block on the agent. Each delegated piece runs in its own thread with a fresh context, in parallel, in the same container. Start with the agent itself on the roster:

```python
lead = client.beta.agents.create(
    name="Research lead",
    model="claude-opus-5-5",
    system="Delegate independent sub-questions to copies of yourself, then verify and combine their reports.",
    tools=[{"type": "agent_toolset_20260401", "default_config": {"permission_policy": {"type": "auto"}}}],
    multiagent={"type": "coordinator", "agents": [{"type": "self"}]},
)
```


**Memory stores** (separate beta header `agent-memory-2026-07-22`, set by the SDK on `client.beta.memory_stores.*`) persist text files across sessions and mount at `/mnt/memory/<store-name>/`:

```python
store = client.beta.memory_stores.create(
    name="User Preferences",
    description="Per-user preferences and project context.",
)
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    resources=[{
        "type": "memory_store",
        "memory_store_id": store.id,
        "access": "read_write",   # or "read_only"
        "instructions": "User preferences. Check before starting any task.",
    }],
)
```

## Common Pitfalls

- **Putting `model`, `system` or `tools` on `sessions.create()`.** They belong to the agent.
- **Creating a new agent per run.** It orphans agents; store the ID and update instead.
- **Answering `allow` to every paused call.** Unattended runs should answer `deny`.
- **Forgetting the network layers.** A secret needs the host allowed on the credential and in the environment.
- **Archiving as cleanup.** Archive is permanent and has no undo.

## Next Steps
- Track what sessions cost in [Admin API, Usage and Cost](./07_admin_usage_and_cost.md); each session also exposes `usage` and `list_cost`.

## Additional Resources
- [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration)
- [Self-hosted sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes)
