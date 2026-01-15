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
# 1. Generar ideas
ideas = client.messages.create(..., prompt="Generate 3 email angles for product X").content[0].text

# 2. Seleccionar mejor (Usuario o Claude)
best_idea = ...

# 3. Escribir copia
copy = client.messages.create(..., prompt=f"Write email based on: {best_idea}").content[0].text
```

## Próximos Pasos
- [Asistentes de Código](04_asistentes_codigo.md).
