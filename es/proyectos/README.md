# Proyectos de Ejemplo

Cuatro proyectos completos y ejecutables construidos sobre la API de Claude. Cada uno tiene una CLI, datos de ejemplo, un README con un diagrama de arquitectura y una **suite de pruebas offline que usa un cliente falso**, así que puedes ejecutar las pruebas y la mayoría de las demos sin clave de API y sin ningún coste.

| # | Proyecto | Ejecución offline | Pruebas |
|---|----------|-------------------|---------|
| 1 | [Bot de Soporte al Cliente](./1_bot_soporte_cliente/) | `python main.py --dry-run` | 26 |
| 2 | [Q&A de Documentos (RAG)](./2_sistema_qa_documentos/) | `python main.py search "refund"` (solo recuperación) | 27 |
| 3 | [Agente de Revisión de Código](./3_agente_revision_codigo/) | `python main.py --diff examples/sample.diff --repo examples/sample_repo --dry-run` | 64 |
| 4 | [Asistente de Investigación](./4_asistente_investigacion/) | `python main.py --offline-demo "your question"` | 31 |

Inicio rápido para cualquier proyecto:
```bash
cd es/proyectos/<proyecto>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q                      # offline
cp .env.example .env           # añade ANTHROPIC_API_KEY para ejecuciones reales
python main.py --help
```

> **Estado honesto:** el código se verificó contra las firmas del SDK instalado y la documentación oficial, y se probó con clientes falsos, pero **no se ha ejecutado contra la API real**. Espera tener que ajustar pequeños detalles (comportamiento del modelo, versiones de herramientas, umbrales de caché) en la primera ejecución real. Cada README indica lo que no está verificado. El Proyecto 5 de abajo sigue siendo un plan.

## 🚀 Proyectos Disponibles

### 1. [Chatbot de Soporte al Cliente](./1_bot_soporte_cliente/)
**Nivel**: Intermedio | **Tiempo**: 3-4 horas

Un chatbot de soporte al cliente con:
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

### 2. [Sistema de Q&A de Documentos](./2_sistema_qa_documentos/)
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

### 3. [Agente de Revisión de Código](./3_agente_revision_codigo/)
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

### 4. [Asistente de Investigación](./4_asistente_investigacion/)
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

### 5. Servidor MCP del Clima (planificado, aún no incluido)
**Nivel**: Intermedio | **Tiempo**: 2-3 horas

Servidor MCP personalizado para información meteorológica:
- Integración con APIs REST
- Múltiples fuentes de datos
- Integración con Claude Desktop
- Manejo de errores

**Tecnologías**: MCP, Claude API, REST APIs

**Características Clave**:
- Datos meteorológicos en tiempo real
- Información de pronóstico
- Búsqueda de ubicaciones
- Datos históricos

---

## 📋 Estructura del Proyecto

Los esqueletos actualmente contienen `README.md`, `requirements.txt` y `main.py`. Un proyecto terminado crecería hasta esta estructura:

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
python main.py   # o python src/main.py cuando adoptes la estructura anterior
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
1. Empieza con el Bot de Soporte al Cliente o el Servidor MCP del Clima
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
import anthropic

# Inicializar conversación
conversation = []
client = anthropic.Anthropic()

# Bucle
while True:
    user_input = get_user_input()
    conversation.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
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
    response = client.messages.create(model="claude-sonnet-5-5", max_tokens=1024,
                                      tools=tools, messages=messages)

    if response.stop_reason == "tool_use":
        # Ejecuta cada bloque tool_use, añade el turno del asistente y un
        # turno de usuario con bloques tool_result, y vuelve a iterar
        result = execute_tool(...)
    else:
        done = True
```

### Patrón 3: Sistema RAG
```python
# Configuración (los embeddings vienen de un proveedor de terceros como Voyage AI;
# Anthropic no ofrece un endpoint de embeddings)
vectordb = setup_vector_database()
documents = load_documents()
vectordb.add(documents)

# Consulta
def query(question):
    # Recuperar documentos relevantes
    docs = vectordb.search(question)

    # Generar respuesta con contexto
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
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
batch = client.messages.batches.create(requests=requests)

# Monitorizar progreso
while batch.processing_status != "ended":
    time.sleep(10)
    batch = client.messages.batches.retrieve(batch.id)

# Procesar resultados (relaciona por custom_id; el orden no está garantizado)
for entry in client.messages.batches.results(batch.id):
    ...
```

## 📊 Comparación de Proyectos

| Proyecto | Dificultad | Tiempo | Tecnologías Clave | Mejor Para Aprender |
|---------|-----------|------|------------------|-------------------|
| Soporte al Cliente | ⭐⭐ | 3-4h | Streaming, Tools | IA Conversacional |
| Q&A de Documentos | ⭐⭐⭐ | 4-6h | RAG, Caching | Recuperación de Información |
| Revisión de Código | ⭐⭐⭐ | 4-5h | Agents, APIs | Sistemas Autónomos |
| Asistente de Investigación | ⭐⭐⭐ | 5-6h | Multi-Agent | Flujos de Trabajo Complejos |
| Servidor MCP del Clima | ⭐⭐ | 2-3h | MCP, APIs | Integración de Herramientas |

## 🎯 Lista de Verificación de Finalización

Rastrea tus finalizaciones de proyecto:

- [ ] Proyecto 1: Chatbot de Soporte al Cliente
- [ ] Proyecto 2: Sistema de Q&A de Documentos
- [ ] Proyecto 3: Agente de Revisión de Código
- [ ] Proyecto 4: Asistente de Investigación
- [ ] Proyecto 5: Servidor MCP del Clima

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

**¿Listo para construir?** Empieza con [Proyecto 1: Chatbot de Soporte al Cliente](1_bot_soporte_cliente/README.md)
