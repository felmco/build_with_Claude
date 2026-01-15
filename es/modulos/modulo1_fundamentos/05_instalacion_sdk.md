# 1.2 Instalando el SDK de Anthropic

## Introducción
El SDK de Python de Anthropic es la biblioteca oficial para interactuar con la API de Claude. Proporciona una interfaz limpia y "Pythonica" con características integradas como manejo de errores, reintentos y sugerencias de tipo (type hints).

## Prerrequisitos
- Python 3.7 o superior
- pip (instalador de paquetes de Python)
- Entorno virtual (recomendado)

## Métodos de Instalación

### Método 1: Usando pip (Recomendado)

```bash
pip install anthropic
```

### Método 2: Usando pip con versión específica

```bash
# Instalar versión específica
pip install anthropic==0.40.0

# Instalar última versión preliminar (pre-release)
pip install --pre anthropic
```

### Método 3: Desde la fuente (Avanzado)

```bash
git clone https://github.com/anthropics/anthropic-sdk-python.git
cd anthropic-sdk-python
pip install -e .
```

## Configurando un Entorno Virtual

Se recomienda encarecidamente usar un entorno virtual para evitar conflictos de dependencias.

### Usando venv (Biblioteca Estándar)

```bash
# Crear entorno virtual
python -m venv claude_env

# Activar en macOS/Linux
source claude_env/bin/activate

# Activar en Windows
claude_env\Scripts\activate

# Instalar SDK de Anthropic
pip install anthropic

# Verificar instalación
python -c "import anthropic; print(anthropic.__version__)"
```

### Usando conda

```bash
# Crear entorno conda
conda create -n claude_env python=3.11

# Activar entorno
conda activate claude_env

# Instalar SDK
pip install anthropic
```

## Verificando la Instalación

Crea un archivo de prueba para verificar la instalación:

**test_installation.py**:
```python
#!/usr/bin/env python3
"""Script de prueba para verificar la instalación del SDK de Anthropic"""

import sys

def test_import():
    """Probar si el paquete anthropic puede ser importado"""
    try:
        import anthropic
        print(f"✅ SDK de Anthropic instalado exitosamente!")
        print(f"   Versión: {anthropic.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Falló la importación de anthropic: {e}")
        return False

def test_client_creation():
    """Probar si el cliente puede ser instanciado"""
    try:
        from anthropic import Anthropic

        # Esto funcionará incluso sin clave API para pruebas
        client = Anthropic(api_key="test-key")
        print(f"✅ Instanciación del cliente exitosa!")
        return True
    except Exception as e:
        print(f"❌ Falló la creación del cliente: {e}")
        return False

def check_python_version():
    """Comprobar si la versión de Python es compatible"""
    version = sys.version_info
    print(f"Versión de Python: {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 7:
        print("✅ La versión de Python es compatible")
        return True
    else:
        print("❌ Se requiere Python 3.7+")
        return False

if __name__ == "__main__":
    print("Probando Instalación del SDK de Anthropic\n" + "="*40)

    checks = [
        check_python_version(),
        test_import(),
        test_client_creation()
    ]

    if all(checks):
        print("\n🎉 ¡Todas las comprobaciones pasaron! Listo para usar la API de Claude")
    else:
        print("\n⚠️  Algunas comprobaciones fallaron. Por favor revisa los errores arriba")
```

Ejecuta la prueba:
```bash
python test_installation.py
```

## Visión General de Características del SDK

El SDK de Python de Anthropic proporciona:

### 1. Cliente Síncrono
```python
from anthropic import Anthropic

client = Anthropic(api_key="tu-clave-api")
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "¡Hola!"}]
)
```

### 2. Cliente Asíncrono
```python
import asyncio
from anthropic import AsyncAnthropic

async def main():
    client = AsyncAnthropic(api_key="tu-clave-api")
    message = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "¡Hola!"}]
    )
    print(message.content)

asyncio.run(main())
```

### 3. Soporte de Streaming
```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Cuéntame una historia"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### 4. Sugerencias de Tipo (Type Hints)
```python
from anthropic.types import Message, MessageParam

# Seguridad de tipos completa con autocompletado de IDE
messages: list[MessageParam] = [
    {"role": "user", "content": "Hola"}
]

response: Message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=messages
)
```

### 5. Manejo de Errores Integrado
```python
from anthropic import (
    APIError,
    APIConnectionError,
    RateLimitError,
    APIStatusError
)

try:
    response = client.messages.create(...)
except RateLimitError as e:
    print(f"Límite de velocidad excedido: {e}")
except APIConnectionError as e:
    print(f"Error de conexión: {e}")
except APIError as e:
    print(f"Error de API: {e}")
```

## Dependencias Adicionales

Para características específicas, puedes necesitar paquetes adicionales:

### Para Procesamiento de Imágenes
```bash
pip install anthropic Pillow
```

### Para Soporte Asíncrono
```bash
pip install anthropic httpx[http2]
```

### Para Desarrollo
```bash
pip install anthropic pytest python-dotenv
```

## Creando un requirements.txt

**requirements.txt**:
```txt
anthropic>=0.40.0
python-dotenv>=1.0.0
httpx[http2]>=0.25.0
```

Instalar todas las dependencias:
```bash
pip install -r requirements.txt
```

## Problemas Comunes de Instalación

### Problema 1: Errores de Certificado SSL

**Problema**: Falla la verificación SSL
```
SSLError: certificate verify failed
```

**Solución**:
```bash
# Actualizar certifi
pip install --upgrade certifi

# O usar certificados del sistema
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
```

### Problema 2: Permiso Denegado

**Problema**: Sin permiso para instalar globalmente
```
ERROR: Could not install packages due to an EnvironmentError
```

**Solución**:
```bash
# Usar flag --user
pip install --user anthropic

# O usar entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate
pip install anthropic
```

### Problema 3: Conflictos de Versión

**Problema**: Conflictos de dependencia con otros paquetes

**Solución**:
```bash
# Crear entorno aislado
python -m venv fresh_env
source fresh_env/bin/activate
pip install anthropic

# O especificar restricciones de versión
pip install 'anthropic>=0.40.0,<1.0.0'
```

### Problema 4: Errores de Importación Después de la Instalación

**Problema**: `ModuleNotFoundError: No module named 'anthropic'`

**Solución**:
```bash
# Verificar que estás usando el Python/pip correcto
which python
which pip

# Comprobar paquetes instalados
pip list | grep anthropic

# Reinstalar
pip uninstall anthropic
pip install anthropic
```

## Recomendaciones de Configuración de IDE

### VS Code
1. Instalar extensión de Python
2. Seleccionar intérprete del entorno virtual
3. Habilitar comprobación de tipos:

**settings.json**:
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.analysis.typeCheckingMode": "basic"
}
```

### PyCharm
1. Configurar intérprete de Python
2. Instalar SDK de Anthropic en el entorno del proyecto
3. Habilitar inspección de type hints

## Plantilla de Inicio Rápido

Crea una estructura de proyecto básica:

```bash
mkdir mi_proyecto_claude
cd mi_proyecto_claude
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install anthropic python-dotenv
```

**estructura_proyecto**:
```
mi_proyecto_claude/
├── venv/
├── .env
├── requirements.txt
├── main.py
└── README.md
```

**main.py**:
```python
"""Plantilla básica de cliente API de Claude"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def main():
    """Función principal"""
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "¡Hola, Claude!"}
        ]
    )
    print(message.content[0].text)

if __name__ == "__main__":
    main()
```

## Actualizando el SDK

Mantén tu SDK actualizado para las últimas características y correcciones de errores:

```bash
# Comprobar versión actual
pip show anthropic

# Actualizar a la última versión
pip install --upgrade anthropic

# Actualizar todas las dependencias
pip install --upgrade -r requirements.txt
```

## Próximos Pasos
- Aprende sobre [Gestión de Claves API](06_claves_api.md)
- Haz [Tu Primera Llamada a la API](07_primera_llamada_api.md)

## Recursos Adicionales
- [GitHub Oficial del SDK de Python](https://github.com/anthropics/anthropic-sdk-python)
- [Documentación del SDK](https://platform.claude.com/docs/en/sdk/python)
- [Paquete PyPI](https://pypi.org/project/anthropic/)
