# 4.5 Pruebas de Aplicaciones Claude

## Pruebas Unitarias
Prueba tus herramientas y funciones auxiliares.
- "¿Devuelve `calculator(2, 2)` 4?"

## Evaluaciones (Evals)
Prueba el comportamiento del modelo.
- **Conjunto de datos:** 50 pares de Pregunta/Respuesta.
- **Métrica:** "Similitud de Respuesta" o "Factualidad".
- **LLM-como-Juez:** Pide a un modelo más potente (p. ej. `claude-opus-5-5`) que califique la respuesta de un modelo más económico (p. ej. `claude-haiku-4-5`) según una rúbrica.

Las pruebas que llaman a la API son lentas, cuestan dinero y no son deterministas. Mantén las pruebas unitarias sin conexión simulando (mock) el cliente, y ejecuta las evals por separado con un conjunto de datos fijo y calificación basada en rúbrica en lugar de coincidencias exactas de texto.

## Flujo de Trabajo
1. Cambia Prompt.
2. Ejecuta Evals.
3. Si la Puntuación aumenta -> Despliega.

## ¡Felicidades!
Has completado el Módulo 4. Estás listo para construir aplicaciones de IA sofisticadas.

## Siguiente Módulo
Procede al [Módulo 5: Optimización y Mejores Prácticas](../modulo5_optimizacion/README.md).
