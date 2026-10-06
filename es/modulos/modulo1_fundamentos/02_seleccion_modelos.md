# 1.1 Eligiendo el Modelo Correcto

Seleccionar el modelo óptimo de Claude para tu aplicación implica equilibrar tres consideraciones clave: **capacidades**, **velocidad** y **coste**.

## Matriz de Decisión

| Característica | Claude Haiku 4.5 | Claude Sonnet 5.5 | Claude Opus 5.5 | Claude Fable 5.1 |
|----------------|------------------|-------------------|-----------------|------------------|
| **Inteligencia** | Casi de frontera, rápido | Alta, equilibrado | Muy alta, programación agéntica | La más alta |
| **Velocidad** | ⚡⚡⚡ Muy Rápido | ⚡⚡ Rápido | ⚡ Moderado | 🐢 Más lento |
| **Precio (entrada/salida por MTok)** | $1 / $5 | $2 / $10 | $4 / $20 | $10 / $50 |
| **Contexto** | 200K | 1M | 1M | 1M |

## Cuándo Elegir Cada Modelo

### 🚀 Claude Haiku 4.5
**Úsalo cuando:**
- La velocidad es crítica (chat en tiempo real, autocompletado)
- El volumen es alto (procesamiento de millones de documentos)
- El coste es una restricción importante
- Las tareas son directas (clasificación, extracción, Q&A simple)

**Escenarios de Ejemplo:**
- Moderación de contenido
- Análisis de logs
- Consultas simples de soporte al cliente
- Traducción de texto simple

### ⭐ Claude Sonnet 5.5 (Inicio Recomendado)
**Úsalo cuando:**
- Necesitas un equilibrio entre alta inteligencia y velocidad
- Estás construyendo aplicaciones empresariales
- Necesitas fuertes capacidades de código o razonamiento
- No estás seguro de por dónde empezar

**Escenarios de Ejemplo:**
- Asistentes de código
- RAG (Generación Aumentada por Recuperación)
- Extracción de datos de documentos complejos
- Generación de copy de marketing
- Soporte al cliente complejo

### 🧠 Claude Opus 5.5
**Úsalo cuando:**
- Necesitas la calidad más alta posible
- La tarea implica razonamiento complejo o escritura creativa
- La velocidad y el coste son menos importantes que la precisión
- Estás manejando investigación abierta o estrategia

**Escenarios de Ejemplo:**
- Análisis estratégico
- Escritura creativa (novelas, guiones)
- Demostraciones matemáticas complejas
- Síntesis de investigación
- Apoyo a decisiones de alto riesgo

### 🔭 Claude Fable 5.1
**Úsalo cuando:**
- Tus evaluaciones con Opus 5.5 y mayor `effort` aún no alcanzan
- El trabajo es autónomo y de largo horizonte (horas, no minutos)
- El coste de un error es alto

Una sola petición en tareas difíciles puede durar minutos: usa streaming y planifica los timeouts.

## Estrategia para la Selección

1. **Empieza con Sonnet**: Maneja bien la mayoría de los casos de uso.
2. **Evalúa el Rendimiento**: Comprueba si las respuestas cumplen con tus estándares de calidad.
3. **Optimiza**:
   - Si Sonnet es demasiado lento o caro, prueba **Haiku**.
   - Si a Sonnet le falta matiz o profundidad de razonamiento, prueba **Opus 5.5** (o sube primero el `effort`).
   - Si Opus 5.5 con esfuerzo alto sigue sin bastar, prueba **Fable 5.1**.
4. **Ajusta `effort`** antes de cambiar de modelo: `low` para chat y sub-agentes, `medium`/`high` para trabajo agéntico. Opus 5.5 usa `medium` por defecto.

## Patrón de Código para Selección de Modelos

Puedes hacer tu código flexible parametrizando la elección del modelo:

```python
import os
from anthropic import Anthropic

# Definir constantes de modelo
MODEL_HAIKU = "claude-haiku-4-5"
MODEL_SONNET = "claude-sonnet-5-5"
MODEL_OPUS = "claude-opus-5-5"
MODEL_FABLE = "claude-fable-5-1"  # problemas más difíciles

client = Anthropic()

def generate_response(prompt, task_type="general"):
    """
    Selecciona el modelo basado en la complejidad de la tarea.
    """
    if task_type == "simple":
        model = MODEL_HAIKU
    elif task_type == "complex":
        model = MODEL_OPUS
    else:
        model = MODEL_SONNET

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

## Próximos Pasos
- Confirma siempre los IDs y límites en la [Visión general de modelos](https://platform.claude.com/docs/en/about-claude/models/overview).
- Aprende sobre [Precios y Límites del Modelo](03_precios_limites.md) para calcular costes.
