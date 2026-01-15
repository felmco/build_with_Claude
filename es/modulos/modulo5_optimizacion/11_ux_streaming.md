# 5.3 Streaming para Mejor UX

Cubrimos los fundamentos del streaming en el Módulo 2. En optimización, nos enfocamos en la **Experiencia Frontend**.

## Suavizado (Smoothing)
Los tokens crudos llegan a intervalos irregulares. El "Jitter" se ve mal.
- **Técnica:** Almacena en búfer los tokens entrantes por 50ms y muéstralos a una tasa constante de caracteres por segundo.

## Analizando mientras se transmite (Parsing while Streaming)
Si solicitas JSON, no esperes a la respuesta completa para analizar.
- **Análisis Incremental:** Usa una librería que pueda analizar cadenas JSON parciales para mostrar elementos de UI (como listas) a medida que se generan.

## Próximos Pasos
- [Async y Concurrencia](12_async_concurrencia.md).
