# 5.1 Cadena de Pensamiento (CoT)

CoT es una técnica donde se anima al modelo a producir pasos de razonamiento intermedios.

## Cómo implementar
1. **Instrucción Explícita:** "Piensa paso a paso."
2. **Etiquetas XML:** Instruye a Claude para que ponga su razonamiento dentro de etiquetas `<thinking>`.

```python
system = "Eres un tutor de matemáticas. Siempre muestra tu pensamiento en etiquetas <thinking> antes de tu respuesta final."
```

## Beneficios
- **Depuración:** Puedes ver *por qué* Claude obtuvo una respuesta incorrecta.
- **Precisión:** Desglosar problemas reduce errores lógicos.

## Próximos Pasos
- [Plantillas de Prompt](05_plantillas_prompts.md).
