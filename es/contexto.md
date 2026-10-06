# Guía Completa: Primeros Pasos con el Desarrollo de la API de Claude en Python

> Basada en la página "Build with Claude" de Anthropic Academy, esta guía te ayuda a empezar a desarrollar aplicaciones impulsadas por Claude usando Python.

---

## 1. Fundamentos: Entender los Modelos de Claude

### Modelos Disponibles

Los modelos más recientes de Claude son:

| Modelo | Ideal Para | Características Clave |
|--------|------------|------------------------|
| **Claude Fable 5.1** | Las tareas más difíciles | El modelo más capaz |
| **Claude Opus 5.5** | Razonamiento complejo | Alta inteligencia para tareas difíciles |
| **Claude Sonnet 5.5** | La mayoría de las aplicaciones | Mejor equilibrio entre velocidad y capacidad |
| **Claude Haiku 4.5** | Alto volumen, tareas simples | El más rápido y rentable |

### Primeros Pasos con los Modelos

Para elegir el modelo adecuado:

- 📊 Revisa el [cuadro comparativo de modelos](https://platform.claude.com/docs/en/models) para entender las capacidades y diferencias
- 🔄 Consulta la guía de migración de modelos si actualizas desde un modelo anterior
- 📝 Sigue las mejores prácticas de prompting vigentes para obtener resultados óptimos
- 💰 Revisa los precios actuales de los modelos para optimizar costes

---

## 2. Configuración e Instalación: SDK de Python

### Instalación del SDK de Python

El SDK de Python es la herramienta principal para los desarrolladores de Python. Empieza así:

1. **Instala el SDK de Python de Anthropic con pip**
   ```bash
   pip install anthropic
   ```

2. **Genera claves API desde la Consola de Anthropic**
   - Visita [platform.claude.com](https://platform.claude.com)
   - Ve a la sección de claves API
   - Crea y guarda tu clave de forma segura

3. **Configura las variables de entorno con tu clave API**
   ```bash
   export ANTHROPIC_API_KEY='tu-clave-api-aqui'
   ```

### Componentes Clave

El SDK de Python incluye:

- ✅ Soporte completo para la API de Mensajes
- ⚡ Capacidades async/await para peticiones concurrentes eficientes
- 🔍 Anotaciones de tipos para un mejor soporte del IDE y comprobación de errores
- 🛡️ Manejo de errores y lógica de reintentos integrados

### Otros SDK Disponibles

Si lo necesitas, Anthropic también ofrece:

- **SDK de TypeScript** (JavaScript/Node.js)
- **SDK de Java**
- **SDK de Go**
- **SDK de Ruby**

---

## 3. APIs y Características Principales para el Desarrollo en Python

### 3.1 API de Mensajes (API Principal)

La API de Mensajes es la interfaz fundamental para comunicarte con Claude:

**Capacidades Principales**:
- 💬 Enviar mensajes de texto y recibir respuestas
- 🌊 Transmitir respuestas en streaming para obtener salida en tiempo real
- 🔄 Gestionar múltiples turnos de conversación
- 📚 Administrar el historial de conversación de forma eficiente

**Características Clave**:
- Soporte para distintos roles de mensaje (user, assistant)
- Conteo de tokens para optimización
- Controles de parámetros (nota: Fable 5.1, Opus 5.5 y Sonnet 5.5 rechazan los parámetros de muestreo como `temperature`; Haiku 4.5 aún los acepta)
- Respuestas en streaming para una mejor experiencia de usuario

### 3.2 API de Lotes de Mensajes (Message Batches)

Para procesar múltiples peticiones de forma eficiente:

- 📦 Enviar varias peticiones a la API a la vez
- 💰 Reducir costes procesando por lotes
- 🎯 Ideal para trabajos por lotes, evaluaciones y análisis a gran escala
- ⏱️ Procesamiento asíncrono para tareas que no son urgentes

### 3.3 API de Archivos (Files)

Gestiona archivos para ampliar el contexto y el manejo de datos:

- 📁 Subir y administrar archivos para usarlos con Claude
- 📄 Incluir PDFs, documentos y otros tipos de archivo
- ♻️ Reutilizar archivos subidos en múltiples llamadas a la API
- 🔍 Soporte para extracción de texto y análisis de documentos

### 3.4 Soporte de PDF

Extrae y comprende el contenido visual de los PDFs:

- 📖 Extraer texto de documentos PDF
- 📊 Analizar gráficos, diagramas e información visual
- 🖼️ Procesar contenido mixto de texto e imágenes
- 🎯 Útil para aplicaciones de análisis de documentos

### 3.5 API de Administración (Admin)

Gestiona permisos y ajustes del espacio de trabajo:

- 👥 Controlar el acceso y los permisos de los usuarios
- ⚙️ Administrar las configuraciones del espacio de trabajo
- 🏢 Escalar despliegues empresariales
- 🔐 Gestionar el control de acceso por equipos

---

## 4. Características Avanzadas para Desarrolladores de Python

### 4.1 Almacenamiento en Caché de Prompts (Prompt Caching)

Optimiza el rendimiento y reduce los costes de la API:

- 🔄 Reutilizar prompts en caché entre múltiples peticiones
- 💰 Reducción significativa de costes en contextos repetidos (hasta un 90%)
- ⚡ Tiempos de respuesta más rápidos en patrones recurrentes
- 🛠️ Implementación: usa parámetros `cache_control` en las llamadas a la API

**Cuándo Usarlo**:
- Prompts de sistema largos repetidos en varias peticiones
- Conjuntos de instrucciones estándar usados varias veces
- Bases de conocimiento consultadas repetidamente
- Tareas recurrentes de análisis de documentos

### 4.2 Capacidades de Visión

Aprovecha la comprensión de imágenes de Claude:

- 🖼️ Analizar imágenes e información visual
- 📝 Extraer texto de imágenes (OCR)
- 📊 Analizar gráficos y diagramas
- 🎨 Describir contenido visual
- 🔗 Soporte para imágenes codificadas en base64 y URLs

### 4.3 Uso de Computadora (Computer Use)

Interactúa con entornos de escritorio de forma programática:

- 🖱️ Automatizar interacciones de escritorio
- 📸 Tomar capturas de pantalla y analizarlas
- ⌨️ Hacer clic, escribir y controlar el ratón
- 🔌 Integración con APIs existentes
- 🔒 Conocer cómo Computer Use gestiona la privacidad de los datos

### 4.4 Pensamiento Extendido (Extended Thinking)

Mejora la capacidad de Claude para resolver tareas complejas:

- 🧠 Habilitar un razonamiento más largo y meditado
- 📈 Mejor rendimiento en problemas difíciles
- 💻 Útil para programación, matemáticas y análisis complejo
- ⚠️ Contrapartida: tiempos de respuesta más largos y costes más altos

**Implementación**:
- En Fable 5.1, Opus 5.5 y Sonnet 5.5 usa `thinking={"type": "adaptive"}` con `output_config={"effort": ...}`; solo Haiku 4.5 usa `budget_tokens`
- Sigue las mejores prácticas de pensamiento extendido
- Monitoriza el uso de tokens (los tokens de pensamiento son más caros)

---

## 5. Construcción de Aplicaciones: Patrones y Técnicas

### 5.1 Uso de Herramientas (Llamadas a Funciones)

Amplía las capacidades de Claude conectándolo con herramientas externas:

**Conceptos Fundamentales**:
- 🛠️ Definir herramientas/funciones que Claude puede llamar
- 🤖 Claude decide cuándo y cómo usar las herramientas
- 📚 Soporta múltiples definiciones de herramientas
- 🔌 Implementar el uso de herramientas con la API de Anthropic

**Casos de Uso Comunes**:
- 🗄️ Consultas a bases de datos
- 🌐 Llamadas a APIs de servicios externos
- ⚙️ Ejecución de código
- 🧮 Funciones de calculadora
- 🔍 Búsquedas web

**Herramientas Disponibles**:
- Herramienta de ejecución de código
- Herramienta de editor de texto
- Herramienta de búsqueda web
- Herramientas personalizadas definidas por tu aplicación

### 5.2 Agentes y Sistemas Agénticos

Construye sistemas autónomos que entienden, planifican y ejecutan tareas:

**Arquitectura**:
- 🎯 Diseñar patrones de agentes con Claude
- 📋 Implementar salidas JSON para un control fiable
- 🔗 Usar el Protocolo de Contexto de Modelo (MCP)
- 🔄 Arquitectura basada en bucles: percibir → planificar → actuar
- 📖 Consultar el Anthropic Cookbook para patrones de agentes

**Componentes Clave**:
- Bucles de agente: percepción y acción continuas
- Integración de herramientas para acciones externas
- Gestión de estado
- Lógica de toma de decisiones

### 5.3 Skills (Habilidades)

Proporciona instrucciones detalladas para tareas específicas:

- 📝 Definir descripciones de skills con ejemplos
- 📈 Usar skills para mejorar el rendimiento en tareas concretas
- ✅ Mejores prácticas para crear skills
- 🔌 Implementar skills en las llamadas a la API

### 5.4 Generación Aumentada por Recuperación (RAG)

Construye sistemas que enriquecen el conocimiento de Claude con datos externos:

**Proceso Principal**:
1. 📚 Recuperar información relevante de los documentos
2. 🤝 Combinar el contexto recuperado con el razonamiento de Claude
3. 🎯 Implementar agentes de soporte al cliente con RAG
4. 🔌 Opciones de integración: LlamaIndex, MongoDB, etc.

**Opciones de Stack Tecnológico**:
- **Voyage AI** para embeddings
- **LlamaIndex** para la orquestación de RAG
- **MongoDB** para almacenamiento vectorial
- **Implementaciones personalizadas**

### 5.5 Protocolo de Contexto de Modelo (MCP)

Construye aplicaciones avanzadas con integración estandarizada de herramientas:

**Opciones de Configuración**:
- 🖥️ Configurar MCP en Claude Desktop para desarrollo local
- 📦 Usar los servidores MCP listos para usar de Anthropic
- 💻 Integrar con Claude Code para soporte en el IDE
- ☁️ Configurar servidores MCP remotos
- 🔌 Conectar MCP remoto desde la API de Mensajes

**Características**:
- Definiciones de herramientas estandarizadas
- Configuración sencilla de servidores
- Contribuciones de la comunidad basadas en Git
- Conceptos avanzados de MCP para aplicaciones complejas

---

## 6. Herramientas y Entornos de Desarrollo

### 6.1 Claude Code

Acelera el desarrollo con programación asistida por IA:

- 📥 Instalar Claude Code localmente
- 🔌 Integrarlo con tu IDE
- ☁️ Conectarlo con Google Vertex AI o Amazon Bedrock
- 📖 Explorar flujos de trabajo y patrones comunes
- 🆘 Acceder a la documentación y guías de solución de problemas

### 6.2 Claude Desktop

Entorno de desarrollo para pruebas y prototipos:

- 🧪 Pruebas locales antes del despliegue en producción
- 🔗 Integración MCP para probar herramientas
- ⚡ Comentarios en tiempo real sobre las respuestas

### 6.3 Consola de Anthropic

Interfaz web para:

- 🔑 Gestión de claves API
- ⚙️ Configuración del espacio de trabajo
- 📊 Monitorización del uso
- 🛠️ Ajustes para desarrolladores

---

## 7. Optimización y Mejores Prácticas

### 7.1 Ingeniería de Prompts

Crea prompts eficaces que maximicen el rendimiento de Claude:

**Recursos de Aprendizaje**:
- 🎓 Sigue tutoriales interactivos de ingeniería de prompts
- 💪 Practica con escenarios del mundo real
- 🛠️ Usa la herramienta generadora de prompts
- 📖 Sigue las mejores prácticas establecidas

**Principios Clave**:
1. ✅ Sé claro y específico
2. 📝 Proporciona ejemplos cuando ayuden
3. 🏗️ Usa formatos estructurados
4. 📋 Especifica el formato de salida
5. 🎯 Incluye el contexto relevante

### 7.2 Evaluaciones

Prueba y mejora tu implementación con Claude:

**Marco de Trabajo**:
- 🏗️ Construir marcos de evaluación sólidos
- 🤖 Crear sistemas de evaluación automatizados
- 🛠️ Usar la herramienta Eval de la Consola de Claude
- 📈 Medir las mejoras de rendimiento

**Tipos de Evaluación**:
- ✅ Evaluación de la calidad de la salida
- 💰 Análisis de eficiencia de costes
- ⚡ Mediciones de latencia
- 😊 Métricas de satisfacción del usuario

### 7.3 Selección de Modelo

Elige el modelo adecuado para tu caso de uso:

| Caso de Uso | Modelo Recomendado | Motivo |
|-------------|--------------------|--------|
| La mayoría de las aplicaciones | Sonnet 5.5 | Velocidad y capacidad equilibradas |
| Razonamiento complejo | Opus 5.5 / Fable 5.1 | Máxima inteligencia |
| Alto volumen, tareas simples | Haiku 4.5 | Más rentable |

**Consideraciones**:
- Límites de tokens y costes
- Usa el cuadro comparativo de modelos para ver las especificaciones detalladas
- Equilibra rendimiento y coste

### 7.4 Optimización de Costes

Reduce los costes de la API manteniendo la calidad:

1. 💾 **Implementa el almacenamiento en caché de prompts** para contextos repetidos
2. 📦 **Usa la API de Lotes de Mensajes** para peticiones no urgentes
3. 📊 **Monitoriza el uso de tokens**
4. ✂️ **Optimiza la longitud y la estructura de los prompts**
5. 🎯 **Usa los modelos adecuados** para cada tarea

---

## 8. Poner en Marcha tu Primera Aplicación en Python

### Configuración Paso a Paso

```python
# 1. Instala el SDK
# pip install anthropic

# 2. Configura tu clave API
# export ANTHROPIC_API_KEY='tu-clave-api'

# 3. Crea una aplicación básica
from anthropic import Anthropic

client = Anthropic()

# 4. Haz tu primera llamada a la API
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Próximos Pasos

Después de tu primera llamada exitosa:

1. 📖 Revisa la documentación completa de la API
2. 🍳 Explora el Anthropic Cookbook para ver ejemplos de código
3. 🚀 Prueba el repositorio Anthropic Quickstarts
4. 🛠️ Construye una aplicación prototipo
5. 🧪 Prueba con diferentes modelos y parámetros
6. ⚡ Optimiza según tu caso de uso

---

## 9. Recursos Avanzados

### Documentación y Aprendizaje

| Recurso | Descripción | Enlace |
|---------|-------------|--------|
| **Documentación completa de la API** | Referencia completa de la API | [platform.claude.com/docs](https://platform.claude.com/docs/en/home) |
| **Anthropic Cookbook** | Fragmentos de código y guías prácticas | [GitHub](https://github.com/anthropics/anthropic-cookbook) |
| **Quickstarts** | Ejemplos de aplicaciones prediseñadas | [GitHub](https://github.com/anthropics/anthropic-quickstarts) |
| **Cursos** | Formación en profundidad sobre temas específicos | [Claude Academy](https://academy.claude.com/courses) |

### Comunidad y Soporte

- 🎉 Recursos para hackathones si participas en eventos
- 📊 Diapositivas de talleres y materiales de formación
- 👥 Comunidad de desarrolladores para preguntas e ideas
- 🐙 Repositorios de GitHub para MCP y otros proyectos

### Integración con Plataformas en la Nube

| Plataforma | Descripción |
|------------|-------------|
| **Amazon Bedrock** | Ejecuta Claude a través de AWS |
| **Google Cloud Vertex AI** | Ejecuta Claude en GCP |
| **API directa** | Acceso a través de la Consola de Anthropic |

---

## 10. Patrones Comunes de Desarrollo

### Patrón 1: Aplicación de Chat Simple

```
1. Inicializar el cliente con la clave API
2. Implementar el bucle de mensajes
3. Gestionar el historial de la conversación
4. Transmitir respuestas en streaming para una mejor UX
```

### Patrón 2: Agente que Usa Herramientas

```
1. Definir las herramientas disponibles
2. Crear el bucle del agente
3. Gestionar las llamadas a herramientas de Claude
4. Ejecutar las herramientas y devolver los resultados
5. Continuar el bucle del agente hasta completar la tarea
```

### Patrón 3: Sistema RAG

```
1. Cargar y generar embeddings de los documentos
2. Crear el almacén vectorial
3. Implementar la función de recuperación
4. Construir prompts con el contexto recuperado
5. Ejecutar la API de Claude con los prompts enriquecidos
```

### Patrón 4: Procesamiento por Lotes

```
1. Preparar múltiples peticiones
2. Enviarlas mediante la API de Lotes de Mensajes
3. Monitorizar el estado del lote
4. Procesar los resultados de forma asíncrona
5. Gestionar errores y reintentos
```

---

## 11. Solución de Problemas y Consejos

| Problema | Solución |
|----------|----------|
| **Límites de tasa de la API** | Espera y reintenta (el SDK reintenta automáticamente), reparte la carga o usa el procesamiento por lotes para el volumen no urgente |
| **Costes altos de tokens** | Implementa el caché de prompts y optimiza los prompts |
| **Respuestas lentas** | Usa un modelo más pequeño (Haiku 4.5), reduce `effort`, transmite las respuestas en streaming |
| **Problemas al llamar herramientas** | Asegúrate de que las definiciones de herramientas sean claras y el formato JSON sea correcto |
| **Problemas de precisión** | Usa pensamiento extendido, mejora los prompts, añade ejemplos |
| **Depuración** | Usa la Consola de Claude para probar prompts y consulta la documentación de la API |

---

## Referencia Rápida: Lo Esencial del SDK de Python

### Instalación
```bash
pip install anthropic
```

### Uso Básico
```python
from anthropic import Anthropic

client = Anthropic()  # lee ANTHROPIC_API_KEY del entorno

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Your prompt"}]
)
```

### Métodos Clave

| Método | Descripción |
|--------|-------------|
| `messages.create()` | Enviar un mensaje y obtener la respuesta |
| `messages.stream()` | Obtener respuestas en streaming |
| `files.upload()` | Subir archivos (la API de Archivos es GA, sin cabecera beta) |
| `messages.batches.create()` | Procesar múltiples peticiones |

---

## 🚀 Empieza a Construir

¡Visita [platform.claude.com](https://platform.claude.com) para comenzar con tu primera aplicación!

Esta guía completa cubre todo lo que necesitas para empezar a desarrollar aplicaciones impulsadas por Claude en Python, desde la configuración básica hasta patrones avanzados y técnicas de optimización.

---

## Recursos Adicionales

- 📚 [Curso de Formación Completo](README.md)
- 🚀 [Guía de Inicio Rápido](INICIO_RAPIDO.md)
- 💻 [Ejemplos de Código](modulos)
- 🎯 [Ejercicios Prácticos](ejercicios)
- 🏗️ [Proyectos de Muestra](proyectos)

---

## 🙏 Créditos

**Creado por [Future Tales](https://futuretales.ai)** - Empoderando a los desarrolladores para construir el futuro con IA.

Esta guía integral fue desarrollada a partir de la documentación oficial de Anthropic y las mejores prácticas de la industria.
