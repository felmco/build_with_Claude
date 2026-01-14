# 5.1 Prompt Templates

In code, you shouldn't hardcode prompts. Use templates.

## Python Example (f-strings)

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

## Libraries
- **Jinja2:** Great for complex templates with logic.
- **LangChain:** Provides `PromptTemplate` abstractions.

## Best Practices
- Keep templates version controlled.
- Separate data from instructions.

## Next Steps
- Move to [Token Optimization](./06_token_optimization.md).
