# Ejercicio 3: Uso Básico de Herramientas

## 🎯 Objetivo
Implementa una herramienta calculadora que Claude pueda llamar.

## ⏱️ Tiempo
40 minutos

## 📚 Requisitos Previos
- Módulo 3 Uso de Herramientas

## 🎓 Nivel de Dificultad
⭐⭐ Intermedio

## 📝 Instrucciones

### Parte 1: Definir Herramienta
Define el esquema JSON para una herramienta `calcular` (suma, resta, mult, div).

### Parte 2: Analizar Respuesta
Comprueba si Claude quiere usar la herramienta.

### Parte 3: Ejecutar y Devolver
Ejecuta la matemática, devuelve el resultado a Claude.

## 💻 Código de Inicio

```python
tools = [{
    "name": "calcular",
    "description": "Realizar matemáticas",
    "input_schema": {
        "type": "object",
        "properties": {
            "op": {"type": "string", "enum": ["suma", "resta"]},
            "a": {"type": "number"},
            "b": {"type": "number"}
        }
    }
}]

```

## ✅ Salida Esperada

```
Claude pide usar herramienta, tú imprimes resultado, Claude responde al usuario.
```

## 🧪 Casos de Prueba

¿Cuánto es 50 + 20?

## 🎁 Pistas

<details>
<summary>Pista 1: Razón de Parada</summary>

Comprueba `message.stop_reason == 'tool_use'`
</details>


## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
# Ver ejemplos del Módulo 3
```
</details>

## 🚀 Extensiones

Añade funciones matemáticas más complejas.

## 📖 Resultados de Aprendizaje

- ✅ Llamada a funciones
- ✅ Definiciones de herramientas

## 🔗 Lecciones Relacionadas
- [Conceptos Básicos de Uso de Herramientas](../../modulos/modulo3_caracteristicas_avanzadas/01_conceptos_basicos_uso_herramientas.md)

## ❓ Problemas Comunes

Esquema JSON inválido.

## 🎉 Finalización

¡Felicidades! Has completado el ejercicio.
