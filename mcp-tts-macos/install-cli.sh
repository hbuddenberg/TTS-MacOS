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

# Limpiar caché de instalaciones previas
echo "🧹 Limpiando caché de instalaciones previas..."
rm -rf ~/.cache/tts-macos 2>/dev/null
rm -rf /tmp/tts-macos-* 2>/dev/null

# Limpiar instalación anterior si existe
if [ -f "$HOME/.local/bin/tts-macos" ]; then
    echo "🗑️  Eliminando instalación anterior en ~/.local/bin/tts-macos"
    rm -f "$HOME/.local/bin/tts-macos"
fi

if [ -f "$HOME/.local/bin/tts-macos.py" ]; then
    echo "🗑️  Eliminando instalación anterior en ~/.local/bin/tts-macos.py"
    rm -f "$HOME/.local/bin/tts-macos.py"
fi

if [ -f "/usr/local/bin/tts-macos" ]; then
    echo "🗑️  Eliminando instalación anterior en /usr/local/bin/tts-macos"
    sudo rm -f "/usr/local/bin/tts-macos" 2>/dev/null
fi

if [ -f "/usr/local/bin/tts-macos.py" ]; then
    echo "🗑️  Eliminando instalación anterior en /usr/local/bin/tts-macos.py"
    sudo rm -f "/usr/local/bin/tts-macos.py" 2>/dev/null
fi

echo "✅ Caché limpio"
echo ""

# Directorio actual
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLI_SCRIPT="$SCRIPT_DIR/tts-macos-standalone.py"

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
echo "4. Reinstalación completa (limpia todo e reinstala)"
echo ""

read -p "Selecciona una opción (1-4): " opcion

case $opcion in
    1)
        # Instalación local
        TARGET_DIR="$HOME/.local/bin"
        mkdir -p "$TARGET_DIR"

        cp "$CLI_SCRIPT" "$TARGET_DIR/tts-macos"
        chmod +x "$TARGET_DIR/tts-macos"

        echo "✅ Instalado en: $TARGET_DIR/tts-macos"
        echo "✅ Versión standalone con todas las dependencias incluidas"

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
            echo "✅ Versión standalone con todas las dependencias incluidas"
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
        echo "✅ Versión standalone con todas las dependencias incluidas"

        if [[ ":$PATH:" != *":$TARGET_DIR:"* ]]; then
            echo ""
            echo "⚠️  Agrega ~/.local/bin a tu PATH (ver instrucciones arriba)"
        fi
        ;;

    4)
        # Reinstalación completa
        echo ""
        echo "🔄 Realizando reinstalación completa..."

        # Limpiar instalación anterior
        echo "🗑️  Eliminando instalaciones anteriores..."
        rm -f "$HOME/.local/bin/tts-macos" 2>/dev/null
        sudo rm -f "/usr/local/bin/tts-macos" 2>/dev/null

        # Limpiar enlaces simbólicos rotos
        find -L "$HOME/.local/bin" -name "tts-macos" -delete 2>/dev/null
        find -L "/usr/local/bin" -name "tts-macos" -delete 2>/dev/null

        # Limpiar caché de Python
        echo "🧹 Limpiando caché de Python..."
        find ~/.cache -name "*tts*" -delete 2>/dev/null
        python3 -m pip cache purge 2>/dev/null

        # Realizar instalación normal
        echo ""
        echo "📦 Realizando instalación fresca..."
        TARGET_DIR="$HOME/.local/bin"
        mkdir -p "$TARGET_DIR"

        cp "$CLI_SCRIPT" "$TARGET_DIR/tts-macos"
        chmod +x "$TARGET_DIR/tts-macos"

        echo "✅ Reinstalado en: $TARGET_DIR/tts-macos"
        echo "✅ Versión standalone con todas las dependencias incluidas"

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
echo "🔍 Nuevas opciones de filtrado:"
echo ""
echo "    tts-macos --list --gen female          # Solo voces femeninas"
echo "    tts-macos --list --gen male            # Solo voces masculinas"
echo "    tts-macos --list --lang es_ES          # Solo voces de España"
echo "    tts-macos --list --lang es_MX          # Solo voces de México"
echo "    tts-macos --list --gen female --lang es_ES  # Combinado"
echo "    tts-macos --list --compact               # Vista resumida"
echo "    tts-macos --list --compact --gen female  # Filtro compacto femenino"
echo ""
echo "🔄 USO CON UVX:"
echo "    uvx --from . --refresh tts-macos --list --gen female  # Forzar actualización"
echo "    uvx --from . tts-macos --list --gen male             # Uso normal después de refresh"
echo "    uvx --from . tts-macos --list --compact              # Vista resumida"
echo "    uvx --from . tts-macos --list --compact --gen female # Filtro compacto"
echo ""
echo "🚀 VERSIÓN STANDALONE:"
echo "✅ Todas las dependencias incluidas"
echo "✅ Funciona fuera del directorio del proyecto"
echo "✅ Instalación automática con limpieza de caché"
echo ""
echo "🎉 ¡Disfruta de tts-macos!"
