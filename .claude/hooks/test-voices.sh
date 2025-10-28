#!/bin/bash
# Test de todas las voces disponibles

echo "🎤 TEST DE VOCES EN ESPAÑOL"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Este test reproducirá todas las voces disponibles."
echo ""

# Obtener voces en español
VOCES=($(say -v ? | grep -i spanish | awk '{print $1}'))

if [ ${#VOCES[@]} -eq 0 ]; then
    echo "❌ No se encontraron voces en español instaladas"
    echo ""
    echo "Para instalar voces:"
    echo "  1. Abre Preferencias del Sistema"
    echo "  2. Ve a Accesibilidad → Contenido Hablado"
    echo "  3. Haz clic en 'Voces del Sistema'"
    echo "  4. Descarga voces en español"
    exit 1
fi

echo "Encontradas ${#VOCES[@]} voces en español:"
echo ""

# Listar voces
for voz in "${VOCES[@]}"; do
    info=$(say -v ? | grep "^$voz" | head -1)
    echo "  • $info"
done

echo ""
read -p "¿Quieres probar todas las voces? (s/n): " probar

if [[ "$probar" != "s" && "$probar" != "S" ]]; then
    exit 0
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "Probando voces..."
echo "═══════════════════════════════════════════════════"
echo ""

contador=1
for voz in "${VOCES[@]}"; do
    echo "[$contador/${#VOCES[@]}] Probando voz: $voz"

    # Texto de prueba
    texto="Hola, soy la voz $voz"

    # Reproducir
    say -v "$voz" -r 175 "$texto"

    sleep 1
    contador=$((contador + 1))
    echo ""
done

echo "═══════════════════════════════════════════════════"
echo "✅ Test de voces completado"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Voces recomendadas para los hooks:"
echo ""
echo "  monica   - Voz femenina clara (México)"
echo "  jorge    - Voz masculina profesional (España)"
echo "  paulina  - Voz femenina suave (México)"
echo ""
echo "Para configurar:"
echo "  export TTS_VOICE=monica"
echo ""
