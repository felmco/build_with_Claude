# 5.2 Optimización de Tokens

Reducir tokens = Reducir Coste + Mejorar Latencia.

## Técnicas

1. **Sé Conciso:** Pide a Claude que "Sea conciso" en el prompt del sistema.
2. **Elimina Relleno:** Elimina HTML innecesario, claves JSON o texto verboso de los datos de entrada.
3. **Limita Salida:** Usa `max_tokens`.
4. **Secuencias de Parada:** Detén la generación temprano.

## Sanitización de Entrada
Eliminar espacios en blanco o usar nombres de variables más cortos en fragmentos de código puede ahorrar cientos de tokens en contextos grandes.

## Próximos Pasos
- [Estrategia de Selección de Modelo](./07_model_selection.md).
