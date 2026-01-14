# 4.2 Arquitectura de Agentes

Un "Agente" es un sistema de IA que puede tomar acciones para lograr un objetivo de forma autónoma.

## Componentes Principales

1. **El Cerebro (Claude):** Razona, planifica y decide.
2. **Herramientas (Manos):** APIs, Calculadoras, Búsqueda Web.
3. **Memoria:** A corto plazo (historial de conversación) y a largo plazo (DB Vectorial).
4. **Planificación:** Descomponer objetivos en pasos.

## Patrón ReAct (Razonar + Actuar)

Este es el bucle estándar para agentes.

1. **Pensamiento (Thought):** El modelo piensa sobre el problema.
2. **Acción (Action):** El modelo llama a una herramienta.
3. **Observación (Observation):** El modelo ve el resultado de la herramienta.
4. **Repetir:** Hasta terminar.

## Diagrama de Arquitectura

```
Meta del Usuario -> [ Planificador ] -> [ Ejecutor (Claude + Herramientas) ] -> [ Evaluador ] -> Resultado
```

## Próximos Pasos
- Implementar [Bucles de Agente](./06_agent_loops.md).
