# Ejercicio 3: Procesamiento por Lotes

## 🎯 Objetivo
Aprender a usar la API de Message Batches para procesar grandes volúmenes de solicitudes de manera asíncrona y más económica.

## ⏱️ Tiempo
60+ minutos

## 📚 Requisitos Previos
- Conceptos asíncronos básicos
- Módulo 3: Procesamiento por Lotes

## 🎓 Nivel de Dificultad
⭐⭐⭐ Avanzado

## 📝 Instrucciones

### Parte 1: Construir las Solicitudes
Crea una lista con una solicitud por cada elemento de entrada, cada una con un `custom_id` único y sus `params` (model, max_tokens, messages).

### Parte 2: Enviar Lote
Usa `client.messages.batches.create(requests=...)` para crear el lote (no hay que subir ningún archivo).

### Parte 3: Comprobar Estado
Sondea (poll) el estado del lote hasta que `processing_status == "ended"`.

### Parte 4: Recuperar Resultados
Itera `client.messages.batches.results(batch.id)` y gestiona cada resultado según `entry.result.type`.

## 💻 Código de Inicio

```python
import time
import anthropic

client = anthropic.Anthropic()

# TODO: construye una solicitud por elemento de entrada, cada una con un custom_id único
requests = []

batch = client.messages.batches.create(requests=requests)
while batch.processing_status != "ended":
    time.sleep(30)
    batch = client.messages.batches.retrieve(batch.id)

for entry in client.messages.batches.results(batch.id):
    # TODO: gestiona entry.result.type: "succeeded", "errored", "canceled", "expired"
    ...
```

## ✅ Salida Esperada

ID del lote creado y, finalmente, los resultados procesados.

## 🎁 Pistas

Usa `client.messages.batches.create(requests=[{"custom_id": ..., "params": {...}}])`, sondea hasta que `processing_status == "ended"` y luego itera `client.messages.batches.results(batch.id)`. Los resultados pueden llegar en cualquier orden, así que relaciónalos por `custom_id`. Los lotes se facturan al 50% de los precios normales.

## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
# Esquema de referencia: consulta las lecciones de Procesamiento por Lotes del Módulo 3 para un ejemplo completo.
# Gestiona cada resultado según entry.result.type ("succeeded" -> entry.result.message,
# "errored"/"expired"/"canceled" -> recopila el custom_id y reenvíalo en un nuevo lote).
```
</details>

## 📖 Resultados de Aprendizaje

- ✅ Optimización de costes (50% de descuento)
- ✅ Manejo de flujos de trabajo asíncronos
