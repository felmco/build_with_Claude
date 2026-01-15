# 5.4 Pruebas Automatizadas

Integra evaluaciones en tu CI/CD.

## Patrón
1. El desarrollador cambia el prompt.
2. Push a Git.
3. Pipeline CI ejecuta `pytest`.
4. `pytest` carga 20 entradas de muestra, llama a Claude, ejecuta Calificadores.
5. Si la precisión cae por debajo del 95%, Falla la Construcción.

## Herramientas
- **Pytest:** Ejecutor estándar de Python.
- **DeepEval:** Marco de pruebas de LLM de código abierto.

## Próximos Pasos
- [Pruebas A/B de Prompts](16_pruebas_ab.md).
