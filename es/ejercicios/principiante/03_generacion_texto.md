# Ejercicio 3: Generación de Texto y Resumen

## 🎯 Objetivo
Usa Claude para tareas comunes de texto: resumen, expansión y reescritura.

## ⏱️ Tiempo
20 minutos

## 📚 Requisitos Previos
- Conocimiento básico de la API

## 🎓 Nivel de Dificultad
⭐ Principiante

## 📝 Instrucciones

### Parte 1: Resumen
Toma un párrafo largo de texto y pide a Claude que lo resuma en una frase.

### Parte 2: Ajuste de Tono
Pide a Claude que reescriba un correo electrónico casual para que sea profesional.

### Parte 3: Extracción
Extrae puntos clave (nombres, fechas) de un texto.

## 💻 Código de Inicio

```python
from anthropic import Anthropic

client = Anthropic()

texto_largo = """
Claude es una familia de grandes modelos de lenguaje desarrollados por Anthropic. 
El primer modelo fue lanzado en marzo de 2023. Los modelos Claude son conocidos 
por su seguridad y alta ventana de contexto.
"""

def resumir(texto):
    # TODO: Pedir a Claude que resuma
    pass

def hacer_profesional(texto):
    # TODO: Pedir a Claude que reescriba
    pass

def main():
    print(resumir(texto_largo))

if __name__ == "__main__":
    main()
```

## ✅ Salida Esperada

```
Resumen: Anthropic lanzó la familia Claude de modelos de IA seguros y de alto contexto a partir de marzo de 2023.
```

## 🧪 Casos de Prueba

Comprobar calidad específica de salida.

## 🎁 Pistas

<details>
<summary>Pista 1: Ingeniería de Prompts</summary>

Prepara tu cadena de prompt concatenando instrucciones + texto.
</details>


## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
from anthropic import Anthropic

client = Anthropic()

def preguntar_claude(prompt):
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def main():
    texto = "Oye jefe, no voy a ir hoy. Enfermo."
    
    prompt = f"Reescribe el siguiente correo para que sea profesional:\n\n{texto}"
    print(preguntar_claude(prompt))

if __name__ == "__main__":
    main()
```
</details>

## 🚀 Extensiones

Intenta traducir texto a otro idioma.

## 📖 Resultados de Aprendizaje

- ✅ Manipulación de prompts
- ✅ Tareas de procesamiento de texto

## 🔗 Lecciones Relacionadas
- [Ingeniería de Prompts](../../modulos/modulo5_optimizacion/01_ingenieria_prompts.md)

## ❓ Problemas Comunes

Ninguno

## 🎉 Finalización

¡Felicidades! Has completado el ejercicio. Avanza al [Ejercicio 4: Sistema QA](04_sistema_qa.md)
