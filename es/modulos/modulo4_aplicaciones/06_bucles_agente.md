# 4.2 Bucles de Agente

El "Bucle" es el código en tiempo de ejecución que mantiene al agente funcionando hasta que la tarea se completa.

## El Algoritmo del Bucle

```python
import anthropic

client = anthropic.Anthropic()

def run_agent(goal, tools, max_loops=10):
    messages = [{"role": "user", "content": goal}]

    for _ in range(max_loops):
        # 1. Preguntar a Claude
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )

        # 2. Comprobar condición de parada
        if response.stop_reason == "tool_use":
            # 3. Ejecutar CADA bloque tool_use (Claude puede llamar a varios en paralelo)
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    try:
                        result = execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result),
                        })
                    except Exception as e:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"Error: {e}",
                            "is_error": True,
                        })

            # 4. Actualizar historial: devolver el turno del asistente y luego TODOS
            #    los resultados en un único mensaje de usuario
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        elif response.stop_reason == "max_tokens":
            raise RuntimeError("Response truncated; raise max_tokens")
        elif response.stop_reason == "refusal":
            raise RuntimeError("Claude declined the request")
        else:  # "end_turn" (o "pause_turn": reenvía para continuar)
            return "".join(b.text for b in response.content if b.type == "text")

    raise RuntimeError("Agent exceeded max_loops")
```

`execute_tool(name, input)` es tu propio despachador. Devuelve todos los bloques `tool_result` de un mismo turno del asistente juntos en un único mensaje de usuario, y colócalos al principio de la lista de contenido.

## Salvaguardas
- **Máx Bucles:** Prevenir bucles infinitos (el argumento `max_loops` de arriba).
- **Tiempo de espera (Timeout):** Parar después de X segundos.
- **Presupuesto:** Parar después de X tokens gastados.

## Próximos Pasos
- [Sistemas Multi-Agente](07_multi_agente.md).
