# 4.2 Multi-Agent Systems

Single agents are powerful, but "Swams" or multi-agent teams can solve more complex problems.

## Patterns

### 1. Handoffs (Router)
- **Router Agent:** Analyzes request and routes to specialist.
  - "I need a graph." -> **DataViz Agent**.
  - "I need a poem." -> **CreativeWriter Agent**.

### 2. Supervisor / Worker
- **Supervisor:** Breaks down task and assigns sub-tasks to workers.
- **Workers:** Execute sub-tasks and report back.

### 3. Debate / Collaboration
- Two agents with different prompts (e.g., "Developer" vs "Security Auditor") critique each other's work to improve quality.

## Implementation Tip
Each agent is just a `client.messages.create` call with a *different* system prompt and *different* tools. You orchestrate the message passing between them in Python.

## Next Steps
- [Agent Memory](./08_agent_memory.md).
