# 6.1 Server-Side Tools: Search, Fetch, Code Execution and Tool Search

## Introduction
Most tools in Module 3 are *client tools*: Claude returns a `tool_use` block, your code runs the function, and you send back a `tool_result`. **Server tools** run on Anthropic's infrastructure instead. You declare them in `tools`, the API runs them during the request, and the results arrive in the same response. This lesson covers web search, web fetch, code execution and tool search, plus the `pause_turn` stop reason that long server-side turns can produce.

## The Four Server Tools

| Tool | `type` | What it does |
|------|--------|--------------|
| Web search | `web_search_20260209` | Searches the web and returns cited results |
| Web fetch | `web_fetch_20260209` | Reads a specific URL (HTML, text or PDF) |
| Code execution | `code_execution_20260521` | Runs Python and bash in a sandboxed container |
| Tool search | `tool_search_tool_regex_20251119` / `tool_search_tool_bm25_20251119` | Lets Claude discover tools from a large catalog |

The `_20260209` web tools add **dynamic filtering**: Claude writes code that filters search or fetch results before they enter its context window, which saves tokens. The API provisions the code execution this needs, so you do not add the code execution tool for it. Newer web tool versions (for example `web_search_20260318`) also exist; check the tool reference for the latest. None of these tools needs a beta header.

## Web Search and Web Fetch

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    tools=[
        {
            "type": "web_search_20260209",
            "name": "web_search",
            "max_uses": 5,  # hard cap on searches per request
            "blocked_domains": ["pinterest.com"],  # use allowed_domains OR blocked_domains, not both
        },
        {
            "type": "web_fetch_20260209",
            "name": "web_fetch",
            "max_uses": 3,
            "citations": {"enabled": True},  # off by default for fetch
            "max_content_tokens": 50000,  # truncates large pages
        },
    ],
    messages=[{
        "role": "user",
        "content": "Find the latest Python release notes and summarize what changed.",
    }],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
```

Response content interleaves `text`, `server_tool_use` (the query or URL Claude chose) and result blocks (`web_search_tool_result`, `web_fetch_tool_result`). Do not execute anything for `server_tool_use` blocks and never send a `tool_result` for their `srvtoolu_...` ids.

### Domain Allow and Block Lists
Pass bare domains (optionally with a path such as `example.com/blog`, no scheme). Sending both `allowed_domains` and `blocked_domains` returns a 400. Organization admins can also restrict domains in the Console, and if web search is disabled for your organization a request that includes the tool fails with a 400.

## Citations
Web search always returns citations. Text blocks carry a `citations` list of `web_search_result_location` entries with `url`, `title` and `cited_text` (up to 150 characters). Web fetch citations are opt-in. If you show Claude's answer to end users, show the sources too.

```python
for block in response.content:
    if block.type == "text" and block.citations:
        for c in block.citations:
            if c.type == "web_search_result_location":
                print(f"- {c.title}: {c.url}")
```

When you continue a conversation, send assistant `content` back exactly as received. Search results include `encrypted_content`, and modifying or dropping it causes a 400.

## Errors Come Back as HTTP 200
If a server tool fails (rate limit, bad input, `max_uses` exceeded), the API still returns 200. The failure is an error object inside the result block, and Claude sees it and carries on. Check for it if your app depends on the result:

```python
def server_tool_errors(response):
    """Collect error codes from server-tool result blocks."""
    errors = []
    for block in response.content:
        if block.type in ("web_search_tool_result", "web_fetch_tool_result"):
            # On success, search content is a list and fetch content is a result object.
            # On failure, content is an object whose type ends in "_error".
            content = block.content
            if not isinstance(content, list) and getattr(content, "type", "").endswith("_error"):
                errors.append((block.type, content.error_code))
    return errors

print(server_tool_errors(response))  # e.g. [("web_search_tool_result", "max_uses_exceeded")]
```

Documented codes include `too_many_requests`, `invalid_tool_input`, `max_uses_exceeded`, `unavailable`, and for fetch `url_not_allowed`, `url_not_accessible` and `url_not_in_prior_context`. A search with no matches is an empty list, not an error.

## Handling `pause_turn`
Server-side tools run in a server loop that is capped at a number of iterations. If a turn is still going when the cap is hit, you get `stop_reason: "pause_turn"`. Re-send the user message plus the paused assistant content, and the server resumes. Do not add a "Continue" message, and cap the number of continuations.

```python
def ask(question: str, tools: list, max_continuations: int = 5):
    messages = [{"role": "user", "content": question}]
    for _ in range(max_continuations + 1):
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=4096,
            tools=tools,
            messages=messages,
        )
        if response.stop_reason != "pause_turn":
            return response
        # Resume: the trailing server_tool_use block tells the API where to pick up
        messages = [
            {"role": "user", "content": question},
            {"role": "assistant", "content": response.content},
        ]
    raise RuntimeError("Turn still paused after max_continuations")
```

If you mix server tools with your own client tools and Claude calls both in parallel, the response ends with `stop_reason: "tool_use"` and the server tool runs on your next request, after you return the client `tool_result` blocks. The SDK tool runner does not auto-resume `pause_turn` (checked against `anthropic` 0.116.0), so use a loop like the one above or restart the runner.

## Code Execution
Code execution gives Claude a sandbox (Python, bash, file editing) with no internet access. Use it for calculations, data analysis and file generation.

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": "Compute the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].",
    }],
)

for block in response.content:
    if block.type == "bash_code_execution_tool_result":
        result = block.content
        if result.type == "bash_code_execution_result":
            print("exit code:", result.return_code, "stdout:", result.stdout)
        else:
            print("tool error:", result.error_code)  # still HTTP 200
    elif block.type == "text":
        print(block.text)

print("container id (reuse it via container=...):", response.container.id)
```

Only add this standalone tool when your app needs code execution for its own purposes. Adding it next to the `_20260209` web tools creates a second execution environment that can confuse the model.

## Tool Search with `defer_loading`
With dozens of tools, definitions eat context and selection accuracy drops. Mark rarely used tools with `"defer_loading": True`, and add a tool search tool. Claude searches your catalog and only the matches are loaded. You still send every definition on every request, and at least one tool (the search tool) must not be deferred.

```python
tools = [
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
    {
        "name": "get_weather",
        "description": "Get the weather at a specific location",
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
        "defer_loading": True,  # only loaded if Claude finds it via search
    },
    # ... many more deferred tools ...
]

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2048,
    tools=tools,
    messages=[{"role": "user", "content": "What is the weather in San Francisco?"}],
)
# stop_reason == "tool_use": run the discovered get_weather yourself, then resend the same
# `tools`, the assistant content unchanged, and your tool_result.
```

Tool search pays off with roughly 10 or more tools or over 10K tokens of definitions. For under 10 small tools, plain tool use is simpler. Keep your 3 to 5 most-used tools non-deferred.

## Cost and Latency
- **Web search**: $10 per 1,000 searches plus tokens. Results count as input tokens on this and later turns. Failed searches are not billed. Track `usage.server_tool_use.web_search_requests`.
- **Web fetch**: no extra charge beyond tokens, but a 100 KB page is roughly 25,000 tokens. Use `max_content_tokens` and `max_uses`.
- **Code execution**: free when used with `_20260209`-or-later web tools. Otherwise there are 1,550 free hours per organization per month, then $0.05 per hour per container.
- **Tool search**: no separate charge, loaded definitions count as input tokens.
- Every search or fetch adds a round trip, so server-tool requests are slower. Stream long ones.

## Common Pitfalls
- Returning a `tool_result` for a `server_tool_use` id (the API rejects it).
- Treating HTTP 200 as success without checking result blocks for error codes.
- Ignoring `pause_turn` and showing a truncated answer.
- Setting both `allowed_domains` and `blocked_domains`.
- Editing or dropping `encrypted_content` when replaying history.
- Enabling web fetch where untrusted input sits next to sensitive data. Fetched content can carry prompt injection and exfiltration attempts, so restrict `allowed_domains` and `max_uses`.
- Setting `defer_loading` on every tool, including the search tool (400).

## Next Steps
- Continue to [Structured Outputs and Refusals](./02_structured_outputs_and_refusals.md)
- Revisit [Tool Use Basics](../module3_advanced_features/01_tool_use_basics.md)

## Additional Resources
- [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
- [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)
- [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)
- [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)
- [Server Tools Guide](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools)
