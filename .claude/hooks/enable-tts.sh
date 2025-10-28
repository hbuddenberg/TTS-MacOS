#!/bin/bash
# Script de activación rápida para TTS-macOS hooks

echo "🎙️  Configuración de TTS-macOS para Claude Code"
echo "=============================================="
echo ""

# Mostrar configuración actual
echo "📋 Configuración actual:"
echo "  TTS_ENABLED: ${TTS_ENABLED:-false}"
echo "  TTS_VOICE: ${TTS_VOICE:-monica}"
echo "  TTS_RATE: ${TTS_RATE:-175}"
echo ""

# Preguntar si quiere habilitar
read -p "¿Habilitar TTS para respuestas? (s/n): " enable

if [[ $enable == "s" || $enable == "S" ]]; then
    export TTS_ENABLED=true

    # Seleccionar voz
    echo ""
    echo "🎤 Voces disponibles:"
    echo "  1. monica   (Español México - Mujer)"
    echo "  2. paulina  (Español México - Mujer)"
    echo "  3. jorge    (Español España - Hombre)"
    echo "  4. juan     (Español España - Hombre)"
    echo "  5. diego    (Español Argentina - Hombre)"
    echo "  6. angelica (Español México - Mujer)"
    echo ""
    read -p "Selecciona una voz (1-6, Enter para monica): " voice_choice

    case $voice_choice in
        2) export TTS_VOICE=paulina ;;
        3) export TTS_VOICE=jorge ;;
        4) export TTS_VOICE=juan ;;
        5) export TTS_VOICE=diego ;;
        6) export TTS_VOICE=angelica ;;
        *) export TTS_VOICE=monica ;;
    esac

    # Seleccionar velocidad
    echo ""
    read -p "Velocidad en palabras por minuto (100-300, Enter para 175): " rate_choice

    if [[ $rate_choice =~ ^[0-9]+$ ]] && [ $rate_choice -ge 100 ] && [ $rate_choice -le 300 ]; then
        export TTS_RATE=$rate_choice
    else
        export TTS_RATE=175
    fi

    # Confirmación de prompts
    echo ""
    read -p "¿Habilitar confirmación de prompts del usuario? (s/n): " prompt_enable

    if [[ $prompt_enable == "s" || $prompt_enable == "S" ]]; then
        export TTS_PROMPT_ENABLED=true
        export TTS_PROMPT_VOICE=jorge
        export TTS_PROMPT_RATE=200
    fi

    echo ""
    echo "✅ TTS habilitado con la siguiente configuración:"
    echo "  Voz: $TTS_VOICE"
    echo "  Velocidad: $TTS_RATE WPM"
    if [ "$TTS_PROMPT_ENABLED" = "true" ]; then
        echo "  Confirmación de prompts: Sí"
    fi
    echo ""
    echo "💡 Para hacer esto permanente, agrega a tu ~/.zshrc:"
    echo ""
    echo "export TTS_ENABLED=true"
    echo "export TTS_VOICE=$TTS_VOICE"
    echo "export TTS_RATE=$TTS_RATE"
    if [ "$TTS_PROMPT_ENABLED" = "true" ]; then
        echo "export TTS_PROMPT_ENABLED=true"
    fi
    echo ""
    echo "🧪 Prueba de audio..."
    if command -v tts-macos &> /dev/null; then
        tts-macos "Sistema TTS configurado correctamente" --voice "$TTS_VOICE" --rate "$TTS_RATE"
    else
        VOICE_CAP="$(echo "${TTS_VOICE:0:1}" | tr '[:lower:]' '[:upper:]')${TTS_VOICE:1}"
        say -v "$VOICE_CAP" -r "$TTS_RATE" "Sistema TTS configurado correctamente"
    fi

else
    export TTS_ENABLED=false
    echo ""
    echo "ℹ️  TTS deshabilitado"
fi

echo ""
echo "🎉 Listo! Las variables están configuradas para esta sesión."
echo "   Ahora puedes usar Claude Code con TTS."
