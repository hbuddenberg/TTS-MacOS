#!/bin/bash
# Configurador interactivo para hooks de TTS en Zed
# Este script configura automáticamente las variables de entorno necesarias

echo "🎭 Configuración de TTS para Zed"
echo "=================================="
echo ""

# Verificar si TTS-macOS está instalado
if ! command -v tts-macos &> /dev/null; then
    echo "❌ TTS-macOS no encontrado. Por favor, instálalo primero:"
    echo "   cd /Volumes/Resources/Develop/TTS-MacOS"
    echo "   ./install-cli.sh"
    exit 1
fi

# Listar voces disponibles
echo "🔍 Buscando voces disponibles en el sistema..."
echo ""
say -v ? | grep -iE "(spanish|español|siri|enhanced|premium)" | head -10
echo ""

echo "Voz por defecto para notificaciones:"
default_voice="monica"
read -p "[$default_voice] " voice
voice=${voice:-$default_voice}

echo "Velocidad de habla (palabras por minuto):"
default_rate="175"
read -p "[$default_rate] " rate
rate=${rate:-$default_rate}

echo "Voz para tareas complejas:"
task_voice="jorge"
read -p "[$task_voice] " task_voice
task_voice=${task_voice:-$task_voice}

echo "Velocidad para tareas complejas:"
task_rate="180"
read -p "[$task_rate] " task_rate
task_rate=${task_rate:-$task_rate}

echo ""
echo "Configuración seleccionada:"
echo "  🔊 Voz normal: $voice"
echo "  ⚡ Velocidad: $rate wpm"
echo "  🔊 Voz tareas: $task_voice"
echo "  ⚡ Velocidad tareas: $task_rate wpm"

echo ""
read -p "¿Guardar configuración? (s/N): " save_config

if [[ "$save_config" =~ ^[sS]$ ]]; then
    # Crear o actualizar el archivo de configuración
    config_file="$HOME/.zed/tts-config"

    mkdir -p "$(dirname "$config_file")"

    cat > "$config_file" << EOF
# Configuración de TTS para Zed
export ZED_TTS_ENABLED=true
export ZED_TTS_VOICE="$voice"
export ZED_TTS_RATE="$rate"
export ZED_TTS_TASK_VOICE="$task_voice"
export ZED_TTS_TASK_RATE="$task_rate"
export ZED_TTS_MAX_LENGTH="100"
export ZED_STARTUP_ANNOUNCE="true"
EOF

    # Añadir al perfil de shell
    shell_profile=""
    if [ -f "$HOME/.zshrc" ]; then
        shell_profile="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        shell_profile="$HOME/.bashrc"
    elif [ -f "$HOME/.bash_profile" ]; then
        shell_profile="$HOME/.bash_profile"
    else
        shell_profile="$HOME/.zshrc"
    fi

    # Verificar si ya está en el archivo
    if ! grep -q "ZED_TTS_ENABLED" "$shell_profile"; then
        echo "" >> "$shell_profile"
        echo "# Configuración de TTS para Zed" >> "$shell_profile"
        echo "source $config_file" >> "$shell_profile"
    fi

    echo "✅ Configuración guardada en: $config_file"
    echo "✅ Configuración añadida a: $shell_profile"

    echo ""
    echo "🔄 Carga la configuración actual:"
    echo "   source $config_file"

    echo ""
    echo "🧪 Prueba los hooks:"
    echo "   echo 'test' | $PWD/zed/hooks/file-save-complete test.py"
    echo "   echo 'build success' | $PWD/zed/hooks/task-complete build"
    echo "   $PWD/zed/hooks/startup-complete mi-proyecto"

    echo ""
    echo "¡Listo! Reinicia tu terminal para que la configuración tenga efecto."
else
    echo "Configuración no guardada. Puedes configurar manualmente las variables:"
    echo "  export ZED_TTS_ENABLED=true"
    echo "  export ZED_TTS_VOICE=\"$voice\""
    echo "  export ZED_TTS_RATE=\"$rate\""
    echo "  export ZED_TTS_TASK_VOICE=\"$task_voice\""
    echo "  export ZED_TTS_TASK_RATE=\"$task_rate\""
fi

echo ""
echo "📖 Documentación completa en: $PWD/zed/README.md"
