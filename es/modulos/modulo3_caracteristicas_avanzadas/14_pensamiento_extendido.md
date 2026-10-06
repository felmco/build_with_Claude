# 3.5 Visión General del Pensamiento Extendido y Adaptativo

El pensamiento permite a Claude razonar antes de responder, lo que mejora el rendimiento en tareas complejas. En los modelos actuales no defines un presupuesto de tokens: Claude decide cuánto pensar (**pensamiento adaptativo**) y tú controlas la profundidad con el parámetro **`effort`**.

## Modelos Soportados y Modos

| Modelo | Cómo usar el pensamiento |
|-------|---------------------|
| **Claude Fable 5.1** | Siempre activo. Omite `thinking` (o envía `{"type": "adaptive"}`). Controla la profundidad con `effort`. |
| **Claude Opus 5.5** | Siempre activo y adaptativo. `{"type": "disabled"}` y `budget_tokens` devuelven 400. `effort` por defecto: `medium`. |
| **Claude Sonnet 5.5** | Adaptativo por defecto. `{"type": "disabled"}` devuelve 400; envía `{"type": "between_tools"}` para desactivarlo (con `effort` `high` o menor). |
| **Claude Haiku 4.5** | *Pensamiento extendido* manual: `{"type": "enabled", "budget_tokens": N}` (mínimo 1024, menor que `max_tokens`). |

> `budget_tokens` está obsoleto en Opus 4.6 / Sonnet 4.6 y se rechaza en los modelos 5.x. Consulta [Pensamiento adaptativo](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) y el [parámetro Effort](https://platform.claude.com/docs/en/build-with-claude/effort).

## Cómo Funciona
Cuando hay pensamiento, la respuesta contiene bloques `thinking` antes del bloque `text`.

```python
import anthropic

client = anthropic.Anthropic()

# Se recomienda streaming para peticiones largas y de esfuerzo alto
with client.messages.stream(
    model="claude-opus-5-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "summarized"},
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": "Resuelve este complejo acertijo lógico..."}],
) as stream:
    response = stream.get_final_message()

for block in response.content:
    if block.type == "thinking":
        print("PENSAMIENTO:", block.thinking)
    elif block.type == "text":
        print(block.text)
```

Haiku 4.5 (presupuesto manual):

```python
client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=4096,
    thinking={"type": "enabled", "budget_tokens": 2048},
    messages=[{"role": "user", "content": "Resuelve este complejo acertijo lógico..."}],
)
```

## El Bloque de "Pensamiento"
- **Visibilidad:** `display` es `"omitted"` por defecto en los modelos 5.x (el bloque llega con texto vacío). Usa `"summarized"` para obtener un resumen legible; la cadena de razonamiento en bruto nunca se devuelve. El pensamiento se factura igual sea cual sea el `display`.
- **Profundidad:** Contrólala con `output_config.effort`: `low`, `medium`, `high`, `xhigh`, `max`. Más esfuerzo implica más profundidad, coste y latencia.
- **Reenvío:** Al continuar una conversación, devuelve los bloques de pensamiento sin cambios (añade `response.content`, no solo el texto).

## Beneficios
- Menos alucinaciones.
- Mejor planificación.
- Autocorrección durante la fase de pensamiento.

## Próximos Pasos
- [Casos de Uso de Pensamiento](15_casos_uso_pensamiento.md).
