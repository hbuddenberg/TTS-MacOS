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
    "tts-notify": {
      "command": "$PROJECT_DIR/venv/bin/python",
      "args": [
        "$PROJECT_DIR/src/mcp_server.py"
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
echo "✨ ¡Instalación de TTS Notify completada!"
echo "================================================"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Cierra Claude Desktop completamente (Cmd+Q)"
echo "2. Abre Claude Desktop nuevamente"
echo "3. Deberías ver el servidor MCP conectado"
echo "4. Prueba diciendo: 'Lee este texto en voz alta: Hola mundo'"
echo ""
echo "📖 Para más información, consulta README.md"
echo ""
echo "🎤 Voces españolas populares:"
echo "   • Jorge (España - Hombre)"
echo "   • Mónica (España - Mujer)"
echo "   • Angélica (México - Mujer)"
echo "   • Juan (México - Hombre)"
echo "   • Carlos (Colombia - Hombre)"
echo "   • Francisca (Chile - Mujer)"
echo ""
echo "💡 Usa 'tts-notify --list' para ver todas las voces disponibles"
echo ""
echo "¡Disfruta de tu sistema TTS Notify! 🎉"
