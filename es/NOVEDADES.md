# Novedades de Esta Revisión (octubre de 2026)

## Modelos

| Ejemplos antiguos | Usa ahora |
|-------------------|-----------|
| `claude-sonnet-4-5-20250929` | `claude-sonnet-5-5` ($2 / $10 por MTok, contexto 1M) |
| `claude-opus-4-5-20251101`, `claude-opus-4-1-20250805` | `claude-opus-5-5` ($4 / $20, contexto 1M) |
| `claude-3-5-haiku-20241022`, `claude-3-7-sonnet-20250219` | `claude-haiku-4-5` ($1 / $5, 200K) o `claude-sonnet-5-5` |
| (nuevo) | `claude-fable-5-1` ($10 / $50) para el trabajo más difícil y de largo horizonte |

Los IDs ahora no llevan fecha y son snapshots fijos: no les añadas sufijos de fecha.

## Cambios de comportamiento de la API

- **Pensamiento**: pensamiento adaptativo + `output_config.effort` sustituye a `budget_tokens` en los modelos 5.x (Haiku 4.5 conserva `budget_tokens`).
- **Muestreo**: `temperature`, `top_p`, `top_k` no predeterminados devuelven 400 en Fable 5.1, Opus 5.5 y Sonnet 5.5.
- **Prefill eliminado**: terminar `messages` con un turno `assistant` devuelve 400; usa salidas estructuradas.
- **API de Archivos GA**: `client.files.*`, sin cabecera beta.
- **Uso de computadora**: `computer_toolset_20260801`, sin cabecera beta.
- **Límites**: 1M de contexto y 128K de salida en Sonnet/Opus/Fable; lee los límites de la Models API.
- Tablas de precios y caché actualizadas.

## Nuevo en el repositorio

- [REFERENCIAS.md](./REFERENCIAS.md) y [MODS.md](./MODS.md) (mod "Consumo" en [`../mods/consumo`](../mods/consumo)).

## Pendiente para la próxima revisión

Nada importante pendiente. El [Módulo 6](./modulos/modulo6_caracteristicas_plataforma/README.md) cubre Managed Agents, Claude Agent SDK, herramientas de servidor (búsqueda web, ejecución de código), fallbacks por rechazo, presupuestos de tarea y Admin API. Los cuatro proyectos siguen siendo esqueletos.
