# 4.1 Pipelines de Generación de Contenido

Claude destaca en la generación de contenido de alta calidad (blogs, correos electrónicos, informes). Un "pipeline" divide esto en pasos para mejores resultados.

## El Patrón de Cascada (Waterfall)

1. **Paso 1: Esquema**
   - Tema de Usuario -> Claude -> Esquema.
2. **Paso 2: Borrador**
   - Esquema -> Claude -> Primer Borrador.
3. **Paso 3: Crítica**
   - Borrador -> Claude -> Retroalimentación (Crítica).
4. **Paso 4: Refinar**
   - Borrador + Crítica -> Claude -> Pulido Final.

## ¿Por qué funciona esto?
Los LLMs funcionan mejor cuando se enfocan en una tarea a la vez (razonamiento vs. escritura vs. edición).

## Ejemplo: Generador de Correos de Marketing

```python
import anthropic

client = anthropic.Anthropic()

def ask(prompt):
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

# 1. Generar ideas
ideas = ask("Generate 3 email angles for product X")

# 2. Seleccionar la mejor (Usuario o Claude)
best_idea = ideas  # o pide a Claude / al usuario que elija una

# 3. Escribir la copia
copy = ask(f"Write email based on: {best_idea}")
```

## Próximos Pasos
- [Asistentes de Código](04_asistentes_codigo.md).
