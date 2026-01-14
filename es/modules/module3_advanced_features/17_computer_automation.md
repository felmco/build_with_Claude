# 3.6 Estrategias de Automatización de Computadora

## El Bucle del Agente

```python
while True:
    response = client.beta.messages.create(...)

    if response.stop_reason == "tool_use":
        # Ejecutar acción (clic, escribir, captura de pantalla)
        # Enviar resultado
    else:
        # Tarea hecha
        break
```

## Mejores Prácticas
1. **Resolución de Pantalla:** Más baja es más barata/rápida (ej. 1024x768).
2. **Capturas de Pantalla:** Envía una captura de pantalla *después* de cada acción para que Claude vea el resultado.
3. **Seguridad:** Ejecuta en un contenedor aislado. ¡No le des acceso a tu banca personal!

## Limitaciones
- **Latencia:** Es lento (captura -> subida -> procesar -> responder -> acción).
- **Video:** Sin flujo de video en tiempo real todavía.

## ¡Felicidades!
Has completado el Módulo 3. Ahora eres un usuario avanzado de la API de Claude.

## Siguiente Módulo
Procede al [Módulo 4: Construcción de Aplicaciones](../module4_applications/README.md) para ponerlo todo junto.
