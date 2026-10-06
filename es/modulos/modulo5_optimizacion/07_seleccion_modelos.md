# 5.2 Estrategia de Selección de Modelos

Elegir el modelo correcto es la mayor palanca de optimización.

## La Estrategia "Haiku Primero"
Intenta resolver el problema primero con **Claude Haiku 4.5** (`claude-haiku-4-5`).
- Es el modelo más rápido y barato ($1 / $5 por MTok) y tiene inteligencia casi de frontera.
- Usa prompting avanzado (Few-Shot, CoT) para potenciar sus capacidades.
- Encaja bien en sub-agentes y rutas de alto volumen.

## Sonnet por Defecto
Usa **Claude Sonnet 5.5** (`claude-sonnet-5-5`) para tareas de producción que requieran fiabilidad y matices ($2 / $10 por MTok, contexto de 1M).

## El Especialista Opus
Usa **Claude Opus 5.5** (`claude-opus-5-5`) para:
- Programación agéntica de larga duración y trabajo de conocimiento.
- Generación de datos (crear datos de entrenamiento para Haiku).
- Razonamiento complejo en el que Sonnet falla.

## La Frontera Fable
Usa **Claude Fable 5.1** (`claude-fable-5-1`) solo para el trabajo más difícil y de largo horizonte, o cuando Opus 5.5 con mayor esfuerzo aún no supera tus evaluaciones.

## Ajusta `effort` antes de cambiar de modelo
`output_config.effort` (`low` a `max`) equilibra la minuciosidad frente al gasto de tokens dentro de un mismo modelo. Mide con peticiones reales, ajusta por ruta y evalúa el **coste por tarea completada**, no por petición. Un solo modelo también implica un único espacio de caché de prompts.

## Próximos Pasos
- [Estrategias de Caché](08_estrategias_cache.md).
- [Guía de coste e inteligencia](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence).
