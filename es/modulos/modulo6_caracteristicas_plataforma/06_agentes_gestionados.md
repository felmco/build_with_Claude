# 6.6 Managed Agents (Beta)

Managed Agents es un arnés de agentes alojado. Defines un **agente** persistente (modelo, prompt de sistema, herramientas), un **entorno** (una plantilla de contenedor en la nube) y luego inicias **sesiones**. El bucle del agente se ejecuta en la capa de orquestación de Anthropic; el contenedor es donde se ejecutan sus herramientas (bash, archivos, código). Tú envías eventos y recibes eventos en streaming.

## Cuándo Elegirlo

| Situación | Mejor opción |
|---|---|
| Petición/respuesta corta, unas pocas herramientas que controlas | Bucle de la Messages API ([4.6](../modulo4_aplicaciones/06_bucles_agente.md)) |
| El agente necesita archivos y un shell en tus propias máquinas | [Agent SDK](./05_agent_sdk.md) |
| Trabajo largo de varios pasos en un entorno aislado que no quieres operar; ejecuciones programadas; entregables evaluados | **Managed Agents** |

Cambias el control del bucle por no tener que alojarlo: sin flota de contenedores, sin código de bucle, con compactación y caché de prompts integradas.

## El Flujo: Agente (una vez) -> Entorno -> Sesión (cada ejecución)

Managed Agents está en beta. El SDK establece por ti la cabecera beta `managed-agents-2026-04-01` en las llamadas `client.beta.{agents,environments,sessions,vaults,deployments}.*`. No la añadas a mano.

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

Actualizar un agente crea una nueva versión inmutable; las sesiones en curso conservan la versión que fijaron. No llames a `agents.create()` en cada petición.

## Eventos: Enviar y Recibir en Streaming

Abre primero el stream y luego envía, para no perder los primeros eventos.

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

Si el stream se corta mientras una llamada a herramienta espera tu respuesta, la sesión se queda atascada. Al reconectar, lista los eventos (`client.beta.sessions.events.list(session_id=...)`), elimina duplicados por ID de evento y reanuda el streaming.

## Herramientas Propias

Declara en el agente una herramienta `{"type": "custom", ...}`. Cuando el agente la llama recibes un evento `agent.custom_tool_use` y respondes con `user.custom_tool_result`:

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

## Políticas de Permisos

Establece un `permission_policy` en el `default_config` del toolset o en una herramienta concreta de `configs`:

| Política | Comportamiento |
|---|---|
| `always_allow` | Se ejecuta automáticamente (por defecto en el toolset del agente) |
| `always_ask` | Se pausa con `requires_action` hasta que envíes `user.tool_confirmation` (por defecto en los toolsets MCP) |
| `auto` | El servidor decide en cada llamada: ejecutar, denegar o pausar para ti |

`auto` no es un punto de control humano: una llamada que considera segura se ejecuta antes de que nadie la mire. Pon `always_ask` en las herramientas que una persona deba revisar, y responde `deny` a las llamadas en pausa cuando nadie esté pendiente.

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

## Credenciales en Vault

La entrada `mcp_servers` del agente contiene solo `{type, name, url}`. Los secretos viven en un **vault** asociado a la sesión al crearla (`vault_ids` no se puede añadir después). Las credenciales OAuth de MCP se renuevan automáticamente; las credenciales `environment_variable` se sustituyen en la salida de red, de modo que el entorno aislado solo ve un marcador de posición.

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

Las formas de credencial (`mcp_oauth`, `static_bearer`, `environment_variable`) están en la sección de vaults de la documentación de herramientas de managed-agents. Mantén las credenciales con el alcance mínimo y nunca las pongas en almacenes de memoria ni en prompts.

## Outcomes: Evaluar contra una Rúbrica

Para trabajo con un entregable verificable, empieza con `user.define_outcome` en lugar de `user.message` (nunca ambos). Un evaluador independiente puntúa cada iteración contra tu rúbrica y el agente revisa hasta que la supera o alcanza `max_iterations`.

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

El stream incluye eventos `span.outcome_evaluation_end` con un `result` de `satisfied`, `needs_revision`, `max_iterations_reached`, `failed` o `interrupted`. Escribe criterios explícitos y evaluables de forma independiente; los vagos producen bucles ruidosos. El ejemplo necesita `web_search` y `web_fetch` activados en el agente.

## Despliegues Programados

Un deployment lanza una sesión según un calendario cron. Necesita un agente, un entorno, `initial_events` y un `schedule`.

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

Las ejecuciones pueden lanzarse con unos minutos de retraso (jitter), no hay ningún cliente conectado cuando se disparan y las llamadas a herramientas en pausa esperan hasta que se respondan (usa webhooks, o evita `always_ask`). Pausa con `client.beta.deployments.pause(id)`.

## Multiagente y Almacenes de Memoria

**Multiagente:** añade un bloque `multiagent` de nivel superior en el agente. Cada parte delegada se ejecuta en su propio hilo con un contexto limpio, en paralelo, en el mismo contenedor. Empieza con el propio agente en la lista:

```python
lead = client.beta.agents.create(
    name="Research lead",
    model="claude-opus-5-5",
    system="Delegate independent sub-questions to copies of yourself, then verify and combine their reports.",
    tools=[{"type": "agent_toolset_20260401", "default_config": {"permission_policy": {"type": "auto"}}}],
    multiagent={"type": "coordinator", "agents": [{"type": "self"}]},
)
```


Los **almacenes de memoria** (cabecera beta aparte `agent-memory-2026-07-22`, establecida por el SDK en `client.beta.memory_stores.*`) persisten archivos de texto entre sesiones y se montan en `/mnt/memory/<store-name>/`:

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

## Errores Comunes

- **Poner `model`, `system` o `tools` en `sessions.create()`.** Pertenecen al agente.
- **Crear un agente nuevo en cada ejecución.** Deja agentes huérfanos; guarda el ID y actualiza en su lugar.
- **Responder `allow` a todas las llamadas en pausa.** Las ejecuciones desatendidas deben responder `deny`.
- **Olvidar las capas de red.** Un secreto necesita que el host esté permitido en la credencial y en el entorno.
- **Archivar como limpieza.** Archivar es permanente y no se puede deshacer.

## Próximos Pasos
- Sigue lo que cuestan las sesiones en [Admin API, Uso y Coste](./07_admin_uso_costes.md); cada sesión también expone `usage` y `list_cost`.

## Recursos Adicionales
- [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration)
- [Self-hosted sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes)
