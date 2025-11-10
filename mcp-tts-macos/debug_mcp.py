#!/usr/bin/env python3
"""
Script para depurar el servidor MCP y verificar los métodos registrados
"""

import asyncio
import json
import subprocess
import sys

from server import app


async def test_mcp_protocol():
    """Prueba el protocolo MCP manualmente"""
    print("🔍 Probando servidor MCP...")

    # 1. Verificar herramientas disponibles
    print("\n1. Herramientas registradas:")
    list_tools_func = app.list_tools()
    tools = await list_tools_func()
    for tool in tools:
        print(f"   - {tool.name}: {tool.description[:50]}...")

    # 2. Probar llamada directa a herramienta
    print("\n2. Probando llamada directa:")
    try:
        result = await app.call_tool(
            "speak_text", {"text": "Test de voz", "voice": "monica"}
        )
        print(f"   ✅ Resultado: {result.content[0].text[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # 3. Simular mensaje JSON-RPC
    print("\n3. Simulando mensaje JSON-RPC:")
    json_rpc_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "speak_text",
            "arguments": {"text": "Test JSON-RPC", "voice": "monica"},
        },
    }

    print(f"   Mensaje: {json.dumps(json_rpc_message, indent=2)}")

    # 4. Verificar si el servidor tiene el método registrado
    print("\n4. Verificando registros internos:")
    if hasattr(app, "_tool_handlers"):
        print(f"   Handlers registrados: {list(app._tool_handlers.keys())}")
    else:
        print("   No se encontró _tool_handlers")

    if hasattr(app, "request_handlers"):
        print(f"   Request handlers: {list(app.request_handlers.keys())}")
    else:
        print("   No se encontró request_handlers")


if __name__ == "__main__":
    asyncio.run(test_mcp_protocol())
