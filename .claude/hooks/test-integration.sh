#!/bin/bash
# Test de integración completo - simula el uso real de Claude Code

echo "═══════════════════════════════════════════════════════════"
echo "  🔗 TEST DE INTEGRACIÓN - Simulación de Claude Code"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Este test simula una conversación completa con Claude Code"
echo "usando los hooks TTS-macOS."
echo ""

# Configuración
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=180
export TTS_MAX_LENGTH=500
export TTS_PROMPT_ENABLED=true
export TTS_PROMPT_VOICE=jorge
export TTS_PROMPT_RATE=200

echo "📋 Configuración:"
echo "  TTS_ENABLED: $TTS_ENABLED"
echo "  TTS_VOICE: $TTS_VOICE"
echo "  TTS_RATE: $TTS_RATE"
echo "  TTS_PROMPT_ENABLED: $TTS_PROMPT_ENABLED"
echo ""

read -p "Presiona Enter para comenzar el test de integración..."
clear

echo "═══════════════════════════════════════════════════════════"
echo "ESCENARIO 1: Pregunta simple"
echo "═══════════════════════════════════════════════════════════"
echo ""

USER_PROMPT="¿Qué es Python?"
CLAUDE_RESPONSE="Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Es conocido por su sintaxis clara y legible."

echo "👤 Usuario pregunta: \"$USER_PROMPT\""
echo ""
echo "Activando hook user-prompt-submit..."
echo "$USER_PROMPT" | ./.claude/hooks/user-prompt-submit
sleep 2

echo ""
echo "🤖 Claude responde: \"$CLAUDE_RESPONSE\""
echo ""
echo "Activando hook post-response..."
echo "$CLAUDE_RESPONSE" | ./.claude/hooks/post-response
sleep 5

echo ""
read -p "¿Se escucharon ambos audios? Presiona Enter para continuar..."
clear

echo "═══════════════════════════════════════════════════════════"
echo "ESCENARIO 2: Respuesta con código (debe filtrar código)"
echo "═══════════════════════════════════════════════════════════"
echo ""

USER_PROMPT="Muéstrame un ejemplo de función en Python"
CLAUDE_RESPONSE="Aquí tienes un ejemplo de función en Python:

\`\`\`python
def saludar(nombre):
    return f'Hola, {nombre}'

resultado = saludar('María')
print(resultado)
\`\`\`

Esta función recibe un nombre y retorna un saludo personalizado."

echo "👤 Usuario pregunta: \"$USER_PROMPT\""
echo ""
echo "Activando hook user-prompt-submit..."
echo "$USER_PROMPT" | ./.claude/hooks/user-prompt-submit
sleep 2

echo ""
echo "🤖 Claude responde con código:"
echo "$CLAUDE_RESPONSE"
echo ""
echo "Activando hook post-response (debe filtrar el código)..."
echo "$CLAUDE_RESPONSE" | ./.claude/hooks/post-response
sleep 5

echo ""
echo "⚠️  Nota: El código Python NO debería haberse leído en voz alta"
read -p "¿Solo se leyó el texto descriptivo? Presiona Enter para continuar..."
clear

echo "═══════════════════════════════════════════════════════════"
echo "ESCENARIO 3: Cambio de voz en tiempo real"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "Cambiando a voz Jorge (masculina, España)..."
export TTS_VOICE=jorge
export TTS_RATE=175

CLAUDE_RESPONSE="Ahora estoy hablando con voz Jorge, una voz masculina de España. ¿Notas la diferencia?"

echo "🤖 Claude responde: \"$CLAUDE_RESPONSE\""
echo ""
echo "Activando hook post-response con voz Jorge..."
echo "$CLAUDE_RESPONSE" | ./.claude/hooks/post-response
sleep 4

echo ""
read -p "¿Notaste el cambio de voz? Presiona Enter para continuar..."
clear

echo "═══════════════════════════════════════════════════════════"
echo "ESCENARIO 4: Velocidad rápida para respuestas cortas"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "Cambiando a velocidad rápida (250 WPM)..."
export TTS_VOICE=paulina
export TTS_RATE=250

CLAUDE_RESPONSE="Esta es una respuesta rápida y concisa."

echo "🤖 Claude responde: \"$CLAUDE_RESPONSE\""
echo ""
echo "Activando hook post-response a 250 WPM..."
echo "$CLAUDE_RESPONSE" | ./.claude/hooks/post-response
sleep 3

echo ""
read -p "¿Se escuchó más rápido? Presiona Enter para continuar..."
clear

echo "═══════════════════════════════════════════════════════════"
echo "ESCENARIO 5: Respuesta larga (debe truncarse)"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "Configurando límite corto (MAX_LENGTH=150)..."
export TTS_MAX_LENGTH=150
export TTS_VOICE=monica
export TTS_RATE=175

CLAUDE_RESPONSE="Esta es una respuesta muy larga que contiene mucha información. El sistema debería truncar este texto después de ciento cincuenta caracteres. Todo este texto adicional no debería ser leído en voz alta porque excede el límite configurado. Si escuchas esto, el truncado no está funcionando correctamente."

echo "🤖 Claude responde (texto largo):"
echo "\"$CLAUDE_RESPONSE\""
echo ""
echo "Activando hook post-response (debe truncar después de 150 chars)..."
echo "$CLAUDE_RESPONSE" | ./.claude/hooks/post-response
sleep 5

echo ""
echo "⚠️  Nota: El texto debería haberse cortado después de ~150 caracteres"
read -p "¿Se truncó el texto? Presiona Enter para continuar..."
clear

echo "═══════════════════════════════════════════════════════════"
echo "ESCENARIO 6: Deshabilitando TTS en tiempo real"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "Deshabilitando TTS..."
export TTS_ENABLED=false

CLAUDE_RESPONSE="Este texto NO debería ser leído en voz alta porque el TTS está deshabilitado."

echo "🤖 Claude responde: \"$CLAUDE_RESPONSE\""
echo ""
echo "Activando hook post-response (con TTS_ENABLED=false)..."
echo "$CLAUDE_RESPONSE" | ./.claude/hooks/post-response
sleep 2

echo ""
echo "✅ Si NO escuchaste nada, el test pasó correctamente"
read -p "¿NO se escuchó audio? Presiona Enter para continuar..."
clear

echo "═══════════════════════════════════════════════════════════"
echo "ESCENARIO 7: Múltiples intercambios rápidos"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "Simulando conversación rápida (3 intercambios)..."
echo ""

# Restaurar TTS
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=200
export TTS_MAX_LENGTH=500

# Intercambio 1
echo "👤 Usuario: ¿Cuánto es dos más dos?"
echo "🤖 Procesando..." | ./.claude/hooks/user-prompt-submit
sleep 1
echo "🤖 Claude: La respuesta es cuatro"
echo "La respuesta es cuatro" | ./.claude/hooks/post-response
sleep 2

# Intercambio 2
echo ""
echo "👤 Usuario: ¿Y cinco por cinco?"
echo "🤖 Procesando..." | ./.claude/hooks/user-prompt-submit
sleep 1
echo "🤖 Claude: Veinticinco"
echo "Veinticinco" | ./.claude/hooks/post-response
sleep 2

# Intercambio 3
echo ""
echo "👤 Usuario: Gracias"
echo "🤖 Procesando..." | ./.claude/hooks/user-prompt-submit
sleep 1
echo "🤖 Claude: De nada, estoy aquí para ayudarte"
echo "De nada, estoy aquí para ayudarte" | ./.claude/hooks/post-response
sleep 3

echo ""
read -p "¿Se escucharon los 3 intercambios? Presiona Enter para continuar..."
clear

echo "═══════════════════════════════════════════════════════════"
echo "  ✅ TEST DE INTEGRACIÓN COMPLETADO"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Escenarios probados:"
echo "  ✓ Pregunta simple con respuesta"
echo "  ✓ Filtrado de código"
echo "  ✓ Cambio de voz dinámico"
echo "  ✓ Velocidad rápida"
echo "  ✓ Truncado de texto largo"
echo "  ✓ Deshabilitar TTS"
echo "  ✓ Múltiples intercambios"
echo ""
echo "Los hooks están listos para usarse con Claude Code."
echo ""
echo "Para activarlos en Claude Code:"
echo "  export TTS_ENABLED=true"
echo "  export TTS_VOICE=monica"
echo "  claude-code"
echo ""
echo "═══════════════════════════════════════════════════════════"

# Limpiar variables
unset TTS_ENABLED
unset TTS_VOICE
unset TTS_RATE
unset TTS_MAX_LENGTH
unset TTS_PROMPT_ENABLED
unset TTS_PROMPT_VOICE
unset TTS_PROMPT_RATE
