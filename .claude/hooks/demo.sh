#!/bin/bash
# Script de demostración de los hooks TTS-macOS

echo "🎙️  DEMOSTRACIÓN DE HOOKS TTS-macOS"
echo "===================================="
echo ""
echo "Este script demuestra cómo funcionan los hooks de TTS."
echo ""

# Verificar que tts-macos esté disponible
if ! command -v tts-macos &> /dev/null; then
    echo "⚠️  tts-macos no está instalado. Usando comando 'say' nativo."
    USE_SAY=true
else
    echo "✅ tts-macos encontrado"
    USE_SAY=false
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "DEMO 1: Hook post-response (Lee respuestas de Claude)"
echo "═══════════════════════════════════════════════════════"
echo ""

# Simular una respuesta de Claude
RESPONSE="Hola, soy Claude. Este es un ejemplo de respuesta que sería leída en voz alta cuando el hook está habilitado."

echo "Respuesta simulada de Claude:"
echo "\"$RESPONSE\""
echo ""
echo "Reproduciendo con voz Monica a 175 WPM..."

if [ "$USE_SAY" = true ]; then
    say -v Monica -r 175 "$RESPONSE"
else
    tts-macos "$RESPONSE" --voice monica --rate 175
fi

sleep 2
echo ""

echo "═══════════════════════════════════════════════════════"
echo "DEMO 2: Diferentes voces"
echo "═══════════════════════════════════════════════════════"
echo ""

declare -a voices=("monica" "jorge" "paulina")
declare -a descriptions=("Mujer México" "Hombre España" "Mujer México")

for i in "${!voices[@]}"; do
    voice="${voices[$i]}"
    desc="${descriptions[$i]}"
    text="Hola, soy la voz $voice, $desc"

    echo "► Voz: $voice ($desc)"

    if [ "$USE_SAY" = true ]; then
        voice_cap="$(echo "${voice:0:1}" | tr '[:lower:]' '[:upper:]')${voice:1}"
        say -v "$voice_cap" -r 175 "$text"
    else
        tts-macos "$text" --voice "$voice" --rate 175
    fi

    sleep 1
done

echo ""

echo "═══════════════════════════════════════════════════════"
echo "DEMO 3: Diferentes velocidades"
echo "═══════════════════════════════════════════════════════"
echo ""

declare -a rates=(120 175 250)
declare -a rate_desc=("Lenta" "Normal" "Rápida")

for i in "${!rates[@]}"; do
    rate="${rates[$i]}"
    desc="${rate_desc[$i]}"
    text="Esta es una velocidad $desc a $rate palabras por minuto"

    echo "► Velocidad: $desc ($rate WPM)"

    if [ "$USE_SAY" = true ]; then
        say -v Monica -r "$rate" "$text"
    else
        tts-macos "$text" --voice monica --rate "$rate"
    fi

    sleep 1
done

echo ""

echo "═══════════════════════════════════════════════════════"
echo "DEMO 4: Hook user-prompt-submit"
echo "═══════════════════════════════════════════════════════"
echo ""

echo "Simulando envío de prompt del usuario..."
ANNOUNCEMENT="Procesando tu solicitud"

if [ "$USE_SAY" = true ]; then
    say -v Jorge -r 200 "$ANNOUNCEMENT"
else
    tts-macos "$ANNOUNCEMENT" --voice jorge --rate 200
fi

echo ""
sleep 1

echo "═══════════════════════════════════════════════════════"
echo "DEMO 5: Filtrado de contenido (sin código)"
echo "═══════════════════════════════════════════════════════"
echo ""

RESPONSE_WITH_CODE="Aquí está el código:

\`\`\`python
def hello():
    print('Hello')
\`\`\`

Este es el texto después del código que sí se lee."

echo "Respuesta original con código:"
echo "$RESPONSE_WITH_CODE"
echo ""

# Filtrar código
TEXT=$(echo "$RESPONSE_WITH_CODE" | sed '/```/,/```/d' | sed 's/[#*`]//g')

echo "Texto filtrado (sin código):"
echo "$TEXT"
echo ""
echo "Reproduciendo solo el texto..."

if [ "$USE_SAY" = true ]; then
    say -v Monica -r 175 "$TEXT"
else
    tts-macos "$TEXT" --voice monica --rate 175
fi

echo ""
sleep 2

echo "═══════════════════════════════════════════════════════"
echo "✅ DEMOSTRACIÓN COMPLETADA"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📚 Para usar estos hooks en Claude Code:"
echo ""
echo "1. Habilita el TTS:"
echo "   export TTS_ENABLED=true"
echo ""
echo "2. (Opcional) Configura la voz y velocidad:"
echo "   export TTS_VOICE=monica"
echo "   export TTS_RATE=175"
echo ""
echo "3. O usa el script de configuración interactiva:"
echo "   source .claude/hooks/enable-tts.sh"
echo ""
echo "📖 Consulta .claude/hooks/README.md para más información"
echo ""
echo "🎉 ¡Disfruta de Claude Code con voz en español!"
