# 4.4 MCP Best Practices

1. **Security:** MCP servers run local code. Don't connect untrusted servers.
2. **Resource vs Tool:**
   - Use **Resources** for passive data (logs, file content).
   - Use **Tools** for actions (queries, API calls).
3. **Error Handling:** Return meaningful errors so the model can retry (MCP tool results support an `isError` flag).
4. **Stdio vs Streamable HTTP:**
   - **Stdio:** Best for local desktop apps.
   - **Streamable HTTP:** Best for remote servers. It replaces the older HTTP+SSE transport, which is deprecated.

## Next Steps
- Move to [Production Patterns](./17_error_patterns.md).
