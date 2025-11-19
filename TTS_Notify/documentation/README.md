# TTS Notify

Sistema de notificaciones Text-to-Speech para macOS usando el motor TTS nativo.

## Características

- **Cero dependencias externas** - Usa el comando nativo `say` de macOS
- **Detección automática de voces** - Detecta ~84+ voces del sistema automáticamente
- **Búsqueda flexible de voces** - Soporta búsqueda sin acentos, case-insensitive y parcial
- **Servidor MCP** - Integración completa con Claude Desktop
- **CLI tool** - Herramienta de línea de comandos para uso directo
- **Modo UVX** - Ejecución directa sin instalación (tipo npx)

## Arquitectura

TTS Notify opera en tres modos:

1. **Servidor MCP** - Se integra con Claude Desktop como servidor MCP
2. **CLI Tool** - Herramienta independiente instalada globalmente
3. **UVX Mode** - Ejecución directa sin instalación

## Instalación Rápida

### Método 1: UVX (Recomendado para desarrollo)

```bash
# Instalar UV primero
brew install uv

# Ejecutar directamente sin instalación
uvx --from TTS_Notify tts-notify "Hola mundo"

# Listar voces disponibles
uvx --from TTS_Notify tts-notify --list
```

### Método 2: Instalación Global

```bash
pip install tts-notify

# Usar directamente
tts-notify "Mensaje de prueba"
tts-notify --voice Monica --rate 200 "Texto con voz personalizada"
```

### Método 3: Servidor MCP

```bash
# Clonar repositorio
git clone <repository-url>
cd TTS_Notify

# Ejecutar instalador
./installers/install-mcp.sh
```

## Uso

### CLI

```bash
# Texto a voz con voz por defecto
tts-notify "Hola, este es un mensaje de prueba"

# Usar voz específica
tts-notify --voice Jorge "Hola, soy Jorge"

# Ajustar velocidad (100-300 palabras por minuto)
tts-notify --rate 200 "Texto rápido"

# Guardar como archivo de audio
tts-notify --save notification "Notificación guardada"

# Listar todas las voces disponibles
tts-notify --list

# Ayuda completa
tts-notify --help
```

### Servidor MCP

Configura en Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "tts-notify": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/TTS_Notify/src/mcp_server.py"]
    }
  }
}
```

Herramientas disponibles:
- `speak_text` - Reproduce texto con voz y velocidad configurables
- `list_voices` - Lista todas las voces disponibles categorizadas
- `save_audio` - Guarda texto como archivo de audio AIFF

## Voces Disponibles

TTS Notify detecta automáticamente **todas las voces** del sistema (~84+ voces).

### Categorías

**Español (16 voces):**
- Eddy, Flo, Grandma, Grandpa, Reed, Rocko, Sandy, Shelley (España y México)

**Enhanced/Premium (12 voces):**
- Angélica (México), Francisca (Chile), Jorge (España), Paulina (México)
- Mónica (España), Juan (México), Diego (Argentina), Carlos (Colombia)
- Isabela (Argentina), Marisol (España), Soledad (Colombia), Jimena (Colombia)

**Siri (cuando están instaladas):**
- Siri Female, Siri Male (auto-detectadas)

### Búsqueda Flexible

Los nombres de voz soportan búsqueda flexible:
- **Exacta**: `Monica`, `Angélica`, `Jorge`
- **Case-insensitive**: `angelica`, `MONICA`, `jorge`
- **Parcial**: `angel` → Angélica, `franc` → Francisca
- **Sin acentos**: `angelica` encuentra `Angélica`

## Estructura del Proyecto

```
TTS_Notify/
├── src/
│   ├── mcp_server.py      # Servidor MCP
│   ├── cli.py            # CLI con detección de voces
│   ├── __main__.py       # Entry point del módulo
│   └── __init__.py       # Paquete
├── documentation/
│   ├── README.md         # Esta guía
│   ├── INSTALLATION.md   # Guía de instalación detallada
│   ├── USAGE.md          # Ejemplos de uso avanzado
│   └── VOICES.md         # Referencia completa de voces
├── installers/
│   ├── install-mcp.sh    # Instalador del servidor MCP
│   └── install-cli.sh    # Instalador CLI global
├── pyproject.toml        # Configuración del paquete
├── requirements.txt      # Dependencias
└── LICENSE              # Licencia MIT
```

## Configuración

### Variables de Entorno

- `TTS_DEFAULT_VOICE` - Voz por defecto (default: "Monica")
- `TTS_DEFAULT_RATE` - Velocidad por defecto (default: 175)
- `TTS_OUTPUT_DIR` - Directorio para archivos de audio (default: Desktop)

### Integración con Claude Code

TTS Notify incluye hooks para Claude Code en `.claude/hooks/`:

```bash
# Habilitar lectura de respuestas
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=175
export TTS_MAX_LENGTH=500

# Habilitar confirmación de prompts
export TTS_PROMPT_ENABLED=true
export TTS_PROMPT_VOICE=jorge
export TTS_PROMPT_RATE=200
```

## Requisitos

- **macOS** - Requiere motor TTS nativo `say`
- **Python 3.10+** - Para ejecución del servidor MCP y CLI
- **Claude Desktop** - Para integración MCP (opcional)

## Licencia

MIT License - ver archivo LICENSE para detalles.

## Contribuciones

Contribuciones son bienvenidas. Por favor:
1. Reportar issues en GitHub
2. Hacer fork y crear branches feature
3. Seguir el estilo del código existente
4. Probar con múltiples voces de macOS

## Soporte

- **Issues**: GitHub Issues
- **Documentación**: `/documentation/`
- **Ejemplos**: Ver `documentation/USAGE.md`