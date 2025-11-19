#!/bin/bash
# Script de instalación global para TTS Notify CLI

echo "🔔  Instalación Global de TTS Notify CLI"
echo "======================================"
echo ""

# Verificar macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Este script es solo para macOS"
    exit 1
fi

# Limpiar caché de instalaciones previas
echo "🧹 Limpiando caché de instalaciones previas..."
rm -rf ~/.cache/tts-notify 2>/dev/null
rm -rf ~/.cache/tts-macos 2>/dev/null
rm -rf /tmp/tts-notify-* 2>/dev/null

# Limpiar instalación anterior si existe
for cmd in tts-notify tts-macos; do
    if [ -f "$HOME/.local/bin/$cmd" ]; then
        echo "🗑️  Eliminando instalación anterior en ~/.local/bin/$cmd"
        rm -f "$HOME/.local/bin/$cmd"
    fi

    if [ -f "/usr/local/bin/$cmd" ]; then
        echo "🗑️  Eliminando instalación anterior en /usr/local/bin/$cmd"
        sudo rm -f "/usr/local/bin/$cmd" 2>/dev/null
    fi
done

echo "✅ Caché limpio"
echo ""

# Obtener directorio del proyecto (subir desde installers/)
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
CLI_SCRIPT="$PROJECT_DIR/src/cli.py"

# Verificar que existe el script
if [ ! -f "$CLI_SCRIPT" ]; then
    echo "❌ No se encuentra el script CLI en: $CLI_SCRIPT"
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "Por favor instala Python desde https://www.python.org/downloads/"
    exit 1
fi

echo "📁 Directorio del proyecto: $PROJECT_DIR"
echo "📄 Script CLI: $CLI_SCRIPT"
echo ""

echo "📦 Opciones de instalación:"
echo ""
echo "1. Instalación para el usuario actual (recomendado)"
echo "   → ~/.local/bin/tts-notify"
echo ""
echo "2. Instalación global del sistema (requiere sudo)"
echo "   → /usr/local/bin/tts-notify"
echo ""
echo "3. Crear wrapper script (ejecutable independiente)"
echo ""
echo "4. Instalación via pip install -e"
echo ""

read -p "Selecciona una opción (1-4): " opcion

case $opcion in
    1)
        # Instalación local - enlace simbólico
        TARGET_DIR="$HOME/.local/bin"
        mkdir -p "$TARGET_DIR"

        # Crear wrapper script
        cat > "$TARGET_DIR/tts-notify" << EOF
#!/bin/bash
python3 "$CLI_SCRIPT" "\$@"
EOF
        chmod +x "$TARGET_DIR/tts-notify"

        echo "✅ Instalado en: $TARGET_DIR/tts-notify"
        echo "✅ Wrapper script creado que apunta al proyecto"

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

        # Crear wrapper script para instalación global
        cat > /tmp/tts-notify-wrapper << EOF
#!/bin/bash
python3 "$CLI_SCRIPT" "\$@"
EOF

        sudo cp /tmp/tts-notify-wrapper /usr/local/bin/tts-notify
        sudo chmod +x /usr/local/bin/tts-notify
        rm -f /tmp/tts-notify-wrapper

        if [ $? -eq 0 ]; then
            echo "✅ Instalado en: /usr/local/bin/tts-notify"
            echo "✅ Wrapper script global creado"
        else
            echo "❌ Error en la instalación"
            exit 1
        fi
        ;;

    3)
        # Crear script independiente
        echo ""
        echo "📦 Creando script independiente..."

        # Crear script con shebang y rutas absolutas
        cat > "$PROJECT_DIR/tts-notify-standalone" << EOF
#!/bin/bash
python3 "$CLI_SCRIPT" "\$@"
EOF
        chmod +x "$PROJECT_DIR/tts-notify-standalone"

        echo "✅ Script independiente creado: $PROJECT_DIR/tts-notify-standalone"
        echo "✅ Puedes moverlo o copiarlo donde quieras"
        echo ""
        echo "Ejemplos:"
        echo "  cp $PROJECT_DIR/tts-notify-standalone /usr/local/bin/tts-notify"
        echo "  cp $PROJECT_DIR/tts-notify-standalone ~/Desktop/tts-notify"
        ;;

    4)
        # Instalación via pip
        echo ""
        echo "📦 Instalando via pip install -e..."

        cd "$PROJECT_DIR"

        # Verificar si tenemos un entorno virtual
        if [[ "$VIRTUAL_ENV" != "" ]]; then
            echo "✅ Detectado entorno virtual: $VIRTUAL_ENV"
            pip install -e .
        else
            echo "⚠️  No se detectó entorno virtual"
            echo "Instalando en el entorno global..."
            pip3 install -e .
        fi

        if [ $? -eq 0 ]; then
            echo "✅ Instalado via pip"
            echo "✅ Comando disponible: tts-notify"
        else
            echo "❌ Error en la instalación pip"
            exit 1
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
echo "    tts-notify \"Hola mundo\""
echo "    tts-notify --list"
echo "    tts-notify --help"
echo ""
echo "📚 Ejemplos de uso:"
echo ""
echo "    tts-notify \"Buenos días\" --voice Jorge"
echo "    tts-notify \"Rápido\" --rate 250"
echo "    tts-notify \"Guardar\" --save audio.aiff"
echo ""
echo "🔍 Opciones avanzadas:"
echo ""
echo "    tts-notify --list --gen female          # Solo voces femeninas"
echo "    tts-notify --list --gen male            # Solo voces masculinas"
echo "    tts-notify --list --lang es_ES          # Solo voces de España"
echo "    tts-notify --list --lang es_MX          # Solo voces de México"
echo "    tts-notify --list --compact             # Vista resumida"
echo ""
echo "🔄 USO CON UVX (alternativa sin instalar):"
echo "    uvx --from $PROJECT_DIR tts-notify \"Hola mundo\""
echo "    uvx --from $PROJECT_DIR tts-notify --list"
echo ""
echo "🎤 VOCES DISPONIBLES:"
echo "    • Jorge, Mónica (España)"
echo "    • Angélica, Juan (México)"
echo "    • Francisca (Chile)"
echo "    • Carlos, Soledad, Jimena (Colombia)"
echo "    • Diego, Isabela (Argentina)"
echo "    • +50 voces adicionales del sistema"
echo ""
echo "📖 Documentación completa:"
echo "    $PROJECT_DIR/documentation/"
echo ""
echo "🎉 ¡Disfruta de TTS Notify v1.5.0!"
