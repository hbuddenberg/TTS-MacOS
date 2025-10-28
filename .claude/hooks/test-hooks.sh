#!/bin/bash
# Script de pruebas automatizadas para los hooks TTS-macOS

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Función para imprimir resultados
print_result() {
    local test_name=$1
    local result=$2
    TESTS_TOTAL=$((TESTS_TOTAL + 1))

    if [ "$result" = "PASS" ]; then
        echo -e "${GREEN}✓${NC} Test $TESTS_TOTAL: $test_name - ${GREEN}PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} Test $TESTS_TOTAL: $test_name - ${RED}FAIL${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

echo "═══════════════════════════════════════════════════════════"
echo "  🧪 TESTS DE HOOKS TTS-MACOS"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Test 1: Verificar que los hooks existen
echo "📋 Verificando archivos..."
echo ""

if [ -f ".claude/hooks/post-response" ]; then
    print_result "Hook post-response existe" "PASS"
else
    print_result "Hook post-response existe" "FAIL"
fi

if [ -f ".claude/hooks/user-prompt-submit" ]; then
    print_result "Hook user-prompt-submit existe" "PASS"
else
    print_result "Hook user-prompt-submit existe" "FAIL"
fi

if [ -f ".claude/hooks/enable-tts.sh" ]; then
    print_result "Script enable-tts.sh existe" "PASS"
else
    print_result "Script enable-tts.sh existe" "FAIL"
fi

if [ -f ".claude/hooks/demo.sh" ]; then
    print_result "Script demo.sh existe" "PASS"
else
    print_result "Script demo.sh existe" "FAIL"
fi

echo ""
echo "📋 Verificando permisos de ejecución..."
echo ""

# Test 2: Verificar permisos
if [ -x ".claude/hooks/post-response" ]; then
    print_result "post-response es ejecutable" "PASS"
else
    print_result "post-response es ejecutable" "FAIL"
    echo "   → Ejecuta: chmod +x .claude/hooks/post-response"
fi

if [ -x ".claude/hooks/user-prompt-submit" ]; then
    print_result "user-prompt-submit es ejecutable" "PASS"
else
    print_result "user-prompt-submit es ejecutable" "FAIL"
    echo "   → Ejecuta: chmod +x .claude/hooks/user-prompt-submit"
fi

if [ -x ".claude/hooks/enable-tts.sh" ]; then
    print_result "enable-tts.sh es ejecutable" "PASS"
else
    print_result "enable-tts.sh es ejecutable" "FAIL"
fi

if [ -x ".claude/hooks/demo.sh" ]; then
    print_result "demo.sh es ejecutable" "PASS"
else
    print_result "demo.sh es ejecutable" "FAIL"
fi

echo ""
echo "📋 Verificando comandos del sistema..."
echo ""

# Test 3: Verificar comando say
if command -v say &> /dev/null; then
    print_result "Comando 'say' disponible" "PASS"
else
    print_result "Comando 'say' disponible" "FAIL"
    echo "   → Este es el comando TTS nativo de macOS"
fi

# Test 4: Verificar tts-macos CLI
if command -v tts-macos &> /dev/null; then
    print_result "Comando 'tts-macos' instalado" "PASS"
else
    print_result "Comando 'tts-macos' instalado" "FAIL"
    echo "   ⚠️  Opcional: Los hooks usarán 'say' como fallback"
fi

echo ""
echo "📋 Probando voces en español..."
echo ""

# Test 5: Verificar voces disponibles
VOCES_DISPONIBLES=$(say -v ? | grep -i spanish | wc -l | tr -d ' ')
if [ "$VOCES_DISPONIBLES" -gt 0 ]; then
    print_result "Voces en español disponibles ($VOCES_DISPONIBLES encontradas)" "PASS"

    # Listar voces
    echo ""
    echo "   Voces encontradas:"
    say -v ? | grep -i spanish | while read line; do
        nombre=$(echo "$line" | awk '{print $1}')
        echo "   - $nombre"
    done
    echo ""
else
    print_result "Voces en español disponibles" "FAIL"
    echo "   → Instala voces: System Preferences → Accessibility → Spoken Content"
fi

# Test 6: Probar voz Monica
if say -v ? | grep -qi "Monica"; then
    print_result "Voz Monica disponible" "PASS"
else
    print_result "Voz Monica disponible" "FAIL"
fi

# Test 7: Probar voz Jorge
if say -v ? | grep -qi "Jorge"; then
    print_result "Voz Jorge disponible" "PASS"
else
    print_result "Voz Jorge disponible" "FAIL"
fi

echo ""
echo "📋 Probando hooks (sin audio, solo lógica)..."
echo ""

# Test 8: Hook post-response con TTS deshabilitado
export TTS_ENABLED=false
TEST_OUTPUT=$(echo "Test con TTS deshabilitado" | ./.claude/hooks/post-response 2>&1)
if [ $? -eq 0 ]; then
    print_result "Hook post-response con TTS_ENABLED=false" "PASS"
else
    print_result "Hook post-response con TTS_ENABLED=false" "FAIL"
fi

# Test 9: Hook user-prompt-submit con TTS deshabilitado
export TTS_PROMPT_ENABLED=false
TEST_OUTPUT=$(echo "Test prompt deshabilitado" | ./.claude/hooks/user-prompt-submit 2>&1)
if [ $? -eq 0 ]; then
    print_result "Hook user-prompt-submit con TTS_PROMPT_ENABLED=false" "PASS"
else
    print_result "Hook user-prompt-submit con TTS_PROMPT_ENABLED=false" "FAIL"
fi

echo ""
echo "📋 Probando hooks CON AUDIO (esto reproducirá sonido)..."
echo ""
read -p "¿Quieres probar con audio? (s/n): " test_audio

if [[ "$test_audio" == "s" || "$test_audio" == "S" ]]; then

    # Test 10: Hook post-response con audio
    echo ""
    echo "Probando post-response (escucharás: 'Prueba de respuesta')..."
    sleep 1
    export TTS_ENABLED=true
    export TTS_VOICE=monica
    export TTS_RATE=175
    echo "Prueba de respuesta" | ./.claude/hooks/post-response
    sleep 3

    read -p "¿Se escuchó el audio correctamente? (s/n): " audio_ok
    if [[ "$audio_ok" == "s" || "$audio_ok" == "S" ]]; then
        print_result "Hook post-response con audio (Monica)" "PASS"
    else
        print_result "Hook post-response con audio (Monica)" "FAIL"
    fi

    # Test 11: Hook con voz Jorge
    echo ""
    echo "Probando con voz Jorge (escucharás: 'Prueba con voz masculina')..."
    sleep 1
    export TTS_VOICE=jorge
    echo "Prueba con voz masculina" | ./.claude/hooks/post-response
    sleep 3

    read -p "¿Se escuchó la voz Jorge? (s/n): " jorge_ok
    if [[ "$jorge_ok" == "s" || "$jorge_ok" == "S" ]]; then
        print_result "Hook post-response con voz Jorge" "PASS"
    else
        print_result "Hook post-response con voz Jorge" "FAIL"
    fi

    # Test 12: Hook con velocidad rápida
    echo ""
    echo "Probando velocidad rápida (250 WPM)..."
    sleep 1
    export TTS_VOICE=monica
    export TTS_RATE=250
    echo "Esta es una prueba de velocidad rápida a doscientas cincuenta palabras por minuto" | ./.claude/hooks/post-response
    sleep 3

    read -p "¿Se escuchó más rápido? (s/n): " fast_ok
    if [[ "$fast_ok" == "s" || "$fast_ok" == "S" ]]; then
        print_result "Hook con velocidad rápida (250 WPM)" "PASS"
    else
        print_result "Hook con velocidad rápida (250 WPM)" "FAIL"
    fi

    # Test 13: Hook user-prompt-submit con audio
    echo ""
    echo "Probando user-prompt-submit (escucharás: 'Procesando tu solicitud')..."
    sleep 1
    export TTS_PROMPT_ENABLED=true
    export TTS_PROMPT_VOICE=jorge
    export TTS_PROMPT_RATE=200
    echo "Esta es una pregunta del usuario" | ./.claude/hooks/user-prompt-submit
    sleep 3

    read -p "¿Se escuchó la confirmación? (s/n): " prompt_ok
    if [[ "$prompt_ok" == "s" || "$prompt_ok" == "S" ]]; then
        print_result "Hook user-prompt-submit con audio" "PASS"
    else
        print_result "Hook user-prompt-submit con audio" "FAIL"
    fi

    # Test 14: Filtrado de código
    echo ""
    echo "Probando filtrado de código (solo debe leer texto, no código)..."
    sleep 1
    export TTS_ENABLED=true
    export TTS_VOICE=monica
    export TTS_RATE=175

    TEST_WITH_CODE="Este es texto antes del código

\`\`\`python
def hello():
    print('esto no se debe leer')
\`\`\`

Este texto después del código sí se debe leer"

    echo "$TEST_WITH_CODE" | ./.claude/hooks/post-response
    sleep 4

    read -p "¿Solo se leyó el texto (NO el código Python)? (s/n): " filter_ok
    if [[ "$filter_ok" == "s" || "$filter_ok" == "S" ]]; then
        print_result "Filtrado de bloques de código" "PASS"
    else
        print_result "Filtrado de bloques de código" "FAIL"
    fi

    # Test 15: Truncado de texto largo
    echo ""
    echo "Probando truncado de texto largo (MAX_LENGTH=100)..."
    sleep 1
    export TTS_MAX_LENGTH=100

    LONG_TEXT="Este es un texto muy largo que debería ser truncado después de cien caracteres. Este texto adicional no debería ser leído porque excede el límite configurado de longitud máxima."

    echo "$LONG_TEXT" | ./.claude/hooks/post-response
    sleep 4

    read -p "¿Se truncó el texto (no se leyó todo)? (s/n): " truncate_ok
    if [[ "$truncate_ok" == "s" || "$truncate_ok" == "S" ]]; then
        print_result "Truncado de texto largo" "PASS"
    else
        print_result "Truncado de texto largo" "FAIL"
    fi

else
    echo "⏭️  Tests de audio omitidos (puedes ejecutarlos manualmente con ./demo.sh)"
fi

# Restaurar valores por defecto
unset TTS_ENABLED
unset TTS_VOICE
unset TTS_RATE
unset TTS_MAX_LENGTH
unset TTS_PROMPT_ENABLED
unset TTS_PROMPT_VOICE
unset TTS_PROMPT_RATE

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  📊 RESUMEN DE TESTS"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo -e "Total de tests: ${BLUE}$TESTS_TOTAL${NC}"
echo -e "Tests exitosos: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests fallidos: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ TODOS LOS TESTS PASARON${NC}"
    echo ""
    echo "🎉 Los hooks están funcionando correctamente!"
    echo ""
    echo "Para usar los hooks:"
    echo "  1. export TTS_ENABLED=true"
    echo "  2. claude-code"
else
    echo ""
    echo -e "${YELLOW}⚠️  ALGUNOS TESTS FALLARON${NC}"
    echo ""
    echo "Revisa los errores arriba para más detalles."
    echo ""
fi

echo "═══════════════════════════════════════════════════════════"

exit $TESTS_FAILED
