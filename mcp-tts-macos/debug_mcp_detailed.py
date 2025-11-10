#!/usr/bin/env python3
"""
Script de depuración MCP para identificar el problema real
"""

import asyncio
import json
import os
import sys

# Asegurar directorio correcto
os.chdir("/Volumes/Resources/Develop/TTS-MacOS/mcp-tts-macos")
sys.path.insert(0, os.getcwd())

from server import mcp


async def debug_mcp():
    """Depurar el servidor MCP paso a paso"""
    print("🔍 **DEPURACIÓN COMPLETA DEL SERVIDOR MCP**")
    print("=" * 60)

    # 1. Verificar información del servidor
    print(f"\n1. 📊 Información del servidor:")
    print(f"   Tipo: {type(mcp)}")
    print(f"   Nombre: {mcp.name}")

    # 2. Listar herramientas disponibles
    print(f"\n2. 🔧 Listando herramientas (list_tools):")
    try:
        tools = await mcp.list_tools()
        print(f"   ✅ Herramientas encontradas: {len(tools)}")

        for i, tool in enumerate(tools):
            print(f"\n   --- Herramienta {i + 1}: {tool.name} ---")
            print(f"   Descripción: {tool.description}")

            # Verificar el schema
            if hasattr(tool, "inputSchema") and tool.inputSchema:
                schema = tool.inputSchema
                print(f"   Schema Type: {schema.get('type')}")
                print(f"   Required: {schema.get('required', [])}")
                print(f"   Properties: {list(schema.get('properties', {}).keys())}")

                # Si es speak_text, mostrar detalles
                if tool.name == "speak_text":
                    print(f"   🔍 **ANÁLISIS DE speak_text**:")
                    props = schema.get("properties", {})
                    for prop_name, prop_def in props.items():
                        print(
                            f"     - {prop_name}: {prop_def.get('type', 'unknown')} (default: {prop_def.get('default', 'none')})"
                        )

                    # Verificar si 'filename' está en required
                    required = schema.get("required", [])
                    if "filename" in required:
                        print(
                            f"   ⚠️ **ERROR GRAVE**: 'filename' está en required para speak_text!"
                        )
                    else:
                        print(f"   ✅ 'filename' NO está en required")
            else:
                print(f"   ⚠️ Sin inputSchema")
    except Exception as e:
        print(f"   ❌ Error listando herramientas: {e}")
        import traceback

        traceback.print_exc()

    # 3. Probar llamada directa a speak_text
    print(f"\n3. 🎤 Probando llamada directa a speak_text:")
    try:
        result = await mcp.call_tool("speak_text", {"text": "test", "voice": "monica"})
        print(f"   ✅ Llamada exitosa")
        print(f"   Resultado: {result}")
    except Exception as e:
        print(f"   ❌ Error en llamada: {e}")
        print(f"   Tipo de error: {type(e)}")
        if hasattr(e, "__dict__"):
            print(f"   Detalles: {e.__dict__}")

    # 4. Verificar qué herramienta está causando el error
    print(f"\n4. 🔍 Verificando save_audio (que sí requiere filename):")
    try:
        tools = await mcp.list_tools()
        for tool in tools:
            if tool.name == "save_audio":
                schema = tool.inputSchema
                required = schema.get("required", [])
                print(f"   save_audio requires: {required}")
                if "filename" in required:
                    print(f"   ✅ save_audio correctamente requiere 'filename'")
                break
    except Exception as e:
        print(f"   ❌ Error verificando save_audio: {e}")

    print(f"\n" + "=" * 60)
    print("🎯 **DIAGNÓSTICO COMPLETADO**")


if __name__ == "__main__":
    asyncio.run(debug_mcp())
