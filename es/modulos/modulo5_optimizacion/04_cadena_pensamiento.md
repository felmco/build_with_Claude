# 5.1 Cadena de Pensamiento (CoT)

CoT es una técnica donde se anima al modelo a producir pasos de razonamiento intermedios.

## Cómo implementar
1. **Instrucción Explícita:** "Piensa paso a paso."
2. **Etiquetas XML:** Instruye a Claude para que ponga su razonamiento dentro de etiquetas `<thinking>`.

```python
system = "You are a math tutor. Reason inside <reasoning> tags, then give the final answer inside <answer> tags."
```

Analiza el bloque `<answer>` en tu código y descarta el resto.

## Pensamiento nativo
El pensamiento integrado de Claude suele ser mejor que el razonamiento inducido por prompt. En `claude-sonnet-5-5`, `claude-opus-5-5` y `claude-fable-5-1`, usa pensamiento adaptativo y controla la profundidad con `effort`:

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "summarized"},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "A train leaves at 3pm going 60 mph..."}],
)
for block in response.content:
    if block.type == "thinking":
        print("Reasoning summary:", block.thinking)
    elif block.type == "text":
        print(block.text)
```

`budget_tokens` es rechazado en estos modelos; solo `claude-haiku-4-5` sigue usando `thinking={"type": "enabled", "budget_tokens": N}`. El pensamiento está oculto por defecto (`display: "omitted"`), así que solicita `"summarized"` si quieres mostrarlo.

## Beneficios
- **Depuración:** Puedes ver *por qué* Claude obtuvo una respuesta incorrecta.
- **Precisión:** Desglosar problemas reduce errores lógicos.

## Próximos Pasos
- [Plantillas de Prompt](05_plantillas_prompts.md).
