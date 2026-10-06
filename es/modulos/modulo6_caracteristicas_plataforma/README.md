# Módulo 6: Características Más Recientes de la Plataforma

**Duración**: 6-8 horas | **Nivel**: Avanzado

## Visión General
Los Módulos 1 a 5 construyen las habilidades centrales. Este módulo cubre las capacidades más nuevas de la plataforma que hoy tocan la mayoría de las aplicaciones de Claude en producción: herramientas del lado del servidor, salidas estructuradas y manejo de rechazos, gestión de contexto de larga duración, Skills y MCP, el Agent SDK, Managed Agents y la Admin API para seguir el uso y el coste.

> Varias de estas características están en **beta** y cambian rápido. Cada lección indica qué cabecera beta o modelo necesita. Confirma con la documentación oficial listada en [REFERENCIAS.md](../../REFERENCIAS.md) antes de publicar.

## Objetivos de Aprendizaje
Al final de este módulo, serás capaz de:
- Usar búsqueda web, web fetch, ejecución de código y tool search sin escribir un bucle de herramientas
- Obtener JSON válido según el esquema y manejar los motivos de parada `refusal`, `max_tokens` y `pause_turn`
- Mantener las ejecuciones largas de agentes dentro del presupuesto con presupuestos de tarea, compactación y edición de contexto
- Conectar Agent Skills y servidores MCP remotos de forma segura
- Elegir entre el bucle de la Messages API, el Agent SDK y Managed Agents
- Seguir el uso y el coste de la organización, y vigilar tu propio consumo en vivo

## Temas Cubiertos

- [6.1 Herramientas del Lado del Servidor](./01_herramientas_servidor.md)
- [6.2 Salidas Estructuradas, Motivos de Parada y Alternativas ante Rechazos](./02_salidas_estructuradas_rechazos.md)
- [6.3 Contexto de Larga Duración: Presupuestos, Compactación y Edición de Contexto](./03_contexto_larga_duracion.md)
- [6.4 Agent Skills y el Conector MCP](./04_skills_conector_mcp.md)
- [6.5 El Claude Agent SDK](./05_agent_sdk.md)
- [6.6 Managed Agents (Beta)](./06_agentes_gestionados.md)
- [6.7 Admin API, Uso y Coste](./07_admin_uso_costes.md)

## Extra
- [Mod Consumo](../../MODS.md): un panel en vivo de Claude Code que muestra tokens, gasto, contexto, llamadas a herramientas y tiempo de sesión.

## Requisitos Previos
Módulos 2 y 3 (Messages API, uso de herramientas, caché), y las lecciones del Módulo 4 sobre agentes y MCP.

## Próximos Pasos
- Vuelve al [proyecto final](../../proyectos/README.md) y aplica las características que encajen.
