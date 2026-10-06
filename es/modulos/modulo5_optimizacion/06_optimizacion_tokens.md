# 5.2 Optimización de Tokens

Reducir tokens = Reducir Coste + Mejorar Latencia.

## Técnicas

1. **Sé Conciso:** Pide a Claude que "Sea conciso" en el prompt del sistema.
2. **Elimina Relleno:** Elimina HTML innecesario, claves JSON o texto verboso de los datos de entrada.
3. **Limita Salida:** Usa `max_tokens`.
4. **Secuencias de Parada:** Detén la generación temprano.

## Mide, no adivines
Cuenta los tokens con la API (nunca con un tokenizador de terceros como tiktoken, que no coincide con el tokenizador de Claude):

```python
import anthropic

client = anthropic.Anthropic()
count = client.messages.count_tokens(
    model="claude-sonnet-5-5",
    messages=[{"role": "user", "content": document_text}],
)
print(count.input_tokens)
```

Los modelos más nuevos usan un tokenizador más reciente que puede producir entre 1x y 1.35x más tokens para el mismo texto que los anteriores, así que vuelve a medir después de cambiar de modelo.

## Sanitización de Entrada
Eliminar marcado, texto repetitivo y espacios en blanco repetidos de entradas grandes puede ahorrar una parte significativa de tokens. Comprueba el ahorro con `count_tokens` antes y después; en prosa normal la ganancia es pequeña, y renombrar variables en código rara vez ayuda y perjudica la legibilidad.

## Palancas mayores
El caché de prompts (10% o menos del precio normal de entrada para lecturas en caché), el procesamiento por lotes (50% de descuento) y `effort` suelen ahorrar mucho más que recortar palabras.

## Próximos Pasos
- [Estrategia de Selección de Modelo](07_seleccion_modelos.md).
