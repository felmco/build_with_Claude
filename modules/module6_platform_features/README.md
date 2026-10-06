# Module 6: Latest Platform Features

**Duration**: 6-8 hours | **Level**: Advanced

## Overview
Modules 1 to 5 build the core skills. This module covers the newer platform capabilities that most production Claude applications now touch: server-side tools, structured outputs and refusal handling, long-running context management, Skills and MCP, the Agent SDK, Managed Agents, and the Admin API for tracking usage and cost.

> Several of these features are in **beta** and change quickly. Each lesson says which beta header or model it needs. Confirm against the official docs listed in [REFERENCES.md](../../REFERENCES.md) before shipping.

## Learning Objectives
By the end of this module, you will be able to:
- Use web search, web fetch, code execution and tool search without writing a tool loop
- Get schema-valid JSON and handle `refusal`, `max_tokens` and `pause_turn` stop reasons
- Keep long agent runs inside budget with task budgets, compaction and context editing
- Attach Agent Skills and remote MCP servers safely
- Choose between the Messages API loop, the Agent SDK and Managed Agents
- Track organization usage and cost, and watch your own consumption live

## Topics Covered

- [6.1 Server-Side Tools](./01_server_tools.md)
- [6.2 Structured Outputs, Stop Reasons and Refusal Fallbacks](./02_structured_outputs_and_refusals.md)
- [6.3 Long-Running Context: Budgets, Compaction and Context Editing](./03_long_running_context.md)
- [6.4 Agent Skills and the MCP Connector](./04_skills_and_mcp_connector.md)
- [6.5 The Claude Agent SDK](./05_agent_sdk.md)
- [6.6 Managed Agents (Beta)](./06_managed_agents.md)
- [6.7 Admin API, Usage and Cost](./07_admin_usage_and_cost.md)

## Bonus
- [Consumo mod](../../MODS.md): a live Claude Code pane showing tokens, spend, context, tool calls and session time.

## Prerequisites
Modules 2 and 3 (Messages API, tool use, caching), and Module 4 lessons on agents and MCP.

## Next Steps
- Revisit the [capstone project](../../projects/README.md) and apply the features that fit.
