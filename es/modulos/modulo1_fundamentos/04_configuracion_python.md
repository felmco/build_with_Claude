# 1.2 Instalando Python y Dependencias

Antes de trabajar con la API de Claude, necesitas configurar un entorno de desarrollo adecuado. Esta guía cubre la instalación de Python, la configuración de un entorno virtual y la instalación de las bibliotecas necesarias.

## 1. Instalar Python

Necesitas **Python 3.7 o superior**.

### Comprobar si Python está instalado
Abre tu terminal o símbolo del sistema y ejecuta:
```bash
python --version
# O
python3 --version
```

Si ves un número de versión (ej., `Python 3.12.0`), estás listo.
Si no, descárgalo desde [python.org](https://www.python.org/downloads/).

## 2. Configurar un Directorio de Proyecto

Crea una carpeta para tu proyecto:
```bash
mkdir mi_proyecto_claude
cd mi_proyecto_claude
```

## 3. Crear un Entorno Virtual (Recomendado)

Usar un entorno virtual mantiene las dependencias de tu proyecto aisladas de tu Python del sistema.

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Deberías ver `(venv)` aparecer en el prompt de tu terminal.

## 4. Instalar Dependencias

Instala el SDK de `anthropic` y `python-dotenv` (para gestionar claves API de forma segura).

```bash
pip install anthropic python-dotenv
```

## 5. Verificar Instalación

Crea un script de prueba `test_install.py`:

```python
import anthropic
print("Versión del SDK de Anthropic:", anthropic.__version__)
```

Ejecútalo:
```bash
python test_install.py
```

Si imprime el número de versión sin errores, ¡tu configuración está completa!

## Próximos Pasos
- Aprende cómo gestionar tus claves en [Gestión de Claves API](06_claves_api.md).
