# Ejercicio 2: Herramienta de Análisis de Imágenes

## 🎯 Objetivo
Envía imágenes a Claude para análisis

## ⏱️ Tiempo
30 minutos

## 📚 Requisitos Previos
- Módulo 2 Visión

## 🎓 Nivel de Dificultad
⭐⭐ Intermedio

## 📝 Instrucciones

### Parte 1: Codificación Base64
Escribe una función auxiliar para codificar un archivo de imagen local a base64.

### Parte 2: Petición de Visión
Envía la imagen base64 a Claude y pide una descripción.

## 💻 Código de Inicio

```python
import base64

def codificar_imagen(ruta_imagen):
    with open(ruta_imagen, "rb") as archivo_imagen:
        return base64.b64encode(archivo_imagen.read()).decode('utf-8')

# TODO: Llamar API con bloque de contenido de imagen
```

## ✅ Salida Esperada

```
Descripción de la imagen.
```

## 🧪 Casos de Prueba

Probar con JPG y PNG.

## 🎁 Pistas

<details>
<summary>Pista 1: Bloque de Contenido</summary>

Usa `type: image` en el contenido del mensaje.
</details>


## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
messages=[{
    "role": "user", 
    "content": [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64_data}},
        {"type": "text", "text": "¿Qué hay en esta imagen?"}
    ]
}]
```
</details>

## 🚀 Extensiones

Haz preguntas específicas sobre la imagen.

## 📖 Resultados de Aprendizaje

- ✅ Capacidades multimodales
- ✅ Manejo de imágenes

## 🔗 Lecciones Relacionadas
- [Visión](../../modulos/modulo2_api_nucleo/06_vision_imagenes.md)

## ❓ Problemas Comunes

Tamaño de archivo demasiado grande (>5MB).

## 🎉 Finalización

¡Felicidades! Has completado el ejercicio.
