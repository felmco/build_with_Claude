# 5.1 Plantillas de Prompt

En código, no deberías codificar los prompts directamente. Usa plantillas.

## Ejemplo Python (f-strings)

```python
import anthropic

client = anthropic.Anthropic()

def classify_email(email_text: str) -> str:
    prompt = f"""You are a customer service classifier.

Classify the following email:
<email>
{email_text}
</email>

Return exactly one of: Billing, Support, Feature Request."""
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=20,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()
```

## Librerías
- **Jinja2:** Genial para plantillas complejas con lógica.
- **LangChain:** Proporciona abstracciones `PromptTemplate`.

## Mejores Prácticas
- Mantén las plantillas bajo control de versiones.
- Separa los datos de las instrucciones.

## Próximos Pasos
- Muévete a [Optimización de Tokens](06_optimizacion_tokens.md).
