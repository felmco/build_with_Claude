# 3.5 Casos de Uso de Pensamiento

## ¿Cuándo usar Pensamiento Extendido?

1. **Matemáticas Complejas y Lógica:** "Resuelve este acertijo." "Calcula la trayectoria..."
2. **Programación:** "Refactoriza esta base de código heredada." (El pensamiento permite planificar la estructura primero).
3. **Escritura Creativa:** "Escribe un esquema de novela de misterio." (Planificación de personajes y giros de la trama).
4. **Seguridad y Política:** "Analiza si este contenido viola nuestros complejos Términos de Servicio."

## ¿Cuándo NO usarlo?
- Saludos simples ("Hola").
- Recuperación de hechos ("Capital de Francia").
- Aplicaciones de baja latencia (Chatbots para consultas simples). Reduce el nivel de esfuerzo o, en Sonnet 5.5, usa `{"type": "between_tools"}`.

## Controlando la Profundidad
En Fable 5.1, Opus 5.5 y Sonnet 5.5 no defines un presupuesto de tokens (`budget_tokens` devuelve 400). Claude decide cuánto pensar, y tú lo guías con `output_config={"effort": ...}`:
- **low / medium:** Comprobaciones rápidas y tareas rutinarias.
- **high:** Programación y análisis estándar.
- **xhigh / max:** Investigación profunda y los problemas más difíciles. Espera más coste y latencia; usa streaming y un `max_tokens` grande.

Solo Claude Haiku 4.5 sigue usando un presupuesto manual (`{"type": "enabled", "budget_tokens": N}`, mínimo 1024, menor que `max_tokens`). Los tokens de pensamiento se facturan como tokens de salida.

## Próximos Pasos
- Aprende sobre la característica beta [Uso de Computadora](16_uso_computadora.md).
