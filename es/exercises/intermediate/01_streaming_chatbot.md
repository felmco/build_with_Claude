# Ejercicio 6: Chatbot en Streaming

## 🎯 Objetivo
Construye un chatbot interactivo con respuestas en streaming y gestión de historial de conversación.

## ⏱️ Tiempo
45 minutos

## 📚 Requisitos Previos
- Completado ejercicios de principiante
- Comprensión de respuestas en streaming
- Completado [Módulo 2: Fundamentos de Streaming](../../modules/module2_core_api/04_streaming_basics.md)

## 🎓 Nivel de Dificultad
⭐⭐ Intermedio

## 📝 Instrucciones

### Parte 1: Streaming Básico
Crea un chatbot que transmita respuestas en tiempo real.

**Requisitos**:
- Transmitir respuestas carácter por carácter
- Mostrar texto inmediatamente a medida que llega
- Mostrar un prompt para entrada del usuario
- Manejar comandos de salida (salir, exit)

### Parte 2: Historial de Conversación
Añade historial de conversación para mantener el contexto.

**Requisitos**:
- Almacenar todos los mensajes (usuario y asistente)
- Enviar historial con cada nueva petición
- Mostrar número de conversación
- Permitir revisar historial de conversación

### Parte 3: UX Mejorada
Añade mejoras de experiencia de usuario.

**Requisitos**:
- Mostrar indicador de "pensando" mientras espera
- Mostrar uso de tokens después de cada respuesta
- Añadir código de colores para usuario vs Claude
- Manejar interrupciones de teclado con gracia

### Parte 4: Guardar Conversaciones
Permite a los usuarios guardar conversaciones en archivo.

**Requisitos**:
- Guardar al comando (/guardar)
- Incluir marcas de tiempo
- Formatear agradablemente
- Confirmar ubicación de guardado

## 💻 Código de Inicio

```python
#!/usr/bin/env python3
"""Ejercicio 6: Chatbot en Streaming"""

from anthropic import Anthropic
from typing import List, Dict

class StreamingChatbot:
    """Chatbot interactivo en streaming"""

    def __init__(self):
        # TODO: Inicializar cliente e historial de conversación
        pass

    def chat(self, user_message: str):
        """Enviar mensaje y transmitir respuesta"""
        # TODO: Añadir mensaje de usuario al historial
        # TODO: Transmitir respuesta de Claude
        # TODO: Añadir respuesta al historial
        pass

    def run(self):
        """Ejecutar el bucle del chatbot"""
        # TODO: Implementar bucle interactivo
        pass

def main():
    bot = StreamingChatbot()
    bot.run()

if __name__ == "__main__":
    main()
```

## ✅ Salida Esperada

```
╔══════════════════════════════════════════════════════════╗
║          Chatbot en Streaming con Historial              ║
║  Escribe 'salir' para salir | '/guardar' para guardar    ║
╚══════════════════════════════════════════════════════════╝

[Turno 1]
Tú: Cuéntame una historia corta sobre un robot

Claude: ⏳ Pensando...

Claude: Érase una vez un pequeño robot de limpieza llamado Dusty
que soñaba con explorar el espacio. Un día, Dusty fue cargado accidentalmente
en una nave espacial y pudo ver las estrellas después de todo. Aunque significaba
dejar la Tierra para siempre, Dusty limpiaba felizmente la nave mientras miraba
galaxias lejanas, viviendo finalmente su sueño.

📊 Tokens: 87 | ⏱️  Tiempo: 2.3s

[Turno 2]
Tú: ¿Cuál era el nombre del robot?

Claude: ⏳ Pensando...

Claude: El nombre del robot era Dusty.

📊 Tokens: 12 | ⏱️  Tiempo: 0.5s

[Turno 3]
Tú: /guardar

💾 Conversación guardada en: conversation_2026-01-14_15-30.txt
```

## 🧪 Casos de Prueba

1. **Prueba 1**: Streaming básico
   - Entrada: "Cuenta hasta 5"
   - Esperado: Números aparecen uno a uno

2. **Prueba 2**: Mantenimiento de contexto
   - Entrada: "Mi nombre es Alicia"
   - Entrada: "¿Cuál es mi nombre?"
   - Esperado: "Tu nombre es Alicia"

3. **Prueba 3**: Respuesta larga
   - Entrada: "Escribe un párrafo sobre Python"
   - Esperado: Texto se transmite suavemente

4. **Prueba 4**: Interrupción
   - Empieza respuesta, pulsa Ctrl+C
   - Esperado: Manejo elegante

5. **Prueba 5**: Guardar conversación
   - Ten una conversación corta
   - Escribe "/guardar"
   - Esperado: Archivo creado exitosamente

## 🎁 Pistas

<details>
<summary>Pista 1: Implementación de streaming</summary>

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=conversation
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
</details>

<details>
<summary>Pista 2: Gestionando historial de conversación</summary>

```python
self.conversation = []

# Añadir mensaje de usuario
self.conversation.append({
    "role": "user",
    "content": user_message
})

# Después de transmitir, añadir mensaje de asistente
self.conversation.append({
    "role": "assistant",
    "content": response_text
})
```
</details>

<details>
<summary>Pista 3: Manejo de errores</summary>

```python
try:
    # Código de streaming
except KeyboardInterrupt:
    print("\n\n⚠️  Interrumpido por el usuario")
    return
except Exception as e:
    print(f"\n❌ Error: {e}")
```
</details>

## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
#!/usr/bin/env python3
"""Ejercicio 6: Chatbot en Streaming - Solución"""

from anthropic import Anthropic
from typing import List, Dict
import time
from datetime import datetime
import sys

class StreamingChatbot:
    """Chatbot interactivo en streaming con historial"""

    def __init__(self):
        self.client = Anthropic()
        self.conversation: List[Dict] = []
        self.model = "claude-sonnet-4-5-20250929"
        self.turn_count = 0

    def chat(self, user_message: str) -> bool:
        """
        Enviar mensaje y transmitir respuesta
        Devuelve False si es comando especial, True de lo contrario
        """
        # Manejar comandos especiales
        if user_message.lower() in ['salir', 'exit', 'quit', 'q']:
            return False

        if user_message.startswith('/'):
            self._handle_command(user_message)
            return True

        # Incrementar contador de turnos
        self.turn_count += 1

        # Añadir mensaje de usuario
        self.conversation.append({
            "role": "user",
            "content": user_message
        })

        # Mostrar indicador de pensando
        print("\nClaude: ⏳ Pensando...\n")
        time.sleep(0.5)  # Breve pausa por efecto
        print("\rClaude: ", end="", flush=True)

        # Transmitir respuesta
        start_time = time.time()
        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=1024,
                messages=self.conversation
            ) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)

                # Obtener mensaje final
                final_message = stream.get_final_message()

            # Calcular estadísticas
            elapsed_time = time.time() - start_time
            output_tokens = final_message.usage.output_tokens

            # Añadir al historial
            self.conversation.append({
                "role": "assistant",
                "content": final_message.content[0].text
            })

            # Mostrar estadísticas
            print(f"\n\n📊 Tokens: {output_tokens} | ⏱️  Tiempo: {elapsed_time:.1f}s")

        except KeyboardInterrupt:
            print("\n\n⚠️  Respuesta interrumpida por el usuario")
        except Exception as e:
            print(f"\n❌ Error: {e}")

        return True

    def _handle_command(self, command: str):
        """Manejar comandos especiales"""
        if command == '/guardar':
            self._save_conversation()
        elif command == '/historial':
            self._show_history()
        elif command == '/limpiar':
            self.conversation = []
            self.turn_count = 0
            print("✅ Conversación limpiada")
        else:
            print(f"Comando desconocido: {command}")
            print("Comandos disponibles: /guardar, /historial, /limpiar")

    def _save_conversation(self):
        """Guardar conversación en archivo"""
        if not self.conversation:
            print("No hay conversación para guardar")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"conversation_{timestamp}.txt"

        with open(filename, 'w') as f:
            f.write("="*60 + "\n")
            f.write("Conversación con Claude\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")

            for i, msg in enumerate(self.conversation, 1):
                role = "Tú" if msg["role"] == "user" else "Claude"
                f.write(f"[{i}] {role}: {msg['content']}\n\n")

        print(f"💾 Conversación guardada en: {filename}")

    def _show_history(self):
        """Mostrar historial de conversación"""
        if not self.conversation:
            print("No hay historial de conversación")
            return

        print("\n" + "="*60)
        print("Historial de Conversación")
        print("="*60)

        for i, msg in enumerate(self.conversation, 1):
            role = "Tú" if msg["role"] == "user" else "Claude"
            content = msg["content"]
            # Truncar mensajes largos
            if len(content) > 100:
                content = content[:97] + "..."
            print(f"[{i}] {role}: {content}")

        print("="*60)

    def run(self):
        """Ejecutar el bucle del chatbot"""
        # Encabezado
        print("╔" + "═"*58 + "╗")
        print("║" + " "*10 + "Chatbot en Streaming con Historial" + " "*14 + "║")
        print("║" + "  Escribe 'salir' para cerrar | '/guardar' para guardar" + " "*1 + "║")
        print("╚" + "═"*58 + "╝")
        print()

        while True:
            try:
                # Obtener entrada de usuario
                print(f"\n[Turno {self.turn_count + 1}]")
                user_input = input("Tú: ").strip()

                if not user_input:
                    continue

                # Procesar mensaje
                continue_chat = self.chat(user_input)
                if not continue_chat:
                    print("\n¡Adiós! 👋")
                    break

            except KeyboardInterrupt:
                print("\n\n⚠️  Interrumpido. Escribe 'salir' para cerrar.")
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Ejecutar el chatbot"""
    bot = StreamingChatbot()
    bot.run()

if __name__ == "__main__":
    main()
```
</details>

## 🚀 Extensiones

### Extensión 1: Prompts del Sistema
Añade capacidad de personalizar la personalidad de Claude con el comando /sistema

### Extensión 2: Múltiples Modelos
Permite cambiar entre Haiku, Sonnet y Opus con el comando /modelo

### Extensión 3: Presupuesto de Tokens
Establece un presupuesto de tokens y advierte cuando se acerque al límite

### Extensión 4: Formatos de Exportación
Soporta múltiples formatos de exportación (JSON, Markdown, HTML)

### Extensión 5: Modo de Voz
Integra texto-a-voz para las respuestas de Claude

### Extensión 6: Interfaz Web
Construye una UI web simple usando Flask o Streamlit

## 📖 Resultados de Aprendizaje

Después de completar este ejercicio, deberías entender:
- ✅ Cómo implementar respuestas en streaming
- ✅ Cómo gestionar historial de conversación
- ✅ Cómo crear aplicaciones CLI interactivas
- ✅ Cómo manejar errores elegantemente
- ✅ Cómo implementar comandos especiales
- ✅ E/S de Archivos para guardar conversaciones

## 🔗 Lecciones Relacionadas
- [Fundamentos de Streaming](../../modules/module2_core_api/04_streaming_basics.md)
- [Gestionando Conversaciones](../../modules/module2_core_api/03_conversations.md)
- [Manejo de Errores](../../modules/module2_core_api/11_error_handling.md)

## 💡 Desafíos Bonus

1. **Añadir Soporte Markdown**: Renderiza el markdown de Claude en la terminal
2. **Implementar Deshacer**: Permite a los usuarios deshacer el último mensaje
3. **Añadir Búsqueda**: Busca a través del historial de conversación
4. **Multi-Sesión**: Soporta múltiples hilos de conversación
5. **Añadir Analítica**: Rastrea y muestra estadísticas de uso

## 🎉 Finalización

¡Gran trabajo! Has construido un chatbot en streaming completamente funcional. Siguiente: [Ejercicio 7: Analizador de Imágenes](./02_image_analyzer.md)

---

**¿Necesitas ayuda?** Revisa [Fundamentos de Streaming](../../modules/module2_core_api/04_streaming_basics.md)
