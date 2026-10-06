# 6.7 Admin API, Usage and Cost

Once several people and services call Claude, you need to answer two questions: who has access to what, and where is the money going. The **Admin API** manages the organization; the **Usage and Cost reports** show consumption; `response.usage` gives per-request accounting inside your own code.

## Admin API: Manage the Organization

The Admin API lives under `https://api.anthropic.com/v1/organizations/*`. It manages the organization itself and does not send messages. The Python SDK exposes it as `client.beta.organization`.

Authentication needs an **Admin API key** (`sk-ant-admin...`, created in the Claude Console by an organization admin) or an `org:admin` OAuth token. Regular API keys do not work on these endpoints, and admin keys do not work on the Messages API. It is unavailable for individual accounts: set up an organization in the Console first.

```python
import os
import anthropic

# Use a dedicated admin client. Keep the admin key out of application servers.
admin = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_ADMIN_KEY"])

org = admin.beta.organization.retrieve()

# Members (iterator auto-fetches pages; limit = page size, not total)
for user in admin.beta.organization.users.list(limit=10):
    print(f"{user.id}: {user.email} ({user.role})")

# Workspaces separate projects, budgets and keys
ws = admin.beta.organization.workspaces.create(name="Production")
admin.beta.organization.workspaces.members.add(
    ws.id, user_id="user_...", workspace_role="workspace_developer"
)

# Deactivate a leaked or unused API key
admin.beta.organization.api_keys.update("apikey_...", status="inactive", name="Retired key")

# Rate limit reports (optional filters: model=..., group_type=...)
admin.beta.organization.rate_limits.list(model="claude-opus-5-5")
admin.beta.organization.workspaces.rate_limits.list(ws.id)
```

Other resources under the same namespace: `invites` (`create`, `list`, `delete`), `users.update` / `users.remove`, and, with an `org:admin` OAuth token only, `service_accounts` and workload identity federation (`federation.issuers`, `federation.rules`).

Organization roles: `user`, `claude_code_user`, `developer`, `billing`, `admin`. Workspace roles: `workspace_user`, `workspace_developer`, `workspace_admin`, `workspace_billing`. Grant the least role that works.

## Usage and Cost Reports (Raw HTTP)

These endpoints are part of the Admin API but are **not in the SDKs**: call them over HTTP with an Admin key. They are not available on Claude Platform on AWS (use the Console pages), and Claude Enterprise orgs use a different Analytics API with an Analytics key.

| Endpoint | Shows | Buckets |
|---|---|---|
| `GET /v1/organizations/usage_report/messages` | Token counts by model, workspace, API key, service tier, context window | `1m`, `1h`, `1d` |
| `GET /v1/organizations/cost_report` | Spend in USD (token, web search, code execution) | `1d` only |

```bash
# Daily token usage by model for a week
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-10-01T00:00:00Z&\
ending_at=2026-10-08T00:00:00Z&\
group_by[]=model&\
bucket_width=1d" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Cost by workspace and line item for a month
curl "https://api.anthropic.com/v1/organizations/cost_report?\
starting_at=2026-10-01T00:00:00Z&\
ending_at=2026-10-31T00:00:00Z&\
group_by[]=workspace_id&\
group_by[]=description" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Filters use arrays such as `models[]=`, `workspace_ids[]=`, `api_key_ids[]=`, `service_tiers[]=`. `group_by` accepts `model`, `workspace_id`, `api_key_id`, `service_tier`, `context_window`, `inference_geo` and more. Each usage `results` entry carries `uncached_input_tokens`, `cache_creation` (`ephemeral_5m_input_tokens`, `ephemeral_1h_input_tokens`), `cache_read_input_tokens`, `output_tokens` and `server_tool_use.web_search_requests`. Cost entries carry `amount` as a decimal string **in cents**, plus `currency`, `description`, `model`, `cost_type` and `token_type`.

Paginate until `has_more` is false, passing `next_page` as `page`:

```python
import os
import json
import urllib.parse
import urllib.request

BASE = "https://api.anthropic.com/v1/organizations/cost_report"
HEADERS = {
    "anthropic-version": "2023-06-01",
    "x-api-key": os.environ["ANTHROPIC_ADMIN_KEY"],
    "User-Agent": "course-cost-report/1.0",
}

def cost_by_workspace(start: str, end: str) -> dict[str, float]:
    """Return USD per workspace_id between two RFC 3339 timestamps."""
    totals: dict[str, float] = {}
    page = None
    while True:
        params = [("starting_at", start), ("ending_at", end), ("group_by[]", "workspace_id")]
        if page:
            params.append(("page", page))
        req = urllib.request.Request(f"{BASE}?{urllib.parse.urlencode(params)}", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.load(resp)
        for bucket in body["data"]:
            for item in bucket["results"]:
                key = item["workspace_id"] or "default"   # null = default workspace
                totals[key] = totals.get(key, 0.0) + float(item["amount"]) / 100  # cents -> USD
        if not body["has_more"]:
            return totals
        page = body["next_page"]

print(cost_by_workspace("2026-10-01T00:00:00Z", "2026-10-31T00:00:00Z"))
```

Notes from the docs: data usually appears within about 5 minutes; poll at most about once per minute; the Priority Tier is missing from the cost report (use usage with `service_tier`); Console playground usage has a `null` `api_key_id`.

## Per-Request Accounting with response.usage

Reports are for the organization. For per-feature or per-user cost, record `usage` from every response.

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Summarize prompt caching in two sentences."}],
)

u = response.usage
print(u.input_tokens)                    # uncached input only
print(u.cache_creation_input_tokens)     # written to cache (premium rate)
print(u.cache_read_input_tokens)         # served from cache (discounted)
print(u.output_tokens)

# Total prompt size is the SUM of the three input fields, not input_tokens alone
prompt_tokens = (
    u.input_tokens
    + (u.cache_creation_input_tokens or 0)
    + (u.cache_read_input_tokens or 0)
)

def request_cost(usage, in_price: float, out_price: float,
                 write_mult: float = 1.25, read_mult: float = 0.1) -> float:
    """USD for one request. Prices are per million tokens: load them from the
    pricing page or config, never hard-code stale numbers."""
    base = usage.input_tokens * in_price
    write = (usage.cache_creation_input_tokens or 0) * in_price * write_mult
    read = (usage.cache_read_input_tokens or 0) * in_price * read_mult
    return (base + write + read + usage.output_tokens * out_price) / 1_000_000
```

The cache multipliers differ by model, so confirm them on the pricing page. To estimate before sending, use `client.messages.count_tokens(...)`. For Agent SDK runs read `ResultMessage.total_cost_usd` ([6.5](./05_agent_sdk.md)); a Managed Agents session reports cumulative `usage` and `list_cost` ([6.6](./06_managed_agents.md)). Treat these as estimates and reconcile with the cost report.

## Watch Your Consumption Live

The reports lag by minutes and are org-wide. While you work in Claude Code you often want the numbers right now. This repo ships a Claude Code mod, **Consumo**, that draws a pane with tokens of the last request, session spend in USD, the percentage of the context window used, tool calls and elapsed time, refreshed every second and on each prompt and tool call.

```bash
claude --plugin-dir ./mods/consumo
# then type /consumo in the session
```

See [`mods/consumo`](../../mods/consumo) and [MODS.md](../../MODS.md) for how it works and how to share it. The pane reads the session's own usage, so it complements, and does not replace, the Admin API reports above.

## Common Pitfalls

- **Using a regular API key on Admin endpoints.** You need `sk-ant-admin...` or an `org:admin` token.
- **Shipping the admin key in an app.** Keep it in an operations job, not a user-facing service.
- **Reading `amount` as dollars.** It is a decimal string in cents.
- **Looking only at `input_tokens`.** With caching it is just the uncached remainder.
- **Expecting Priority Tier or code execution in the wrong report.** Priority is usage-only; code execution is cost-only.
- **Forgetting that `null` `workspace_id` means the default workspace.**
- **Reconciling too early.** Allow several minutes for data to land.

## Next Steps
- Combine reports with caching and batching from Module 5 to cut spend.
- Review [Managed Agents](./06_managed_agents.md) budgets before running scheduled deployments.

## Additional Resources
- [Admin API guide](https://platform.claude.com/docs/en/manage-claude/admin-api)
- [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api)
- [Usage report reference](https://platform.claude.com/docs/en/api/beta/organization/usage_report/retrieve_messages)
- [Cost report reference](https://platform.claude.com/docs/en/api/beta/organization/cost_report/retrieve)
- [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api)
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
