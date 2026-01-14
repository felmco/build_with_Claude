# 5.1 Fundamentos de Ingeniería de Prompts

La ingeniería de prompts es el arte de comunicarse con modelos de IA para obtener los mejores resultados posibles.

## Los Principios Fundamentales

### 1. Sé Claro y Directo
- **Mal:** "Escribe algo sobre gatos."
- **Bien:** "Escribe una entrada de blog de 300 palabras sobre los beneficios de adoptar gatos mayores para vivir en apartamentos."

### 2. Usa Ejemplos (Few-Shot)
Proporcionar ejemplos ayuda al modelo a entender el patrón y tono deseado.

### 3. Dale a Claude un Rol
Asignar una persona (ej. "Eres un científico de datos experto") ayuda a enmarcar el conocimiento y estilo del modelo.

### 4. Usa Etiquetas XML
Las etiquetas XML ayudan a estructurar las entradas y separar los datos de las instrucciones.

```xml
<instructions>
Resume el texto de abajo.
</instructions>

<text>
...
</text>
```

## La Estructura de Prompt "Perfecta"

1. **Rol:** ¿Quién es Claude?
2. **Contexto:** ¿Cuál es la situación?
3. **Instrucciones:** ¿Qué pasos específicos debe tomar?
4. **Datos:** La entrada para procesar.
5. **Formato de Salida:** ¿JSON, Markdown, CSV?
6. **Restricciones:** Qué *no* hacer.

## Próximos Pasos
- [Prompting Avanzado](./02_advanced_prompting.md).
