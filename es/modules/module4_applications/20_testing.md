# 4.5 Pruebas de Aplicaciones Claude

## Pruebas Unitarias
Prueba tus herramientas y funciones auxiliares.
- "¿Devuelve `calculator(2, 2)` 4?"

## Evaluaciones (Evals)
Prueba el comportamiento del modelo.
- **Conjunto de datos:** 50 pares de Pregunta/Respuesta.
- **Métrica:** "Similitud de Respuesta" o "Factualidad".
- **LLM-como-Juez:** Pide a Claude Opus que califique la respuesta de Claude Haiku.

## Flujo de Trabajo
1. Cambia Prompt.
2. Ejecuta Evals.
3. Si la Puntuación aumenta -> Despliega.

## ¡Felicidades!
Has completado el Módulo 4. Estás listo para construir aplicaciones de IA sofisticadas.

## Siguiente Módulo
Procede al [Módulo 5: Optimización y Mejores Prácticas](../module5_optimization/README.md).
