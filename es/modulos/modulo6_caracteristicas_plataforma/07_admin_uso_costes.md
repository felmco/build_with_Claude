# 6.7 Admin API, Uso y Coste

Cuando varias personas y servicios llaman a Claude, necesitas responder dos preguntas: quién tiene acceso a qué y adónde va el dinero. La **Admin API** gestiona la organización; los **informes de Uso y Coste** muestran el consumo; `response.usage` da la contabilidad por petición dentro de tu propio código.

## Admin API: Gestionar la Organización

La Admin API vive bajo `https://api.anthropic.com/v1/organizations/*`. Gestiona la propia organización y no envía mensajes. El SDK de Python la expone como `client.beta.organization`.

La autenticación requiere una **clave de Admin API** (`sk-ant-admin...`, creada en la Claude Console por un administrador de la organización) o un token OAuth `org:admin`. Las claves de API normales no funcionan en estos endpoints, y las claves de admin no funcionan en la Messages API. No está disponible para cuentas individuales: configura primero una organización en la Console.

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

Otros recursos bajo el mismo espacio de nombres: `invites` (`create`, `list`, `delete`), `users.update` / `users.remove` y, solo con un token OAuth `org:admin`, `service_accounts` y la federación de identidad de cargas de trabajo (`federation.issuers`, `federation.rules`).

Roles de organización: `user`, `claude_code_user`, `developer`, `billing`, `admin`. Roles de workspace: `workspace_user`, `workspace_developer`, `workspace_admin`, `workspace_billing`. Concede el rol mínimo que funcione.

## Informes de Uso y Coste (HTTP Directo)

Estos endpoints forman parte de la Admin API pero **no están en los SDK**: llámalos por HTTP con una clave de Admin. No están disponibles en Claude Platform on AWS (usa las páginas de la Console), y las organizaciones Claude Enterprise usan una Analytics API distinta con una clave de Analytics.

| Endpoint | Muestra | Intervalos |
|---|---|---|
| `GET /v1/organizations/usage_report/messages` | Recuento de tokens por modelo, workspace, clave de API, nivel de servicio, ventana de contexto | `1m`, `1h`, `1d` |
| `GET /v1/organizations/cost_report` | Gasto en USD (tokens, búsqueda web, ejecución de código) | Solo `1d` |

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

Los filtros usan arrays como `models[]=`, `workspace_ids[]=`, `api_key_ids[]=`, `service_tiers[]=`. `group_by` acepta `model`, `workspace_id`, `api_key_id`, `service_tier`, `context_window`, `inference_geo` y más. Cada entrada `results` de uso incluye `uncached_input_tokens`, `cache_creation` (`ephemeral_5m_input_tokens`, `ephemeral_1h_input_tokens`), `cache_read_input_tokens`, `output_tokens` y `server_tool_use.web_search_requests`. Las entradas de coste incluyen `amount` como cadena decimal **en centavos**, además de `currency`, `description`, `model`, `cost_type` y `token_type`.

Pagina hasta que `has_more` sea falso, pasando `next_page` como `page`:

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

Notas de la documentación: los datos suelen aparecer en unos 5 minutos; consulta como máximo una vez por minuto aproximadamente; el Priority Tier no aparece en el informe de coste (usa el de uso con `service_tier`); el uso del playground de la Console tiene un `api_key_id` `null`.

## Contabilidad por Petición con response.usage

Los informes son para la organización. Para el coste por característica o por usuario, registra `usage` de cada respuesta.

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

Los multiplicadores de caché varían según el modelo, así que confírmalos en la página de precios. Para estimar antes de enviar, usa `client.messages.count_tokens(...)`. En ejecuciones del Agent SDK lee `ResultMessage.total_cost_usd` ([6.5](./05_agent_sdk.md)); una sesión de Managed Agents informa `usage` acumulado y `list_cost` ([6.6](./06_agentes_gestionados.md)). Trátalos como estimaciones y concílialos con el informe de coste.

## Vigila tu Consumo en Vivo

Los informes tienen minutos de retraso y son de toda la organización. Mientras trabajas en Claude Code, a menudo quieres los números ahora mismo. Este repositorio incluye un mod de Claude Code, **Consumo**, que dibuja un panel con los tokens de la última petición, el gasto de la sesión en USD, el porcentaje de la ventana de contexto usado, las llamadas a herramientas y el tiempo transcurrido, actualizado cada segundo y en cada prompt y llamada a herramienta.

```bash
claude --plugin-dir ./mods/consumo
# then type /consumo in the session
```

Consulta [`mods/consumo`](../../../mods/consumo) y [MODS.md](../../MODS.md) para ver cómo funciona y cómo compartirlo. El panel lee el uso de la propia sesión, así que complementa, y no sustituye, los informes de la Admin API anteriores.

## Errores Comunes

- **Usar una clave de API normal en endpoints de Admin.** Necesitas `sk-ant-admin...` o un token `org:admin`.
- **Distribuir la clave de admin dentro de una aplicación.** Mantenla en un trabajo de operaciones, no en un servicio de cara al usuario.
- **Leer `amount` como dólares.** Es una cadena decimal en centavos.
- **Mirar solo `input_tokens`.** Con caché es solo el resto sin cachear.
- **Esperar el Priority Tier o la ejecución de código en el informe equivocado.** Priority es solo de uso; la ejecución de código es solo de coste.
- **Olvidar que un `workspace_id` `null` significa el workspace por defecto.**
- **Conciliar demasiado pronto.** Deja pasar varios minutos para que los datos lleguen.

## Próximos Pasos
- Combina los informes con el caché y el procesamiento por lotes del Módulo 5 para reducir el gasto.
- Revisa los presupuestos de [Managed Agents](./06_agentes_gestionados.md) antes de ejecutar despliegues programados.

## Recursos Adicionales
- [Admin API guide](https://platform.claude.com/docs/en/manage-claude/admin-api)
- [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api)
- [Usage report reference](https://platform.claude.com/docs/en/api/beta/organization/usage_report/retrieve_messages)
- [Cost report reference](https://platform.claude.com/docs/en/api/beta/organization/cost_report/retrieve)
- [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api)
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
