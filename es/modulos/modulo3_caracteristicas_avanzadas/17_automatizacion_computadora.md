# 3.6 Estrategias de Automatización de Computadora

## El Bucle del Agente

```python
tools = [{"type": "computer_toolset_20260801"}]
messages = [{"role": "user", "content": "Open the settings page and enable dark mode"}]

MAX_STEPS = 50  # limita siempre el bucle

for _ in range(MAX_STEPS):
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=4096,
        tools=tools,
        messages=messages,
    )
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason != "tool_use":
        break  # tarea hecha (o detenida por otro motivo)

    results = []
    for block in response.content:
        if block.type != "tool_use":
            continue
        # La acción es el nombre del bloque (screenshot, left_click, type, ...)
        output = execute_on_vm(block.name, block.input)  # tu código de sandbox
        content = (
            [{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": output}}]
            if block.name in ("screenshot", "zoom")
            else [{"type": "text", "text": "OK"}]
        )
        results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "toolset_name": "computer",  # obligatorio en cada resultado
            "content": content,
        })

    # Devuelve un tool_result por cada tool_use, todos en un único mensaje de usuario
    messages.append({"role": "user", "content": results})
```

`execute_on_vm` es tu propio código que realiza la acción en la sandbox (y, para `screenshot` y `zoom`, devuelve un PNG en base64). Claude puede solicitar varias acciones en un mismo turno, así que procesa cada bloque `tool_use`.

## Mejores Prácticas
1. **Resolución de Pantalla:** Más baja es más barata/rápida (ej. de 1024x768 a 1080p). Las capturas que devuelves ya deben ajustarse a los límites de imagen del modelo; la API rechaza las imágenes de `tool_result` demasiado grandes en lugar de reducirlas, así que redimensiónalas tú mismo.
2. **Capturas de Pantalla:** Claude solicita un `screenshot` cuando necesita ver la pantalla; devuelve la imagen para las llamadas `screenshot` y `zoom` y un breve resultado de texto para las demás acciones. Mantén las capturas pequeñas, ya que se acumulan en la conversación.
3. **Seguridad:** Ejecuta en un contenedor aislado con privilegios mínimos. ¡No le des acceso a tu banca personal! Las páginas web y documentos en pantalla pueden contener inyección de prompt, así que mantén a una persona en el bucle para acciones sensibles.

## Limitaciones
- **Latencia:** Es lento (captura -> subida -> procesar -> responder -> acción).
- **Video:** Sin flujo de video en tiempo real; Claude trabaja a partir de capturas de pantalla discretas.

## ¡Felicidades!
Has completado el Módulo 3. Ahora eres un usuario avanzado de la API de Claude.

## Siguiente Módulo
Procede al [Módulo 4: Construcción de Aplicaciones](../modulo4_aplicaciones/README.md) para ponerlo todo junto.
