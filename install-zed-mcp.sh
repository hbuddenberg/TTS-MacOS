#!/bin/bash
# Instalador del servidor MCP para Zed con notificaciones TTS

set -e

echo "🎭 Instalador del Servidor MCP para Zed con TTS"
echo "=============================================="
echo ""

# Rutas
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_SCRIPT="$SCRIPT_DIR/zed-mcp-server.py"
CONFIG_DIR="$HOME/.zed"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Por favor, instala Python 3.10+"
    exit 1
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no encontrado. Por favor, instala pip"
    exit 1
fi

# Verificar TTS-macOS
if ! command -v tts-macos &> /dev/null; then
    echo "🔍 Instalando TTS-macOS..."
    cd "$SCRIPT_DIR/mcp-tts-macos"
    ./install-cli.sh
fi

# Crear entorno virtual para las dependencias
echo "📦 Creando entorno virtual para dependencias..."
VENV_DIR="$SCRIPT_DIR/zed-mcp-env"

if [ -d "$VENV_DIR" ]; then
    echo "✅ Entorno virtual ya existe"
else
    python3 -m venv "$VENV_DIR"
    echo "✅ Entorno virtual creado"
fi

# Instalar dependencias del servidor MCP
echo "📦 Instalando dependencias del servidor MCP..."
source "$VENV_DIR/bin/activate"
pip install -q mcp

# Crear directorio de configuración
echo "📁 Creando directorio de configuración..."
mkdir -p "$CONFIG_DIR"

# Verificar si existe el archivo de configuración
if [ -f "$CONFIG_FILE" ]; then
    echo "📖 Archivo de configuración encontrado: $CONFIG_FILE"

    # Hacer backup del archivo existente
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
    echo "✅ Backup creado: $CONFIG_FILE.backup"

    # Verificar si ya está configurado el servidor MCP de Zed
    if grep -q "zed-tts-notifications" "$CONFIG_FILE"; then
        echo "⚠️  El servidor MCP de Zed ya está configurado"

        # Preguntar si quiere actualizar
        read -p "¿Actualizar configuración? (s/N): " update_config
        if [[ ! "$update_config" =~ ^[sS]$ ]]; then
            echo "👋 Instalación cancelada"
            exit 0
        fi
    fi
else
    echo "📄 Creando archivo de configuración nuevo: $CONFIG_FILE"
fi

# Obtener rutas absolutas
PYTHON_PATH=$(which python3)
SERVER_PATH="$SERVER_SCRIPT"

# Crear configuración
echo "⚙️  Configurando servidor MCP para Zed..."

# Usar el Python del entorno virtual
PYTHON_VENV="$VENV_DIR/bin/python"

# Usar jq si está disponible, sino usar sed
if command -v jq &> /dev/null; then
    # jq está disponible, usar JSON complejo
    jq -n \
        --arg python "$PYTHON_VENV" \
        --arg server "$SERVER_PATH" \
        '{
            "mcpServers": {
                "zed-tts-notifications": {
                    "command": $python,
                    "args": [$server]
                },
                "tts-macos": {
                    "command": $python,
                    "args": ["/path/to/mcp-tts-macos/server.py"]
                }
            }
        }' > "$CONFIG_FILE"
else
    # jq no disponible, crear JSON básico con sed
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "zed-tts-notifications": {
      "command": "$PYTHON_VENV",
      "args": ["$SERVER_PATH"]
    }
  }
}
EOF
fi

echo "✅ Configuración guardada en: $CONFIG_FILE"

# Crear script de verificación
cat > "$CONFIG_DIR/verify-zed-mcp.sh" << 'EOF'
#!/bin/bash
# Verificar instalación del servidor MCP para Zed

echo "🔍 Verificando instalación del servidor MCP para Zed..."
echo ""

# Verificar configuración
CONFIG_FILE="$HOME/.zed/claude_desktop_config.json"
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ Archivo de configuración encontrado: $CONFIG_FILE"
    if grep -q "zed-tts-notifications" "$CONFIG_FILE"; then
        echo "✅ Servidor MCP de Zed configurado"
    else
        echo "❌ Servidor MCP de Zed no encontrado en la configuración"
        exit 1
    fi
else
    echo "❌ Archivo de configuración no encontrado: $CONFIG_FILE"
    exit 1
fi

# Verificar dependencias
echo ""
echo "🔍 Verificando dependencias..."
if command -v python3 &> /dev/null; then
    echo "✅ Python 3: $(python3 --version)"
else
    echo "❌ Python 3 no encontrado"
    exit 1
fi

if command -v pip3 &> /dev/null; then
    echo "✅ pip3: $(pip3 --version)"
else
    echo "❌ pip3 no encontrado"
    exit 1
fi

if command -v tts-macos &> /dev/null; then
    echo "✅ TTS-macOS: $(tts-macos --help | head -1)"
else
    echo "❌ TTS-macOS no encontrado"
    exit 1
fi

# Verificar entorno virtual
SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
VENV_DIR="$SCRIPT_ROOT/zed-mcp-env"
if [ -d "$VENV_DIR" ]; then
    echo "✅ Entorno virtual encontrado: $VENV_DIR"

    # Verificar que MCP está instalado en el entorno
    if "$VENV_DIR/bin/python" -c "import mcp" 2>/dev/null; then
        echo "✅ MCP instalado en el entorno virtual"
    else
        echo "❌ MCP no encontrado en el entorno virtual"
        exit 1
    fi
else
    echo "❌ Entorno virtual no encontrado: $VENV_DIR"
    exit 1
fi

# Verificar servidor MCP
SERVER_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../zed-mcp-server.py"
if [ -f "$SERVER_SCRIPT" ]; then
    echo "✅ Servidor MCP encontrado: $SERVER_SCRIPT"
    echo "✅ Permisos: $(ls -la "$SERVER_SCRIPT" | awk '{print $1}')"
else
    echo "❌ Servidor MCP no encontrado: $SERVER_SCRIPT"
    exit 1
fi

echo ""
echo "🎉 Todo está listo para usar!"
echo ""
echo "📖 Instrucciones de uso:"
echo "1. Reinicia Claude Desktop"
echo "2. Puedes usar las herramientas:"
echo "   - notify_file_save: Notificar guardado de archivo"
echo "   - notify_task_complete: Notificar tareas complejas"
echo "   - notify_startup: Notificar inicio de Zed"
echo ""
echo "Ejemplo en Claude:"
echo '  Usa "notify_file_save" con filename="script.py"'
EOF

chmod +x "$CONFIG_DIR/verify-zed-mcp.sh"

# Configurar variables de entorno
echo ""
echo "🔧 Configurando variables de entorno..."
echo "export ZED_TTS_ENABLED=true" >> ~/.zshrc
echo "export ZED_TTS_VOICE=monica" >> ~/.zshrc
echo "export ZED_TTS_RATE=175" >> ~/.zshrc
echo "export ZED_TTS_TASK_VOICE=jorge" >> ~/.zshrc
echo "export ZED_TTS_TASK_RATE=180" >> ~/.zshrc

echo ""
echo "✅ Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Reinicia Claude Desktop para cargar la nueva configuración"
echo "2. Ejecuta '$CONFIG_DIR/verify-zed-mcp.sh' para verificar"
echo "3. Configura TTS si no lo has hecho:"
echo "   cd '$SCRIPT_DIR/zed/hooks' && ./enable-tts.sh"
echo ""
echo "🎭 ¡Listo para recibir notificaciones TTS en Zed!"
echo ""
echo "📖 Documentación:"
echo "   Servidor MCP: $SERVER_SCRIPT"
echo "   Hooks Zed: $SCRIPT_DIR/zed/hooks/README.md"
echo "   Configuración: $CONFIG_FILE"
