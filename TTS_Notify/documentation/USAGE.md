# Guía de Uso Avanzado - TTS Notify

Esta guía cubre casos de uso avanzados y ejemplos detallados para TTS Notify v1.5.0.

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