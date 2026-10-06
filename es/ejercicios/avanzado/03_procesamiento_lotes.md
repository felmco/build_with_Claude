# Ejercicio 3: Procesamiento por Lotes

## 🎯 Objetivo
Aprender a usar la API de Message Batches para procesar grandes volúmenes de solicitudes de manera asíncrona y más económica.

## ⏱️ Tiempo
30 minutos

## 📚 Requisitos Previos
- Comprensión de JSONL
- Conceptos asíncronos básicos

## 🎓 Nivel de Dificultad
⭐⭐⭐ Avanzado

## 📝 Instrucciones

### Parte 1: Crear Archivo de Lote
Crea un archivo `.jsonl` donde cada línea es una solicitud de mensaje (custom_id, params, messages).

### Parte 2: Enviar Lote
Usa `client.messages.batches.create` para subir y crear el lote.

### Parte 3: Comprobar Estado
Sondea (poll) el estado del lote hasta que esté completo.

### Parte 4: Recuperar Resultados
Descarga los resultados cuando estén listos.

## 💻 Código de Inicio

```python
# 1. Preparar datos
solicitudes = [
    {"custom_id": "req1", "params": {"model": "claude-haiku-4-5", "max_tokens": 100, "messages": [...]}},
    {"custom_id": "req2", "params": {"model": "claude-haiku-4-5", "max_tokens": 100, "messages": [...]}}
]

# TODO: Escribir a batch.jsonl
# TODO: Subir y Crear Lote
```

## ✅ Salida Esperada

ID del lote creado y eventualmente los resultados procesados.

## 📖 Resultados de Aprendizaje

- ✅ Optimización de costes (50% de descuento)
- ✅ Manejo de flujos de trabajo asíncronos
