# Ejercicio 2: Chatbot Simple

## 🎯 Objetivo
Construye un bucle interactivo que permita una conversación continua con Claude.

## ⏱️ Tiempo
20 minutos

## 📚 Requisitos Previos
- Python 3.7+ instalado
- SDK de Anthropic instalado
- Clave API configurada

## 🎓 Nivel de Dificultad
⭐ Principiante

## 📝 Instrucciones

### Parte 1: El Bucle
Crea un bucle `while True` que pida continuamente la entrada del usuario.

### Parte 2: Enviando Mensajes
Envía la entrada del usuario a Claude e imprime la respuesta.

### Parte 3: Condición de Salida
Permite al usuario escribir 'salir' o 'exit' para terminar el programa limpiamente.

### Parte 4: Contexto (Opcional por ahora)
Para este ejercicio de principiante estricto, no necesitas mantener el historial (haremos eso en Intermedio), pero intenta notar que Claude no recuerda mensajes anteriores en esta implementación simple de bucle.

## 💻 Código de Inicio

```python
import os
from anthropic import Anthropic

client = Anthropic()

def main():
    print("Chatbot Simple (escribe 'salir' para terminar)")
    
    while True:
        # TODO: Obtener entrada del usuario
        
        # TODO: Comprobar condición de salida
        
        # TODO: Enviar mensaje a Claude
        
        # TODO: Imprimir respuesta
        pass

if __name__ == "__main__":
    main()
```

## ✅ Salida Esperada

```
Chatbot Simple (escribe 'salir' para terminar)
Tú: ¡Hola!
Claude: ¡Hola! ¿Cómo puedo ayudarte hoy?
Tú: salir
¡Adiós!
```

## 🧪 Casos de Prueba

1. **Prueba 1**: Conversación básica
   - Entrada: "Hola"
   - Esperado: Respuesta de Claude

2. **Prueba 2**: Salida
   - Entrada: "salir"
   - Esperado: El programa termina

## 🎁 Pistas

<details>
<summary>Pista 1: Estructura del bucle</summary>

Usa `while True:` y `input()`.
</details>
<details>
<summary>Pista 2: Comprobación de salida</summary>

Usa `if user_input.lower() == 'salir': break`
</details>


## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
import os
from anthropic import Anthropic

def main():
    client = Anthropic()
    print("Chatbot inicializado. Escribe 'salir' para terminar.")

    while True:
        user_input = input("\nTú: ")
        
        if user_input.lower() in ['salir', 'exit']:
            print("¡Adiós!")
            break
            
        try:
            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            print(f"Claude: {message.content[0].text}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
```
</details>

## 🚀 Extensiones

1. Añade un prompt del sistema para darle una personalidad al bot (ej., un pirata).
2. Añade color a la salida.

## 📖 Resultados de Aprendizaje

- ✅ Construcción de bucles interactivos
- ✅ Manejo de entrada de usuario
- ✅ Manejo de errores básico en bucles

## 🔗 Lecciones Relacionadas
- [Primera Llamada a la API](../../modulos/modulo1_fundamentos/07_primera_llamada_api.md)

## ❓ Problemas Comunes

### Problema 1: Bucle Infinito
Si olvidas la declaración break, no podrás salir. Usa Ctrl+C para forzar el cierre.

## 🎉 Finalización

¡Felicidades! Has completado el ejercicio. Avanza al [Ejercicio 3: Generación de Texto](03_generacion_texto.md)
