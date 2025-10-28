#!/bin/bash
# Test rápido de 30 segundos para verificar funcionamiento básico

echo "⚡ TEST RÁPIDO DE HOOKS TTS-MACOS (30 segundos)"
echo "════════════════════════════════════════════════"
echo ""

# Test 1: Archivos existen
echo -n "1. Verificando archivos... "
if [ -f ".claude/hooks/post-response" ] && [ -f ".claude/hooks/user-prompt-submit" ]; then
    echo "✅"
else
    echo "❌"
    exit 1
fi

# Test 2: Permisos
echo -n "2. Verificando permisos... "
if [ -x ".claude/hooks/post-response" ] && [ -x ".claude/hooks/user-prompt-submit" ]; then
    echo "✅"
else
    echo "❌ (ejecuta: chmod +x .claude/hooks/*)"
    exit 1
fi

# Test 3: Comando say
echo -n "3. Verificando comando 'say'... "
if command -v say &> /dev/null; then
    echo "✅"
else
    echo "❌ (solo funciona en macOS)"
    exit 1
fi

# Test 4: Voces disponibles
echo -n "4. Verificando voces en español... "
VOCES=$(say -v ? | grep -i spanish | wc -l | tr -d ' ')
if [ "$VOCES" -gt 0 ]; then
    echo "✅ ($VOCES encontradas)"
else
    echo "❌ (instala voces en español)"
    exit 1
fi

# Test 5: Prueba de audio
echo ""
echo "5. Prueba de audio (escucharás 'Prueba exitosa')..."
export TTS_ENABLED=true
export TTS_VOICE=monica
echo "Prueba exitosa" | ./.claude/hooks/post-response &
PID=$!
sleep 3

echo ""
read -p "¿Escuchaste el audio? (s/n): " respuesta

if [[ "$respuesta" == "s" || "$respuesta" == "S" ]]; then
    echo ""
    echo "✅ TODOS LOS TESTS PASARON"
    echo ""
    echo "Los hooks están funcionando correctamente."
    echo ""
    echo "Para usar:"
    echo "  export TTS_ENABLED=true"
    echo "  claude-code"
    echo ""
    exit 0
else
    echo ""
    echo "❌ TEST DE AUDIO FALLÓ"
    echo ""
    echo "Verifica:"
    echo "  - Volumen del sistema"
    echo "  - Comando: say -v Monica 'test'"
    echo ""
    exit 1
fi
