#!/bin/bash
# Script de instalación global para tts-macos CLI

echo "🎙️  Instalación Global de TTS-macOS CLI"
echo "========================================"
echo ""

# Verificar macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Este script es solo para macOS"
    exit 1
fi

# Directorio actual
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLI_SCRIPT="$SCRIPT_DIR/tts-macos"

# Verificar que existe el script
if [ ! -f "$CLI_SCRIPT" ]; then
    echo "❌ No se encuentra el script tts-macos"
    exit 1
fi

echo "📦 Opciones de instalación:"
echo ""
echo "1. Instalación para el usuario actual (recomendado)"
echo "   → ~/.local/bin/tts-macos"
echo ""
echo "2. Instalación global del sistema (requiere sudo)"
echo "   → /usr/local/bin/tts-macos"
echo ""
echo "3. Solo crear enlace simbólico"
echo ""

read -p "Selecciona una opción (1-3): " opcion

case $opcion in
    1)
        # Instalación local
        TARGET_DIR="$HOME/.local/bin"
        mkdir -p "$TARGET_DIR"
        
        cp "$CLI_SCRIPT" "$TARGET_DIR/tts-macos"
        chmod +x "$TARGET_DIR/tts-macos"
        
        echo "✅ Instalado en: $TARGET_DIR/tts-macos"
        
        # Verificar si está en el PATH
        if [[ ":$PATH:" != *":$TARGET_DIR:"* ]]; then
            echo ""
            echo "⚠️  Necesitas agregar ~/.local/bin a tu PATH"
            echo ""
            echo "Agrega esta línea a tu ~/.zshrc o ~/.bash_profile:"
            echo ""
            echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
            echo ""
            read -p "¿Quieres que lo agregue automáticamente? (s/n): " add_path
            
            if [[ $add_path == "s" || $add_path == "S" ]]; then
                if [ -f "$HOME/.zshrc" ]; then
                    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
                    echo "✅ Agregado a ~/.zshrc"
                    echo "Ejecuta: source ~/.zshrc"
                elif [ -f "$HOME/.bash_profile" ]; then
                    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bash_profile"
                    echo "✅ Agregado a ~/.bash_profile"
                    echo "Ejecuta: source ~/.bash_profile"
                fi
            fi
        fi
        ;;
        
    2)
        # Instalación global
        echo ""
        echo "Se requieren permisos de administrador..."
        sudo cp "$CLI_SCRIPT" /usr/local/bin/tts-macos
        sudo chmod +x /usr/local/bin/tts-macos
        
        if [ $? -eq 0 ]; then
            echo "✅ Instalado en: /usr/local/bin/tts-macos"
        else
            echo "❌ Error en la instalación"
            exit 1
        fi
        ;;
        
    3)
        # Solo enlace simbólico
        TARGET_DIR="$HOME/.local/bin"
        mkdir -p "$TARGET_DIR"
        
        ln -sf "$CLI_SCRIPT" "$TARGET_DIR/tts-macos"
        
        echo "✅ Enlace creado: $TARGET_DIR/tts-macos → $CLI_SCRIPT"
        
        if [[ ":$PATH:" != *":$TARGET_DIR:"* ]]; then
            echo ""
            echo "⚠️  Agrega ~/.local/bin a tu PATH (ver instrucciones arriba)"
        fi
        ;;
        
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "================================================"
echo "✨ Instalación completada!"
echo "================================================"
echo ""
echo "🧪 Prueba el comando:"
echo ""
echo "    tts-macos \"Hola mundo\""
echo "    tts-macos --list"
echo "    tts-macos --help"
echo ""
echo "📚 Ejemplos de uso:"
echo ""
echo "    tts-macos \"Buenos días\" --voice jorge"
echo "    tts-macos \"Rápido\" --rate 250"
echo "    tts-macos \"Guardar\" --save audio.aiff"
echo ""
echo "🎉 ¡Disfruta de tts-macos!"
