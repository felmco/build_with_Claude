# 5.2 Estrategia de Selección de Modelo

Elegir el modelo correcto es la mayor palanca de optimización.

## La Estrategia "Haiku Primero"
Siempre intenta resolver el problema con **Claude 3.5 Haiku** primero.
- Es significativamente más rápido y barato.
- Usa prompting avanzado (Few-Shot, CoT) para potenciar sus capacidades.

## El Sonnet por Defecto
Usa **Claude 3.5 Sonnet** para tareas de producción que requieran fiabilidad y matices.

## El Especialista Opus
Usa **Claude 3 Opus** (o 4.5 Opus) para:
- Generación de datos (crear datos de entrenamiento para Haiku).
- Razonamiento complejo en el que Sonnet falla.

## Próximos Pasos
- [Estrategias de Caché](./08_caching_strategies.md).
