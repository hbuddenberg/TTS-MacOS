#!/bin/bash
# Script de instalación para MCP TTS macOS

echo "🎙️  Instalador de MCP Text-to-Speech para macOS"
echo "================================================"
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

# Obtener directorio actual
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "📁 Directorio del proyecto: $PROJECT_DIR"

# Crear entorno virtual
echo ""
echo "🔨 Creando entorno virtual..."
python3 -m venv "$PROJECT_DIR/venv"

# Activar entorno virtual
source "$PROJECT_DIR/venv/bin/activate"

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

# Crear configuración para Claude Desktop
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

echo ""
echo "⚙️  Configuración de Claude Desktop"
echo "===================================="

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

# Generar configuración
cat > "$CLAUDE_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "tts-macos": {
      "command": "$PROJECT_DIR/venv/bin/python",
      "args": [
        "$PROJECT_DIR/server.py"
      ]
    }
  }
}
EOF

echo "✅ Archivo de configuración creado en:"
echo "   $CLAUDE_CONFIG_FILE"

# Probar instalación
echo ""
echo "🧪 Probando instalación..."
echo "Intentando reproducir un mensaje de prueba..."

"$PROJECT_DIR/venv/bin/python" -c "
import subprocess
try:
    subprocess.run(['say', '-v', 'Monica', 'Instalación exitosa'], check=True)
    print('✅ Test de audio exitoso')
except Exception as e:
    print(f'⚠️  Error en test de audio: {e}')
"

echo ""
echo "================================================"
echo "✨ ¡Instalación completada!"
echo "================================================"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Cierra Claude Desktop completamente (Cmd+Q)"
echo "2. Abre Claude Desktop nuevamente"
echo "3. Deberías ver el servidor MCP conectado"
echo "4. Prueba diciendo: 'Lee este texto en voz alta: Hola mundo'"
echo ""
echo "📖 Para más información, consulta el README.md"
echo ""
echo "🎤 Voces disponibles:"
echo "   • monica (Español México - Mujer)"
echo "   • paulina (Español México - Mujer)"
echo "   • jorge (Español España - Hombre)"
echo "   • juan (Español España - Hombre)"
echo "   • diego (Español Argentina - Hombre)"
echo "   • angelica (Español México - Mujer)"
echo ""
echo "¡Disfruta de tu servidor TTS! 🎉"
