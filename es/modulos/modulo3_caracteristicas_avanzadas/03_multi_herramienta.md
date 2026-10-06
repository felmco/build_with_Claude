# 3.1 Orquestación Multi-Herramienta

Claude puede elegir entre múltiples herramientas en un solo turno, o usar herramientas secuencialmente.

## Proporcionando Múltiples Herramientas

Simplemente añádelas a la lista `tools`.

```python
tools = [weather_tool, stock_tool, calculator_tool]

response = client.messages.create(
    ...,
    tools=tools,
    messages=[{"role": "user", "content": "What is the stock price of Apple + Google?"}]
)
```

## Uso Paralelo de Herramientas

Claude puede llamar a múltiples herramientas independientes a la vez (ej. obteniendo el precio de acciones para AAPL y GOOGL simultáneamente).

La API devuelve una lista de bloques `content`. Podrías ver múltiples bloques `tool_use`.

**Bucle de Manejo:**
1. Itera a través de `response.content`.
2. Recolecta todos los bloques `tool_use`.
3. Ejecútalos (secuencialmente o en paralelo usando `asyncio`).
4. Añade *todos* los bloques `tool_result` al siguiente mensaje de usuario.

```python
tool_results = []
for block in response.content:
    if block.type == "tool_use":
        result = execute(block)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": str(result)
        })

# Enviar de vuelta todos los resultados
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": tool_results})
```

Añade `"disable_parallel_tool_use": true` a `tool_choice` (`{"type": "auto", "disable_parallel_tool_use": True}`) si quieres como máximo una llamada a herramienta por turno.

Si una herramienta falla, devuelve su `tool_result` con `"is_error": True` y un mensaje de error para que Claude pueda recuperarse. Cada bloque `tool_use` necesita un `tool_result` correspondiente en el siguiente mensaje de usuario.

## Orquestación Secuencial (Encadenamiento)

A veces la herramienta B necesita la salida de la herramienta A.
- Claude maneja esto automáticamente, siempre que sigas iterando: llama a la API, ejecuta las herramientas solicitadas, devuelve los resultados y repite hasta que `stop_reason` deje de ser `"tool_use"`. Limita el número de iteraciones.
- Llama a la Herramienta A.
- Devuelves el resultado.
- Claude ve el resultado, luego llama a la Herramienta B.

## Próximos Pasos
- Revisa [Mejores Prácticas de Herramientas](04_mejores_practicas_herramientas.md).
