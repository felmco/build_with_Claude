# Proyectos de Ejemplo

Este directorio contiene proyectos completos y del mundo real que demuestran cómo construir aplicaciones listas para producción con la API de Claude.

## 🚀 Proyectos Disponibles

### 1. [Chatbot de Soporte al Cliente](./01_customer_support_bot/)
**Nivel**: Intermedio | **Tiempo**: 3-4 horas

Un chatbot de soporte al cliente listo para producción con:
- Respuestas en streaming para interacción en tiempo real
- Historial de conversación y gestión de contexto
- Uso de herramientas para acceder a base de conocimiento
- Integración de creación de tickets
- Soporte multi-idioma

**Tecnologías**: Claude API, Streaming, Tool Use, File Storage

**Características Clave**:
- Flujo de conversación natural
- Respuestas conscientes del contexto
- Escalada a agentes humanos
- Analítica y logging

---

### 2. [Sistema de Q&A de Documentos](./02_document_qa/)
**Nivel**: Avanzado | **Tiempo**: 4-6 horas

Sistema basado en RAG para responder preguntas sobre documentos:
- Procesamiento de documentos PDF y de texto
- Base de datos vectorial para búsqueda semántica
- Caché de prompts para eficiencia
- Soporte multi-documento

**Tecnologías**: Claude API, RAG, Vector DB, Prompt Caching

**Características Clave**:
- Sube múltiples documentos
- Búsqueda semántica
- Cita de fuentes
- Coste optimizado con caché

---

### 3. [Agente de Revisión de Código](./03_code_review_agent/)
**Nivel**: Avanzado | **Tiempo**: 4-5 horas

Agente autónomo para revisar código:
- Integración con GitHub
- Análisis multi-archivo
- Sugerencias automatizadas
- Comprobación de mejores prácticas

**Tecnologías**: Claude API, Tool Use, GitHub API, Async

**Características Clave**:
- Análisis de Pull Request
- Comentarios de código en línea
- Detección de vulnerabilidades de seguridad
- Sugerencias de rendimiento

---

### 4. [Asistente de Investigación](./04_research_assistant/)
**Nivel**: Avanzado | **Tiempo**: 5-6 horas

Sistema multi-agente para tareas de investigación:
- Integración de búsqueda web
- Síntesis de información
- Generación de informes
- Rastreo de fuentes

**Tecnologías**: Claude API, Multi-Agent, Web APIs, Tool Use

**Características Clave**:
- Investigación autónoma
- Múltiples fuentes de información
- Informes estructurados
- Comprobación de hechos (Fact checking)

---

### 5. [Servidor MCP del Tiempo](./05_mcp_weather/)
**Nivel**: Intermedio | **Tiempo**: 2-3 horas

Servidor MCP personalizado para información del tiempo:
- Integración API REST
- Múltiples fuentes de datos
- Integración con Claude Desktop
- Manejo de errores

**Tecnologías**: MCP, Claude API, REST APIs

**Características Clave**:
- Datos del tiempo en tiempo real
- Información de pronóstico
- Búsqueda de ubicación
- Datos históricos

---

## 📋 Estructura del Proyecto

Cada proyecto incluye:

```
project_name/
├── README.md              # Visión general del proyecto y configuración
├── requirements.txt       # Dependencias Python
├── .env.example          # Plantilla de variables de entorno
├── src/                  # Código fuente
│   ├── main.py          # Punto de entrada
│   ├── config.py        # Configuración
│   └── ...              # Otros módulos
├── tests/               # Archivos de prueba
│   └── test_*.py
├── docs/                # Documentación adicional
│   ├── architecture.md
│   └── api.md
└── examples/            # Ejemplos de uso
    └── example_*.py
```

## 🎯 Cómo Usar los Proyectos

### Paso 1: Elige un Proyecto
Selecciona un proyecto que coincida con tu:
- Nivel de habilidad
- Tiempo disponible
- Objetivos de aprendizaje
- Área de interés

### Paso 2: Configura el Entorno
```bash
cd project_name
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

### Paso 3: Configura
```bash
cp .env.example .env
# Edita .env con tus claves API y configuraciones
```

### Paso 4: Ejecuta el Proyecto
```bash
python src/main.py
```

### Paso 5: Estudia y Modifica
- Lee a través del código
- Entiende la arquitectura
- Haz modificaciones
- Añade nuevas características

## 🎓 Ruta de Aprendizaje

### Para Principiantes
1. Empieza con módulos más simples de ejercicios
2. Estudia el código del proyecto a fondo
3. Haz pequeñas modificaciones
4. Construye tu propia versión

### Para Desarrolladores Intermedios
1. Empieza con Bot de Soporte o MCP Weather
2. Implementa todas las características
3. Añade extensiones
4. Despliega a producción

### Para Desarrolladores Avanzados
1. Aborda Agente de Revisión de Código o Asistente de Investigación
2. Optimiza para producción
3. Añade características avanzadas
4. Contribuye mejoras

## 💡 Ideas de Proyectos

¿Quieres construir tu propio proyecto? Aquí hay algunas ideas:

### Proyectos de Principiante
- [ ] Diario personal con resúmenes de IA
- [ ] Chatbot de aprendizaje de idiomas
- [ ] Generador de recetas y planificador de comidas
- [ ] Resumidor de noticias diarias
- [ ] Asistente de estudio con tarjetas de memoria (Flashcards)

### Proyectos Intermedios
- [ ] Auto-respondedor de correo electrónico
- [ ] Generador de contenido para redes sociales
- [ ] Analizador de notas de reuniones
- [ ] Escritor de documentación técnica
- [ ] Generador de consultas SQL

### Proyectos Avanzados
- [ ] Maestro de juego multi-agente para RPGs
- [ ] Generador de suite de pruebas automatizadas
- [ ] Analizador de documentos legales
- [ ] Generador de informes financieros
- [ ] Tutor de IA personal con plan de estudios

## 🛠️ Patrones Comunes

### Patrón 1: Aplicación Conversacional
```python
# Inicializar conversación
conversation = []

# Bucle
while True:
    user_input = get_user_input()
    conversation.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        messages=conversation
    )

    conversation.append({"role": "assistant", "content": response.content[0].text})
```

### Patrón 2: Agente Basado en Herramientas
```python
# Definir herramientas
tools = [define_tool_1(), define_tool_2()]

# Bucle de agente
while not done:
    response = client.messages.create(tools=tools, ...)

    if response.stop_reason == "tool_use":
        # Ejecutar herramienta
        result = execute_tool(...)
        # Continuar con resultado
    else:
        done = True
```

### Patrón 3: Sistema RAG
```python
# Configuración
vectordb = setup_vector_database()
documents = load_documents()
vectordb.add(documents)

# Consulta
def query(question):
    # Recuperar documentos relevantes
    docs = vectordb.search(question)

    # Generar respuesta con contexto
    response = client.messages.create(
        system=f"Usa estos documentos: {docs}",
        messages=[{"role": "user", "content": question}]
    )

    return response.content[0].text
```

### Patrón 4: Procesamiento por Lotes
```python
# Preparar peticiones
requests = [create_request(item) for item in items]

# Enviar lote
batch = client.batches.create(requests=requests)

# Monitorizar progreso
while not batch.complete:
    time.sleep(10)
    batch = client.batches.retrieve(batch.id)

# Procesar resultados
results = batch.results
```

## 📊 Comparación de Proyectos

| Proyecto | Dificultad | Tiempo | Tecnologías Clave | Mejor Para Aprender |
|---------|-----------|------|------------------|-------------------|
| Soporte al Cliente | ⭐⭐ | 3-4h | Streaming, Tools | IA Conversacional |
| Q&A de Documentos | ⭐⭐⭐ | 4-6h | RAG, Caching | Recuperación de Información |
| Revisión de Código | ⭐⭐⭐ | 4-5h | Agents, APIs | Sistemas Autónomos |
| Asistente de Investigación | ⭐⭐⭐ | 5-6h | Multi-Agent | Flujos de Trabajo Complejos |
| MCP Tiempo | ⭐⭐ | 2-3h | MCP, APIs | Integración de Herramientas |

## 🎯 Lista de Verificación de Finalización

Rastrea tus finalizaciones de proyecto:

- [ ] Proyecto 1: Chatbot de Soporte al Cliente
- [ ] Proyecto 2: Sistema de Q&A de Documentos
- [ ] Proyecto 3: Agente de Revisión de Código
- [ ] Proyecto 4: Asistente de Investigación
- [ ] Proyecto 5: Servidor MCP del Tiempo

### Logros Bonus
- [ ] Completar todos los proyectos
- [ ] Añadir características personalizadas a cada proyecto
- [ ] Desplegar un proyecto a producción
- [ ] Construir tu propio proyecto desde cero
- [ ] Contribuir al código abierto

## 🤝 Pautas de Contribución

¿Quieres contribuir un proyecto?

### Requisitos
1. Código completo y funcional
2. Documentación clara
3. Requirements.txt
4. Uso de ejemplo
5. Pruebas (opcional pero recomendado)

### Pasos
1. Crea proyecto en nuevo directorio
2. Sigue pautas de estructura
3. Incluye README detallado
4. Prueba a fondo
5. Envía para revisión

## 📚 Recursos Adicionales

### Ejemplos de Código
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Anthropic Quickstarts](https://github.com/anthropics/anthropic-quickstarts)

### Documentación
- [Claude API Docs](https://platform.claude.com/docs/en/home)
- [MCP Documentation](https://modelcontextprotocol.io/docs/getting-started/intro)

### Comunidad
- [Discord Community](https://discord.gg/anthropic)
- [GitHub Discussions](https://github.com/anthropics/anthropic-sdk-python/discussions)

## 🎉 Próximos Pasos

1. Elige tu primer proyecto
2. Configura tu entorno
3. Estudia el código
4. Construye y modifica
5. ¡Comparte tus resultados!

---

**¿Listo para construir?** Empieza con [Proyecto 1: Chatbot de Soporte al Cliente](./01_customer_support_bot/README.md)
