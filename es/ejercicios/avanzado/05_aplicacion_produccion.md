# Ejercicio 5: Aplicación de Producción

## 🎯 Objetivo
Simular un entorno de producción real añadiendo robustez a tu aplicación Claude.

## ⏱️ Tiempo
45 minutos

## 📚 Requisitos Previos
- Todos los módulos anteriores

## 🎓 Nivel de Dificultad
⭐⭐⭐ Avanzado

## 📝 Instrucciones

### Parte 1: Logging Estructurado
Implementa logs que registren tokens de entrada/salida, latencia y modelo usado para cada llamada.

### Parte 2: Manejo de Errores y Reintentos
Usa la biblioteca `tenacity` o lógica propia para reintentar llamadas fallidas con backoff exponencial.

### Parte 3: Moderación / Guardrails
Implementa una comprobación posterior a la generación para asegurar que la respuesta no contenga contenido prohibido.

## 💻 Código de Inicio

```python
import logging
import time
from anthropic import Anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prod-app")

def llamada_segura(prompt):
    start = time.time()
    try:
        # TODO: Llamada API
        pass
    except Exception as e:
        logger.error(f"Fallo: {e}")
        # TODO: Lógica de reintento
    finally:
        duration = time.time() - start
        logger.info(f"Duración: {duration}s")

```

## 📖 Resultados de Aprendizaje

- ✅ Observabilidad
- ✅ Resiliencia
- ✅ Seguridad de IA
