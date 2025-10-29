#!/bin/bash
# Verificación final del sistema TTS-macOS

echo "═══════════════════════════════════════════════════════════"
echo "  ✅ VERIFICACIÓN FINAL DEL SISTEMA TTS-MACOS"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Contadores
OK=0
WARN=0
FAIL=0

check() {
    local description="$1"
    local command="$2"
    
    echo -n "Verificando: $description... "
    
    if eval "$command" &>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        OK=$((OK + 1))
    else
        echo -e "${RED}✗${NC}"
        FAIL=$((FAIL + 1))
    fi
}

check_warn() {
    local description="$1"
    local command="$2"
    
    echo -n "Verificando: $description... "
    
    if eval "$command" &>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        OK=$((OK + 1))
    else
        echo -e "${YELLOW}⚠${NC}"
        WARN=$((WARN + 1))
    fi
}

echo "📋 Archivos del sistema"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check "Hook post-response" "[ -f .claude/hooks/post-response ]"
check "Hook user-prompt-submit" "[ -f .claude/hooks/user-prompt-submit ]"
check "Script enable-tts.sh" "[ -f .claude/hooks/enable-tts.sh ]"
check "Script list-all-voices.sh" "[ -f .claude/hooks/list-all-voices.sh ]"
check "Script demo.sh" "[ -f .claude/hooks/demo.sh ]"
echo ""

echo "📋 Permisos de ejecución"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check "post-response ejecutable" "[ -x .claude/hooks/post-response ]"
check "user-prompt-submit ejecutable" "[ -x .claude/hooks/user-prompt-submit ]"
check "enable-tts.sh ejecutable" "[ -x .claude/hooks/enable-tts.sh ]"
check "demo.sh ejecutable" "[ -x .claude/hooks/demo.sh ]"
echo ""

echo "📋 Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check "test-quick.sh" "[ -x .claude/hooks/test-quick.sh ]"
check "test-hooks.sh" "[ -x .claude/hooks/test-hooks.sh ]"
check "test-integration.sh" "[ -x .claude/hooks/test-integration.sh ]"
check "test-voices.sh" "[ -x .claude/hooks/test-voices.sh ]"
check "test-siri-voices.sh" "[ -x .claude/hooks/test-siri-voices.sh ]"
echo ""

echo "📋 Documentación"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check "README.md" "[ -f .claude/hooks/README.md ]"
check "INICIO-RAPIDO.md" "[ -f .claude/hooks/INICIO-RAPIDO.md ]"
check "EJEMPLOS.md" "[ -f .claude/hooks/EJEMPLOS.md ]"
check "VOCES-SIRI.md" "[ -f .claude/hooks/VOCES-SIRI.md ]"
check "ACTUALIZACION-VOCES.md" "[ -f .claude/hooks/ACTUALIZACION-VOCES.md ]"
check "RUN-TESTS.md" "[ -f .claude/hooks/RUN-TESTS.md ]"
check "RESUMEN-FINAL.md" "[ -f .claude/hooks/RESUMEN-FINAL.md ]"
echo ""

echo "📋 Sistema macOS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check "Comando 'say' disponible" "command -v say"
check_warn "Comando 'tts-macos' instalado" "command -v tts-macos"
echo ""

echo "📋 Voces del sistema"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SPANISH_COUNT=$(say -v \? 2>/dev/null | grep -iE "(spanish|español)" | wc -l | tr -d ' ')
ENHANCED_COUNT=$(say -v \? 2>/dev/null | grep -iE "(enhanced|premium)" | wc -l | tr -d ' ')
SIRI_COUNT=$(say -v \? 2>/dev/null | grep -i "siri" | wc -l | tr -d ' ')
TOTAL_COUNT=$(say -v \? 2>/dev/null | wc -l | tr -d ' ')

echo "  Voces en español: $SPANISH_COUNT"
echo "  Voces Enhanced/Premium: $ENHANCED_COUNT"
echo "  Voces de Siri: $SIRI_COUNT"
echo "  Total de voces: $TOTAL_COUNT"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "  📊 RESULTADO"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}✓ Verificaciones exitosas: $OK${NC}"
if [ $WARN -gt 0 ]; then
    echo -e "${YELLOW}⚠ Advertencias: $WARN${NC}"
fi
if [ $FAIL -gt 0 ]; then
    echo -e "${RED}✗ Verificaciones fallidas: $FAIL${NC}"
fi
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ SISTEMA COMPLETAMENTE FUNCIONAL${NC}"
    echo ""
    echo "Siguiente paso:"
    echo "  export TTS_ENABLED=true"
    echo "  claude-code"
else
    echo -e "${RED}❌ HAY PROBLEMAS QUE RESOLVER${NC}"
    echo ""
    echo "Revisa los errores arriba y consulta:"
    echo "  .claude/hooks/README.md"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
