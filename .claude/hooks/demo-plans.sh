#!/bin/bash
# Demo script for TTS Plan Reading System

echo "🎯 Demostración del Sistema de Lectura de Planes TTS"
echo "================================================"

# Ensure TTS is enabled
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=175

echo "1. Probando detección de plan básico..."
python3 "$(dirname "$0")/notification.py" --leer-plan "# Plan simple
## Objetivo
Testear el sistema

## Acciones
- Probar notificaciones
- Verificar detección
- Confirmar funcionamiento

Por favor, confirma si deseas continuar."

echo ""
echo "2. Probando anuncio de acción requerida..."
python3 "$(dirname "$0")/notification.py" --accion-req "Se requiere tu aprobación para eliminar archivos"

echo ""
echo "3. Probando lectura desde stdin..."
echo "# Plan desde stdin
## Tarea
Verificar lectura desde entrada estándar

## Pasos
- Enviar texto por stdin
- Detectar automáticamente
- Leer en voz alta

¿Estás listo para proceder?" | python3 "$(dirname "$0")/notification.py" --stdin

echo ""
echo "4. Probando con texto que no es un plan..."
python3 "$(dirname "$0")/notification.py" --leer-plan "Este es un mensaje normal que no es un plan."

echo ""
echo "5. Probando anuncio de implementación completada..."
python3 "$(dirname "$0")/notification.py" --implementacion-completada "Sistema de Notificaciones TTS:Se han agregado funciones de lectura de planes y detección de acciones requeridas"

echo ""
echo "6. Probando anuncio de plan finalizado..."
python3 "$(dirname "$0")/notification.py" --plan-finalizado "Limpieza de Archivos:Se eliminaron 8 archivos redundantes, se consolidó la documentación y se mejoró la estructura del proyecto"

echo ""
echo "✅ Demostración completada!"
echo "El sistema está listo para:"
echo "- Leer planes automáticamente"
echo "- Anunciar cuando se requiere tu intervención"
echo "- Anunciar cuando la implementación se ha completado"
echo "- Anunciar cuando los planes han finalizado su ejecución"