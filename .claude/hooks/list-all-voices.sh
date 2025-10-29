#!/bin/bash
# Script para listar TODAS las voces disponibles en el sistema

echo "🎙️  TODAS LAS VOCES DISPONIBLES EN EL SISTEMA"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Función para categorizar voces
categorize_voices() {
    # Voces en Español
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📍 VOCES EN ESPAÑOL"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    SPANISH_COUNT=$(say -v ? | grep -iE "(spanish|español)" | wc -l | tr -d ' ')
    if [ "$SPANISH_COUNT" -gt 0 ]; then
        say -v ? | grep -iE "(spanish|español)" | while read line; do
            nombre=$(echo "$line" | awk '{print $1}')
            resto=$(echo "$line" | cut -d' ' -f2-)
            printf "  %-15s %s\n" "$nombre" "$resto"
        done
        echo ""
        echo "  Total: $SPANISH_COUNT voces"
    else
        echo "  ❌ No hay voces en español instaladas"
    fi
    echo ""

    # Voces de Siri
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🤖 VOCES DE SIRI"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    SIRI_COUNT=$(say -v ? | grep -i "siri" | wc -l | tr -d ' ')
    if [ "$SIRI_COUNT" -gt 0 ]; then
        say -v ? | grep -i "siri" | while read line; do
            nombre=$(echo "$line" | awk '{print $1}')
            resto=$(echo "$line" | cut -d' ' -f2-)
            printf "  %-15s %s\n" "$nombre" "$resto"
        done
        echo ""
        echo "  Total: $SIRI_COUNT voces"
    else
        echo "  ℹ️  No hay voces de Siri instaladas"
    fi
    echo ""

    # Voces Premium/Mejoradas
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⭐ VOCES PREMIUM/MEJORADAS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    PREMIUM_COUNT=$(say -v ? | grep -iE "(premium|enhanced|superior)" | wc -l | tr -d ' ')
    if [ "$PREMIUM_COUNT" -gt 0 ]; then
        say -v ? | grep -iE "(premium|enhanced|superior)" | while read line; do
            nombre=$(echo "$line" | awk '{print $1}')
            resto=$(echo "$line" | cut -d' ' -f2-)
            printf "  %-15s %s\n" "$nombre" "$resto"
        done
        echo ""
        echo "  Total: $PREMIUM_COUNT voces"
    else
        echo "  ℹ️  No hay voces premium instaladas"
    fi
    echo ""

    # Todas las voces (resumen compacto)
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 TODAS LAS VOCES (LISTA COMPLETA)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    TOTAL_COUNT=$(say -v ? | wc -l | tr -d ' ')
    echo "  Total de voces instaladas: $TOTAL_COUNT"
    echo ""
    echo "  Nombres disponibles para usar:"
    say -v ? | awk '{print "    • " $1}' | sort -u
    echo ""
}

categorize_voices

echo "═══════════════════════════════════════════════════════════"
echo "💡 CÓMO USAR"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Para usar cualquier voz con los hooks:"
echo ""
echo "  # Voces en español (nombre exacto o lowercase)"
echo "  export TTS_VOICE=Monica"
echo "  export TTS_VOICE=Jorge"
echo "  export TTS_VOICE=Paulina"
echo "  export TTS_VOICE=Angelica"
echo "  export TTS_VOICE=Francisca"
echo ""
echo "  # Voces de Siri (búsqueda parcial funciona)"
echo "  export TTS_VOICE=Siri"
echo "  export TTS_VOICE=\"Siri Female\""
echo "  export TTS_VOICE=\"Siri Male\""
echo ""
echo "  # También funciona búsqueda parcial"
echo "  export TTS_VOICE=siri      # Encontrará la primera voz Siri"
echo "  export TTS_VOICE=female    # Encontrará primera voz femenina"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "🧪 PROBAR VOCES"
echo "═══════════════════════════════════════════════════════════"
echo ""
read -p "¿Quieres probar alguna voz? (s/n): " test_voice

if [[ "$test_voice" == "s" || "$test_voice" == "S" ]]; then
    echo ""
    read -p "Escribe el nombre de la voz (ej: Monica, Siri, Jorge): " voice_name

    if [ -n "$voice_name" ]; then
        # Buscar voz
        voice_found=$(say -v ? | grep -i "^${voice_name}" | head -1 | awk '{print $1}')
        if [ -z "$voice_found" ]; then
            voice_found=$(say -v ? | grep -i "$voice_name" | head -1 | awk '{print $1}')
        fi

        if [ -n "$voice_found" ]; then
            echo ""
            echo "🔊 Probando voz: $voice_found"
            say -v "$voice_found" "Hola, soy la voz $voice_found. Esta es una prueba de audio."
            echo ""
            echo "✅ Para usar esta voz:"
            echo "   export TTS_VOICE=\"$voice_found\""
        else
            echo "❌ Voz no encontrada: $voice_name"
        fi
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "📖 Más información: .claude/hooks/README.md"
echo "═══════════════════════════════════════════════════════════"
