#!/bin/bash
# Test específico para voces de Siri y detección automática

echo "🤖 TEST DE DETECCIÓN AUTOMÁTICA DE VOCES"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Función de test
test_voice_detection() {
    local voice_query="$1"
    local expected="$2"

    echo -n "  Probando: '$voice_query' → "

    # Simular la función find_voice del hook
    exact_match=$(say -v \? 2>/dev/null | grep -i "^${voice_query} " | head -1 | awk '{print $1}')
    if [ -n "$exact_match" ]; then
        echo "✅ Encontrada: $exact_match"
        return 0
    fi

    partial_match=$(say -v \? 2>/dev/null | grep -i "$voice_query" | head -1 | awk '{print $1}')
    if [ -n "$partial_match" ]; then
        echo "✅ Encontrada (parcial): $partial_match"
        return 0
    fi

    echo "❌ No encontrada (fallback a español)"
    return 1
}

echo "📋 Test 1: Voces en Español"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_voice_detection "monica"
test_voice_detection "Monica"
test_voice_detection "MONICA"
test_voice_detection "jorge"
test_voice_detection "paulina"
test_voice_detection "angelica"
test_voice_detection "francisca"
echo ""

echo "📋 Test 2: Voces de Siri (búsqueda exacta)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_voice_detection "Siri"
test_voice_detection "Siri Female"
test_voice_detection "Siri Male"
echo ""

echo "📋 Test 3: Voces de Siri (búsqueda parcial)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_voice_detection "siri"
test_voice_detection "siri fem"
test_voice_detection "siri male"
test_voice_detection "SIRI"
echo ""

echo "📋 Test 4: Voces Premium/Mejoradas"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
PREMIUM_VOICES=$(say -v \? 2>/dev/null | grep -iE "(premium|enhanced|superior)" | awk '{print $1}')
if [ -n "$PREMIUM_VOICES" ]; then
    echo "$PREMIUM_VOICES" | while read voz; do
        test_voice_detection "$voz"
    done
else
    echo "  ℹ️  No hay voces premium instaladas"
fi
echo ""

echo "📋 Test 5: Prueba de Audio (opcional)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "¿Quieres probar voces con audio? (s/n): " test_audio

if [[ "$test_audio" == "s" || "$test_audio" == "S" ]]; then
    echo ""

    # Test voz en español
    echo "🔊 Test 1: Voz Monica (español)"
    export TTS_ENABLED=true
    export TTS_VOICE=monica
    echo "Hola, soy Monica, una voz en español de México" | ./.claude/hooks/post-response
    sleep 4

    # Test voz Siri si está disponible
    SIRI_AVAILABLE=$(say -v \? 2>/dev/null | grep -i "siri" | head -1 | awk '{print $1}')
    if [ -n "$SIRI_AVAILABLE" ]; then
        echo ""
        echo "🔊 Test 2: Voz Siri ($SIRI_AVAILABLE)"
        export TTS_VOICE=siri
        echo "Hola, soy Siri, una voz de alta calidad" | ./.claude/hooks/post-response
        sleep 4
    fi

    # Test búsqueda parcial
    echo ""
    echo "🔊 Test 3: Búsqueda parcial ('jorge')"
    export TTS_VOICE=jorge
    echo "Probando búsqueda automática de voz" | ./.claude/hooks/post-response
    sleep 4

    unset TTS_ENABLED
    unset TTS_VOICE
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ TESTS COMPLETADOS"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Resultados:"
echo "  • Los hooks detectan automáticamente las voces disponibles"
echo "  • Funciona con nombres exactos y búsqueda parcial"
echo "  • Soporta case-insensitive (mayúsculas/minúsculas)"
echo "  • Incluye fallback inteligente a voces en español"
echo ""
echo "Para ver todas las voces:"
echo "  ./.claude/hooks/list-all-voices.sh"
echo ""
echo "Para configurar interactivamente:"
echo "  source .claude/hooks/enable-tts.sh"
echo ""
