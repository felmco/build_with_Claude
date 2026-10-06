# 3.1 Mejores Prácticas de Uso de Herramientas

## 1. Descripciones Claras son Clave
Claude elige herramientas basándose en su `description`.
- ❌ "Calcula cosas"
- ✅ "Calcula la raíz cuadrada de un número. Devuelve un error para entradas negativas."

## 2. Usa Enums para Entradas Estrictas
Si un parámetro tiene un conjunto fijo de valores válidos, usa `enum` en el esquema. Esto limita a Claude a opciones válidas. Añade `"strict": true` a la definición de la herramienta para garantizar que las entradas coincidan exactamente con el esquema, y sigue validando las entradas en tu código.

```json
"unit": {
    "type": "string",
    "enum": ["celsius", "fahrenheit"]
}
```

## 3. Maneja Errores con Elegancia
Si una herramienta falla (ej. API caída, ID inválido), devuelve un **Tool Result** con el mensaje de error, en lugar de bloquearse.

**Devolver a Claude:**
```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01...",
  "is_error": true,
  "content": "Error: User ID 123 not found."
}
```
Claude a menudo puede autocorregirse (ej. "Oh, me disculpo. Déjame buscar por nombre en su lugar.").

## 4. Mantén la Salida de Herramienta Concisa
Claude tiene que leer la salida de la herramienta. Si tu herramienta devuelve un volcado JSON de 5MB, consume tokens y contexto.
- **Filtra** los datos antes de devolverlos.
- **Resume** archivos de texto grandes.

## 5. Seguridad (Inyección de Prompt)
Ten cuidado con herramientas que ejecutan código o SQL.
- **Aísla (Sandbox)** entornos de ejecución.
- Acceso a base de datos **solo lectura** donde sea posible.
- **Trata las entradas y salidas como no confiables.** Nunca pases texto escrito por el modelo a `eval`, `exec` ni a una shell, y usa SQL parametrizado. Los resultados de herramientas (páginas web, documentos) pueden contener instrucciones inyectadas.
- **Humano en el bucle** para acciones sensibles (enviar correos, borrar archivos).

## Próximos Pasos
- Optimiza costes con [Almacenamiento en Caché de Prompts](05_cache_prompt.md).
