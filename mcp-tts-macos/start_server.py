#!/usr/bin/env python3
"""
Script de inicio robusto para el servidor MCP TTS-macOS
Este script asegura que el PYTHONPATH esté configurado correctamente
"""

import os
import sys

# Asegurar PYTHONPATH correcto
server_dir = "/Volumes/Resources/Develop/TTS-MacOS/mcp-tts-macos"
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

# Cambiar al directorio del servidor
os.chdir(server_dir)

# Importar y ejecutar el servidor
try:
    import server

    print(f"🚀 Iniciando servidor MCP TTS-macOS desde {server_dir}")
    server.mcp.run()
except ImportError as e:
    print(f"❌ Error importando servidor: {e}")
    print(f"PYTHONPATH: {sys.path}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error iniciando servidor: {e}")
    sys.exit(1)
