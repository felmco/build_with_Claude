# 4.2 Bucles de Agente

El "Bucle" es el código en tiempo de ejecución que mantiene al agente funcionando hasta que la tarea se completa.

## El Algoritmo del Bucle

```python
def run_agent(goal, tools):
    messages = [{"role": "user", "content": goal}]

    while True:
        # 1. Preguntar a Claude
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # 2. Comprobar condición de parada
        if response.stop_reason == "end_turn":
            return response.content[0].text

        # 3. Manejar Uso de Herramienta
        if response.stop_reason == "tool_use":
            tool_use = ... # Obtener bloque de herramienta
            result = execute_tool(tool_use)

            # 4. Actualizar Historial
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": str(result)
                }]
            })
```

## Salvaguardas
- **Máx Bucles:** Prevenir bucles infinitos (ej. `if loop_count > 10: break`).
- **Tiempo de espera (Timeout):** Parar después de X segundos.
- **Presupuesto:** Parar después de X tokens gastados.

## Próximos Pasos
- [Sistemas Multi-Agente](./07_multi_agent.md).
