# 1.1 Eligiendo el Modelo Correcto

Seleccionar el modelo óptimo de Claude para tu aplicación implica equilibrar tres consideraciones clave: **capacidades**, **velocidad** y **coste**.

## Matriz de Decisión

| Característica | Claude Haiku 3.5 | Claude Sonnet 4.5 | Claude Opus 4.5 |
|----------------|------------------|-------------------|-----------------|
| **Inteligencia** | Buen razonamiento, rápido | Alta inteligencia, equilibrado | Inteligencia máxima |
| **Velocidad** | ⚡⚡⚡ Muy Rápido | ⚡⚡ Rápido | ⚡ Moderado |
| **Coste** | $ | $$ | $$$ |
| **Contexto** | 200K | 200K | 200K |

## Cuándo Elegir Cada Modelo

### 🚀 Claude Haiku 3.5
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

### ⭐ Claude Sonnet 4.5 (Inicio Recomendado)
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

### 🧠 Claude Opus 4.5
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

## Estrategia para la Selección

1. **Empieza con Sonnet**: Maneja bien la mayoría de los casos de uso.
2. **Evalúa el Rendimiento**: Comprueba si las respuestas cumplen con tus estándares de calidad.
3. **Optimiza**:
   - Si Sonnet es demasiado lento o caro, prueba **Haiku**.
   - Si a Sonnet le falta matiz o profundidad de razonamiento, prueba **Opus**.

## Patrón de Código para Selección de Modelos

Puedes hacer tu código flexible parametrizando la elección del modelo:

```python
import os
from anthropic import Anthropic

# Definir constantes de modelo
MODEL_HAIKU = "claude-3-5-haiku-20241022"
MODEL_SONNET = "claude-sonnet-4-5-20250929"
MODEL_OPUS = "claude-opus-4-5-20251101"

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
- Aprende sobre [Precios y Límites del Modelo](03_precios_limites.md) para calcular costes.
