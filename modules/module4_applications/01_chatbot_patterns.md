# 4.1 Chatbot Patterns

Chatbots are the most common application of LLMs. This guide covers architectural patterns for building robust conversational interfaces.

## 1. The Basic Stateless Chatbot
- **Architecture:** Client sends message -> Server calls API -> Server returns response.
- **State:** Managed by the client (browser/app) or not at all (single turn).
- **Pros:** Simple, scalable.
- **Cons:** No history persistence.

## 2. The Stateful Chatbot (Database-backed)
- **Architecture:**
  1. Client sends message + session ID.
  2. Server fetches history from DB (Postgres/Redis).
  3. Server appends new message.
  4. Server calls Claude API.
  5. Server saves new user & assistant messages.
  6. Server returns response.
- **Pros:** Persistent history across devices.
- **Cons:** More complex backend.

## 3. The Context-Aware Chatbot (RAG)
- **Architecture:**
  1. User message received.
  2. Search Vector DB for relevant docs.
  3. Inject docs into System Prompt.
  4. Call Claude.
- **Use Case:** Customer support, Internal knowledge base.

## 4. The Streaming Chatbot
- **Architecture:** Use WebSockets or Server-Sent Events (SSE) to push token chunks to the client as they arrive.
- **UX:** Essential for long responses to reduce perceived latency.

## Best Practices
- **System Prompt:** Define personality and constraints clearly.
- **Truncation:** Manage context window by summarizing or dropping old messages.
- **Moderation:** Check inputs/outputs for safety.

## Next Steps
- Build a [Q&A System](./02_qa_systems.md).
