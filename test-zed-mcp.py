#!/usr/bin/env python3
"""
Script de prueba para el servidor MCP de Zed
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path

# Agregar el path al script del servidor
sys.path.append(str(Path(__file__).parent))


async def test_server():
    """Probar el servidor MCP localmente"""
    print("🧪 Probando servidor MCP para Zed...")
    print("=" * 50)

    # Probar dependencias
    print("\n1. Verificando dependencias:")

    # Python
    try:
        result = subprocess.run(
            [sys.executable, "--version"], capture_output=True, text=True
        )
        print(f"✅ Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Python error: {e}")

    # TTS-macOS
    try:
        result = subprocess.run(["tts-macos", "--help"], capture_output=True, text=True)
        print(f"✅ TTS-macOS: instalado")
    except FileNotFoundError:
        print("❌ TTS-macOS: no encontrado")

    # MCP
    try:
        import mcp

        print(f"✅ MCP: {mcp.__version__}")
    except ImportError:
        print("❌ MCP: no instalado")

    # Probar funciones del servidor
    print("\n2. Probar funciones de TTS:")

    # Importar funciones del servidor
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import zed_mcp_server

        # Probar find_voice
        voice = zed_mcp_server.find_voice("monica")
        print(f"✅ find_voice('monica'): {voice}")

        # Probar speak_text
        success = zed_mcp_server.speak_text("Mensaje de prueba", voice=voice)
        print(f"✅ speak_text: {success}")

    except Exception as e:
        print(f"❌ Error al importar servidor: {e}")

    # Probar sintaxis del script
    print("\n3. Probar sintaxis del script del servidor:")
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "py_compile",
                str(Path(__file__).parent / "zed-mcp-server.py"),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ Sintaxis del servidor: correcta")
        else:
            print(f"❌ Sintaxis del servidor: {result.stderr}")

    except Exception as e:
        print(f"❌ Error al compilar servidor: {e}")

    # Verificar estructura del archivo de configuración
    print("\n4. Verificar estructura de configuración:")
    config_dir = Path.home() / ".zed"
    config_file = config_dir / "claude_desktop_config.json"

    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = json.load(f)

            if "mcpServers" in config:
                servers = config["mcpServers"]
                if "zed-tts-notifications" in servers:
                    print("✅ Servidor MCP de Zed configurado en Claude Desktop")
                    server_config = servers["zed-tts-notifications"]
                    print(f"   Comando: {server_config.get('command', 'N/A')}")
                    print(f"   Args: {server_config.get('args', 'N/A')}")
                else:
                    print("❌ Servidor MCP de Zed no encontrado en la configuración")
            else:
                print("❌ Sección 'mcpServers' no encontrada en la configuración")

        except json.JSONDecodeError:
            print("❌ Archivo de configuración JSON inválido")
        except Exception as e:
            print(f"❌ Error al leer configuración: {e}")
    else:
        print(f"⚠️  Archivo de configuración no encontrado: {config_file}")

    print("\n" + "=" * 50)
    print("🎉 Pruebas completadas!")
    print("\n📖 Siguientes pasos:")
    print("1. Ejecutar 'install-zed-mcp.sh' para instalar el servidor")
    print("2. Reiniciar Claude Desktop")
    print("3. Probar herramientas en Claude:")
    print("   - notify_file_save: {filename: 'test.py'}")
    print("   - notify_task_complete: {task: 'build', result: 'success'}")
    print("   - notify_startup: {project: 'mi-proyecto'}")


if __name__ == "__main__":
    asyncio.run(test_server())
