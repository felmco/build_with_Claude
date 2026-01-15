# 3.5 Visión General del Pensamiento Extendido

El Pensamiento Extendido permite a Claude "pensar" antes de responder, haciendo visible su razonamiento y mejorando el rendimiento en tareas complejas.

## Modelos Soportados
- **Claude Sonnet 3.7+**
- **Claude 4+** (Futuro)

## Cómo Funciona
Cuando se habilita, Claude genera un bloque `thinking` antes del bloque `text`.

```python
client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    thinking={
        "type": "enabled",
        "budget_tokens": 1024
    },
    messages=[{"role": "user", "content": "Solve this complex logic puzzle..."}]
)
```

## El Bloque "Thinking" (Pensamiento)
- **Visibilidad:** Puedes elegir mostrar esto al usuario u ocultarlo.
- **Presupuesto (Budget):** Estableces un presupuesto de tokens para pensar. Mayor presupuesto = pensamiento más profundo (y mayor coste/latencia).

## Beneficios
- Alucinaciones reducidas.
- Mejor planificación.
- Autocorrección durante la fase de pensamiento.

## Próximos Pasos
- [Casos de Uso de Pensamiento](15_casos_uso_pensamiento.md).
