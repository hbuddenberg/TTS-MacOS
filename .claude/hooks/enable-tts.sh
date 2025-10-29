#!/bin/bash
# Script de activación rápida para TTS-macOS hooks

echo "🎙️  Configuración de TTS-macOS para Claude Code"
echo "=============================================="
echo ""

# Detectar todas las voces disponibles
echo "🔍 Detectando voces disponibles en el sistema..."
echo ""

# Función para obtener voces categorizadas
get_spanish_voices() {
    say -v ? | grep -iE "(spanish|español)" | awk '{print $1}'
}

get_siri_voices() {
    say -v ? | grep -i "siri" | awk '{print $1}'
}

get_premium_voices() {
    say -v ? | grep -iE "(premium|enhanced|superior)" | awk '{print $1}'
}

# Obtener listas
SPANISH_VOICES=($(get_spanish_voices))
SIRI_VOICES=($(get_siri_voices))
ALL_VOICES=($(say -v ? | awk '{print $1}' | sort -u))

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

    # Mostrar voces disponibles
    echo ""
    echo "🎤 Voces disponibles en tu sistema:"
    echo ""

    if [ ${#SPANISH_VOICES[@]} -gt 0 ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📍 VOCES EN ESPAÑOL (${#SPANISH_VOICES[@]})"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        counter=1
        for voz in "${SPANISH_VOICES[@]}"; do
            info=$(say -v ? | grep "^$voz " | head -1)
            echo "  $counter. $info"
            counter=$((counter + 1))
        done
        echo ""
    fi

    if [ ${#SIRI_VOICES[@]} -gt 0 ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🤖 VOCES DE SIRI (${#SIRI_VOICES[@]})"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        counter=1
        for voz in "${SIRI_VOICES[@]}"; do
            info=$(say -v ? | grep "^$voz " | head -1)
            echo "  $counter. $info"
            counter=$((counter + 1))
        done
        echo ""
    fi

    # Seleccionar voz
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Selecciona una voz:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Opciones:"
    echo "  - Escribe el NOMBRE de la voz (ej: Monica, Jorge, Siri, Paulina)"
    echo "  - Escribe NÚMERO de la lista de arriba"
    echo "  - Presiona Enter para usar Monica (por defecto)"
    echo ""
    read -p "Tu elección: " voice_choice

    if [ -z "$voice_choice" ]; then
        # Default: Monica
        export TTS_VOICE=monica
    elif [[ "$voice_choice" =~ ^[0-9]+$ ]]; then
        # Es un número - buscar en la lista combinada
        all_voices_array=(${SPANISH_VOICES[@]} ${SIRI_VOICES[@]})
        if [ $voice_choice -gt 0 ] && [ $voice_choice -le ${#all_voices_array[@]} ]; then
            selected_voice="${all_voices_array[$((voice_choice - 1))]}"
            export TTS_VOICE="$selected_voice"
        else
            echo "⚠️  Número inválido, usando Monica"
            export TTS_VOICE=monica
        fi
    else
        # Es un nombre - buscar la voz
        voice_found=$(say -v ? | grep -i "^${voice_choice}" | head -1 | awk '{print $1}')
        if [ -n "$voice_found" ]; then
            export TTS_VOICE="$voice_found"
        else
            # Búsqueda parcial (para "siri", "female", etc)
            voice_partial=$(say -v ? | grep -i "$voice_choice" | head -1 | awk '{print $1}')
            if [ -n "$voice_partial" ]; then
                export TTS_VOICE="$voice_partial"
            else
                echo "⚠️  Voz no encontrada, usando Monica"
                export TTS_VOICE=monica
            fi
        fi
    fi

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

        echo ""
        echo "Selecciona voz para confirmaciones (o Enter para usar la misma):"
        read -p "Voz: " prompt_voice

        if [ -z "$prompt_voice" ]; then
            export TTS_PROMPT_VOICE="$TTS_VOICE"
        else
            voice_found=$(say -v ? | grep -i "^${prompt_voice}" | head -1 | awk '{print $1}')
            if [ -n "$voice_found" ]; then
                export TTS_PROMPT_VOICE="$voice_found"
            else
                voice_partial=$(say -v ? | grep -i "$prompt_voice" | head -1 | awk '{print $1}')
                if [ -n "$voice_partial" ]; then
                    export TTS_PROMPT_VOICE="$voice_partial"
                else
                    export TTS_PROMPT_VOICE="$TTS_VOICE"
                fi
            fi
        fi

        export TTS_PROMPT_RATE=200
    fi

    echo ""
    echo "✅ TTS habilitado con la siguiente configuración:"
    echo "  Voz: $TTS_VOICE"
    echo "  Velocidad: $TTS_RATE WPM"
    if [ "$TTS_PROMPT_ENABLED" = "true" ]; then
        echo "  Confirmación de prompts: Sí (voz: $TTS_PROMPT_VOICE)"
    fi
    echo ""
    echo "💡 Para hacer esto permanente, agrega a tu ~/.zshrc:"
    echo ""
    echo "export TTS_ENABLED=true"
    echo "export TTS_VOICE=\"$TTS_VOICE\""
    echo "export TTS_RATE=$TTS_RATE"
    if [ "$TTS_PROMPT_ENABLED" = "true" ]; then
        echo "export TTS_PROMPT_ENABLED=true"
        echo "export TTS_PROMPT_VOICE=\"$TTS_PROMPT_VOICE\""
    fi
    echo ""
    echo "🧪 Prueba de audio..."

    # Probar con la voz seleccionada
    if command -v tts-macos &> /dev/null; then
        tts-macos "Sistema TTS configurado correctamente con voz $TTS_VOICE" --voice "$(echo "$TTS_VOICE" | tr '[:upper:]' '[:lower:]')" --rate "$TTS_RATE"
    else
        say -v "$TTS_VOICE" -r "$TTS_RATE" "Sistema TTS configurado correctamente con voz $TTS_VOICE"
    fi

else
    export TTS_ENABLED=false
    echo ""
    echo "ℹ️  TTS deshabilitado"
fi

echo ""
echo "🎉 Listo! Las variables están configuradas para esta sesión."
echo "   Ahora puedes usar Claude Code con TTS."
