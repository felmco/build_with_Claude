# 5.1 Técnicas Avanzadas de Prompting

Una vez que dominas lo básico, estas técnicas permiten resolver problemas complejos.

## 1. Cadena de Pensamiento (Chain of Thought - CoT)
Pide a Claude que "Piense paso a paso" antes de responder. Esto mejora el razonamiento significativamente.

```
Pregunta: Si tengo 3 manzanas y como una, luego compro dos más, ¿cuántas tengo?
Respuesta: Pensemos paso a paso.
1. Empiezo con 3 manzanas.
2. Como una: 3 - 1 = 2.
3. Compro dos: 2 + 2 = 4.
Respuesta Final: 4.
```

## 2. Encadenamiento de Prompts (Prompt Chaining)
Romper una tarea compleja en múltiples llamadas a la API.
- **Llamada 1:** Extraer datos.
- **Llamada 2:** Analizar datos.
- **Llamada 3:** Formatear informe.

## 3. Metaprompting
Pedir a Claude que escriba un prompt por ti.
"Quiero un prompt que clasifique correos de clientes. Escribe un prompt de alta calidad para esta tarea."

## Próximos Pasos
- [Aprendizaje Few-Shot](./03_few_shot.md).
