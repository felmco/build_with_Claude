# 5.4 Construyendo Marcos de Evaluación

La Ingeniería de Prompts es ingeniería. Necesitas pruebas.

## Componentes de una Evaluación
1. **Conjunto de Datos (Dataset):** Entradas y respuestas "Doradas" (Verdad Terreno).
2. **Ejecutor (Runner):** Código para enviar entradas a Claude.
3. **Calificador (Grader):** Lógica para comprobar si la salida de Claude coincide con la respuesta Dorada.

## Tipos de Calificación
1. **Coincidencia Exacta:** Bueno para extracción (JSON).
2. **Coincidencia Difusa:** "Contiene la palabra clave X".
3. **LLM-como-Juez:** Pide a otro LLM (ej. Opus) que califique la respuesta en una escala de 1-5.

## Próximos Pasos
- [Pruebas Automatizadas](15_pruebas_automatizadas.md).
