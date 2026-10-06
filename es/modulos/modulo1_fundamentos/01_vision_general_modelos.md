# 1.1 Modelos Disponibles y Capacidades

## Introducción
Claude ofrece múltiples modelos, cada uno optimizado para diferentes casos de uso. Entender estos modelos te ayudará a elegir el correcto para tu aplicación.

## Modelos Actuales de Claude (octubre de 2026)

> Verificado con la [Visión general de modelos](https://platform.claude.com/docs/en/about-claude/models/overview). Los modelos cambian con frecuencia: consulta esa página (o la Models API) antes de fijar un ID en tu código.

### Claude Fable 5.1
**ID del modelo**: `claude-fable-5-1`

**Ideal para**:
- El razonamiento más exigente
- Trabajo agéntico autónomo de largo horizonte
- Casos en los que tus evaluaciones con Opus 5.5 y mayor esfuerzo aún no alcanzan

**Características**:
- Modelo más capaz de amplia disponibilidad
- El pensamiento siempre está activo (se controla con `effort`)
- El más lento y caro ($10 / $50 por MTok)

### Claude Opus 5.5
**ID del modelo**: `claude-opus-5-5`

**Ideal para**:
- Programación agéntica de larga duración y trabajo de conocimiento
- Razonamiento y análisis complejos
- Una excelente opción por defecto cuando la calidad importa más

**Características**:
- Pensamiento adaptativo siempre activo; `effort` por defecto: `medium`
- Contexto de 1M tokens, salida máxima de 128K
- $4 / $20 por MTok

### Claude Sonnet 5.5
**ID del modelo**: `claude-sonnet-5-5`

**Ideal para**:
- La mayoría de las aplicaciones en producción
- La mejor combinación de velocidad e inteligencia
- Programación, agentes y trabajo empresarial del día a día

**Características**:
- Rápido, con pensamiento adaptativo (`effort` por defecto: `high`)
- Contexto de 1M tokens, salida máxima de 128K
- $2 / $10 por MTok

**Casos de uso**:
```
✅ Chatbots e IA conversacional
✅ Generación y edición de contenido
✅ Asistencia y revisión de código
✅ Análisis de datos y resúmenes
✅ Automatización de soporte al cliente
```

### Claude Haiku 4.5
**ID del modelo**: `claude-haiku-4-5` (snapshot fijo: `claude-haiku-4-5-20251001`)

**Ideal para**:
- Aplicaciones de alto volumen
- Respuestas en tiempo real
- Sub-agentes y tareas simples
- Proyectos con presupuesto ajustado

**Características**:
- El modelo más rápido, con inteligencia casi de frontera
- Contexto de 200K tokens, salida máxima de 64K
- Usa pensamiento extendido manual (`budget_tokens`), sin parámetro `effort`
- $1 / $5 por MTok

> **Modelos heredados** (aún disponibles): Claude Fable 5, Opus 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 5 y Sonnet 4.6. Los IDs antiguos que aparecen en tutoriales, como `claude-3-5-haiku-20241022` o `claude-sonnet-4-5-20250929`, están en camino de retirada. Consulta [Deprecaciones de modelos](https://platform.claude.com/docs/en/about-claude/model-deprecations).

## Tabla de Comparación de Modelos

| Característica | Haiku 4.5 | Sonnet 5.5 | Opus 5.5 | Fable 5.1 |
|----------------|-----------|------------|----------|-----------|
| Velocidad | ⚡⚡⚡ La más rápida | ⚡⚡ Rápida | ⚡ Moderada | 🐢 Más lenta |
| Precio (entrada / salida por MTok) | $1 / $5 | $2 / $10 | $4 / $20 | $10 / $50 |
| Ventana de contexto | 200K tokens | 1M tokens | 1M tokens | 1M tokens |
| Salida máxima | 64K tokens | 128K tokens | 128K tokens | 128K tokens |
| Pensamiento | Extendido (`budget_tokens`) | Adaptativo | Adaptativo (siempre activo) | Adaptativo (siempre activo) |
| Mejor uso | Alto volumen | Producción | Programación agéntica | Problemas más difíciles |

## Límites de Tokens

Los límites varían según el modelo (tabla anterior). No los des por sentados: consulta la **Models API** (`client.models.retrieve("claude-sonnet-5-5")`), que devuelve `max_input_tokens`, `max_tokens` y un objeto `capabilities`.

## Capacidades del Modelo

### Todos los Modelos Soportan:
- ✅ Generación de texto y conversación
- ✅ Comprensión y generación de código
- ✅ Soporte multi-idioma (Inglés, Español, Francés, Alemán, etc.)
- ✅ Modo JSON para salidas estructuradas
- ✅ Llamada a funciones/herramientas
- ✅ Visión (comprensión de imágenes)
- ✅ Procesamiento de contexto largo

### Características Avanzadas (Específicas del Modelo):
- **Pensamiento adaptativo + `effort`**: Claude decide cuánto pensar; tú controlas la profundidad con `output_config.effort`
- **Uso de Computadora**: Característica beta para automatización de escritorio

## Eligiendo Tu Modelo: Árbol de Decisión Rápida

```
Comienza Aquí
    |
    ├─ ¿Necesitas el razonamiento de más alta calidad? → Usa Opus 5.5
    |
    ├─ ¿Necesitas las respuestas más rápidas? → Usa Haiku 4.5
    |
    ├─ ¿Necesitas el mejor equilibrio? → Usa Sonnet 5.5 ⭐ (Recomendado para la mayoría)
    |
    └─ ¿No estás seguro? → Empieza con Sonnet 5.5, optimiza después
```

## Ejemplo en Python: Comprobando Capacidades del Modelo

```python
from anthropic import Anthropic

client = Anthropic()

# Diccionario de modelos disponibles
MODELS = {
    "haiku": "claude-haiku-4-5",
    "sonnet": "claude-sonnet-5-5",
    "opus": "claude-opus-5-5",
    "fable": "claude-fable-5-1",
}

def test_model(model_name: str, prompt: str):
    """Probar un modelo específico con un prompt"""
    response = client.messages.create(
        model=MODELS[model_name],
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text

# Ejemplo de uso
prompt = "Explain quantum computing in one sentence."

print("Testing Haiku:")
print(test_model("haiku", prompt))

print("\nTesting Sonnet:")
print(test_model("sonnet", prompt))

print("\nTesting Opus:")
print(test_model("opus", prompt))
```

## Mejores Prácticas

1. **Empieza con Sonnet 5.5**: Ofrece el mejor equilibrio para la mayoría de las aplicaciones
2. **Prototipa Primero**: Prueba con Sonnet antes de optimizar costes
3. **Usa Haiku para Escalar**: Una vez que tu aplicación funcione, considera Haiku para tareas de alto volumen
4. **Reserva Opus para Complejidad**: Usa Opus solo cuando Sonnet no cumpla con tus necesidades de calidad
5. **Monitoriza el Rendimiento**: Rastrea métricas de calidad, velocidad y coste para optimizar

## Versiones y Actualizaciones de Modelos

Desde la generación 4.6, los IDs de modelos Claude no llevan fecha y cada uno es un **snapshot fijo** (por ejemplo `claude-sonnet-5-5`). No les añadas sufijos de fecha.
- Elige un modelo actual para trabajo nuevo y planifica según las fechas de retirada de [Deprecaciones de modelos](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- Las plataformas cloud usan sus propios formatos: Amazon Bedrock `anthropic.claude-sonnet-5-5`, Google Cloud `claude-sonnet-5-5`
- Vuelve a ejecutar tus evaluaciones al migrar: valores por defecto como `effort` y el comportamiento del pensamiento cambian entre generaciones ([Guía de migración](https://platform.claude.com/docs/en/about-claude/models/migration-guide))

## Conceptos Erróneos Comunes

❌ **"Opus es siempre mejor"**: No es cierto - Sonnet a menudo rinde igual de bien para la mayoría de las tareas
❌ **"Haiku no puede manejar tareas complejas"**: Puede, solo que no tan bien como Sonnet/Opus
❌ **"Necesitas código diferente para modelos diferentes"**: Misma API, solo cambia el ID del modelo
❌ **"Contexto más grande = mejores resultados"**: No siempre - los prompts enfocados a menudo funcionan mejor

## Referencia Rápida

```python
# Ayudante de selección de modelo
def select_model(task_complexity: str, speed_priority: bool = False, budget_tight: bool = False):
    """Función auxiliar para seleccionar el modelo apropiado"""
    if budget_tight and task_complexity == "simple":
        return "claude-haiku-4-5"
    elif speed_priority and task_complexity != "complex":
        return "claude-haiku-4-5"
    elif task_complexity == "complex":
        return "claude-opus-5-5"
    else:
        return "claude-sonnet-5-5"  # Elección por defecto
```

## Próximos Pasos
- Procede a [Eligiendo el Modelo Correcto](02_seleccion_modelos.md)
- Aprende sobre [Precios y Límites del Modelo](03_precios_limites.md)

## Recursos Adicionales
- [Visión general de modelos](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Elegir un modelo](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- [Precios](https://platform.claude.com/docs/en/about-claude/pricing)
- [Deprecaciones de modelos](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- [Notas de lanzamiento](https://platform.claude.com/docs/en/release-notes/overview)
- [Centro de referencias oficiales](../../REFERENCIAS.md)
