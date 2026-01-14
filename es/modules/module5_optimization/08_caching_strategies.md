# 5.2 Estrategias de Caché

## La Regla "Cachear Todo lo Estático"
Si el texto aparece en más de una petición, cachéalo.

## Candidatos Comunes
1. **Prompts del Sistema:** Si son largos (>1024 tokens).
2. **Ejemplos Few-Shot:** Si proporcionas 50 ejemplos, cachéalos.
3. **Documentos de Referencia:** Docs de políticas, especificaciones de API.
4. **Historial de Conversación:** En chatbots, cachea el historial hasta el último turno.

## Gestión de Puntos de Ruptura (Breakpoints)
Coloca breakpoints al *final* de la sección estática.

`[Prompt de Sistema Estático] -> [CACHE] -> [Entrada de Usuario Dinámica]`

## Próximos Pasos
- [Procesamiento por Lotes por Coste](./09_batch_cost.md).
