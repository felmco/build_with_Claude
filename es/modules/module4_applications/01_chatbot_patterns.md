# 4.1 Patrones de Chatbot

Los chatbots son la aplicación más común de los LLMs. Esta guía cubre patrones arquitectónicos para construir interfaces conversacionales robustas.

## 1. El Chatbot Básico Sin Estado (Stateless)
- **Arquitectura:** Cliente envía mensaje -> Servidor llama API -> Servidor devuelve respuesta.
- **Estado:** Gestionado por el cliente (navegador/app) o en absoluto (turno único).
- **Pros:** Simple, escalable.
- **Contras:** Sin persistencia del historial.

## 2. El Chatbot Con Estado (Con Base de Datos)
- **Arquitectura:**
  1. Cliente envía mensaje + ID de sesión.
  2. Servidor obtiene historial de DB (Postgres/Redis).
  3. Servidor añade nuevo mensaje.
  4. Servidor llama a API de Claude.
  5. Servidor guarda nuevos mensajes de usuario y asistente.
  6. Servidor devuelve respuesta.
- **Pros:** Historial persistente a través de dispositivos.
- **Contras:** Backend más complejo.

## 3. El Chatbot Consciente del Contexto (RAG)
- **Arquitectura:**
  1. Mensaje de usuario recibido.
  2. Buscar en DB Vectorial documentos relevantes.
  3. Inyectar documentos en Prompt del Sistema.
  4. Llamar a Claude.
- **Caso de Uso:** Soporte al cliente, Base de conocimiento interna.

## 4. El Chatbot en Streaming
- **Arquitectura:** Usar WebSockets o Eventos Enviados por el Servidor (SSE) para enviar fragmentos de tokens al cliente a medida que llegan.
- **UX:** Esencial para respuestas largas para reducir la latencia percibida.

## Mejores Prácticas
- **Prompt del Sistema:** Define personalidad y restricciones claramente.
- **Truncamiento:** Gestiona la ventana de contexto resumiendo o descartando mensajes antiguos.
- **Moderación:** Comprueba entradas/salidas por seguridad.

## Próximos Pasos
- Construye un [Sistema de Q&A](./02_qa_systems.md).
