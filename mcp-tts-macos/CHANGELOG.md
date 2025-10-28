# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-10-28

### Arreglado
- 🐛 **Detección automática de voces**: El CLI ahora detecta automáticamente las voces en español disponibles en el sistema
- 🔧 Las voces ahora cambian correctamente según el argumento --voice
- ✅ Mejor manejo cuando faltan voces instaladas

### Añadido
- 🔍 Script de diagnóstico (diagnostico-voces.py) para verificar voces disponibles
- 📖 Guía completa de solución de problemas con voces (SOLUCION-VOCES.md)
- 💡 Mensajes más claros cuando no hay voces instaladas

### Mejorado
- La función `listar_voces()` ahora muestra las voces realmente disponibles
- Mejor manejo de errores cuando el comando `say` falla
- Documentación actualizada sobre instalación de voces

## [1.2.0] - 2025-10-28

### Añadido
- 🚀 **Soporte completo para uvx** (herramienta moderna de Python)
- Estructura de paquete Python moderna con pyproject.toml
- Módulo `tts_macos` con `__init__.py`, `__main__.py` y `cli.py`
- Guía completa de uso con uvx (UVX-GUIDE.md)
- Script de ejemplos interactivo (examples.sh)
- Soporte para `python -m tts_macos`
- Entry points configurables en pyproject.toml

### Mejorado
- README actualizado con tres métodos de uso
- Estructura del proyecto más profesional
- CLI con mejor manejo de versiones
- Documentación expandida con ejemplos de uvx

### Técnico
- src/tts_macos/ - Estructura de paquete Python estándar
- pyproject.toml - Configuración moderna (PEP 517/518)
- Soporte para hatchling como build backend
- Compatible con pip, pipx, uvx y instalación directa

## [1.1.0] - 2025-10-28

### Añadido
- Modo CLI añadido para uso desde terminal
- Script tts-macos ejecutable
- Instalador CLI (install-cli.sh)
- Setup.py para instalación con pip
- Guía completa CLI (CLI-GUIDE.md)
- Soporte para argumentos tipo npx
- Flags: --voice, --rate, --save, --list, --help

### Mejorado
- README.md actualizado con info CLI
- Mejor manejo de errores
- Documentación expandida
- Más ejemplos de uso

## [1.0.0] - 2025-10-28

### Añadido
- Servidor MCP inicial para Text-to-Speech en macOS
- Soporte para 6 voces en español (México, España, Argentina)
- Herramienta `speak_text` para reproducir audio
- Herramienta `list_voices` para listar voces disponibles
- Herramienta `save_audio` para guardar audio en archivos AIFF
- Control de velocidad de lectura (100-300 palabras por minuto)
- Script de instalación automatizada (`install.sh`)
- Script de prueba de voces (`test_tts.py`)
- Documentación completa en README.md
- Ejemplos de configuración para Claude Desktop
- Licencia MIT

### Voces soportadas
- Monica (Español Mexicano - Mujer)
- Paulina (Español Mexicano - Mujer)
- Jorge (Español España - Hombre)
- Juan (Español España - Hombre)
- Diego (Español Argentino - Hombre)
- Angelica (Español México - Mujer)

### Características técnicas
- Ejecución asíncrona de comandos TTS
- Manejo robusto de errores
- Validación de parámetros
- Integración completa con Claude Desktop

[1.2.0]: https://github.com/tu-usuario/mcp-tts-macos/releases/tag/v1.2.0
[1.1.0]: https://github.com/tu-usuario/mcp-tts-macos/releases/tag/v1.1.0
[1.0.0]: https://github.com/tu-usuario/mcp-tts-macos/releases/tag/v1.0.0
