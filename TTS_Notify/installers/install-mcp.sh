#!/bin/bash
# Script de instalación para TTS Notify MCP

echo "🔔  Instalador de TTS Notify MCP Server"
echo "======================================"
echo ""

# Verificar que estamos en macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Este script es solo para macOS"
    exit 1
fi

# Verificar Python
echo "📦 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "Por favor instala Python desde https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION encontrado"

# Obtener directorio actual (subir un nivel desde installers/)
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
echo "📁 Directorio del proyecto: $PROJECT_DIR"

# Crear entorno virtual
echo ""
echo "🔨 Creando entorno virtual..."

# Eliminar entorno virtual existente si existe
if [ -d "$PROJECT_DIR/venv" ]; then
    echo "🗑️  Eliminando entorno virtual existente..."
    rm -rf "$PROJECT_DIR/venv"
fi

# Crear nuevo entorno virtual
python3 -m venv "$PROJECT_DIR/venv"

# Verificar que el entorno virtual se creó correctamente
if [ ! -f "$PROJECT_DIR/venv/bin/python" ]; then
    echo "❌ Error al crear el entorno virtual"
    exit 1
fi

# Activar entorno virtual
source "$PROJECT_DIR/venv/bin/activate"

# Verificar que estamos usando el Python correcto
echo "🐍 Python en uso: $(which python)"
echo "🐍 Versión de Python: $(python --version)"

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r "$PROJECT_DIR/requirements.txt"

if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas correctamente"
else
    echo "❌ Error al instalar dependencias"
    exit 1
fi

# Obtener usuario actual
CURRENT_USER=$(whoami)

# Configuración del Servidor MCP
echo ""
echo "⚙️  Configuración del Servidor MCP"
echo "=================================="

# Variables de entorno completas para TTS-Notify
TTS_ENV_VARS=(
    "TTS_NOTIFY_VOICE=Siri Female (Spanish Spain)"
    "TTS_NOTIFY_RATE=175"
    "TTS_NOTIFY_LANGUAGE=es"
    "TTS_NOTIFY_QUALITY=siri"
    "TTS_NOTIFY_PITCH=1.0"
    "TTS_NOTIFY_VOLUME=1.0"
    "TTS_NOTIFY_ENABLED=true"
    "TTS_NOTIFY_CACHE_ENABLED=true"
    "TTS_NOTIFY_LOG_LEVEL=INFO"
    "TTS_NOTIFY_MAX_TEXT_LENGTH=5000"
    "TTS_NOTIFY_OUTPUT_FORMAT=aiff"
)

# Detectar si Claude Code está disponible
if command -v claude &> /dev/null; then
    echo "✅ Claude Code detectado - Usando configuración global"

    # Eliminar configuración existente si la hay
    echo "🗑️  Eliminando configuración previa..."
    claude mcp remove tts-notify -s user &> /dev/null || true
    claude mcp remove tts-notify -s project &> /dev/null || true

    # Construir comando con todas las variables de entorno
    MCP_CMD="claude mcp add --scope user tts-notify --transport stdio"

    # Agregar variables de entorno
    for var in "${TTS_ENV_VARS[@]}"; do
        key=$(echo "$var" | cut -d'=' -f1)
        value=$(echo "$var" | cut -d'=' -f2)
        MCP_CMD="$MCP_CMD --env $key=\"$value\""
    done

    # Agregar comando Python y argumentos
    MCP_CMD="$MCP_CMD -- \"$PROJECT_DIR/venv/bin/python\" \"-m\" \"tts_notify\" \"--mode\" \"mcp\""

    echo "🚀 Ejecutando configuración global..."
    echo "Comando: $MCP_CMD"

    # Ejecutar configuración
    if eval "$MCP_CMD"; then
        echo "✅ Servidor MCP configurado globalmente"
        echo "   Disponible para todos los proyectos de Claude Code"

        # Verificar configuración
        echo ""
        echo "🔍 Verificando configuración..."
        if claude mcp list | grep -q "tts-notify"; then
            echo "✅ Servidor conectado y operativo"
            claude mcp list | grep "tts-notify"
        else
            echo "⚠️  Configuración creada pero sin conexión aún"
            echo "   Reinicia Claude Code si es necesario"
        fi
    else
        echo "❌ Error en configuración global"
        echo "🔄 Intentando configuración para Claude Desktop..."
        CLAUDE_CODE_AVAILABLE=false
    fi
else
    echo "⚠️  Claude Code no detectado"
    CLAUDE_CODE_AVAILABLE=false
fi

# Fallback a Claude Desktop si Claude Code no está disponible
if [ "$CLAUDE_CODE_AVAILABLE" = false ]; then
    echo "🔄 Usando configuración para Claude Desktop (método legacy)"

    # Crear configuración para Claude Desktop
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

    # Verificar si el directorio existe
    if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
        echo "⚠️  El directorio de Claude Desktop no existe"
        echo "Asegúrate de tener Claude Desktop instalado"
        echo ""
        mkdir -p "$CLAUDE_CONFIG_DIR"
    fi

    # Crear o actualizar configuración
    if [ -f "$CLAUDE_CONFIG_FILE" ]; then
        echo "⚠️  Ya existe un archivo de configuración"
        echo "Se creará un backup en: ${CLAUDE_CONFIG_FILE}.backup"
        cp "$CLAUDE_CONFIG_FILE" "${CLAUDE_CONFIG_FILE}.backup"
    fi

    # Generar configuración con variables de entorno
    cat > "$CLAUDE_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "tts-notify": {
      "command": "$PROJECT_DIR/venv/bin/python",
      "args": [
        "$PROJECT_DIR/src/mcp_server.py"
      ],
      "env": {
        $(printf '        "%s": "%s",\n' $(echo "${TTS_ENV_VARS[0]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[0]}" | cut -d'=' -f2))
        $(printf '        "%s": "%s",\n' $(echo "${TTS_ENV_VARS[1]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[1]}" | cut -d'=' -f2))
        $(printf '        "%s": "%s",\n' $(echo "${TTS_ENV_VARS[2]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[2]}" | cut -d'=' -f2))
        $(printf '        "%s": "%s",\n' $(echo "${TTS_ENV_VARS[3]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[3]}" | cut -d'=' -f2))
        $(printf '        "%s": "%s",\n' $(echo "${TTS_ENV_VARS[4]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[4]}" | cut -d'=' -f2))
        $(printf '        "%s": "%s",\n' $(echo "${TTS_ENV_VARS[5]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[5]}" | cut -d'=' -f2))
        $(printf '        "%s": "%s",\n' $(echo "${TTS_ENV_VARS[6]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[6]}" | cut -d'=' -f2))
        $(printf '        "%s": "%s",\n' $(echo "${TTS_ENV_VARS[7]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[7]}" | cut -d'=' -f2))
        $(printf '        "%s": "%s",\n' $(echo "${TTS_ENV_VARS[8]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[8]}" | cut -d'=' -f2))
        $(printf '        "%s": "%s",\n' $(echo "${TTS_ENV_VARS[9]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[9]}" | cut -d'=' -f2))
        $(printf '        "%s": "%s"\n' $(echo "${TTS_ENV_VARS[10]}" | cut -d'=' -f1) $(echo "${TTS_ENV_VARS[10]}" | cut -d'=' -f2))
      }
    }
  }
}
EOF

    echo "✅ Archivo de configuración creado en:"
    echo "   $CLAUDE_CONFIG_FILE"
    echo ""
    echo "💡 Se recomienda instalar Claude Code para configuración global automática:"
    echo "   pip install claude-code"
fi

# Probar instalación
echo ""
echo "🧪 Probando instalación..."
echo "Intentando reproducir un mensaje de prueba..."

# Verificar que el intérprete de Python existe y funciona
if [ ! -f "$PROJECT_DIR/venv/bin/python" ]; then
    echo "❌ El intérprete de Python no se encuentra en la ruta esperada"
    exit 1
fi

# Probar el intérprete directamente
"$PROJECT_DIR/venv/bin/python" --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ El intérprete de Python no funciona correctamente"
    exit 1
fi

# Probar el comando say y reproducir mensaje
"$PROJECT_DIR/venv/bin/python" -c "
import subprocess
import sys
try:
    # Verificar que el comando say existe
    subprocess.run(['which', 'say'], check=True, capture_output=True)
    print('✅ Comando say encontrado')

    # Probar reproducción de audio
    subprocess.run(['say', '-v', 'Monica', 'Instalación exitosa'], check=True)
    print('✅ Test de audio exitoso')
except subprocess.CalledProcessError as e:
    print(f'⚠️  Error en test: {e}')
    sys.exit(1)
except Exception as e:
    print(f'⚠️  Error inesperado: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "✅ Prueba de instalación exitosa"
else
    echo "❌ Error en la prueba de instalación"
    exit 1
fi

echo ""
echo "================================================"
echo "✨ ¡Instalación de TTS Notify MCP completada!"
echo "================================================"
echo ""

# Verificar qué método de configuración se usó
if command -v claude &> /dev/null && claude mcp list | grep -q "tts-notify"; then
    echo "✅ Configuración global para Claude Code activa"
    echo ""
    echo "📋 Próximos pasos:"
    echo ""
    echo "1. El servidor ya está disponible en TODOS tus proyectos de Claude Code"
    echo "2. Prueba con: 'Lista todas las voces disponibles'"
    echo "3. O prueba: 'Lee en voz alta: Hola mundo desde TTS Notify'"
    echo ""
    echo "🔧 Herramientas MCP disponibles:"
    echo "   • mcp__tts-notify__speak_text - Texto a voz"
    echo "   • mcp__tts-notify__list_voices - Listar voces"
    echo "   • mcp__tts-notify__save_audio - Guardar audio"
    echo ""
    echo "📊 Variables de entorno configuradas (11 total):"
    echo "   • VOICE, RATE, LANGUAGE, QUALITY"
    echo "   • PITCH, VOLUME, ENABLED, CACHE_ENABLED"
    echo "   • LOG_LEVEL, MAX_TEXT_LENGTH, OUTPUT_FORMAT"
else
    echo "✅ Configuración para Claude Desktop completada"
    echo ""
    echo "📋 Próximos pasos:"
    echo ""
    echo "1. Cierra Claude Desktop completamente (Cmd+Q)"
    echo "2. Abre Claude Desktop nuevamente"
    echo "3. Deberías ver el servidor MCP conectado"
    echo "4. Prueba diciendo: 'Lee este texto en voz alta: Hola mundo'"
    echo ""
    echo "💡 Para configuración global automática en todos los proyectos:"
    echo "   pip install claude-code"
    echo "   ./installers/install-mcp.sh"
fi

echo ""
echo "📖 Para más información, consulta:"
echo "   • README.md - Documentación general"
echo "   • configuracion-global-mcp-tts-notify.md - Guía de configuración global"
echo ""
echo "🎤 Voces españolas populares configuradas:"
echo "   • Siri Female (Spanish Spain) - Voz principal (España)"
echo "   • Jorge (España - Hombre)"
echo "   • Mónica (España - Mujer)"
echo "   • Angélica (México - Mujer)"
echo "   • Juan (México - Hombre)"
echo "   • Carlos (Colombia - Hombre)"
echo "   • Francisca (Chile - Mujer)"
echo ""
echo "💡 Comandos útiles:"
echo "   claude mcp list                    # Ver servidores MCP"
echo "   claude mcp doctor                  # Verificar estado"
echo "   tts-notify --list                  # Listar voces (CLI)"
echo ""
echo "🌐 Configuración global: Disponible en todos los proyectos"
echo "🖥️  Configuración Desktop: Solo en Claude Desktop"
echo ""
echo "¡Disfruta de tu sistema TTS Notify mejorado! 🎉"
