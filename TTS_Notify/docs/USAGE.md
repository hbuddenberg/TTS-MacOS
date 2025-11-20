# Usage Guide - TTS Notify v2.0.0

Comprehensive usage guide covering all interfaces and advanced features of TTS Notify v2.0.0 modular text-to-speech system.

## 🎯 Quick Start by Interface

### 1. CLI Interface

```bash
# Installation
./installers/install.sh development
source venv/bin/activate

# Basic usage
tts-notify "Hello world"

# With voice and rate
tts-notify "Hola mundo" --voice monica --rate 200

# List available voices
tts-notify --list

# Save audio file
tts-notify "Test message" --save output --format wav

# System information
tts-notify --info
```

### 2. MCP Server (Claude Desktop)

```bash
# Start MCP server
tts-notify --mode mcp

# Automatic Claude Desktop configuration
# Voice search with natural language in Claude:
"Lee en voz alta: Hola mundo"
"Lista todas las voces en español"
"Guarda este texto como archivo: prueba de audio"
```

### 3. REST API

```bash
# Start API server
tts-notify --mode api

# API available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs

# Test endpoints
curl http://localhost:8000/status
curl -X POST http://localhost:8000/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "monica"}'
```

## 🎵 Voice System v2.0.0

### 84+ Voice Support with Categories

The v2.0.0 voice system automatically detects all system voices and categorizes them:

```bash
# List all voices with categories
tts-notify --list

# Expected output:
Español (16 voces):
  • monica        • jorge        • angélica     • paulina
  • diego         • francisca    • carlos       • juan
  • isabela       • marisol      • soledad      • jimena
  • eddy          • flo          • grandma      • grandpa
  • reed          • rocko        • sandy        • shelley

Enhanced/Premium (12 voces):
  • angélica (enhanced)    • francisca (enhanced)
  • jorge (enhanced)       • paulina (enhanced)
  • mónica (enhanced)      • juan (enhanced)
  • diego (enhanced)       • carlos (enhanced)
  • isabela (enhanced)     • marisol (enhanced)
  • soledad (enhanced)     • jimena (enhanced)

Siri (2 voces):
  • siri female    • siri male

Otras voces del sistema: 50+
```

### Advanced Voice Search v2.0

The v2.0.0 search system is more flexible and intelligent:

```bash
# Exact match
tts-notify --voice monica "Test"

# Case-insensitive
tts-notify --voice MONICA "Test"

# Partial match
tts-notify --voice angel  # Finds Angélica

# Quality variants
tts-notify --voice "monica enhanced"  # Enhanced variant
tts-notify --voice "jorge premium"    # Premium variant

# Fallback behavior
tts-notify --voice nonexistent_voice "Test"  # → uses first Spanish voice
```

### Voice Filtering

```bash
# Filter by gender
tts-notify --list --gen female    # Female voices only
tts-notify --list --gen male      # Male voices only

# Filter by language
tts-notify --list --lang es_ES    # Spanish voices only
tts-notify --list --lang en_US    # English voices only

# Filter by voice type
tts-notify --list --type enhanced  # Enhanced voices only
tts-notify --list --type siri      # Siri voices only

# Compact format
tts-notify --list --compact
```

## ⚙️ Configuration System v2.0.0

### Environment Variables (30+ available)

```bash
# Voice Settings
export TTS_NOTIFY_VOICE=monica
export TTS_NOTIFY_RATE=175
export TTS_NOTIFY_LANGUAGE=es
export TTS_NOTIFY_QUALITY=enhanced

# Functionality
export TTS_NOTIFY_ENABLED=true
export TTS_NOTIFY_CACHE_ENABLED=true
export TTS_NOTIFY_LOG_LEVEL=INFO

# API Server
export TTS_NOTIFY_API_PORT=8000
export TTS_NOTIFY_API_HOST=localhost

# Output Settings
export TTS_NOTIFY_OUTPUT_FORMAT=aiff
export TTS_NOTIFY_OUTPUT_DIR=~/Desktop
export TTS_NOTIFY_AUTO_SAVE=false
```

### Configuration Profiles

```bash
# Use predefined profiles
tts-notify --profile claude-desktop  # Optimized for Claude Desktop
tts-notify --profile development      # Development with debugging
tts-notify --profile production       # Production ready
tts-notify --profile api-server       # API server optimized
tts-notify --profile accessibility    # Accessibility focused
```

### YAML Configuration Files

```bash
# Create configuration directory
mkdir -p ~/.config/tts-notify

# Copy default configurations
cp config/default.yaml ~/.config/tts-notify/
cp config/profiles.yaml ~/.config/tts-notify/

# Edit configuration
nano ~/.config/tts-notify/default.yaml
```

## 🚀 Interface-Specific Usage

### CLI Interface Advanced Features

```bash
# Multiple text processing
echo "Line 1\nLine 2\nLine 3" | tts-notify --voice jorge

# File reading
tts-notify --voice monica "$(cat README.md)"

# Pipeline operations
ls -la | tts-notify --voice angélica --rate 200

# Background execution
tts-notify "Background task" &

# Output to specific format
tts-notify "Test" --save output --format wav
tts-notify "Test" --save alert --format aiff

# System diagnostics
tts-notify --info
tts-notify --list --verbose
```

### MCP Server Tools

#### 1. speak_text Tool
```python
# Natural language usage in Claude Desktop
"Lee en voz alta: 'Este es un mensaje importante' con voz de Jorge"

"Reproduce el siguiente texto a 200 palabras por minuto: 'Alerta crítica'"

"Usa voz de Siri Female para leer: 'Notificación del sistema'"
```

#### 2. list_voices Tool
```python
"Lista todas las voces en español disponibles"

"Muestra las voces Enhanced y Premium disponibles"

"Filtra voces por género femenino"

"Busca voces que contengan 'siri'"
```

#### 3. save_audio Tool
```python
"Guarda el siguiente mensaje como archivo de audio: 'Notificación importante'"

"Crea un archivo llamado 'alarma' con el texto: 'Hora de la reunión'"

"Guarda en formato WAV el texto: 'Audio de alta calidad'"
```

#### 4. get_system_info Tool
```python
"Muestra información del sistema TTS Notify"

"Lista las variables de entorno configuradas"

"Verifica el estado del servidor MCP"
```

### REST API Endpoints

```bash
# Health check
curl http://localhost:8000/status

# Speak text
curl -X POST http://localhost:8000/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "monica", "rate": 175}'

# List voices
curl http://localhost:8000/voices

# Get voice info
curl http://localhost:8000/voices/monica

# Save audio
curl -X POST http://localhost:8000/save \
  -H "Content-Type: application/json" \
  -d '{"text": "Test message", "filename": "output", "voice": "jorge"}'

# Get file
curl http://localhost:8000/files/output.aiff

# System info
curl http://localhost:8000/info

# Interactive documentation
open http://localhost:8000/docs
```

## 🔧 Development & Testing

### Development Mode

```bash
# Install development dependencies
./installers/install.sh development
source venv/bin/activate

# Run with debug logging
export TTS_NOTIFY_LOG_LEVEL=DEBUG
tts-notify --debug "Test message"

# Test all interfaces
python src/main.py "CLI test"
python src/main.py --mode mcp  # MCP server mode
python src/main.py --mode api  # API server mode
```

### Testing Commands

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/test_core.py
pytest tests/test_api.py
pytest tests/test_cli.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run tests by markers
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests
```

### Code Quality

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Type checking
mypy src

# Linting
flake8 src
```

## 🛠️ Real-World Integration Examples

### 1. Notification System

```bash
#!/bin/bash
# notification_system.sh

# Load configuration
source ~/.config/tts-notify/config

notify() {
    local message="$1"
    local priority="${2:-normal}"

    case "$priority" in
        "urgent")
            tts-notify --voice "siri female" --rate 250 "🚨 URGENTE: $message"
            ;;
        "important")
            tts-notify --voice "jorge enhanced" --rate 200 "⚠️ $message"
            ;;
        *)
            tts-notify --voice "$TTS_NOTIFY_VOICE" "$message"
            ;;
    esac
}

# Usage examples
notify "Build completed successfully" "important"
notify "Email received from John Doe"
notify "Disk space critically low" "urgent"
```

### 2. Development Workflow Integration

```bash
#!/bin/bash
# dev_notifications.sh

# Pre-commit hook
pre_commit_notification() {
    tts-notify --voice "monica enhanced" "Pre-commit checks running..."
}

# Post-build notification
build_notification() {
    local result="$1"
    local project="$2"

    if [ "$result" = "success" ]; then
        tts-notify --voice "jorge" "✅ Build successful for $project"
    else
        tts-notify --voice "siri male" --rate 250 "❌ Build failed for $project"
    fi
}

# Test completion
test_notification() {
    local passed="$1"
    local failed="$2"

    tts-notify --voice "angélica" "✅ Tests completed: $passed passed, $failed failed"
}
```

### 3. API Integration

```python
#!/usr/bin/env python3
# api_client_example.py

import requests
import json

class TTSNotifyClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def speak(self, text, voice="monica", rate=175):
        """Speak text using TTS Notify API"""
        response = requests.post(
            f"{self.base_url}/speak",
            json={"text": text, "voice": voice, "rate": rate}
        )
        return response.json()

    def save_audio(self, text, filename, voice="monica"):
        """Save text as audio file"""
        response = requests.post(
            f"{self.base_url}/save",
            json={"text": text, "filename": filename, "voice": voice}
        )
        return response.json()

    def get_voices(self):
        """Get list of available voices"""
        response = requests.get(f"{self.base_url}/voices")
        return response.json()

# Usage
client = TTSNotifyClient()

# Speak text
client.speak("Hello world", voice="jorge", rate=200)

# Save audio
client.save_audio("Test message", "output", voice="angélica")

# List voices
voices = client.get_voices()
print(f"Available voices: {len(voices['voices'])}")
```

### 4. Claude Desktop Integration

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "tts-notify": {
      "command": "/Users/username/.local/bin/tts-notify",
      "args": ["--mode", "mcp"],
      "env": {
        "TTS_NOTIFY_VOICE": "monica",
        "TTS_NOTIFY_RATE": "175",
        "TTS_NOTIFY_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## 🔍 Advanced Troubleshooting

### Performance Issues

```bash
# Check voice caching performance
time tts-notify --list

# Test voice detection speed
export TTS_NOTIFY_CACHE_ENABLED=false
time tts-notify --list

# Monitor API performance
curl -w "@curl-format.txt" http://localhost:8000/status
```

### Configuration Debugging

```bash
# Show current configuration
tts-notify --info

# Test configuration profiles
tts-notify --profile claude-desktop --info

# Validate environment variables
env | grep TTS_NOTIFY_
```

### Voice Problems

```bash
# Test system voice directly
say -v monica "Test"

# Check voice availability
say -v "?" | grep -i monica

# Test fallback system
tts-notify --voice nonexistent "Test fallback"
```

## 📊 Performance Optimization

### Caching Configuration

```bash
# Enable voice caching (default: 5 minutes)
export TTS_NOTIFY_CACHE_ENABLED=true
export TTS_NOTIFY_CACHE_TTL=300

# Pre-load voices
tts-notify --list > /dev/null
```

### API Performance

```bash
# Configure API for production
export TTS_NOTIFY_API_HOST=0.0.0.0
export TTS_NOTIFY_API_PORT=8000
export TTS_NOTIFY_API_WORKERS=4

# Enable request logging
export TTS_NOTIFY_LOG_LEVEL=INFO
```

### Resource Management

```bash
# Monitor memory usage
ps aux | grep tts-notify

# Clean cache manually
rm -rf ~/.cache/tts-notify/

# Limit concurrent requests
export TTS_NOTIFY_MAX_CONCURRENT=10
```

## 🎯 Best Practices v2.0.0

### 1. Configuration Management
- Use environment variables for deployment-specific settings
- Create YAML files for complex configurations
- Use predefined profiles for common scenarios

### 2. Performance
- Enable voice caching for better performance
- Use enhanced voices for better quality and speed
- Configure appropriate timeouts for API usage

### 3. Security
- Validate input text before processing
- Use appropriate file paths for audio output
- Configure CORS properly for API deployment

### 4. Monitoring
- Use structured logging for production
- Monitor API endpoints for health checks
- Track voice usage and performance metrics

This v2.0.0 usage guide provides comprehensive coverage of all TTS Notify interfaces and features, enabling users to leverage the full power of the modular architecture.

## Uso Básico de CLI

### Comandos Esenciales

```bash
# Sintaxis básica
tts-notify [OPCIONES] "TEXTO A REPRODUCIR"

# Ejemplo simple
tts-notify "Hola mundo"

# Con voz específica
tts-notify --voice Monica "Hola, soy Monica"

# Con velocidad personalizada
tts-notify --rate 200 "Texto rápido"

# Guardar como archivo
tts-notify --save alerta "Mensaje importante"
```

### Lista de Voces

```bash
# Listar todas las voces del sistema
tts-notify --list

# Salida categorizada
Español (16 voces):
  • Monica        • Jorge        • Angélica     • Paulina
  • Diego         • Francisca    • Carlos       • Juan
  • Isabela       • Marisol      • Soledad      • Jimena
  • Eddy          • Flo          • Grandma      • Grandpa
  • Reed          • Rocko        • Sandy        • Shelley

Enhanced/Premium (12 voces):
  • Angélica (Enhanced)    • Francisca (Enhanced)
  • Jorge (Enhanced)       • Paulina (Enhanced)
  • Mónica (Enhanced)      • Juan (Enhanced)
  • Diego (Enhanced)       • Carlos (Enhanced)
  • Isabela (Enhanced)     • Marisol (Enhanced)
  • Soledad (Enhanced)     • Jimena (Enhanced)

Siri (2 voces):
  • Siri Female    • Siri Male

Otras voces del sistema: 50+
```

## Búsqueda Avanzada de Voces

### Estrategias de Búsqueda

TTS Notify implementa búsqueda flexible con 3 estrategias:

1. **Búsqueda exacta** (sin acentos, case-insensitive)
2. **Búsqueda por prefijo**
3. **Búsqueda por subcadena**

```bash
# Búsqueda exacta - encuentra "Angélica"
tts-notify --voice angelica "Hola"

# Búsqueda por prefijo - encuentra "Angélica"
tts-notify --voice angel "Hola"

# Búsqueda por subcadena - encuentra "Francisca"
tts-notify --voice franc "Hola"

# Case-insensitive
tts-notify --voice MONICA "Mayúsculas"
tts-notify --voice monica "minúsculas"
```

### Cadena de Fallback

Si una voz no se encuentra, TTS Notify sigue esta secuencia:

1. **Voz solicitada** → Búsqueda flexible
2. **Primera voz española** → Auto-detectada
3. **Monica** → Voz por defecto final

```bash
# Este voice fallback funciona:
tts-notify --voice voz_inexistente "Texto"  # → usa primera voz española
```

## Uso con Servidor MCP

### Configuración en Claude Desktop

```json
{
  "mcpServers": {
    "tts-notify": {
      "command": "/Users/tuusuario/TTS_Notify/venv/bin/python",
      "args": ["/Users/tuusuario/TTS_Notify/src/mcp_server.py"]
    }
  }
}
```

### Herramientas MCP Disponibles

#### 1. speak_text
```python
# Uso desde Claude
"Lee en voz alta: 'Este es un mensaje importante' con voz de Jorge"

# Con velocidad específica
"Reproduce el siguiente texto a 200 palabras por minuto: 'Alerta crítica'"
```

#### 2. list_voices
```python
"Lista todas las voces en español disponibles en el sistema"

"Muestra las voces Enhanced y Premium disponibles"
```

#### 3. save_audio
```python
"Guarda el siguiente mensaje como archivo de audio: 'Notificación del sistema'"
"Crea un archivo de audio llamado 'alarma' con el texto: 'Hora de la reunión'"
```

## Casos de Uso Prácticos

### 1. Sistema de Notificaciones

```bash
# Script de notificaciones
#!/bin/bash
#!/bin/bash

NOTIFICATION_FILE="$HOME/.notification_queue"

# Función para enviar notificación
notify() {
    local message="$1"
    local voice="${2:-Monica}"
    local rate="${3:-175}"

    tts-notify --voice "$voice" --rate "$rate" "$message"
}

# Ejemplos de uso
notify "Correo recibido de Juan Pérez" "Jorge" 180
notify "Reunión en 5 minutos" "Angélica" 200
notify "Proceso completado exitosamente" "Monica" 160

# Notificaciones prioritarias
critical_alert() {
    tts-notify --voice "Siri Female" --rate 250 "⚠️ $1 ⚠️"
}

critical_alert "Espacio en disco casi lleno"
```

### 2. Lectura de Archivos

```bash
# Leer archivo completo
tts-notify --voice Monica "$(cat important_email.txt)"

# Leer línea por línea
while IFS= read -r line; do
    tts-notify --voice Jorge "$line"
    sleep 1
done < document.txt

# Solo primeras 10 líneas
head -n 10 README.md | tts-notify --voice Angélica
```

### 3. Integración con Development

```bash
# Notificaciones de build
#!/bin/bash

build_success() {
    tts-notify --voice "Siri Female" --rate 200 "✅ Build exitoso en $1"
}

build_failed() {
    tts-notify --voice "Siri Male" --rate 250 "❌ Build fallido en $1"
}

test_complete() {
    tts-notify --voice Monica "✅ Tests completados: $1 passed, $2 failed"
}

# Uso en CI/CD
npm run build && build_success "frontend" || build_failed "frontend"
npm test && test_success "$?" || test_failed "$?"
```

### 4. Sistema de Recordatorios

```bash
#!/bin/bash
# reminder_system.sh

REMINDER_FILE="$HOME/.reminders"

add_reminder() {
    local time="$1"
    local message="$2"
    local voice="${3:-Monica}"

    echo "$time|$message|$voice" >> "$REMINDER_FILE"
    tts-notify --voice "$voice" "Recordatorio agregado: $message a las $time"
}

check_reminders() {
    local current_time=$(date +"%H:%M")

    while IFS='|' read -r time message voice; do
        if [ "$time" = "$current_time" ]; then
            tts-notify --voice "$voice" "⏰ Recordatorio: $message"
            # Eliminar recordatorio procesado
            sed -i '' "/^$time|/d" "$REMINDER_FILE"
        fi
    done < "$REMINDER_FILE"
}

# Uso
add_reminder "14:00" "Reunión con el equipo" "Jorge"
add_reminder "18:30" "Llamar al doctor" "Angélica"
```

## Integración con otras Herramientas

### 1. Alfred/Spotlight

```bash
# Crear workflow para Alfred
# Script: /usr/local/bin/tts-notify "{query}"
# Keyword: tts

# Uso: tts "Hola mundo"
```

### 2. Automator

```bash
# Crear acción "Ejecutar Shell Script"
# Comando: tts-notify --voice Monica "{input}"
```

### 3. Raycast

```bash
# Comando personalizado
# Script: tts-notify --voice Jorge "{query}"
# Placeholder: {query}
```

### 4. Keyboard Maestro

```bash
# Macro para leer texto seleccionado
# Action: Execute Shell Script
# Command: echo "%SystemClipboard%" | tts-notify --voice Monica
```

## Uso con Variables de Entorno

### Configuración Global

```bash
# Agregar a ~/.zshrc
export TTS_DEFAULT_VOICE="Jorge"
export TTS_DEFAULT_RATE="180"
export TTS_OUTPUT_DIR="$HOME/Documents/Audio"

# Recargar configuración
source ~/.zshrc
```

### Uso en Scripts

```bash
#!/bin/bash
# Respetar configuración del usuario

VOICE=${TTS_DEFAULT_VOICE:-"Monica"}
RATE=${TTS_DEFAULT_RATE:-175}
OUTPUT_DIR=${TTS_OUTPUT_DIR:-"$HOME/Desktop"}

tts-notify --voice "$VOICE" --rate "$RATE" "Mensaje personalizado"
```

### Configuración por Contexto

```bash
# Modo trabajo
export TTS_DEFAULT_VOICE="Jorge"
export TTS_DEFAULT_RATE="180"

# Modo personal
export TTS_DEFAULT_VOICE="Angélica"
export TTS_DEFAULT_RATE="160"

# Modo accesibilidad
export TTS_DEFAULT_VOICE="Siri Female"
export TTS_DEFAULT_RATE="200"
```

## Técnicas Avanzadas

### 1. Procesamiento de Audio

```bash
# Convertir a diferentes formatos
ffmpeg -i notification.aiff -f mp3 notification.mp3

# Ajustar volumen
ffmpeg -i input.aiff -filter:a "volume=1.5" output.aiff

# Combinar múltiples audios
ffmpeg -i "concat:part1.aiff|part2.aiff|part3.aiff" -c copy output.aiff
```

### 2. Detección Automática de Idioma

```bash
#!/bin/bash
# detect_language_and_speak.sh

TEXT="$1"

if echo "$TEXT" | grep -q -E "[ñáéíóú]"; then
    tts-notify --voice Jorge "$TEXT"
else
    tts-notify --voice "Siri Female" "$TEXT"
fi
```

### 3. Sistema de Colas

```bash
#!/bin/bash
# tts_queue.sh

QUEUE_DIR="/tmp/tts_queue"
mkdir -p "$QUEUE_DIR"

enqueue() {
    local message="$1"
    local voice="${2:-Monica}"
    local timestamp=$(date +%s)

    echo "$message|$voice" > "$QUEUE_DIR/$timestamp"
}

process_queue() {
    for file in "$QUEUE_DIR"/*; do
        if [ -f "$file" ]; then
            IFS='|' read -r message voice < "$file"
            tts-notify --voice "$voice" "$message"
            rm "$file"
        fi
    done
}

# Procesar en background
while true; do
    process_queue
    sleep 1
done &
```

## Solución de Problemas Comunes

### Voz No Funciona

```bash
# Verificar disponibilidad
say -v "NombreVoz" "Test"

# Listar voces similares
say -v ? | grep -i "parte_del_nombre"

# Probar con fallback
tts-notify --voice nonexistent "Test"  # Debería usar fallback
```

### Problemas de Velocidad

```bash
# Velocidad soportada: 100-300 WPM
tts-notify --rate 100 "Muy lento"
tts-notify --rate 200 "Normal"
tts-notify --rate 300 "Muy rápido"
```

### Archivos de Audio No Se Guardan

```bash
# Verificar permisos del Desktop
ls -la ~/Desktop/

# Especificar ruta completa
tts-notify --save "/tmp/test" "Mensaje temporal"

# Verificar resultado
ls -la /tmp/test.aiff
```

## Optimización de Rendimiento

### 1. Caching de Voces

```bash
# Pre-cargar voces al inicio
tts-notify --list > /dev/null
```

### 2. Procesamiento por Lotes

```bash
# Procesar múltiples textos
for text in "Mensaje 1" "Mensaje 2" "Mensaje 3"; do
    tts-notify --voice Monica "$text"
    sleep 0.5
done
```

### 3. Reducción de Latencia

```bash
# Usar voces Enhanced (generalmente más rápidas)
tts-notify --voice "Monica (Enhanced)" "Texto"
```

## Ejemplos de Integración Completa

### Sistema de Notificaciones Inteligente

```bash
#!/bin/bash
# smart_notifications.sh

TYPE="$1"
MESSAGE="$2"

case "$TYPE" in
    "email")
        tts-notify --voice Jorge "📧 Correo: $MESSAGE"
        ;;
    "calendar")
        tts-notify --voice Angélica "📅 Calendario: $MESSAGE"
        ;;
    "system")
        tts-notify --voice "Siri Female" "⚙️ Sistema: $MESSAGE"
        ;;
    "urgent")
        tts-notify --voice "Siri Male" --rate 250 "🚨 URGENTE: $MESSAGE"
        ;;
    *)
        tts-notify --voice Monica "$MESSAGE"
        ;;
esac
```

Este sistema proporciona una base sólida para integrar TTS Notify en flujos de trabajo reales y automatizaciones complejas.