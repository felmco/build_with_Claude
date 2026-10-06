# 6.2 Salidas Estructuradas, Motivos de Parada y Alternativas ante Rechazos

## Introducción
El código de producción necesita dos garantías: que la salida tenga la forma que tu programa espera, y que tu programa sepa *por qué* se detuvo la generación. Las salidas estructuradas te dan la primera. Comprobar `stop_reason` te da la segunda, incluido el caso `refusal` que los modelos actuales pueden devolver cuando un clasificador de seguridad rechaza una petición. Esta lección también muestra la alternativa del lado del servidor que reintenta en otro modelo una petición rechazada.

## Salidas Estructuradas
Las salidas estructuradas restringen la respuesta de Claude a un JSON Schema. Como los modelos Claude 5.x rechazan el prefill del asistente (un 400), esta es la forma admitida de forzar una estructura JSON.

### Con Pydantic: `client.messages.parse`
```python
import anthropic
from pydantic import BaseModel

client = anthropic.Anthropic()

class ContactInfo(BaseModel):
    name: str
    email: str
    plan: str
    demo_requested: bool

response = client.messages.parse(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Extract: Jane Doe (jane@co.com) wants Enterprise and asked for a demo.",
    }],
    output_format=ContactInfo,  # SDK helper: converts the model to a schema and validates the reply
)

# Always check why generation stopped before trusting the parsed object
if response.stop_reason == "end_turn":
    contact = response.parsed_output  # a validated ContactInfo instance
    print(contact.name, contact.demo_requested)
```

`output_format` es una comodidad aceptada por `.parse()`. El parámetro a nivel de API es `output_config.format`, que se muestra a continuación.

### Esquema directo: `output_config.format`
```python
import json

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Extract: John Smith (john@example.com) wants Enterprise."}],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "plan": {"type": "string"},
                },
                "required": ["name", "email", "plan"],
                "additionalProperties": False,  # required on every object
            },
        }
    },
)

if response.stop_reason == "end_turn":
    text = next(b.text for b in response.content if b.type == "text")
    data = json.loads(text)
```

Límites del esquema: sin esquemas recursivos, sin restricciones numéricas (`minimum`, `maximum`) y sin restricciones de longitud de cadena. El SDK de Python elimina del esquema que envía las restricciones no admitidas y las valida en el cliente. La primera petición con un esquema nuevo paga un coste único de compilación, y las salidas estructuradas no se pueden combinar con citas (400). Los valores `enum` de tipo cadena pueden volver con otra capitalización, así que compáralos sin distinguir mayúsculas.

### Uso estricto de herramientas
Añade `"strict": True` a una herramienta para garantizar que `input` coincida con su esquema. También sustituye al `tool_choice` forzado en los modelos actuales: `{"type": "any"}` y `{"type": "tool", ...}` devuelven un 400 en Fable 5.1, Opus 5.5 y Sonnet 5.5, así que mantén `auto`, indica a Claude que use la herramienta y comprueba que haya un bloque `tool_use`.

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    tools=[{
        "name": "book_flight",
        "description": "Book a flight to a destination",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "date": {"type": "string", "format": "date"},
                "passengers": {"type": "integer"},
            },
            "required": ["destination", "date", "passengers"],
            "additionalProperties": False,
        },
    }],
    messages=[{"role": "user", "content": "Use the book_flight tool: Tokyo, 2 passengers, March 15."}],
)
calls = [b for b in response.content if b.type == "tool_use"]
if not calls:
    ...  # auto does not guarantee a call: re-prompt or handle the text reply
```

## Comprueba Siempre `stop_reason`

| `stop_reason` | Significado | Qué hacer |
|---------------|-------------|-----------|
| `end_turn` | Terminó de forma natural | Usa la salida |
| `max_tokens` | Alcanzó tu `max_tokens` | La salida puede estar cortada y ser JSON inválido. Sube `max_tokens` o usa streaming |
| `tool_use` | Claude quiere que se ejecute una herramienta de cliente | Ejecútala y responde con `tool_result` |
| `pause_turn` | Turno de herramienta de servidor en pausa | Reenvía para reanudar (ver 6.1) |
| `refusal` | Un clasificador o el modelo declinó | No leas `content` como una respuesta normal |

```python
def handle(response):
    if response.stop_reason == "refusal":
        # A refusal is HTTP 200, not an exception. Content is empty or partial.
        details = response.stop_details  # only present on refusals
        category = details.category if details else None  # e.g. "cyber", "bio", or None
        raise RuntimeError(f"Request declined (category={category})")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("Output truncated: increase max_tokens")
    return next(b.text for b in response.content if b.type == "text")
```

Ramifica según `stop_reason`, nunca según `stop_details`: es informativo y `category` puede ser `None`. Con salidas estructuradas, un rechazo tiene prioridad sobre el esquema, así que la salida puede no ajustarse a él. Los rechazos siguen contando para los límites de velocidad aunque no se produzca salida. Pedirle a un modelo que reproduzca su razonamiento interno en la respuesta puede provocar un rechazo `reasoning_extraction`. Usa en su lugar el `display: "summarized"` del pensamiento.

## Alternativas del Lado del Servidor ante Rechazos
Los rechazos del clasificador pueden afectar a peticiones legítimas (herramientas de seguridad y trabajo en ciencias de la vida son casos comunes). Sin una alternativa, una petición rechazada simplemente se detiene. Con el parámetro beta `fallbacks`, la API vuelve a ejecutar la petición rechazada en otro modelo dentro de la misma llamada:

```python
response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    betas=["server-side-fallback-2026-07-01"],
    fallbacks="default",  # Anthropic picks the recommended fallback for the refusal category
    messages=[{"role": "user", "content": "Review this nginx config for hardening issues: ..."}],
)

print("served by:", response.model)
if response.stop_reason == "refusal":
    # The whole chain refused. recommended_model, when set, is a hint for a direct retry.
    print(response.stop_details)
```

Datos clave:
- La cabecera y la forma van juntas. `fallbacks: "default"` necesita `server-side-fallback-2026-07-01`. La forma antigua de lista `fallbacks=[{"model": "..."}]` necesita `server-side-fallback-2026-06-01`. Mezclarlas devuelve un 400.
- Se activa solo ante rechazos por política, no ante límites de velocidad, sobrecargas ni errores del servidor.
- Un rechazo a mitad de streaming se factura a tarifa normal, y el rescate se factura a las tarifas propias del modelo alternativo. Consulta `usage.iterations` para el desglose por intento.
- Una vez que una conversación recurre a la alternativa, las peticiones posteriores con `fallbacks` pueden ser atendidas directamente por el modelo alternativo durante aproximadamente una hora.
- Disponible en la Claude API y en Claude Platform on AWS. Se rechaza en la Batches API y no está disponible en Bedrock, Vertex AI ni Foundry, donde usas el `BetaRefusalFallbackMiddleware` del SDK en el cliente o tu propio reintento.
- Los rechazos `reasoning_extraction` no se reintentan en un modelo alternativo.

## Errores Comunes
- Leer `response.content[0].text` sin comprobar `stop_reason` (un rechazo tiene contenido vacío o parcial).
- Tratar una salida por `max_tokens` como JSON válido. El JSON truncado falla al analizarse.
- Ramificar según `stop_details.category`, que puede ser `None`.
- Usar prefill o `tool_choice` forzado para obtener JSON. Ambos devuelven un 400 en los modelos actuales.
- Olvidar `additionalProperties: False` en los objetos del esquema y en los esquemas de herramientas estrictas.
- Combinar la forma de lista de `fallbacks` con la cabecera `2026-07-01` (o al revés).
- Enviar `fallbacks` a través de la Batches API o a Bedrock, Vertex o Foundry.

## Próximos Pasos
- Continúa con [Gestión de Contexto de Larga Duración](./03_contexto_larga_duracion.md)
- Repasa [Herramientas de Servidor](./01_herramientas_servidor.md) para `pause_turn`

## Recursos Adicionales
- [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Refusals and Fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)
- [Handling Stop Reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
- [Strict Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)
