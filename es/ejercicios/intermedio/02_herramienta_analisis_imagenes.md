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
# TODO: deduce el media_type a partir de la extensión del archivo (image/jpeg, image/png, image/gif, image/webp)
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
import base64
import mimetypes
import sys

import anthropic

client = anthropic.Anthropic()

def codificar_imagen(ruta_imagen):
    with open(ruta_imagen, "rb") as archivo_imagen:
        return base64.b64encode(archivo_imagen.read()).decode("utf-8")

def describir(ruta_imagen, pregunta="¿Qué hay en esta imagen?"):
    media_type = mimetypes.guess_type(ruta_imagen)[0]
    if media_type not in ("image/jpeg", "image/png", "image/gif", "image/webp"):
        raise ValueError(f"Tipo de imagen no soportado: {media_type}")
    message = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": codificar_imagen(ruta_imagen)}},
                {"type": "text", "text": pregunta},
            ],
        }],
    )
    return message.content[0].text

if __name__ == "__main__":
    print(describir(sys.argv[1]))
```</details>

## 🚀 Extensiones

Haz preguntas específicas sobre la imagen.

## 📖 Resultados de Aprendizaje

- ✅ Capacidades multimodales
- ✅ Manejo de imágenes

## 🔗 Lecciones Relacionadas
- [Visión](../../modulos/modulo2_api_nucleo/06_vision_imagenes.md)

## ❓ Problemas Comunes

Tamaño de archivo demasiado grande: la API rechaza las imágenes de más de 5 MB (y las imágenes muy grandes se reducen), así que redimensiona antes de enviar. Asegúrate de que `media_type` coincida con el formato real del archivo.

## 🎉 Finalización

¡Felicidades! Has completado el ejercicio.
