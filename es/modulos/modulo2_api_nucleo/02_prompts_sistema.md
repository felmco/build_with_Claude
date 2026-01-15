# 2.1 Prompts del Sistema

Los prompts del sistema son la forma principal de influir en el comportamiento, la personalidad y las restricciones de Claude durante una conversación.

## ¿Qué es un Prompt del Sistema?

Un prompt del sistema es un texto proporcionado a Claude que se sitúa "por encima" de la conversación. Establece el contexto, el rol y las reglas sobre cómo debe comportarse Claude.

### Uso Básico

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="You are a helpful assistant who speaks like a pirate.",
    messages=[
        {"role": "user", "content": "Hello there!"}
    ]
)
print(message.content[0].text)
```

## Mejores Prácticas para Prompts del Sistema

### 1. Asignar un Rol
Da a Claude una personalidad específica. Esto ayuda a enmarcar su conocimiento y tono.

```python
system = "You are a senior Python backend developer conducting a code review."
```

### 2. Definir Restricciones Claras
Dile a Claude lo que *no* debe hacer.

```python
system = """
You are a customer support agent.
- Be polite and professional.
- Do NOT make up information about our products.
- If you don't know the answer, say "I don't know" and refer them to support@example.com.
"""
```

### 3. Especificar Formato de Salida
Si necesitas JSON, Markdown o una estructura específica, defínela aquí.

```python
system = """
You are a data extraction tool.
Always respond with valid JSON in the following format:
{
  "name": "string",
  "age": "integer",
  "occupation": "string"
}
"""
```

### 4. Usar Etiquetas XML para Estructura
Para prompts complejos, usa etiquetas XML para separar secciones.

```python
system = """
<role>
You are an expert academic editor.
</role>

<task>
Review the user's paper for clarity, grammar, and flow.
</task>

<style>
Maintain a formal, academic tone.
</style>
"""
```

## Técnicas Avanzadas

### Prompting de Rol
Asignar un rol detallado puede mejorar significativamente el rendimiento en tareas complejas.

**Ejemplo: Análisis Legal**
```python
system = """
You are a veteran intellectual property lawyer with 20 years of experience.
Your task is to analyze the provided contract clauses for potential risks.
Focus specifically on indemnification and liability caps.
"""
```

### Cadena de Pensamiento (Chain of Thought) en Prompts del Sistema
Puedes instruir a Claude para que piense antes de responder dentro del prompt del sistema para mejorar el razonamiento.

```python
system = """
You are a math tutor. When solving problems, first think through the steps step-by-step
inside <thinking> tags, and then provide the final answer to the student.
"""
```

## Errores Comunes

- **Poner instrucciones en el mensaje del usuario:** Aunque funciona, el prompt del sistema es más robusto para instrucciones persistentes.
- **Ser demasiado vago:** "Sé útil" es menos efectivo que "Sé conciso, técnico y directo."
- **Instrucciones conflictivas:** Asegúrate de que tus restricciones no contradigan la descripción de tu tarea.

## Próximos Pasos
- Aprende cómo gestionar [Conversaciones](03_conversaciones.md).
