# 5.1 Plantillas de Prompt

En código, no deberías codificar los prompts directamente. Usa plantillas.

## Ejemplo Python (f-strings)

```python
def classify_email(email_text):
    prompt = f"""
    You are a customer service classifier.

    Classify the following email:
    <email>
    {email_text}
    </email>

    Return one of: [Billing, Support, Feature Request].
    """
    return call_claude(prompt)
```

## Librerías
- **Jinja2:** Genial para plantillas complejas con lógica.
- **LangChain:** Proporciona abstracciones `PromptTemplate`.

## Mejores Prácticas
- Mantén las plantillas bajo control de versiones.
- Separa los datos de las instrucciones.

## Próximos Pasos
- Muévete a [Optimización de Tokens](./06_token_optimization.md).
