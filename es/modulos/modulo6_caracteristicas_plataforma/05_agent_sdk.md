# 6.5 El Claude Agent SDK

En el Módulo 4 construiste un bucle de agente a mano. El **Claude Agent SDK** te da como biblioteca el bucle que impulsa Claude Code: herramientas integradas, permisos, hooks, subagentes, MCP y sesiones, listo para incrustar en tu propio proceso de Python o TypeScript.

## Cuatro Formas de Construir un Agente

| Quieres... | Usa | ¿Quién ejecuta el bucle? |
|---|---|---|
| Llamar a la API de Claude y controlar cada paso | Messages API (Módulos 2-4) | Tú |
| Lo mismo, pero dejando que el SDK dirija el bucle de herramientas | Tool Runner (beta): `@beta_tool` + `client.beta.messages.tool_runner(...)` | El SDK cliente, en tu proceso |
| Incrustar el agente de Claude Code (archivos, shell, búsqueda) en tu aplicación | **Agent SDK** | El binario de Claude Code, en un proceso que tú operas |
| Que Anthropic aloje el agente en un entorno aislado en la nube | Managed Agents (ver [6.6](./06_agentes_gestionados.md)) | Anthropic |

Regla general: elige el Agent SDK cuando el agente necesite un sistema de archivos y un shell reales en **tu** infraestructura y quieras el comportamiento de Claude Code sin reconstruirlo. Elige la Messages API cuando necesites control total de una tarea acotada.

## Instalar y Autenticarse

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install claude-agent-sdk          # TypeScript: npm install @anthropic-ai/claude-agent-sdk
export ANTHROPIC_API_KEY="..."        # use API-key auth, never hard-code the key
```

Anthropic no permite que productos de terceros ofrezcan inicio de sesión con claude.ai para agentes construidos sobre el SDK. Usa autenticación con clave de API.

## query(): Una Tarea, Mensajes en Streaming

`query()` es un generador asíncrono. Le pasas un prompt y `ClaudeAgentOptions`, e iteras sobre los mensajes mientras el agente trabaja.

```python
import asyncio
from claude_agent_sdk import (
    query, ClaudeAgentOptions, AssistantMessage, ResultMessage, TextBlock,
)

async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep"],  # pre-approved, read-only
        max_turns=10,                            # hard stop on the loop
        max_budget_usd=0.50,                     # hard stop on spend
        cwd=".",
    )
    async for message in query(prompt="Summarize what this repo does", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            # Final message: status, cost, usage, session id
            print(message.subtype, message.num_turns, message.total_cost_usd)
            print("session:", message.session_id)

asyncio.run(main())
```

`ResultMessage.total_cost_usd` y `ResultMessage.usage` dan la contabilidad por ejecución (ver [6.7](./07_admin_uso_costes.md)).

## Herramientas Integradas

El agente incluye las mismas herramientas que Claude Code: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `WebFetch` y más. No escribes el bucle de herramientas ni los ejecutores. `allowed_tools` lista las herramientas que se ejecutan sin preguntar; `disallowed_tools` las elimina.

## Permisos

`permission_mode` establece la base:

| Modo | Comportamiento |
|---|---|
| `"default"` | Comportamiento de permisos estándar |
| `"acceptEdits"` | Acepta automáticamente las ediciones de archivos |
| `"plan"` | Explora sin editar |
| `"dontAsk"` | Deniega todo lo que no esté preaprobado (bueno para trabajos desatendidos) |
| `"auto"` | Un clasificador de modelo revisa las acciones |
| `"bypassPermissions"` | Sin comprobaciones: solo dentro de un entorno aislado desechable |

Para ejecuciones desatendidas, combina un `allowed_tools` reducido con `permission_mode="dontAsk"`.

## Hooks

Los hooks son callbacks de Python que se ejecutan en puntos del ciclo de vida. Python admite `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `UserPromptSubmit`, `Stop`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PermissionRequest` y `Notification`. Un matcher filtra por nombre de herramienta. Devolver `{}` permite; una decisión `deny` bloquea.

```python
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

async def protect_env_files(input_data, tool_use_id, context):
    file_path = input_data["tool_input"].get("file_path", "")
    if file_path.split("/")[-1] == ".env":
        return {
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "deny",
                "permissionDecisionReason": "Cannot modify .env files",
            }
        }
    return {}  # empty dict = allow

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="Write|Edit", hooks=[protect_env_files])]}
)
```

Los matchers solo comparan nombres de herramienta, no rutas: comprueba `tool_input` dentro del callback. `SessionStart` y `SessionEnd` son callbacks exclusivos de TypeScript.

## Subagentes

Define especialistas con `AgentDefinition`. El agente principal delega en ellos y solo su informe vuelve a su contexto.

```python
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Agent"],  # the parent needs the Agent tool to delegate
    agents={
        "code-reviewer": AgentDefinition(
            description="Reviews code changes for bugs. Use after edits.",
            prompt="You are a code reviewer. Report concrete issues with file and line.",
            tools=["Read", "Grep"],   # least privilege
            maxTurns=5,
        )
    },
)
```

Claude invoca a los subagentes mediante la herramienta `Agent`. Las versiones antiguas del SDK la llamaban `Task`, así que detecta ambas al identificar delegaciones en bloques `tool_use`. La salida de los subagentes cuenta para el `total_cost_usd` de la consulta; `max_budget_usd` la limita.

## Herramientas Propias y MCP

Añade tus propias herramientas en proceso con `@tool` y `create_sdk_mcp_server`, o conecta servidores externos mediante `mcp_servers`. Las herramientas MCP se llaman `mcp__<servidor>__<herramienta>`.

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions

@tool("add", "Add two numbers", {"a": float, "b": float})
async def add(args):
    return {"content": [{"type": "text", "text": f"Sum: {args['a'] + args['b']}"}]}

calculator = create_sdk_mcp_server(name="calculator", version="1.0.0", tools=[add])

options = ClaudeAgentOptions(
    mcp_servers={"calc": calculator},
    allowed_tools=["mcp__calc__add"],
)
```

## Sesiones: Continuar, Reanudar, Bifurcar

Una sesión es el historial de la conversación, guardado automáticamente en disco. Para un chat de varios turnos en un mismo proceso usa `ClaudeSDKClient`; para volver más tarde, captura `session_id` y pasa `resume`.

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, query, ResultMessage

async def chat():
    async with ClaudeSDKClient(options=ClaudeAgentOptions(allowed_tools=["Read", "Grep"])) as client:
        await client.query("Analyze the auth module")
        async for message in client.receive_response():
            pass  # handle messages
        await client.query("Now list the risks you found")   # same session, full context
        async for message in client.receive_response():
            print(message)

async def resume_later(session_id: str):
    options = ClaudeAgentOptions(resume=session_id)          # fork_session=True to branch instead
    async for message in query(prompt="Implement your suggestions", options=options):
        if isinstance(message, ResultMessage):
            print(message.subtype)
```

Las sesiones persisten la conversación, no el sistema de archivos. Reanudar funciona en la misma máquina salvo que añadas un adaptador de almacén de sesiones.

## Errores Comunes

- **Tratarlo como la Messages API.** El SDK lanza el binario de Claude Code; necesita un entorno donde pueda ejecutarse y actúa sobre un sistema de archivos real.
- **`bypassPermissions` fuera de un entorno aislado.** Usa `dontAsk` junto con una lista `allowed_tools` ajustada.
- **Sin límites.** Establece siempre `max_turns` y `max_budget_usd` en ejecuciones desatendidas.
- **Hooks que lanzan excepciones o se bloquean en E/S lenta.** Captura los errores dentro del hook y ejecuta las llamadas bloqueantes en un hilo.
- **Esperar hooks `SessionStart` en Python.** Son callbacks exclusivos de TypeScript.
- **Suponer que una transcripción almacenada se traslada entre hosts.** Usa un almacén de sesiones o pasa los resultados como estado.

## Próximos Pasos
- Compara con la opción alojada en [Managed Agents](./06_agentes_gestionados.md).
- Sigue lo que cuestan las ejecuciones en [Admin API, Uso y Coste](./07_admin_uso_costes.md).

## Recursos Adicionales
- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Python SDK reference](https://code.claude.com/docs/en/agent-sdk/python)
- [Hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions)
- [Permissions](https://code.claude.com/docs/en/agent-sdk/permissions)
- [Subagents](https://code.claude.com/docs/en/agent-sdk/subagents)
- [MCP in the SDK](https://code.claude.com/docs/en/agent-sdk/mcp)
