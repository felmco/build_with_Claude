# 5.2 Estrategias de Caché

## La Regla "Cachear Todo lo Estático"
Si el texto aparece en más de una petición, cachéalo.

## Candidatos Comunes
1. **Prompts del Sistema:** Si son largos. El prefijo mínimo cacheable depende del modelo (de 512 a 4096 tokens); los prefijos más cortos no se cachean y no se te avisa.
2. **Ejemplos Few-Shot:** Si proporcionas 50 ejemplos, cachéalos.
3. **Documentos de Referencia:** Docs de políticas, especificaciones de API.
4. **Historial de Conversación:** En chatbots, cachea el historial hasta el último turno.

## Gestión de Puntos de Ruptura (Breakpoints)
Coloca breakpoints al *final* de la sección estática.

`[Prompt de Sistema Estático] -> [CACHE] -> [Entrada de Usuario Dinámica]`

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": LONG_STATIC_INSTRUCTIONS,
        "cache_control": {"type": "ephemeral"},
    }],
    messages=[{"role": "user", "content": user_input}],
)
print(response.usage.cache_creation_input_tokens, response.usage.cache_read_input_tokens)
```

## Economía
- Las escrituras en caché cuestan 1.25x el precio base de entrada (TTL de 5 minutos) o 2x (TTL de 1 hora, `"ttl": "1h"`).
- Las lecturas de caché cuestan alrededor de 0.1x el precio base de entrada (menos en algunos modelos, p. ej. 0.05x en Opus 5.5).
- Con el TTL de 5 minutos, dos peticiones ya alcanzan el punto de equilibrio. Cada lectura reinicia el temporizador.

## Verifica que funciona
Una caché rota falla en silencio: las peticiones tienen éxito, solo que la factura es mayor. Comprueba que `usage.cache_read_input_tokens > 0` en la segunda petición idéntica, y monitorízalo en producción. Cualquier cosa que cambie el prefijo (una marca de tiempo en el prompt del sistema, un orden no determinista de herramientas) provoca un fallo de caché.

En las integraciones más antiguas de Amazon Bedrock no se admite el `cache_control` automático de nivel superior; usa breakpoints explícitos en los bloques de contenido.

## Próximos Pasos
- [Procesamiento por Lotes por Coste](09_costo_lotes.md).
