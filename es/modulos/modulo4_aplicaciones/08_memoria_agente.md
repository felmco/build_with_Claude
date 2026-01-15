# 4.2 Memoria del Agente

Los agentes necesitan memoria para persistir el estado a través de sesiones.

## Memoria a Corto Plazo
- **Mecanismo:** La lista `messages` enviada a la API.
- **Límite:** Ventana de contexto (200k tokens).
- **Estrategia:** Resumir (Ver Módulo 2).

## Memoria a Largo Plazo
- **Mecanismo:** Base de Datos Externa / DB Vectorial.
- **Proceso:**
  1. El agente decide "Necesito recordar esta preferencia."
  2. Llama a `save_memory(key="user_hobby", value="chess")`.
  3. Más tarde, el agente llama a `search_memory("hobby")`.

## Memoria Semántica (RAG)
Almacenar documentos o conocimiento que el agente pueda recuperar cuando lo necesite. Este es el puente a la siguiente sección.

## Próximos Pasos
- Sumérgete en [Fundamentos de RAG](09_fundamentos_rag.md).
