# 4.2 Agent Memory

Agents need memory to persist state across sessions.

## Short-term Memory
- **Mechanism:** The `messages` list sent to the API.
- **Limit:** Context window (200k tokens).
- **Strategy:** Summarization (See Module 2).

## Long-term Memory
- **Mechanism:** External Database / Vector DB.
- **Process:**
  1. Agent decides "I need to remember this preference."
  2. Calls `save_memory(key="user_hobby", value="chess")`.
  3. Later, agent calls `search_memory("hobby")`.

## Semantic Memory (RAG)
Storing documents or knowledge that the agent can retrieve when needed. This is the bridge to the next section.

## Next Steps
- Dive into [RAG Fundamentals](./09_rag_fundamentals.md).
