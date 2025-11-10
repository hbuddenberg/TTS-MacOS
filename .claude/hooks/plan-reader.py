#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plan Reader - Specialized hook for reading plans in Claude Code
Integrates with the notification system to read plans automatically
"""

import sys
import os
import subprocess
from pathlib import Path

# Add the hooks directory to the path
hooks_dir = Path(__file__).parent
sys.path.insert(0, str(hooks_dir))

try:
    from notification import es_plan, leer_plan
except ImportError:
    print("Error: No se puede importar el módulo notification", file=sys.stderr)
    sys.exit(1)

def main():
    """Main function - read plan from stdin or argument"""
    # Check if TTS is enabled
    if not os.getenv('TTS_ENABLED', '').lower() in ['true', '1', 'yes']:
        return

    # Get settings
    voice = os.getenv('TTS_PLAN_VOICE', os.getenv('TTS_VOICE', 'monica'))
    rate = int(os.getenv('TTS_PLAN_RATE', os.getenv('TTS_RATE', '175')))

    # Read plan text from stdin or argument
    if len(sys.argv) > 1:
        plan_text = ' '.join(sys.argv[1:])
    else:
        plan_text = sys.stdin.read()

    # Check if it's a plan and read it
    if es_plan(plan_text):
        leer_plan(plan_text, voice, rate)
    else:
        # If it's not a plan, just speak it normally
        from notification import speak_text
        speak_text(plan_text or "No se recibió texto", voice, rate)

if __name__ == '__main__':
    main()