# 4.2 Sistemas Multi-Agente

Los agentes individuales son poderosos, pero los "Enjambres" (Swarms) o equipos multi-agente pueden resolver problemas más complejos.

## Patrones

### 1. Traspasos (Router)
- **Agente Enrutador:** Analiza la petición y enruta al especialista.
  - "Necesito un gráfico." -> **Agente DataViz**.
  - "Necesito un poema." -> **Agente EscritorCreativo**.

### 2. Supervisor / Trabajador
- **Supervisor:** Desglosa la tarea y asigna subtareas a los trabajadores.
- **Trabajadores:** Ejecutan subtareas y reportan de vuelta.

### 3. Debate / Colaboración
- Dos agentes con diferentes prompts (ej. "Desarrollador" vs "Auditor de Seguridad") critican el trabajo del otro para mejorar la calidad.

## Consejo de Implementación
Cada agente es solo una llamada `client.messages.create` con un prompt del sistema *diferente* y herramientas *diferentes*. Tú orquestas el paso de mensajes entre ellos en Python.

## Próximos Pasos
- [Memoria del Agente](08_memoria_agente.md).
