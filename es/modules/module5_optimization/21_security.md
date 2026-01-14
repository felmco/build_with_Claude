# 5.6 Mejores Prácticas de Seguridad

## 1. Inyección de Prompt
Usuarios intentando anular tus instrucciones ("Ignora instrucciones anteriores...").
- **Defensa:** Separa datos de instrucciones.
- **Defensa:** Usa etiquetas XML (`<user_input>`).

## 2. Fugas de PII
No envíes datos sensibles (SSN, Tarjetas de Crédito) a la API a menos que tengas un acuerdo BAA/Enterprise que lo cubra.
- **Limpieza (Scrubbing):** Elimina PII antes de enviar.

## 3. Gestión de Claves
- Nunca hagas commit de claves a Git.
- Usa `.env`.
- Rota claves si se filtran.

## Próximos Pasos
- [Cumplimiento](./22_compliance.md).
