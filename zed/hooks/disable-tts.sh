#!/bin/bash
# Deshabilitar TTS para Zed

echo "🔇 Deshabilitando TTS para Zed"
echo "=================================="

# Deshabilitar el TTS
unset ZED_TTS_ENABLED
export ZED_TTS_ENABLED="false"

# Deshabilitar específicos para tareas complejas
unset ZED_TTS_TASK_VOICE
unset ZED_TTS_TASK_RATE

echo "✅ TTS deshabilitado para Zed"

echo ""
echo "Si quieres volver a habilitarlo:"
echo "  export ZED_TTS_ENABLED=true"
echo ""
echo "O usa el script de configuración:"
echo "  $PWD/enable-tts.sh"

echo ""
echo "📖 Documentación completa en: $PWD/zed/README.md"
