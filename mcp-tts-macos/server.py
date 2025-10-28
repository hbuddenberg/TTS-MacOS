#!/usr/bin/env python3
"""
Servidor MCP para Text-to-Speech usando el TTS nativo de macOS
"""
import asyncio
import subprocess
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Crear instancia del servidor
app = Server("mcp-tts-macos")

# Voces disponibles en español para macOS
VOCES_ESPANOL = {
    "monica": "Monica (Español Mexicano - Mujer)",
    "paulina": "Paulina (Español Mexicano - Mujer)",
    "jorge": "Jorge (Español España - Hombre)",
    "juan": "Juan (Español España - Hombre)",
    "diego": "Diego (Español Argentino - Hombre)",
    "angelica": "Angelica (Español México - Mujer)"
}

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Lista las herramientas disponibles en el servidor MCP
    """
    return [
        Tool(
            name="speak_text",
            description="Convierte texto a voz y lo reproduce usando el TTS nativo de macOS. Ideal para escuchar respuestas del asistente de IA.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "El texto que deseas convertir a audio"
                    },
                    "voice": {
                        "type": "string",
                        "description": f"Voz a utilizar. Opciones: {', '.join(VOCES_ESPANOL.keys())}",
                        "enum": list(VOCES_ESPANOL.keys()),
                        "default": "monica"
                    },
                    "rate": {
                        "type": "integer",
                        "description": "Velocidad de lectura en palabras por minuto (100-300). Default: 175",
                        "default": 175,
                        "minimum": 100,
                        "maximum": 300
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="list_voices",
            description="Lista todas las voces en español disponibles en el sistema macOS",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="save_audio",
            description="Convierte texto a voz y lo guarda como archivo de audio (AIFF)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "El texto a convertir"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Nombre del archivo (sin extensión)"
                    },
                    "voice": {
                        "type": "string",
                        "description": "Voz a utilizar",
                        "enum": list(VOCES_ESPANOL.keys()),
                        "default": "monica"
                    }
                },
                "required": ["text", "filename"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Ejecuta la herramienta solicitada
    """
    try:
        if name == "speak_text":
            return await speak_text(arguments)
        elif name == "list_voices":
            return await list_voices()
        elif name == "save_audio":
            return await save_audio(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"Herramienta desconocida: {name}"
            )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error al ejecutar {name}: {str(e)}"
        )]

async def speak_text(arguments: dict) -> list[TextContent]:
    """
    Reproduce el texto usando TTS de macOS
    """
    text = arguments["text"]
    voice = arguments.get("voice", "monica").capitalize()
    rate = arguments.get("rate", 175)
    
    # Construir comando
    cmd = ["say", "-v", voice, "-r", str(rate), text]
    
    # Ejecutar de forma asíncrona
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    if process.returncode == 0:
        return [TextContent(
            type="text",
            text=f"✅ Audio reproducido exitosamente\nVoz: {VOCES_ESPANOL.get(voice.lower(), voice)}\nVelocidad: {rate} palabras/min"
        )]
    else:
        error_msg = stderr.decode() if stderr else "Error desconocido"
        return [TextContent(
            type="text",
            text=f"❌ Error al reproducir audio: {error_msg}"
        )]

async def list_voices() -> list[TextContent]:
    """
    Lista las voces en español disponibles
    """
    voices_info = "🎤 **Voces en Español Disponibles:**\n\n"
    for key, description in VOCES_ESPANOL.items():
        voices_info += f"• **{key}**: {description}\n"
    
    voices_info += "\n💡 **Uso:** Usa el parámetro 'voice' con uno de estos nombres en minúsculas."
    
    return [TextContent(
        type="text",
        text=voices_info
    )]

async def save_audio(arguments: dict) -> list[TextContent]:
    """
    Guarda el texto como archivo de audio
    """
    text = arguments["text"]
    filename = arguments["filename"]
    voice = arguments.get("voice", "monica").capitalize()
    
    # Asegurar extensión .aiff
    if not filename.endswith(".aiff"):
        filename += ".aiff"
    
    # Ruta completa (guardar en el directorio home del usuario)
    output_path = f"/Users/{subprocess.getoutput('whoami')}/Desktop/{filename}"
    
    # Comando para guardar
    cmd = ["say", "-v", voice, "-o", output_path, text]
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    if process.returncode == 0:
        return [TextContent(
            type="text",
            text=f"✅ Audio guardado exitosamente en:\n{output_path}"
        )]
    else:
        error_msg = stderr.decode() if stderr else "Error desconocido"
        return [TextContent(
            type="text",
            text=f"❌ Error al guardar audio: {error_msg}"
        )]

async def main():
    """
    Punto de entrada principal del servidor
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
