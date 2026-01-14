# 4.2 Agent Architecture

An "Agent" is an AI system that can take actions to achieve a goal autonomously.

## Core Components

1. **The Brain (Claude):** Reasons, plans, and decides.
2. **Tools (Hands):** APIs, Calculators, Web Search.
3. **Memory:** Short-term (conversation history) and Long-term (Vector DB).
4. **Planning:** Decomposing goals into steps.

## ReAct Pattern (Reason + Act)

This is the standard loop for agents.

1. **Thought:** The model thinks about the problem.
2. **Action:** The model calls a tool.
3. **Observation:** The model sees the tool result.
4. **Repeat:** Until done.

## Architecture Diagram

```
User Goal -> [ Planner ] -> [ Executor (Claude + Tools) ] -> [ Evaluator ] -> Result
```

## Next Steps
- Implement [Agent Loops](./06_agent_loops.md).
