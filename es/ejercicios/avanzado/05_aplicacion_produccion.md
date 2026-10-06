# Ejercicio 5: Aplicación de Producción

## 🎯 Objetivo
Simular un entorno de producción real añadiendo robustez a tu aplicación Claude.

## ⏱️ Tiempo
60+ minutos

## 📚 Requisitos Previos
- Todos los módulos anteriores

## 🎓 Nivel de Dificultad
⭐⭐⭐ Avanzado

## 📝 Instrucciones

### Parte 1: Logging Estructurado
Implementa logs que registren tokens de entrada/salida, latencia y modelo usado para cada llamada.

### Parte 2: Manejo de Errores y Reintentos
Ajusta los reintentos y timeouts del propio SDK (reintenta automáticamente los errores 429/5xx con backoff exponencial) o usa lógica propia para los casos adicionales.

### Parte 3: Moderación / Guardrails
Implementa una comprobación posterior a la generación para asegurar que la respuesta no contenga contenido prohibido.

## 💻 Código de Inicio

```python
import logging
import time

import anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prod-app")

client = anthropic.Anthropic(max_retries=3, timeout=60.0)

def llamada_segura(prompt):
    start = time.time()
    try:
        # TODO: Llamada API con client.messages.create(model="claude-sonnet-5-5", ...)
        # y registro de usage (tokens de entrada/salida)
        pass
    except (anthropic.RateLimitError, anthropic.APIConnectionError) as e:
        logger.error(f"Fallo transitorio: {e}")
        # TODO: Lógica de reintento adicional
    except anthropic.APIStatusError as e:
        logger.error(f"Error de la API: {e.status_code}")
    finally:
        duration = time.time() - start
        logger.info(f"Duración: {duration}s")

```

## 🎁 Pistas

Cubre: reintentos y timeouts (el SDK reintenta automáticamente los errores 429/5xx; ajusta `max_retries` y `timeout`), el registro de `usage` y de los ids de petición, el prompt caching, el conteo de tokens con `client.messages.count_tokens`, y pruebas/evals.

## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
# Esquema de referencia: consulta el Módulo 5 (manejo de errores, observabilidad, despliegue) y la
# carpeta de proyectos para ver un esqueleto de aplicación completo.
```
</details>

## 📖 Resultados de Aprendizaje

- ✅ Observabilidad
- ✅ Resiliencia
- ✅ Seguridad de IA
