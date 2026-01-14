# 1.1 Modelos Disponibles y Capacidades

## Introducción
Claude ofrece múltiples modelos, cada uno optimizado para diferentes casos de uso. Entender estos modelos te ayudará a elegir el correcto para tu aplicación.

## Modelos Actuales de Claude (2026)

### Claude Opus 4.5
**ID del Modelo**: `claude-opus-4-5-20251101`

**Mejor Para**:
- Tareas de razonamiento complejo
- Generación de código avanzada
- Análisis e investigación detallada
- Tareas que requieren la más alta inteligencia

**Características**:
- Nivel de capacidad más alto
- Opción más costosa
- Tiempos de respuesta más lentos
- Lo mejor para aplicaciones críticas de calidad

**Casos de Uso**:
```
✅ Diseño de arquitectura de software compleja
✅ Resolución de problemas matemáticos avanzados
✅ Análisis detallado de documentos legales o técnicos
✅ Tareas de razonamiento de múltiples pasos
✅ Investigación y planificación estratégica
```

### Claude Sonnet 4.5
**ID del Modelo**: `claude-sonnet-4-5-20250929`

**Mejor Para**:
- La mayoría de las aplicaciones de producción
- Rendimiento y velocidad equilibrados
- Tareas de propósito general
- Soluciones rentables

**Características**:
- Excelente equilibrio entre capacidad y velocidad
- Opción más popular para producción
- Precios moderados
- Tiempos de respuesta rápidos

**Casos de Uso**:
```
✅ Chatbots e IA conversacional
✅ Generación y edición de contenido
✅ Asistencia y revisión de código
✅ Análisis y resumen de datos
✅ Automatización de soporte al cliente
```

### Claude Haiku 3.5
**ID del Modelo**: `claude-3-5-haiku-20241022`

**Mejor Para**:
- Aplicaciones de alto volumen
- Respuestas en tiempo real
- Tareas simples
- Proyectos conscientes del presupuesto

**Características**:
- Tiempos de respuesta más rápidos
- El más rentable
- Menor capacidad que Sonnet/Opus
- Genial para tareas directas

**Casos de Uso**:
```
✅ Tareas de clasificación simple
✅ Sistemas rápidos de Preguntas y Respuestas (Q&A)
✅ Procesamiento por lotes de grandes conjuntos de datos
✅ Aplicaciones de chat en tiempo real
✅ Moderación de contenido simple
```

## Tabla de Comparación de Modelos

| Característica | Haiku 3.5 | Sonnet 4.5 | Opus 4.5 |
|----------------|-----------|------------|----------|
| Velocidad | ⚡⚡⚡ Más Rápido | ⚡⚡ Rápido | ⚡ Moderado |
| Inteligencia | 🧠 Buena | 🧠🧠 Excelente | 🧠🧠🧠 Mejor |
| Coste | 💰 Más Bajo | 💰💰 Moderado | 💰💰💰 Más Alto |
| Ventana de Contexto | 200K tokens | 200K tokens | 200K tokens |
| Mejor Uso | Alto volumen | Producción | Tareas complejas |

## Límites de Tokens

Todos los modelos de Claude soportan:
- **Ventana de Contexto**: 200,000 tokens (~150,000 palabras)
- **Tokens de Salida**: Hasta 8,192 tokens por petición (configurable)

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
- **Pensamiento Extendido**: Disponible en modelos seleccionados para razonamiento complejo
- **Uso de Computadora**: Característica beta para automatización de escritorio

## Eligiendo Tu Modelo: Árbol de Decisión Rápida

```
Comienza Aquí
    |
    ├─ ¿Necesitas el razonamiento de más alta calidad? → Usa Opus 4.5
    |
    ├─ ¿Necesitas las respuestas más rápidas? → Usa Haiku 3.5
    |
    ├─ ¿Necesitas el mejor equilibrio? → Usa Sonnet 4.5 ⭐ (Recomendado para la mayoría)
    |
    └─ ¿No estás seguro? → Empieza con Sonnet 4.5, optimiza después
```

## Ejemplo en Python: Comprobando Capacidades del Modelo

```python
from anthropic import Anthropic

client = Anthropic()

# Diccionario de modelos disponibles
MODELS = {
    "haiku": "claude-3-5-haiku-20241022",
    "sonnet": "claude-sonnet-4-5-20250929",
    "opus": "claude-opus-4-5-20251101"
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

1. **Empieza con Sonnet 4.5**: Ofrece el mejor equilibrio para la mayoría de las aplicaciones
2. **Prototipa Primero**: Prueba con Sonnet antes de optimizar costes
3. **Usa Haiku para Escalar**: Una vez que tu aplicación funcione, considera Haiku para tareas de alto volumen
4. **Reserva Opus para Complejidad**: Usa Opus solo cuando Sonnet no cumpla con tus necesidades de calidad
5. **Monitoriza el Rendimiento**: Rastrea métricas de calidad, velocidad y coste para optimizar

## Versiones y Actualizaciones de Modelos

Los modelos de Claude están versionados con fechas de lanzamiento:
- Ejemplo: `claude-sonnet-4-5-20250929` (lanzado el 29 de Septiembre de 2025)
- Usa siempre la última versión estable para producción
- Las versiones antiguas pueden quedar obsoletas con el tiempo
- Revisa las notas de lanzamiento para cambios importantes

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
        return "claude-3-5-haiku-20241022"
    elif speed_priority and task_complexity != "complex":
        return "claude-3-5-haiku-20241022"
    elif task_complexity == "complex":
        return "claude-opus-4-5-20251101"
    else:
        return "claude-sonnet-4-5-20250929"  # Elección por defecto
```

## Próximos Pasos
- Procede a [Eligiendo el Modelo Correcto](./02_model_selection.md)
- Aprende sobre [Precios y Límites del Modelo](./03_pricing_limits.md)

## Recursos Adicionales
- [Comparación Oficial de Modelos](https://platform.claude.com/docs/en/models/overview)
- [Página de Precios de Anthropic](https://www.anthropic.com/pricing)
- [Notas de Lanzamiento de Modelos](https://platform.claude.com/docs/en/release-notes)
