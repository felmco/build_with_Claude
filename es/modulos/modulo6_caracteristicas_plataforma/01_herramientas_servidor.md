# 6.1 Herramientas del Lado del Servidor: Búsqueda, Fetch, Ejecución de Código y Tool Search

## Introducción
La mayoría de las herramientas del Módulo 3 son *herramientas de cliente*: Claude devuelve un bloque `tool_use`, tu código ejecuta la función y envías de vuelta un `tool_result`. Las **herramientas de servidor** se ejecutan en cambio en la infraestructura de Anthropic. Las declaras en `tools`, la API las ejecuta durante la petición y los resultados llegan en la misma respuesta. Esta lección cubre búsqueda web, web fetch, ejecución de código y tool search, además del motivo de parada `pause_turn` que pueden producir los turnos largos del lado del servidor.

## Las Cuatro Herramientas de Servidor

| Herramienta | `type` | Qué hace |
|-------------|--------|----------|
| Búsqueda web | `web_search_20260209` | Busca en la web y devuelve resultados con citas |
| Web fetch | `web_fetch_20260209` | Lee una URL concreta (HTML, texto o PDF) |
| Ejecución de código | `code_execution_20260521` | Ejecuta Python y bash en un contenedor aislado |
| Tool search | `tool_search_tool_regex_20251119` / `tool_search_tool_bm25_20251119` | Permite a Claude descubrir herramientas de un catálogo grande |

Las herramientas web `_20260209` añaden **filtrado dinámico**: Claude escribe código que filtra los resultados de búsqueda o fetch antes de que entren en su ventana de contexto, lo que ahorra tokens. La API aprovisiona la ejecución de código que esto necesita, así que no añades la herramienta de ejecución de código para ello. También existen versiones más nuevas de las herramientas web (por ejemplo `web_search_20260318`); consulta la referencia de herramientas para la última. Ninguna de estas herramientas necesita cabecera beta.

## Búsqueda Web y Web Fetch

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
            "max_uses": 5,  # límite estricto de búsquedas por petición
            "blocked_domains": ["pinterest.com"],  # usa allowed_domains O blocked_domains, no ambos
        },
        {
            "type": "web_fetch_20260209",
            "name": "web_fetch",
            "max_uses": 3,
            "citations": {"enabled": True},  # desactivado por defecto en fetch
            "max_content_tokens": 50000,  # trunca páginas grandes
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

El contenido de la respuesta intercala bloques `text`, `server_tool_use` (la consulta o URL que Claude eligió) y bloques de resultado (`web_search_tool_result`, `web_fetch_tool_result`). No ejecutes nada para los bloques `server_tool_use` y nunca envíes un `tool_result` para sus ids `srvtoolu_...`.

### Listas de Dominios Permitidos y Bloqueados
Pasa dominios sin esquema (opcionalmente con una ruta como `example.com/blog`). Enviar `allowed_domains` y `blocked_domains` a la vez devuelve un 400. Los administradores de la organización también pueden restringir dominios en la Console, y si la búsqueda web está desactivada para tu organización, una petición que incluya la herramienta falla con un 400.

## Citas
La búsqueda web siempre devuelve citas. Los bloques de texto llevan una lista `citations` con entradas `web_search_result_location` que contienen `url`, `title` y `cited_text` (hasta 150 caracteres). Las citas de web fetch son opcionales. Si muestras la respuesta de Claude a usuarios finales, muestra también las fuentes.

```python
for block in response.content:
    if block.type == "text" and block.citations:
        for c in block.citations:
            if c.type == "web_search_result_location":
                print(f"- {c.title}: {c.url}")
```

Cuando continúes una conversación, reenvía el `content` del asistente exactamente como lo recibiste. Los resultados de búsqueda incluyen `encrypted_content`, y modificarlo o eliminarlo provoca un 400.

## Los Errores Llegan como HTTP 200
Si una herramienta de servidor falla (límite de velocidad, entrada inválida, `max_uses` superado), la API sigue devolviendo 200. El fallo es un objeto de error dentro del bloque de resultado, y Claude lo ve y continúa. Compruébalo si tu aplicación depende del resultado:

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

Los códigos documentados incluyen `too_many_requests`, `invalid_tool_input`, `max_uses_exceeded`, `unavailable` y, para fetch, `url_not_allowed`, `url_not_accessible` y `url_not_in_prior_context`. Una búsqueda sin coincidencias es una lista vacía, no un error.

## Manejo de `pause_turn`
Las herramientas de servidor se ejecutan en un bucle del servidor con un número máximo de iteraciones. Si un turno sigue en marcha cuando se alcanza el límite, recibes `stop_reason: "pause_turn"`. Reenvía el mensaje del usuario más el contenido pausado del asistente, y el servidor continúa. No añadas un mensaje "Continue" y limita el número de continuaciones.

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

Si mezclas herramientas de servidor con tus propias herramientas de cliente y Claude llama a ambas en paralelo, la respuesta termina con `stop_reason: "tool_use"` y la herramienta de servidor se ejecuta en tu siguiente petición, después de que devuelvas los bloques `tool_result` del cliente. El tool runner del SDK no reanuda automáticamente `pause_turn` (comprobado con `anthropic` 0.116.0), así que usa un bucle como el anterior o reinicia el runner.

## Ejecución de Código
La ejecución de código da a Claude un entorno aislado (Python, bash, edición de archivos) sin acceso a internet. Úsala para cálculos, análisis de datos y generación de archivos.

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

Añade esta herramienta independiente solo cuando tu aplicación necesite ejecución de código para sus propios fines. Añadirla junto a las herramientas web `_20260209` crea un segundo entorno de ejecución que puede confundir al modelo.

## Tool Search con `defer_loading`
Con decenas de herramientas, las definiciones consumen contexto y la precisión de selección baja. Marca las herramientas poco usadas con `"defer_loading": True` y añade una herramienta de tool search. Claude busca en tu catálogo y solo se cargan las coincidencias. Sigues enviando todas las definiciones en cada petición, y al menos una herramienta (la de búsqueda) no debe estar diferida.

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

Tool search compensa con unas 10 o más herramientas, o más de 10K tokens de definiciones. Para menos de 10 herramientas pequeñas, el uso de herramientas normal es más simple. Mantén tus 3 a 5 herramientas más usadas sin diferir.

## Coste y Latencia
- **Búsqueda web**: 10 $ por 1.000 búsquedas más tokens. Los resultados cuentan como tokens de entrada en este turno y los siguientes. Las búsquedas fallidas no se facturan. Sigue `usage.server_tool_use.web_search_requests`.
- **Web fetch**: sin cargo extra más allá de los tokens, pero una página de 100 KB son unos 25.000 tokens. Usa `max_content_tokens` y `max_uses`.
- **Ejecución de código**: gratis cuando se usa con herramientas web `_20260209` o posteriores. En otro caso hay 1.550 horas gratuitas por organización al mes, y después 0,05 $ por hora por contenedor.
- **Tool search**: sin cargo aparte; las definiciones cargadas cuentan como tokens de entrada.
- Cada búsqueda o fetch añade un viaje de ida y vuelta, así que las peticiones con herramientas de servidor son más lentas. Usa streaming en las largas.

## Errores Comunes
- Devolver un `tool_result` para un id de `server_tool_use` (la API lo rechaza).
- Tratar el HTTP 200 como éxito sin revisar los bloques de resultado en busca de códigos de error.
- Ignorar `pause_turn` y mostrar una respuesta truncada.
- Establecer `allowed_domains` y `blocked_domains` a la vez.
- Editar o eliminar `encrypted_content` al reenviar el historial.
- Activar web fetch donde la entrada no confiable convive con datos sensibles. El contenido obtenido puede llevar inyección de prompts e intentos de exfiltración, así que restringe `allowed_domains` y `max_uses`.
- Poner `defer_loading` en todas las herramientas, incluida la de búsqueda (400).

## Próximos Pasos
- Continúa con [Salidas Estructuradas y Rechazos](./02_salidas_estructuradas_rechazos.md)
- Repasa [Fundamentos del Uso de Herramientas](../modulo3_caracteristicas_avanzadas/01_conceptos_basicos_uso_herramientas.md)

## Recursos Adicionales
- [Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
- [Web Fetch Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)
- [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)
- [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)
- [Server Tools Guide](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools)
