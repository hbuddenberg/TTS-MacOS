#!/bin/bash
# examples.sh - Ejemplos de uso de tts-macos

echo "🎙️  Ejemplos de uso de TTS-macOS"
echo "=================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 Método 1: Con uvx (sin instalar)${NC}"
echo "───────────────────────────────────────────────"
echo ""
echo "# Básico"
echo "uvx --from . tts-macos \"Hola mundo\""
echo ""
echo "# Con opciones"
echo "uvx --from . tts-macos \"Buenos días\" --voice jorge --rate 200"
echo ""
echo "# Guardar audio"
echo "uvx --from . tts-macos \"Mi mensaje\" --save audio.aiff"
echo ""
echo "# Crear alias"
echo "alias tts='uvx --from \$(pwd) tts-macos'"
echo "tts \"Uso simplificado\""
echo ""
echo "Presiona Enter para continuar..."
read

echo -e "${BLUE}📦 Método 2: CLI instalado globalmente${NC}"
echo "───────────────────────────────────────────────"
echo ""
echo "# Instalar primero"
echo "./install-cli.sh"
echo ""
echo "# Luego usar desde cualquier lugar"
echo "tts-macos \"Hola mundo\""
echo "tts-macos \"Buenos días\" --voice jorge"
echo "tts-macos \"Rápido\" --rate 250"
echo ""
echo "Presiona Enter para continuar..."
read

echo -e "${BLUE}📦 Método 3: Python -m${NC}"
echo "───────────────────────────────────────────────"
echo ""
echo "# Ejecutar como módulo Python"
echo "python -m tts_macos \"Hola mundo\""
echo "python -m tts_macos --list"
echo ""
echo "Presiona Enter para continuar..."
read

echo -e "${BLUE}📦 Método 4: Servidor MCP con Claude Desktop${NC}"
echo "───────────────────────────────────────────────"
echo ""
echo "# Instalar servidor"
echo "./install.sh"
echo ""
echo "# Usar en Claude Desktop:"
echo "\"Lee en voz alta: Hola mundo\""
echo "\"Usa la voz de Jorge: Buenos días\""
echo "\"Guarda como audio: Mi mensaje\""
echo ""
echo "Presiona Enter para continuar..."
read

echo ""
echo -e "${GREEN}🎯 Casos de uso comunes${NC}"
echo "───────────────────────────────────────────────"
echo ""

echo "1️⃣  Notificación de script:"
echo "   ./mi_script.sh && uvx --from . tts-macos \"Completado\""
echo ""

echo "2️⃣  Timer/Recordatorio:"
echo "   sleep 1800 && uvx --from . tts-macos \"Han pasado 30 minutos\""
echo ""

echo "3️⃣  Leer archivo:"
echo "   uvx --from . tts-macos \"\$(cat documento.txt)\" --voice jorge"
echo ""

echo "4️⃣  En loop (monitor):"
cat << 'EOF'
   while true; do
       status=$(check_status)
       if [ "$status" == "error" ]; then
           uvx --from . tts-macos "Alerta: Error detectado"
       fi
       sleep 60
   done
EOF
echo ""

echo "5️⃣  Con cron (recordatorios):"
echo "   # En crontab:"
echo "   0 9 * * * uvx --from ~/mcp-tts-macos tts-macos \"Buenos días\""
echo ""

echo "6️⃣  Pipeline con otros comandos:"
echo "   cat noticias.txt | head -3 | xargs uvx --from . tts-macos"
echo ""

echo ""
echo -e "${GREEN}✨ Ejecutar ejemplos prácticos${NC}"
echo "───────────────────────────────────────────────"
echo ""

read -p "¿Quieres ejecutar ejemplos en vivo? (s/n): " ejecutar

if [[ $ejecutar == "s" || $ejecutar == "S" ]]; then
    echo ""
    echo "Ejemplo 1: Básico"
    uvx --from . tts-macos "Hola, este es un ejemplo básico"
    sleep 2
    
    echo ""
    echo "Ejemplo 2: Con voz de España"
    uvx --from . tts-macos "Hola desde España" --voice jorge
    sleep 2
    
    echo ""
    echo "Ejemplo 3: Velocidad rápida"
    uvx --from . tts-macos "Este mensaje es muy rápido" --rate 250
    sleep 2
    
    echo ""
    echo "Ejemplo 4: Velocidad lenta"
    uvx --from . tts-macos "Este mensaje es muy lento" --rate 125
    sleep 2
    
    echo ""
    echo "Ejemplo 5: Listar voces"
    uvx --from . tts-macos --list
    
    echo ""
    echo -e "${GREEN}✅ Ejemplos completados!${NC}"
else
    echo ""
    echo "Puedes ejecutar cualquier ejemplo manualmente."
fi

echo ""
echo "───────────────────────────────────────────────"
echo "📚 Más información:"
echo "   UVX-GUIDE.md  - Guía completa de uvx"
echo "   CLI-GUIDE.md  - Guía completa CLI"
echo "   README.md     - Documentación general"
echo "───────────────────────────────────────────────"
