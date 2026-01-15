# Guía de Inicio Rápido

## 🎉 ¡Bienvenido al Curso de Formación Construir con Claude!

Este curso de formación integral te enseñará cómo construir aplicaciones impulsadas por IA utilizando la API de Claude y Python.

## 📚 Qué Incluye

### 5 Módulos Completos (30+ Lecciones)
1. **Módulo 1: Fundamentos y Configuración** - Empieza con la API de Claude
2. **Módulo 2: Características Principales de la API** - Domina la API de Mensajes y streaming
3. **Módulo 3: Características Avanzadas** - Uso de herramientas, almacenamiento en caché, procesamiento por lotes
4. **Módulo 4: Construcción de Aplicaciones** - Agentes, RAG, MCP
5. **Módulo 5: Optimización** - Mejores prácticas de producción

### Aprendizaje Práctico
- **15+ Ejercicios** con instrucciones paso a paso y soluciones
- **5 Proyectos del Mundo Real** demostrando patrones de producción
- **100+ Ejemplos de Código** en Python
- **Ruta de Aprendizaje Progresiva** de principiante a avanzado

## 🚀 Empieza en 5 Minutos

### Paso 1: Configurar el Entorno
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install anthropic python-dotenv
```

### Paso 2: Configurar Clave API
```bash
# Crear archivo .env
echo "ANTHROPIC_API_KEY=tu-clave-api-aqui" > .env
```

Obtén tu clave API en: https://console.anthropic.com

### Paso 3: Probar tu Configuración
```python
# test_setup.py
from anthropic import Anthropic

client = Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content[0].text)
```

Ejecútalo:
```bash
python test_setup.py
```

## 📖 Rutas de Aprendizaje

### Ruta 1: Principiante Completo (¡Empieza Aquí!)
1. Lee [Módulo 1: Fundamentos](modulos/modulo1_fundamentos/README.md)
2. Completa [Ejercicio 1: Hola Claude](ejercicios/principiante/01_hola_claude.md)
3. Continúa a través de las lecciones del Módulo 1
4. Practica con ejercicios para principiantes

**Tiempo**: 2-3 horas

### Ruta 2: Desarrollador Experimentado
1. Echa un vistazo al Módulo 1 para la configuración
2. Profundiza en [Módulo 2: API Principal](modulos/modulo2_api_nucleo/README.md)
3. Explora [Módulo 3: Características Avanzadas](modulos/modulo3_caracteristicas_avanzadas/README.md)
4. Construye [Proyecto 1: Bot de Soporte al Cliente](proyectos/README.md)

**Tiempo**: 6-8 horas

### Ruta 3: Listo para Producción
1. Revisa los Módulos 1-3 rápidamente
2. Céntrate en [Módulo 4: Aplicaciones](modulos/modulo4_aplicaciones/README.md)
3. Domina [Módulo 5: Optimización](modulos/modulo5_optimizacion/README.md)
4. Completa todos los proyectos

**Tiempo**: 12-15 horas

## 🎯 Navegación Rápida

### Lecciones Esenciales
- [Entendiendo Modelos](modulos/modulo1_fundamentos/01_vision_general_modelos.md) - Elige el modelo correcto
- [Primera Llamada a la API](modulos/modulo1_fundamentos/07_primera_llamada_api.md) - Tus primeros pasos
- [API de Mensajes](modulos/modulo2_api_nucleo/01_api_mensajes.md) - Funcionalidad principal
- [Streaming](modulos/modulo2_api_nucleo/04_conceptos_basicos_streaming.md) - Respuestas en tiempo real
- [Uso de Herramientas](modulos/modulo3_caracteristicas_avanzadas/01_conceptos_basicos_uso_herramientas.md) - Llamadas a funciones
- [Caché de Prompts](modulos/modulo3_caracteristicas_avanzadas/05_cache_prompt.md) - Optimización de costes

### Práctica
- [Todos los Ejercicios](ejercicios/README.md) - Práctica práctica
- [Proyectos de Muestra](proyectos/README.md) - Ejemplos del mundo real

## 💡 Lo Que Aprenderás

### Semana 1: Fundamentos
- ✅ Modelos y capacidades de Claude
- ✅ Configuración del SDK de Python
- ✅ Gestión de claves API
- ✅ Realización de llamadas a la API
- ✅ Manejo básico de errores

### Semana 2: Características Principales
- ✅ Maestría en la API de Mensajes
- ✅ Respuestas en streaming
- ✅ Gestión de conversaciones
- ✅ Trabajo con imágenes
- ✅ Manejo de archivos

### Semana 3: Avanzado
- ✅ Uso de herramientas / llamadas a funciones
- ✅ Almacenamiento en caché de prompts
- ✅ Procesamiento por lotes
- ✅ Capacidades de visión
- ✅ Pensamiento extendido

### Semana 4: Aplicaciones
- ✅ Construcción de chatbots
- ✅ Creación de agentes
- ✅ Sistemas RAG
- ✅ Integración MCP
- ✅ Patrones de producción

## 📊 Estadísticas del Curso

- **30+** Lecciones completas
- **5** Módulos principales
- **15+** Ejercicios prácticos
- **5** Proyectos del mundo real
- **100+** Ejemplos de código
- **6,000+** Líneas de documentación

## 🎓 Lista de Verificación de Finalización

### Principiante (Semana 1-2)
- [ ] Completar Módulo 1
- [ ] Completar Módulo 2
- [ ] Terminar 5 ejercicios para principiantes
- [ ] Construir un chatbot simple

### Intermedio (Semana 3)
- [ ] Completar Módulo 3
- [ ] Terminar 5 ejercicios intermedios
- [ ] Implementar uso de herramientas
- [ ] Construir aplicación de streaming

### Avanzado (Semana 4+)
- [ ] Completar Módulo 4 y 5
- [ ] Terminar ejercicios avanzados
- [ ] Construir sistema RAG
- [ ] Desplegar aplicación de producción

## 🛠️ Herramientas y Recursos

### Requerido
- Python 3.7+
- Clave API de Anthropic
- Editor de texto/IDE

### Recomendado
- VS Code o PyCharm
- Git para control de versiones
- Entorno virtual
- Terminal/línea de comandos

### Recursos Adicionales
- [Documentación Oficial de Claude](https://platform.claude.com/docs/en/home)
- [Libro de Recetas (Cookbook) de Anthropic](https://github.com/anthropics/anthropic-cookbook)
- [GitHub del SDK de Python](https://github.com/anthropics/anthropic-sdk-python)
- [Documentación de MCP](https://modelcontextprotocol.io/docs/getting-started/intro)

## 🎯 Próximos Pasos

### Hoy
1. ✅ Configura tu entorno
2. ✅ Obtén tu clave API
3. ✅ Haz tu primera llamada a la API
4. ✅ Empieza el Módulo 1

### Esta Semana
1. Completa el Módulo 1 y 2
2. Haz ejercicios para principiantes
3. Construye un chatbot simple
4. Experimenta con streaming

### Este Mes
1. Completa todos los módulos
2. Termina todos los ejercicios
3. Construye 2-3 proyectos
4. Despliega una aplicación

## 💬 Obteniendo Ayuda

### Documentación
- Revisa los README de los módulos
- Revisa ejemplos de código
- Lee materiales de las lecciones

### Comunidad
- [Discord](https://discord.gg/anthropic)
- [Discusiones de GitHub](https://github.com/anthropics/anthropic-sdk-python/discussions)
- [Twitter](https://twitter.com/AnthropicAI)

### Solución de Problemas
- Revisa la [documentación de la API](https://platform.claude.com/docs/en/api/overview)
- Revisa guías de manejo de errores
- Prueba con ejemplos simples

## 🎉 ¿Listo para Empezar?

Comienza tu viaje con el [Módulo 1: Fundamentos y Configuración](modulos/modulo1_fundamentos/README.md)

O sumérgete directamenente en el código con [Ejercicio 1: Hola Claude](ejercicios/principiante/01_hola_claude.md)

---

**¡Feliz Aprendizaje! 🚀**

---

*Este curso fue creado y desarrollado por **[Future Tales](https://futuretales.ai)***

*Basado en documentación oficial de Anthropic y mejores prácticas. Última actualización: Enero 2026*
