#!/bin/bash
# Script de prueba completa para TTS-macOS

echo "🧪 PRUEBA COMPLETA DE TTS-MACOS"
echo "================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para verificar resultado
check_result() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
        return 1
    fi
}

# Verificar que estamos en macOS
echo "🔍 Verificando sistema operativo..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    check_result "macOS detectado"
else
    echo -e "${RED}❌ Este script es solo para macOS${NC}"
    exit 1
fi

# Verificar comando say
echo ""
echo "🔍 Verificando comando 'say'..."
if command -v say &> /dev/null; then
    check_result "Comando 'say' disponible"
else
    echo -e "${RED}❌ Comando 'say' no encontrado${NC}"
    exit 1
fi

# Ir al directorio del proyecto
cd "$(dirname "$0")"
echo ""
echo "📁 Directorio del proyecto: $(pwd)"

# Probar el CLI directamente desde el proyecto
echo ""
echo "🔍 Probando CLI desde el directorio del proyecto..."
python3 tts-macos --help > /dev/null 2>&1
check_result "CLI wrapper funciona"

# Probar el standalone
echo ""
echo "🔍 Probando versión standalone..."
./tts-macos-standalone.py --help > /dev/null 2>&1
check_result "CLI standalone funciona"

# Probar detección de voces
echo ""
echo "🔍 Probando detección de voces..."
python3 tts-macos --list | grep -q "Total de voces:"
check_result "Detección de voces funciona"

# Probar filtros
echo ""
echo "🔍 Probando filtros de género e idioma..."

# Filtro femenino
python3 tts-macos --list --gen female | grep -q "VOCES EN ESPAÑOL" && \
python3 tts-macos --list --gen female | grep -q "VOCES ENHANCED/PREMIUM"
check_result "Filtro --gen female funciona"

# Filtro masculino
python3 tts-macos --list --gen male | grep -q "VOCES EN ESPAÑOL"
check_result "Filtro --gen male funciona"

# Filtro idioma
python3 tts-macos --list --lang es_ES | grep -q "es_ES"
check_result "Filtro --lang es_ES funciona"

# Filtro combinado
python3 tts-macos --list --gen female --lang es_ES | grep -q "FILTROS ACTIVOS"
check_result "Filtro combinado --gen female --lang es_ES funciona"

# Probar síntesis de voz
echo ""
echo "🔍 Probando síntesis de voz..."

# Crear archivo de audio de prueba
TEST_AUDIO="/tmp/tts-test.aiff"
python3 tts-macos "Hola, esto es una prueba" --save "$TEST_AUDIO" > /dev/null 2>&1
if [ -f "$TEST_AUDIO" ]; then
    check_result "Generación de archivo de audio funciona"
    rm -f "$TEST_AUDIO"
else
    echo -e "${RED}❌ No se pudo generar archivo de audio${NC}"
fi

# Probar instalación local
echo ""
echo "🔍 Probando instalación local..."

# Backup de instalación anterior si existe
if [ -f "$HOME/.local/bin/tts-macos" ]; then
    cp "$HOME/.local/bin/tts-macos" "$HOME/.local/bin/tts-macos.backup"
fi

# Instalar en local
mkdir -p "$HOME/.local/bin"
cp tts-macos-standalone.py "$HOME/.local/bin/tts-macos" 2>/dev/null
chmod +x "$HOME/.local/bin/tts-macos" 2>/dev/null

# Verificar instalación
if [ -f "$HOME/.local/bin/tts-macos" ]; then
    check_result "Instalación local completada"

    # Probar instalación local
    "$HOME/.local/bin/tts-macos" --help > /dev/null 2>&1
    check_result "Instalación local funciona"

    # Probar filtros en instalación local
    "$HOME/.local/bin/tts-macos" --list --gen female --lang es_ES | grep -q "FILTROS ACTIVOS"
    check_result "Filtros funcionan en instalación local"
else
    echo -e "${RED}❌ Falló la instalación local${NC}"
fi

# Resumen de voces
echo ""
echo "📊 RESUMEN DE VOCES DETECTADAS"
echo "=============================="
python3 tts-macos --list | grep "Total de voces:" | tail -1

# Ejemplos de uso
echo ""
echo "💡 EJEMPLOS DE USO QUE FUNCIONAN:"
echo "================================"
echo ""
echo "Listar todas las voces:"
echo "  tts-macos --list"
echo ""
echo "Filtrar voces femeninas:"
echo "  tts-macos --list --gen female"
echo ""
echo "Filtrar voces masculinas:"
echo "  tts-macos --list --gen male"
echo ""
echo "Filtrar voces de España:"
echo "  tts-macos --list --lang es_ES"
echo ""
echo "Filtrar voces femeninas de España:"
echo "  tts-macos --list --gen female --lang es_ES"
echo ""
echo "Reproducir texto con voz específica:"
echo "  tts-macos \"Hola mundo\" --voice Monica"
echo ""
echo "Guardar audio:"
echo "  tts-macos \"Hola mundo\" --save mi_voz.aiff"

# Verificar PATH
echo ""
echo "🔍 Verificando configuración PATH..."
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "${YELLOW}⚠️  ~/.local/bin no está en tu PATH${NC}"
    echo ""
    echo "Agrega esta línea a tu ~/.zshrc o ~/.bash_profile:"
    echo ""
    echo -e "${BLUE}    export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
    echo ""
    echo "Luego ejecuta:"
    echo -e "${BLUE}    source ~/.zshrc${NC}  # o source ~/.bash_profile"
else
    check_result "~/.local/bin está en el PATH"
fi

# Restaurar backup si existía
if [ -f "$HOME/.local/bin/tts-macos.backup" ]; then
    mv "$HOME/.local/bin/tts-macos.backup" "$HOME/.local/bin/tts-macos"
    echo ""
    echo -e "${YELLOW}🔄 Restaurada instalación anterior${NC}"
fi

echo ""
echo "================================="
echo -e "${GREEN}✅ PRUEBA COMPLETADA${NC}"
echo "================================="
echo ""
echo "Si todas las pruebas pasaron, tu instalación de TTS-macOS está lista para usar."
