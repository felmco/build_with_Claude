# 1.3 Gestión de Claves API

## Introducción
Las claves API son tus credenciales para acceder a la API de Claude. La gestión adecuada de las claves API es crucial para la seguridad y para prevenir el acceso no autorizado.

## Obteniendo Tu Clave API

### Paso 1: Crear una Cuenta de Anthropic
1. Visita [console.anthropic.com](https://console.anthropic.com)
2. Regístrate o inicia sesión
3. Completa cualquier verificación requerida

### Paso 2: Generar una Clave API
1. Navega a **Settings** (Configuración) → **API Keys** (Claves API)
2. Haz clic en **Create Key** (Crear Clave)
3. Dale a tu clave un nombre descriptivo (ej. "Desarrollo", "Producción")
4. Copia la clave inmediatamente (¡no la volverás a ver!)
5. Guárdala de forma segura

## Mejores Prácticas de Seguridad para Claves API

### ❌ NUNCA Hagas Esto
```python
# ¡NO codifiques (hardcode) claves API en tu código!
client = Anthropic(api_key="sk-ant-api03-abc123...")  # ¡MAL!

# ¡NO envíes (commit) claves API al control de versiones!
# ¡NO compartas claves API en repositorios públicos!
# ¡NO registres (log) claves API en los registros de la aplicación!
# ¡NO envíes claves API en URLs o parámetros de consulta!
```

### ✅ HAZ Esto en su Lugar
```python
# SÍ usa variables de entorno
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# SÍ usa archivos de configuración (no rastreados por git)
# SÍ rota las claves regularmente
# SÍ usa claves diferentes para desarrollo/staging/producción
# SÍ monitoriza el uso de claves
```

## Método 1: Variables de Entorno (Recomendado)

### En macOS/Linux

**Temporal (solo sesión actual)**:
```bash
export ANTHROPIC_API_KEY='tu-clave-api-aqui'
```

**Permanente (añadir a la configuración del shell)**:
```bash
# Para bash (~/.bashrc o ~/.bash_profile)
echo 'export ANTHROPIC_API_KEY="tu-clave-api-aqui"' >> ~/.bashrc
source ~/.bashrc

# Para zsh (~/.zshrc)
echo 'export ANTHROPIC_API_KEY="tu-clave-api-aqui"' >> ~/.zshrc
source ~/.zshrc
```

### En Windows

**PowerShell (temporal)**:
```powershell
$env:ANTHROPIC_API_KEY="tu-clave-api-aqui"
```

**PowerShell (permanente)**:
```powershell
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'tu-clave-api-aqui', 'User')
```

**Command Prompt (temporal)**:
```cmd
set ANTHROPIC_API_KEY=tu-clave-api-aqui
```

### Verificando Variable de Entorno

```python
import os

# Comprobar si la clave API está configurada
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print("✅ La clave API está configurada")
    print(f"   Prefijo de la clave: {api_key[:10]}...")  # Solo mostrar primeros 10 caracteres
else:
    print("❌ Clave API no encontrada")
```

## Método 2: Archivo .env (Desarrollo)

### Paso 1: Instalar python-dotenv
```bash
pip install python-dotenv
```

### Paso 2: Crear Archivo .env

**.env**:
```bash
# Configuración de la API de Anthropic
ANTHROPIC_API_KEY=tu-clave-api-aqui
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929

# Configuraciones opcionales
MAX_TOKENS=1024
TEMPERATURE=1.0
```

### Paso 3: Añadir .env a .gitignore

**.gitignore**:
```
# Variables de entorno
.env
.env.local
.env.*.local

# Claves API
*.key
secrets.json
```

### Paso 4: Cargar en Tu Código

```python
import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializar cliente
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Usar otras variables de entorno
model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
max_tokens = int(os.getenv("MAX_TOKENS", "1024"))
```

## Método 3: Archivos de Configuración

### Usando Configuración JSON

**config.json** (añadir a .gitignore):
```json
{
    "api_key": "tu-clave-api-aqui",
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "temperature": 1.0
}
```

**config_loader.py**:
```python
import json
from pathlib import Path
from anthropic import Anthropic

def load_config(config_path: str = "config.json"):
    """Cargar configuración desde archivo JSON"""
    with open(config_path, 'r') as f:
        return json.load(f)

def create_client(config_path: str = "config.json"):
    """Crear cliente Anthropic desde archivo de configuración"""
    config = load_config(config_path)
    return Anthropic(api_key=config["api_key"])

# Uso
client = create_client()
```

### Usando Módulo de Configuración Python

**config.py**:
```python
import os

class Config:
    """Configuración de la aplicación"""

    # Configuración de la API
    API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

    # Valores predeterminados de la petición
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "1.0"))

    # Configuraciones de la aplicación
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls):
        """Validar configuración requerida"""
        if not cls.API_KEY:
            raise ValueError("ANTHROPIC_API_KEY no establecida")
        return True
```

**main.py**:
```python
from anthropic import Anthropic
from config import Config

# Validar configuración
Config.validate()

# Crear cliente
client = Anthropic(api_key=Config.API_KEY)

# Usar configuración
response = client.messages.create(
    model=Config.MODEL,
    max_tokens=Config.MAX_TOKENS,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Método 4: Gestión de Secretos en la Nube

### AWS Secrets Manager

```python
import boto3
import json
from anthropic import Anthropic

def get_secret(secret_name: str, region_name: str = "us-east-1"):
    """Recuperar secreto de AWS Secrets Manager"""
    client = boto3.client('secretsmanager', region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Uso
secrets = get_secret("prod/anthropic/api-key")
client = Anthropic(api_key=secrets["api_key"])
```

### Google Cloud Secret Manager

```python
from google.cloud import secretmanager
from anthropic import Anthropic

def get_secret(project_id: str, secret_id: str, version: str = "latest"):
    """Recuperar secreto de Google Cloud Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Uso
api_key = get_secret("mi-proyecto", "anthropic-api-key")
client = Anthropic(api_key=api_key)
```

### Azure Key Vault

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from anthropic import Anthropic

def get_secret(vault_url: str, secret_name: str):
    """Recuperar secreto de Azure Key Vault"""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    return client.get_secret(secret_name).value

# Uso
api_key = get_secret("https://mi-boveda.vault.azure.net", "anthropic-api-key")
client = Anthropic(api_key=api_key)
```

## Gestión de Múltiples Claves API

### Escenario 1: Múltiples Entornos

```python
import os
from anthropic import Anthropic

class ClientFactory:
    """Fábrica para crear clientes específicos de entorno"""

    @staticmethod
    def create(environment: str = "development"):
        """Crear cliente para entorno específico"""
        key_map = {
            "development": os.getenv("ANTHROPIC_DEV_KEY"),
            "staging": os.getenv("ANTHROPIC_STAGING_KEY"),
            "production": os.getenv("ANTHROPIC_PROD_KEY")
        }

        api_key = key_map.get(environment)
        if not api_key:
            raise ValueError(f"Clave API no encontrada para entorno: {environment}")

        return Anthropic(api_key=api_key)

# Uso
dev_client = ClientFactory.create("development")
prod_client = ClientFactory.create("production")
```

### Escenario 2: Múltiples Proyectos

**.env**:
```bash
# Proyecto A
PROJECT_A_API_KEY=sk-ant-api03-...

# Proyecto B
PROJECT_B_API_KEY=sk-ant-api03-...
```

```python
import os
from anthropic import Anthropic

# Crear clientes para diferentes proyectos
project_a_client = Anthropic(api_key=os.getenv("PROJECT_A_API_KEY"))
project_b_client = Anthropic(api_key=os.getenv("PROJECT_B_API_KEY"))
```

## Rotación de Claves API

### ¿Por Qué Rotar Claves?
- Mejor práctica de seguridad
- Recuperación de clave comprometida
- Cambios de miembros del equipo
- Requisitos de cumplimiento

### Estrategia de Rotación

```python
import os
from datetime import datetime
from anthropic import Anthropic

class RotatingKeyClient:
    """Cliente con rotación automática de claves"""

    def __init__(self):
        self.primary_key = os.getenv("ANTHROPIC_API_KEY_PRIMARY")
        self.secondary_key = os.getenv("ANTHROPIC_API_KEY_SECONDARY")
        self.current_client = Anthropic(api_key=self.primary_key)

    def rotate_key(self):
        """Cambiar a clave secundaria"""
        print(f"Rotando a clave secundaria en {datetime.now()}")
        self.current_client = Anthropic(api_key=self.secondary_key)

    def get_client(self):
        """Obtener cliente activo actual"""
        return self.current_client
```

### Lista de Verificación de Rotación
1. ✅ Generar nueva clave API en la consola
2. ✅ Actualizar clave secundaria en el entorno
3. ✅ Probar clave secundaria
4. ✅ Cambiar a clave secundaria
5. ✅ Revocar antigua clave primaria
6. ✅ Actualizar documentación

## Monitorizando el Uso de Claves API

### Comprobar Uso Programáticamente

```python
from anthropic import Anthropic

client = Anthropic()

# Nota: La monitorización de uso se hace típicamente vía Consola
# Este es un marcador de posición para cuando la API lo soporte
def check_usage():
    """Comprobar uso de API (vía Consola actualmente)"""
    print("Comprobar uso en: https://console.anthropic.com/settings/usage")
```

### Configurar Alertas

1. **Alertas de Consola**: Configurar en la Consola de Anthropic
2. **Monitorización Personalizada**: Rastrear uso en tu aplicación

```python
import logging
from anthropic import Anthropic

class MonitoredClient:
    """Cliente con monitorización de uso"""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.request_count = 0
        self.token_count = 0

    def create_message(self, **kwargs):
        """Crear mensaje con monitorización"""
        response = self.client.messages.create(**kwargs)

        # Rastrear uso
        self.request_count += 1
        self.token_count += response.usage.input_tokens + response.usage.output_tokens

        logging.info(f"Petición #{self.request_count} | Tokens: {self.token_count}")

        return response
```

## Solución de Problemas

### Error: Clave API Inválida

```python
from anthropic import APIError, AuthenticationError

try:
    client = Anthropic(api_key="invalid-key")
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except AuthenticationError as e:
    print("❌ Autenticación fallida:")
    print("   - Comprueba si la clave API es correcta")
    print("   - Verifica que la clave no esté expirada")
    print("   - Asegúrate de que la clave tenga los permisos adecuados")
```

### Error: Clave API No Encontrada

```python
import os
from anthropic import Anthropic

# Validar antes de crear cliente
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise EnvironmentError(
        "ANTHROPIC_API_KEY no encontrada. "
        "Configúrala usando: export ANTHROPIC_API_KEY='tu-clave'"
    )

client = Anthropic(api_key=api_key)
```

### Mejor Práctica: Función de Validación

```python
import os
import sys
from anthropic import Anthropic, AuthenticationError

def validate_api_key() -> str:
    """Validar y devolver clave API"""

    # Comprobar si la clave existe
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Variable de entorno ANTHROPIC_API_KEY no establecida")
        print("\nPara establecerla:")
        print("  export ANTHROPIC_API_KEY='tu-clave-api'")
        sys.exit(1)

    # Comprobar formato de clave
    if not api_key.startswith("sk-ant-api"):
        print("⚠️  Advertencia: El formato de la clave API parece incorrecto")
        print("   Las claves deberían empezar con 'sk-ant-api'")

    # Probar clave con llamada a API
    try:
        client = Anthropic(api_key=api_key)
        client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}]
        )
        print("✅ Clave API validada exitosamente")
        return api_key
    except AuthenticationError:
        print("❌ Validación de clave API fallida")
        sys.exit(1)

# Uso en tu aplicación
api_key = validate_api_key()
client = Anthropic(api_key=api_key)
```

## Lista de Verificación de Seguridad

- ✅ Claves API almacenadas en variables de entorno o gestor de secretos
- ✅ Archivo .env añadido a .gitignore
- ✅ Sin claves API en código o registros (logs)
- ✅ Claves diferentes para desarrollo/staging/producción
- ✅ Horario de rotación de claves regular
- ✅ Monitorización de uso habilitada
- ✅ Acceso de equipo gestionado adecuadamente
- ✅ Claves revocadas para miembros del equipo que se van

## Próximos Pasos
- Haz [Tu Primera Llamada a la API](07_primera_llamada_api.md)
- Aprende sobre [Manejo de Peticiones y Respuestas](08_solicitud_respuesta.md)

## Recursos Adicionales
- [Consola de Anthropic](https://console.anthropic.com)
- [Mejores Prácticas de Claves API](https://platform.claude.com/docs/en/security/api-keys)
- [Documentación de python-dotenv](https://pypi.org/project/python-dotenv/)
