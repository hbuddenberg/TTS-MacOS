#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced notification hook for Claude Code TTS integration.
Provides spoken notifications and plan reading capabilities.
"""

import os
import sys
import subprocess
import argparse
import re
import time
from pathlib import Path

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='TTS Notification Hook')
    parser.add_argument('--event', type=str, help='Event type (start, complete, error)')
    parser.add_argument('--message', type=str, help='Message to speak')
    parser.add_argument('--voice', type=str, default=os.getenv('TTS_VOICE', 'monica'), help='Voice to use')
    parser.add_argument('--rate', type=int, default=int(os.getenv('TTS_RATE', '175')), help='Speech rate')
    parser.add_argument('--leer-plan', type=str, help='Read a plan text')
    parser.add_argument('--accion-req', type=str, help='Announce required action')
    parser.add_argument('--implementacion-completada', type=str, help='Announce implementation completion')
    parser.add_argument('--plan-finalizado', type=str, help='Announce plan execution completed')
    parser.add_argument('--stdin', action='store_true', help='Read text from stdin')
    return parser.parse_args()

def speak_text(text: str, voice: str = 'monica', rate: int = 175, pause: float = 0.0):
    """Speak text using macOS say command"""
    try:
        if pause > 0:
            time.sleep(pause)
        cmd = ['say', '-v', voice, '-r', str(rate), text]
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error speaking text: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

def es_plan(texto: str) -> bool:
    """Detect if text contains a plan structure"""
    if not texto:
        return False

    # Buscar indicadores de plan en markdown
    plan_indicators = [
        r'^#\s*.*[Pp]lan',  # # Plan, # Plan de limpieza, etc.
        r'^##\s*[Oo]bjetivo',  # ## Objetivo
        r'^##\s*[Ii]mplementaci',  # ## Implementación
        r'^##\s*[Aa]cciones',  # ## Acciones
        r'^##\s*[Tt]areas',  # ## Tareas
        r'^##\s*[Pp]asos',  # ## Pasos
        r'^\*\s*.*\[\s*\]',  # Listas con checkbox []
        r'^\*\s*.*\[\s*x\s*\]',  # Listas con checkbox completados [x]
        r'^- \*\*.*\*\*:.*',  # - **Objetivo**: texto
        r'## [Pp]lan|## [Ll]impieza|## [Ii]mplementaci'  # Encabezados específicos
    ]

    texto_lower = texto.lower()
    for pattern in plan_indicators:
        if re.search(pattern, texto, re.MULTILINE | re.IGNORECASE):
            return True

    # Buscar palabras clave de planificación
    plan_keywords = [
        'objetivo', 'implementar', 'limpieza', 'archivos', 'eliminar',
        'acciones', 'tareas', 'pasos', 'impacto', 'riesgo', 'consideraciones'
    ]

    keyword_count = sum(1 for keyword in plan_keywords if keyword in texto_lower)
    return keyword_count >= 3  # Si hay 3+ palabras clave, es probablemente un plan

def detectar_acciones_requeridas(texto: str) -> list:
    """Detect sections where user action is required"""
    if not texto:
        return []

    acciones = []

    # Patrones de acción requerida
    action_patterns = [
        r'(confirma|confirmar|aprobar|proceder|continuar|ejecutar).*?[\.\!\?]',
        r'necesito.*?(confirmaci|aprobaci|intervenci|decisi)',
        r'espero.*?(respuesta|confirmaci|aprobaci)',
        r'por favor.*?(confirma|revisa|verifica)',
        r'estas.*?(de acuerdo|listo|seguro)',
        r'quiere.*?(continuar|proceder|ejecutar)',
        r'[\.\?]\s*(debo|puedo).*?\?',
        r'[¡]\s*(importante|cuidado|atenci)',
        r'(warning|cuidado|precauci)',
        r'[Aa]ntes de.*:(.*?)(?=\n|$)'
    ]

    for pattern in action_patterns:
        matches = re.findall(pattern, texto, re.IGNORECASE | re.MULTILINE)
        acciones.extend(matches)

    # Buscar secciones específicas que requieren acción
    if re.search(r'##\s*[Pp]recauciones|##\s*[Aa]ntes de|##\s*[Nn]ecesario', texto, re.IGNORECASE):
        acciones.append("sección de precauciones")

    if re.search(r'##\s*[Cc]onfirmaci|##\s*[Aa]probaci', texto, re.IGNORECASE):
        acciones.append("sección de confirmación")

    return acciones

def leer_plan(texto: str, voice: str = 'monica', rate: int = 175):
    """Read a plan with appropriate pauses and emphasis"""
    lines = texto.split('\n')
    acciones_req = detectar_acciones_requeridas(texto)

    # Anunciar que se va a leer un plan
    speak_text("Plan detectado. Leyendo contenido.", voice, rate, 0.5)

    current_section = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Identificar secciones principales
        if line.startswith('#'):
            speak_text(f"Sección: {line.replace('#', '').strip()}", voice, rate, 0.3)
            current_section = line.lower()
        elif line.startswith('##'):
            speak_text(f"Subsección: {line.replace('##', '').strip()}", voice, rate, 0.2)
            current_section = line.lower()
        elif line.startswith('*') or line.startswith('-'):
            # Leer elementos de lista
            item = re.sub(r'^[\*\-\+]\s*', '', line)
            # Limpiar formato markdown
            item = re.sub(r'\*\*(.*?)\*\*', r'\1', item)
            item = re.sub(r'\[(x|\s)\]', '', item).strip()
            if item:
                speak_text(item, voice, rate)
        elif len(line) > 10:  # Evitar leer líneas muy cortas
            speak_text(line, voice, rate)

    # Anunciar acciones requeridas
    if acciones_req:
        speak_text("Atención: Se requiere tu intervención en los siguientes puntos:", voice, rate, 1.0)
        for i, accion in enumerate(acciones_req, 1):
            speak_text(f"Acción {i}: {accion}", voice, rate, 0.5)
        speak_text("Por favor, confirma si deseas proceder con la ejecución.", voice, rate, 1.0)
    else:
        speak_text("Plan completado. Esperando tu confirmación para proceder.", voice, rate, 0.5)

def anunciar_implementacion_completada(plan_nombre: str = "", detalles: str = "", voice: str = 'monica', rate: int = 175):
    """Announce that implementation has been completed"""
    speak_text("¡Implementación completada con éxito!", voice, rate, 0.5)

    if plan_nombre:
        speak_text(f"El plan {plan_nombre} ha sido implementado completamente.", voice, rate, 0.3)

    if detalles:
        speak_text(detalles, voice, rate, 0.3)

    speak_text("Todas las tareas han sido ejecutadas y el sistema está listo para su uso.", voice, rate, 0.5)
    speak_text("¿Hay algo más en lo que pueda ayudarte?", voice, rate, 0.3)

def anunciar_plan_finalizado(plan_nombre: str = "", resumen: str = "", voice: str = 'monica', rate: int = 175):
    """Announce that plan execution has been completed"""
    speak_text("¡Plan ejecutado completamente!", voice, rate, 0.5)

    if plan_nombre:
        speak_text(f"El plan {plan_nombre} ha finalizado su ejecución.", voice, rate, 0.3)

    if resumen:
        speak_text("Resumen de acciones completadas:", voice, rate, 0.3)
        speak_text(resumen, voice, rate, 0.2)

    speak_text("Todos los objetivos del plan han sido alcanzados.", voice, rate, 0.5)
    speak_text("El sistema ha sido actualizado correctamente.", voice, rate, 0.3)

def main():
    """Main hook function"""
    args = parse_arguments()

    # Check if TTS is enabled
    if not os.getenv('TTS_ENABLED', '').lower() in ['true', '1', 'yes']:
        return

    # Get voice and rate settings (check for plan-specific settings)
    voice = os.getenv('TTS_PLAN_VOICE', args.voice)
    plan_rate = int(os.getenv('TTS_PLAN_RATE', str(args.rate)))

    # Handle plan reading
    if args.leer_plan:
        if es_plan(args.leer_plan):
            leer_plan(args.leer_plan, voice, plan_rate)
        else:
            speak_text("El texto proporcionado no parece ser un plan.", voice, args.rate)
        return

    # Handle required action announcement
    if args.accion_req:
        speak_text("Atención: Acción requerida.", voice, args.rate, 0.5)
        speak_text(args.accion_req, voice, args.rate, 0.3)
        speak_text("Por favor, proporciona tu confirmación.", voice, args.rate, 0.5)
        return

    # Handle implementation completion announcement
    if args.implementacion_completada:
        # Check if there are additional details after a colon
        if ':' in args.implementacion_completada:
            plan_name, detalles = args.implementacion_completada.split(':', 1)
            anunciar_implementacion_completada(plan_name.strip(), detalles.strip(), voice, plan_rate)
        else:
            anunciar_implementacion_completada(args.implementacion_completada, "", voice, plan_rate)
        return

    # Handle plan completion announcement
    if args.plan_finalizado:
        # Check if there are additional details after a colon
        if ':' in args.plan_finalizado:
            plan_name, resumen = args.plan_finalizado.split(':', 1)
            anunciar_plan_finalizado(plan_name.strip(), resumen.strip(), voice, plan_rate)
        else:
            anunciar_plan_finalizado(args.plan_finalizado, "", voice, plan_rate)
        return

    # Handle stdin input
    if args.stdin:
        try:
            text = sys.stdin.read()
            if es_plan(text):
                leer_plan(text, voice, plan_rate)
            else:
                speak_text(text or "No se recibió texto", voice, args.rate)
        except Exception as e:
            speak_text(f"Error leyendo entrada: {e}", voice, args.rate)
        return

    # Default messages based on event type
    if args.event:
        if args.event == 'start':
            message = args.message or "Iniciando tarea"
        elif args.event == 'complete':
            message = args.message or "Tarea completada"
        elif args.event == 'error':
            message = args.message or "Error en la tarea"
        else:
            message = args.message or "Notificación"
    else:
        message = args.message or "Notificación del sistema"

    # Speak the notification
    speak_text(message, args.voice, args.rate)

if __name__ == '__main__':
    main()