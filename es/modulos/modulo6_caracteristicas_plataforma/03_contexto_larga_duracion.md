# 6.3 Contexto de Larga Duración: Presupuestos, Compactación y Edición de Contexto

## Introducción
Los agentes que ejecutan decenas de llamadas a herramientas se topan con tres problemas: pueden gastar más tokens de los previstos, su contexto se llena de salidas de herramientas obsoletas y acaban acercándose a la ventana de contexto. La plataforma tiene una característica para cada uno. Esta lección cubre los **presupuestos de tarea**, la **compactación**, la **edición de contexto** y dos formas compatibles con la caché de dirigir una conversación en curso (**mensajes de sistema a mitad de conversación** y **esfuerzo por mensaje**). Termina con una tabla para elegir entre ellas.

## Presupuestos de Tarea: Dosificar Todo el Bucle
Un presupuesto de tarea le indica a Claude cuántos tokens puede gastar en todo un bucle agéntico (pensamiento, llamadas a herramientas, resultados de herramientas y salida). El modelo ve una cuenta atrás y va cerrando con elegancia a medida que se reduce.

```python
import anthropic

client = anthropic.Anthropic()

# Beta: task-budgets-2026-03-13. Minimum total is 20,000 tokens (smaller returns a 400).
with client.beta.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=64000,  # hard per-request ceiling, independent of the budget
    betas=["task-budgets-2026-03-13"],
    output_config={
        "effort": "high",
        "task_budget": {"type": "tokens", "total": 64000},
    },
    messages=[{"role": "user", "content": "Review the repo and propose a refactor plan."}],
) as stream:
    response = stream.get_final_message()

print(response.usage)
```

- El presupuesto es **orientativo**, no un tope estricto. `max_tokens` sigue siendo el límite impuesto por petición, así que usa ambos.
- Un presupuesto demasiado pequeño para la tarea puede causar un comportamiento similar a un rechazo (declinar, reducir el alcance, parar pronto). Mide primero el uso real de tokens y dimensiona el presupuesto con tu propia distribución.
- La cuenta atrás solo es visible para el modelo. La respuesta no tiene un campo de presupuesto restante.
- Si tu propio código reescribe o compacta el historial, pasa `"remaining"` en `task_budget` para que la cuenta atrás continúe en lugar de reiniciarse. En bucles que reenvían el historial completo, omítelo.
- Cambiar el valor entre peticiones invalida los prefijos en caché que lo contienen. Establécelo una sola vez.
- No es compatible con Haiku 4.5 ni con Sonnet 5.

## Compactación: Resúmenes del Lado del Servidor
La compactación resume los turnos antiguos en el servidor cuando la entrada alcanza un umbral. La API devuelve un bloque `compaction` y, en peticiones posteriores, ignora todo lo anterior a ese bloque. **Debes añadir el `response.content` completo**, no solo el texto, o el resumen se pierde.

```python
messages = []

def chat(user_message: str) -> str:
    messages.append({"role": "user", "content": user_message})

    response = client.beta.messages.create(
        betas=["compact-2026-01-12"],
        model="claude-sonnet-5-5",
        max_tokens=4096,
        messages=messages,
        context_management={
            "edits": [{
                "type": "compact_20260112",
                "trigger": {"type": "input_tokens", "value": 150000},  # default; minimum 50000
                # "instructions": "Keep file paths and open TODOs.",  # replaces the default summary prompt
                # "pause_after_compaction": True,  # stop with stop_reason "compaction" to inspect the summary
            }]
        },
    )

    # Preserve compaction blocks: append blocks, not response.content[0].text
    messages.append({"role": "assistant", "content": response.content})
    return "".join(b.text for b in response.content if b.type == "text")
```

Nota de facturación: el `usage` de nivel superior cubre solo el mensaje final. Suma `usage.iterations` para ver también el coste del paso de resumen. Existe una variante más nueva de compactación bajo demanda (beta `compact-2026-09-04`), en la que tú decides cuándo compactar. Consulta la visión general de compactación para saber cuándo preferirla.

## Edición de Contexto: Podar por Reglas
La edición de contexto elimina resultados de herramientas obsoletos (o bloques de pensamiento) en lugar de resumirlos. La estructura de la conversación se mantiene y el contenido borrado se quita.

```python
response = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    betas=["context-management-2025-06-27"],
    tools=tools,  # your tools
    messages=messages,
    context_management={
        "edits": [{
            "type": "clear_tool_uses_20250919",
            "trigger": {"type": "input_tokens", "value": 30000},  # default 100,000
            "keep": {"type": "tool_uses", "value": 3},  # keep the 3 most recent results
            "clear_at_least": {"type": "input_tokens", "value": 5000},  # make each clear worth a cache miss
            "exclude_tools": ["search_docs"],  # never clear these
        }]
    },
)

print(response.context_management.applied_edits)  # what was cleared this turn
```

Borrar resultados de herramientas invalida el prefijo en caché a partir de ese punto, así que usa `clear_at_least` para asegurar que cada borrado ahorre lo suficiente como para compensar. `clear_thinking_20251015` gestiona los bloques de pensamiento y, al combinar ambas estrategias, lista esta primero. Combina la edición de contexto con la herramienta de memoria para que Claude pueda guardar resultados importantes antes de que se borren.

## Mensajes de Sistema a Mitad de Conversación
Para cambiar las instrucciones a mitad de conversación ("pasa a modo conciso"), añade un mensaje `role: "system"` en lugar de editar el `system` de nivel superior. El prefijo en caché permanece intacto y la instrucción tiene autoridad de operador, por lo que es más difícil de suplantar que un texto dentro de un turno de usuario.

```python
response = client.messages.create(  # no beta header needed
    model="claude-sonnet-5-5",
    max_tokens=2048,
    system=[{"type": "text", "text": "You are a support assistant.",
             "cache_control": {"type": "ephemeral"}}],
    messages=history + [
        {"role": "user", "content": user_message},
        {"role": "system", "content": "Terse mode enabled - keep responses under 40 words."},
    ],
)
```

Reglas: debe ir después de un mensaje de usuario, ser el último en `messages` o ir seguido de un turno del asistente, y no puede ser `messages[0]`. El contenido es solo texto. Es compatible con Opus 5/5.5, Fable 5/5.1 y Sonnet 5.5, pero no con Sonnet 5, donde devuelve un 400, así que captura `anthropic.BadRequestError` y recurre a un recordatorio dentro del turno del usuario.

## Esfuerzo por Mensaje
Cambiar el `effort` de nivel superior entre peticiones invalida la caché de prompts. Un mensaje `role: "system"` con contenido vacío y un `output_config` cambia el esfuerzo desde ese punto sin invalidarla. Es una beta (`mid-conversation-output-config-2026-07-01`) y requiere pensamiento activado.

```python
response = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    betas=["mid-conversation-output-config-2026-07-01"],
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[
        {"role": "user", "content": "Plan the database migration."},
        {"role": "assistant", "content": "Here is the plan: ..."},
        {"role": "system", "content": [], "output_config": {"effort": "low"}},
        {"role": "user", "content": "Now rename the config file."},
    ],
)
```

El nuevo nivel se aplica desde el siguiente turno del usuario hasta que un mensaje de sistema posterior lo cambie. Bajar el esfuerzo es fiable, y subirlo funciona mejor con saltos grandes (por ejemplo de `low` a `xhigh`).

## Elegir entre Ellas

| Necesidad | Usa |
|-----------|-----|
| Evitar que un agente gaste de más en tokens | Presupuesto de tarea (más `max_tokens` como tope estricto) |
| Mantener una conversación muy larga dentro de la ventana | Compactación |
| Descartar salidas voluminosas y antiguas de herramientas conservando la transcripción | Edición de contexto |
| Cambiar instrucciones sin romper la caché | Mensaje de sistema a mitad de conversación |
| Dedicar más o menos pensamiento a un paso | Esfuerzo por mensaje |
| Recordar datos entre conversaciones distintas | Herramienta de memoria |

### Herramienta de Memoria
La compactación y la edición de contexto gestionan *una* conversación. La herramienta de memoria (`{"type": "memory_20250818", "name": "memory"}`) es una herramienta de cliente que permite a Claude leer y escribir archivos en un directorio `/memories` para que el conocimiento sobreviva entre sesiones. Tú implementas el almacenamiento. El SDK ofrece un ayudante `BetaAbstractMemoryTool`. Nunca guardes secretos en los archivos de memoria, y añade aislamiento por usuario en sistemas multiusuario.

## Errores Comunes
- Añadir solo el texto de una respuesta con compactación (el resumen se pierde y el contexto vuelve a crecer).
- Tratar un presupuesto de tarea como un límite estricto, o fijarlo muy por debajo del coste real de la tarea.
- Decrementar `task_budget.remaining` en cada petición (rompe la caché y hace que Claude cierre antes de tiempo).
- Borrar resultados de herramientas sin `clear_at_least` (fallos de caché repetidos por ahorros pequeños).
- Poner un mensaje de sistema a mitad de conversación el primero en `messages` o después de un turno del asistente.
- Usar esfuerzo por mensaje con el pensamiento desactivado, o en un modelo que no lo admite (400).

## Próximos Pasos
- Continúa con [Agent Skills y el Conector MCP](./04_skills_conector_mcp.md)
- Repasa [Caché de Prompts](../modulo3_caracteristicas_avanzadas/05_cache_prompt.md)

## Recursos Adicionales
- [Task Budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets)
- [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)
- [Context Editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)
- [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
