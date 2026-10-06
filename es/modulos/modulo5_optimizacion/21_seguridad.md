# 5.6 Mejores Prácticas de Seguridad

## 1. Inyección de Prompt
Usuarios intentando anular tus instrucciones ("Ignora instrucciones anteriores...").
- **Defensa:** Separa datos de instrucciones.
- **Defensa:** Usa etiquetas XML (`<user_input>`). Ayuda, pero no es una garantía.
- **Defensa:** Da a las herramientas el mínimo privilegio, valida sus argumentos y exige aprobación humana para acciones destructivas. Nunca uses `eval`/`exec` con la salida del modelo ni se la pases a un shell.

## 2. Fugas de PII
No envíes datos sensibles (SSN, Tarjetas de Crédito) a la API a menos que tengas un acuerdo BAA/Enterprise que lo cubra.
- **Limpieza (Scrubbing):** Elimina PII antes de enviar.

## 3. Gestión de Claves
- Nunca hagas commit de claves a Git.
- Usa variables de entorno o un gestor de secretos (los archivos `.env` deben estar en el `.gitignore`).
- Rota claves si se filtran.

## Próximos Pasos
- [Cumplimiento](22_cumplimiento.md).
