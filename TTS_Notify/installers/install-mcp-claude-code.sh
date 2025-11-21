#!/bin/bash
# Script especializado de instalación para TTS Notify MCP en Claude Code
# Configuración global automática para todos los proyectos

echo "🚀 Instalador Especializado de TTS Notify para Claude Code"
echo "=========================================================="
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

# Verificar Claude Code
echo ""
echo "🔍 Verificando Claude Code..."
if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code no está instalado"
    echo ""
    echo "Instálalo con:"
    echo "   pip install claude-code"
    echo ""
    echo "O visita: https://docs.claude.com/en/docs/claude-code"
    exit 1
fi

echo "✅ Claude Code encontrado"
CLAUDE_VERSION=$(claude --version 2>/dev/null || echo "versión desconocida")
echo "   Versión: $CLAUDE_VERSION"

# Obtener directorio actual (subir un nivel desde installers/)
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
echo "📁 Directorio del proyecto: $PROJECT_DIR"

# Opciones de configuración interactiva
echo ""
echo "⚙️  Opciones de Configuración"
echo "============================"

# Variable para controlar el modo interactivo
INTERACTIVE_MODE=true
SKIP_VENV=false
CUSTOM_VOICE=""
CUSTOM_RATE=""

# Parsear argumentos de línea de comandos
while [[ $# -gt 0 ]]; do
    case $1 in
        --non-interactive)
            INTERACTIVE_MODE=false
            shift
            ;;
        --skip-venv)
            SKIP_VENV=true
            shift
            ;;
        --voice)
            CUSTOM_VOICE="$2"
            shift 2
            ;;
        --rate)
            CUSTOM_RATE="$2"
            shift 2
            ;;
        --help)
            echo "Uso: $0 [opciones]"
            echo ""
            echo "Opciones:"
            echo "  --non-interactive    No hacer preguntas interactivas"
            echo "  --skip-venv         Omitir creación de entorno virtual"
            echo "  --voice VOZ         Usar voz específica"
            echo "  --rate VELOCIDAD    Usar velocidad específica (100-300)"
            echo "  --help              Mostrar esta ayuda"
            echo ""
            exit 0
            ;;
        *)
            echo "Opción desconocida: $1"
            echo "Usa --help para ver las opciones disponibles"
            exit 1
            ;;
    esac
done

# Modo interactivo
if [ "$INTERACTIVE_MODE" = true ]; then
    echo ""
    read -p "¿Deseas configurar opciones personalizadas? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        # Selección de voz
        echo ""
        echo "🎤 Selección de Voz (presiona Enter para usar Siri Female Spanish Spain):"
        echo "   1. Siri Female (Spanish Spain) - Por defecto"
        echo "   2. Jorge (España - Hombre)"
        echo "   3. Mónica (España - Mujer)"
        echo "   4. Angélica (México - Mujer)"
        echo "   5. Juan (México - Hombre)"
        echo "   6. Personalizada"
        read -p "Elige una opción [1-6]: " -n 1 -r
        echo

        case $REPLY in
            2) CUSTOM_VOICE="Jorge" ;;
            3) CUSTOM_VOICE="Mónica" ;;
            4) CUSTOM_VOICE="Angélica" ;;
            5) CUSTOM_VOICE="Juan" ;;
            6)
                read -p "Ingresa el nombre exacto de la voz: " CUSTOM_VOICE
                ;;
            *) CUSTOM_VOICE="Siri Female (Spanish Spain)" ;;
        esac

        # Velocidad
        read -p "Velocidad de habla (100-300, por defecto 175): " CUSTOM_RATE
        if [[ -z "$CUSTOM_RATE" ]]; then
            CUSTOM_RATE="175"
        fi

        # Entorno virtual
        read -p "¿Crear nuevo entorno virtual? (S/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            SKIP_VENV=true
        fi
    fi
fi

# Configurar valores por defecto si no se proporcionaron
if [[ -z "$CUSTOM_VOICE" ]]; then
    CUSTOM_VOICE="Siri Female (Spanish Spain)"
fi

if [[ -z "$CUSTOM_RATE" ]]; then
    CUSTOM_RATE="175"
fi

# Validar rango de velocidad
if [[ "$CUSTOM_RATE" -lt 100 || "$CUSTOM_RATE" -gt 300 ]]; then
    echo "⚠️  La velocidad debe estar entre 100 y 300. Usando 175."
    CUSTOM_RATE="175"
fi

echo "✅ Configuración seleccionada:"
echo "   Voz: $CUSTOM_VOICE"
echo "   Velocidad: $CUSTOM_RATE"

# Setup del entorno virtual si es necesario
VENV_PATH="$PROJECT_DIR/venv"

if [ "$SKIP_VENV" = false ]; then
    echo ""
    echo "🔨 Configurando entorno virtual..."

    # Eliminar entorno virtual existente si existe
    if [ -d "$VENV_PATH" ]; then
        echo "🗑️  Eliminando entorno virtual existente..."
        rm -rf "$VENV_PATH"
    fi

    # Crear nuevo entorno virtual
    echo "📦 Creando nuevo entorno virtual..."
    python3 -m venv "$VENV_PATH"

    # Verificar que el entorno virtual se creó correctamente
    if [ ! -f "$VENV_PATH/bin/python" ]; then
        echo "❌ Error al crear el entorno virtual"
        exit 1
    fi

    # Activar entorno virtual
    source "$VENV_PATH/bin/activate"

    echo "🐍 Entorno virtual activado: $(which python)"
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
else
    echo ""
    echo "⏭️  Omitiendo configuración de entorno virtual"

    # Buscar Python existente
    if [ -f "$VENV_PATH/bin/python" ]; then
        PYTHON_PATH="$VENV_PATH/bin/python"
    elif command -v python &> /dev/null; then
        PYTHON_PATH="$(which python)"
    else
        echo "❌ No se encuentra un intérprete de Python adecuado"
        exit 1
    fi

    echo "🐍 Usando Python: $PYTHON_PATH"
fi

# Configuración del servidor MCP con Claude Code
echo ""
echo "🚀 Configurando Servidor MCP Global"
echo "==================================="

# Variables de entorno completas (con valores personalizados si se proporcionaron)
TTS_ENV_VARS=(
    "TTS_NOTIFY_VOICE=$CUSTOM_VOICE"
    "TTS_NOTIFY_RATE=$CUSTOM_RATE"
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

# Mostrar configuración
echo ""
echo "📊 Variables de entorno a configurar:"
for var in "${TTS_ENV_VARS[@]}"; do
    key=$(echo "$var" | cut -d'=' -f1)
    value=$(echo "$var" | cut -d'=' -f2)
    echo "   • $key=$value"
done

# Eliminar configuración existente
echo ""
echo "🗑️  Eliminando configuración previa..."
claude mcp remove tts-notify -s user &> /dev/null || true
claude mcp remove tts-notify -s project &> /dev/null || true

# Construir comando MCP
MCP_CMD="claude mcp add --scope user tts-notify --transport stdio"

# Agregar variables de entorno
for var in "${TTS_ENV_VARS[@]}"; do
    key=$(echo "$var" | cut -d'=' -f1)
    value=$(echo "$var" | cut -d'=' -f2)
    MCP_CMD="$MCP_CMD --env $key=\"$value\""
done

# Determinar ruta de Python y argumentos
if [ "$SKIP_VENV" = false ]; then
    PYTHON_EXEC="$VENV_PATH/bin/python"
else
    PYTHON_EXEC="$PYTHON_PATH"
fi

MCP_CMD="$MCP_CMD -- \"$PYTHON_EXEC\" \"-m\" \"tts_notify\" \"--mode\" \"mcp\""

echo ""
echo "🔧 Ejecutando configuración global..."
echo "Comando: $MCP_CMD"

# Ejecutar configuración
if eval "$MCP_CMD"; then
    echo ""
    echo "✅ Servidor MCP configurado globalmente"
    echo "   Disponible para TODOS los proyectos de Claude Code"

    # Verificación inmediata
    echo ""
    echo "🔍 Verificando configuración..."
    sleep 2  # Dar tiempo para que se establezca la conexión

    if claude mcp list | grep -q "tts-notify"; then
        echo "✅ Servidor conectado y operativo"
        echo ""
        claude mcp list | grep "tts-notify" || echo "   tts-notify: Configurado globalmente"
    else
        echo "⚠️  Configuración creada pero sin conexión inmediata"
        echo "   Esto es normal, el servidor se conectará cuando sea necesario"
    fi
else
    echo "❌ Error en configuración global"
    echo ""
    echo "Solución de problemas:"
    echo "1. Verifica que Claude Code está funcionando: claude --version"
    echo "2. Revisa permisos en el directorio del proyecto"
    echo "3. Intenta reinstalar Claude Code: pip uninstall claude-code && pip install claude-code"
    exit 1
fi

# Pruebas funcionales
echo ""
echo "🧪 Ejecutando Pruebas Funcionales"
echo "================================="

# Verificar instalación del módulo
echo "📋 Verificando módulo tts_notify..."
if [ "$SKIP_VENV" = false ]; then
    source "$VENV_PATH/bin/activate"
fi

if "$PYTHON_EXEC" -m tts_notify --help &> /dev/null; then
    echo "✅ Módulo tts_notify funciona correctamente"
else
    echo "❌ Error al ejecutar el módulo tts_notify"
    exit 1
fi

# Probar comando say
echo "🎤 Probando sistema TTS de macOS..."
if command -v say &> /dev/null; then
    echo "✅ Comando 'say' disponible"

    # Probar reproducción con voz seleccionada
    if say -v "$CUSTOM_VOICE" "Instalación completada exitosamente" 2>/dev/null; then
        echo "✅ Test de voz exitoso con: $CUSTOM_VOICE"
    else
        echo "⚠️  Test de voz falló, pero la instalación puede funcionar igualmente"
        echo "   Verifica que la voz '$CUSTOM_VOICE' esté instalada en tu sistema"
    fi
else
    echo "❌ Comando 'say' no disponible (esto es inusual en macOS)"
fi

# Verificación final de configuración global
echo ""
echo "🔍 Verificación Final de Configuración Global"
echo "============================================"

echo ""
echo "📊 Estado actual de servidores MCP:"
claude mcp list

echo ""
echo "🏥 Diagnóstico del sistema MCP:"
claude mcp doctor 2>/dev/null || echo "   Diagnóstico no disponible (es normal)"

# Resumen final
echo ""
echo "================================================"
echo "✨ ¡Instalación Global Completada!"
echo "================================================"
echo ""
echo "🌐 CONFIGURACIÓN GLOBAL ACTIVA"
echo "   El servidor TTS-Notify está disponible en TODOS tus proyectos"
echo ""
echo "🔧 Herramientas MCP disponibles:"
echo "   • mcp__tts-notify__speak_text - Convertir texto a voz"
echo "   • mcp__tts-notify__list_voices - Listar voces del sistema"
echo "   • mcp__tts-notify__save_audio - Guardar texto como archivo de audio"
echo ""
echo "💬 Ejemplos de uso en Claude Code:"
echo '   "Lee en voz alta: Hola mundo desde TTS Notify"'
echo "   'Lista todas las voces disponibles'"
echo "   'Guarda este audio: prueba de TTS-Notify'"
echo ""
echo "🎤 Configuración aplicada:"
echo "   • Voz principal: $CUSTOM_VOICE"
echo "   • Velocidad: $CUSTOM_RATE wpm"
echo "   • 11 variables de entorno configuradas"
echo ""
echo "🔧 Comandos útiles:"
echo "   claude mcp list                    # Ver servidores"
echo "   claude mcp doctor                  # Diagnóstico"
echo "   claude mcp remove tts-notify -s user  # Desinstalar"
echo ""
echo "📖 Documentación de referencia:"
echo "   • configuracion-global-mcp-tts-notify.md"
echo "   • README.md"
echo ""
echo "🎉 ¡Tu sistema TTS-Notify está listo para usar en todos los proyectos!"