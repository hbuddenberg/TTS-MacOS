#!/usr/bin/env python3
"""
Servidor MCP para Zed con notificaciones TTS
Integra hooks de TTS con el protocolo de Modelo de Comunicación de Claude (MCP)
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import mcp
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    InitializeRequest,
    InitializeResult,
    ListToolsRequest,
    ListToolsResult,
    Resource,
    ServerCapabilities,
    TextContent,
    Tool,
)

# Crear instancia del servidor
server = Server("zed-tts-notifications")

# Configuración predeterminada
DEFAULT_CONFIG = {
    "voice": "monica",
    "rate": 175,
    "task_voice": "jorge",
    "task_rate": 180,
    "max_length": 100,
    "startup_announce": True,
}


def find_voice(voice_query: str) -> str:
    """Buscar una voz disponible en el sistema"""
    try:
        # Búsqueda exacta primero (case-insensitive)
        result = subprocess.run(
            ["say", "-v", "?"], capture_output=True, text=True, check=True
        )

        # Búsqueda exacta
        for line in result.stdout.split("\n"):
            if line.lower().startswith(f"{voice_query.lower()} "):
                return line.split()[0]

        # Búsqueda parcial
        for line in result.stdout.split("\n"):
            if voice_query.lower() in line.lower():
                return line.split()[0]

        # Buscar voz en español
        for line in result.stdout.split("\n"):
            if any(spanish in line.lower() for spanish in ["spanish", "español"]):
                return line.split()[0]

        # Fallback
        return "Monica"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Monica"


def speak_text(text: str, voice: str = None, rate: int = None) -> bool:
    """Reproducir texto usando TTS"""
    try:
        # Obtener configuración
        if voice is None:
            voice = os.getenv("ZED_TTS_VOICE", DEFAULT_CONFIG["voice"])
        if rate is None:
            rate = int(os.getenv("ZED_TTS_RATE", DEFAULT_CONFIG["rate"]))

        # Buscar voz disponible
        voice_name = find_voice(voice)

        # Usar TTS-macOS CLI si está disponible
        if subprocess.run(["which", "tts-macos"], capture_output=True).returncode == 0:
            cmd = [
                "tts-macos",
                text,
                "--voice",
                voice_name.lower(),
                "--rate",
                str(rate),
            ]
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True

        # Fallback con say
        subprocess.Popen(["say", "-v", voice_name, "-r", str(rate), text])
        return True

    except Exception:
        return False


@server.call_tool()
async def notify_file_save(arguments: Dict[str, Any]) -> CallToolResult:
    """
    Notificar cuando un archivo se guarda

    Args:
        filename: Nombre del archivo guardado
        file_type: Tipo de archivo (opcional)
        success: Si el guardado fue exitoso (opcional, default: true)
    """
    filename = arguments.get("filename", "archivo")
    file_type = arguments.get("file_type", "")
    success = arguments.get("success", True)

    if success:
        if file_type:
            message = f"Archivo {file_type} guardado: {filename}"
        else:
            # Detectar tipo de archivo por extensión
            ext = Path(filename).suffix.lower()
            type_map = {
                ".py": "Python",
                ".js": "JavaScript",
                ".ts": "TypeScript",
                ".jsx": "React",
                ".tsx": "React TypeScript",
                ".md": "Markdown",
                ".json": "JSON",
                ".html": "HTML",
                ".css": "CSS",
                ".sh": "Script",
                ".bash": "Script",
                ".zsh": "Script",
                ".txt": "Texto",
            }
            file_type_name = type_map.get(ext, "archivo")
            message = f"Archivo {file_type_name} guardado: {filename}"
    else:
        message = f"Error al guardar: {filename}"

    speak_text(message)
    return CallToolResult(
        content=[TextContent(type="text", text=f"Notificación enviada: {message}")]
    )


@server.call_tool()
async def notify_task_complete(arguments: Dict[str, Any]) -> CallToolResult:
    """
    Notificar cuando una tarea se completa

    Args:
        task: Nombre de la tarea
        result: Resultado de la tarea (opcional)
        success: Si la tarea fue exitosa (opcional)
    """
    task = arguments.get("task", "tarea")
    result = arguments.get("result", "completada")
    success = arguments.get("success", True)

    if success:
        if "success" in result.lower() or "exitoso" in result.lower():
            message = f"{task} completada exitosamente"
        else:
            message = f"{task}: {result}"
    else:
        if "error" in result.lower() or "fail" in result.lower():
            message = f"{task} con errores, revisa la consola"
        else:
            message = f"{task}: {result}"

    speak_text(message)
    return CallToolResult(
        content=[TextContent(type="text", text=f"Notificación enviada: {message}")]
    )


@server.call_tool()
async def notify_startup(arguments: Dict[str, Any]) -> CallToolResult:
    """
    Notificar cuando Zed se inicia

    Args:
        project: Nombre del proyecto (opcional)
    """
    project = arguments.get("project", "")

    if project:
        message = f"Zed listo, proyecto: {project}"
    else:
        message = "Zed listo, empezamos a programar"

    speak_text(message)
    return CallToolResult(
        content=[TextContent(type="text", text=f"Notificación enviada: {message}")]
    )


@server.list_tools()
async def list_tools() -> ListToolsResult:
    """Listar herramientas disponibles"""
    return ListToolsResult(
        tools=[
            Tool(
                name="notify_file_save",
                description="Notificar cuando un archivo se guarda correctamente",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Nombre del archivo guardado",
                        },
                        "file_type": {
                            "type": "string",
                            "description": "Tipo de archivo (opcional)",
                        },
                        "success": {
                            "type": "boolean",
                            "description": "Si el guardado fue exitoso (opcional, default: true)",
                        },
                    },
                    "required": ["filename"],
                },
            ),
            Tool(
                name="notify_task_complete",
                description="Notificar cuando una tarea compleja se completa",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "Nombre de la tarea (build, test, lint, etc.)",
                        },
                        "result": {
                            "type": "string",
                            "description": "Resultado de la tarea (opcional)",
                        },
                        "success": {
                            "type": "boolean",
                            "description": "Si la tarea fue exitosa (opcional)",
                        },
                    },
                    "required": ["task"],
                },
            ),
            Tool(
                name="notify_startup",
                description="Notificar cuando Zed se inicia",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project": {
                            "type": "string",
                            "description": "Nombre del proyecto (opcional)",
                        }
                    },
                },
            ),
        ]
    )


@server.list_resources()
async def list_resources() -> List[Resource]:
    """Listar recursos disponibles"""
    return []


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Leer un recurso"""
    raise Exception("Not implemented")


async def main():
    """Función principal"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializeRequest(
                protocolVersion="2024-11-05",
                capabilities={},
                clientInfo={"name": "zed-tts-notifications", "version": "1.0.0"},
            ),
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
