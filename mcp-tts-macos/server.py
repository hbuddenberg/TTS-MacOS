#!/usr/bin/env python3
"""
Servidor MCP para Text-to-Speech usando el TTS nativo de macOS
Versión 1.4.4 - Soporte completo para selección de variantes de voz
"""

import asyncio
import subprocess
import json
import unicodedata
from typing import Any, Dict, List, Tuple
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Crear instancia del servidor
app = Server("mcp-tts-macos")


def normalize_text(text: str) -> str:
    """Normaliza texto removiendo acentos para comparación

    Args:
        text: Texto a normalizar

    Returns:
        Texto sin acentos en minúsculas
    """
    # Normalizar a NFD (separa caracteres base de acentos)
    nfd = unicodedata.normalize("NFD", text)
    # Filtrar los acentos (categoría Mn = Nonspacing Mark)
    without_accents = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return without_accents.lower()


def get_system_voices() -> Dict[str, str]:
    """Obtiene todas las voces disponibles en el sistema"""
    try:
        result = subprocess.run(
            ["say", "-v", "?"], capture_output=True, text=True, check=True
        )

        voces = {}
        for linea in result.stdout.split("\n"):
            partes = linea.strip().split()
            if partes:
                nombre_voz = partes[0]
                voces[nombre_voz.lower()] = nombre_voz

        return voces
    except:
        # Fallback a voces predeterminadas
        return {
            "monica": "Monica",
            "paulina": "Paulina",
            "jorge": "Jorge",
            "juan": "Juan",
            "diego": "Diego",
            "angelica": "Angelica",
        }


def categorize_voices() -> Dict[str, List[Tuple[str, str]]]:
    """Categoriza las voces disponibles por tipo"""
    try:
        result = subprocess.run(
            ["say", "-v", "?"], capture_output=True, text=True, check=True
        )

        categorias = {
            "espanol": [],
            "siri": [],
            "enhanced": [],
            "premium": [],
            "otras": [],
        }

        for linea in result.stdout.split("\n"):
            if not linea.strip():
                continue

            partes = linea.strip().split()
            if not partes:
                continue

            nombre_voz = partes[0]
            linea_lower = linea.lower()

            # Categorizar
            if "spanish" in linea_lower or "español" in linea_lower:
                categorias["espanol"].append((nombre_voz, linea.strip()))

            if "siri" in linea_lower:
                categorias["siri"].append((nombre_voz, linea.strip()))

            if "enhanced" in linea_lower:
                categorias["enhanced"].append((nombre_voz, linea.strip()))

            if "premium" in linea_lower:
                categorias["premium"].append((nombre_voz, linea.strip()))

            # Si no está en ninguna categoría específica
            if not any(
                [
                    "spanish" in linea_lower,
                    "español" in linea_lower,
                    "siri" in linea_lower,
                    "enhanced" in linea_lower,
                    "premium" in linea_lower,
                ]
            ):
                categorias["otras"].append((nombre_voz, linea.strip()))

        return categorias
    except:
        return None


def find_voice_in_system(query: str) -> str:
    """Busca una voz en el sistema de forma flexible"""
    try:
        result = subprocess.run(
            ["say", "-v", "?"], capture_output=True, text=True, check=True
        )

        query_normalized = normalize_text(query)

        # 1. Búsqueda exacta (case-insensitive y accent-insensitive)
        for linea in result.stdout.split("\n"):
            partes = linea.strip().split()
            if partes:
                nombre_voz = partes[0]
                if normalize_text(nombre_voz) == query_normalized:
                    return nombre_voz

        # 2. Búsqueda por inicio de nombre (prioridad)
        for linea in result.stdout.split("\n"):
            partes = linea.strip().split()
            if partes:
                nombre_voz = partes[0]
                if normalize_text(nombre_voz).startswith(query_normalized):
                    return nombre_voz

        # 3. Búsqueda parcial en toda la línea (accent-insensitive)
        for linea in result.stdout.split("\n"):
            if query_normalized in normalize_text(linea):
                partes = linea.strip().split()
                if partes:
                    return partes[0]

        # Fallback a primera voz en español
        for linea in result.stdout.split("\n"):
            if "spanish" in linea.lower() or "español" in linea.lower():
                partes = linea.strip().split()
                if partes:
                    return partes[0]

        return "Monica"
    except:
        return "Monica"


# Obtener voces disponibles al iniciar
SYSTEM_VOICES = get_system_voices()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Lista las herramientas disponibles en el servidor MCP
    """
    return [
        Tool(
            name="speak_text",
            description="Convierte texto a voz y lo reproduce usando el TTS nativo de macOS. Soporta TODAS las voces del sistema incluyendo español, Siri, Enhanced y Premium. Puede forzar variante específica con el parámetro 'type'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "El texto que deseas convertir a audio",
                    },
                    "voice": {
                        "type": "string",
                        "description": "Nombre de la voz a utilizar (ej: Monica, Jorge, Siri, Angélica). Acepta cualquier voz instalada en el sistema. Usa list_voices para ver opciones.",
                        "default": "monica",
                    },
                    "rate": {
                        "type": "integer",
                        "description": "Velocidad de lectura en palabras por minuto (100-300). Default: 175",
                        "default": 175,
                        "minimum": 100,
                        "maximum": 300,
                    },
                    "type": {
                        "type": "string",
                        "description": "Forzar variante específica de voz (normal/enhanced/premium/siri). Útil para voces con múltiples variantes como Marisol (Enhanced + Premium).",
                        "enum": ["normal", "enhanced", "premium", "siri"],
                    },
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="list_voices",
            description="Lista TODAS las voces disponibles en el sistema macOS categorizadas por tipo: Español, Siri, Enhanced/Premium y otras",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="save_audio",
            description="Convierte texto a voz y lo guarda como archivo de audio (AIFF). Soporta todas las voces del sistema. Puede forzar variante específica con el parámetro 'type'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "El texto a convertir"},
                    "filename": {
                        "type": "string",
                        "description": "Nombre del archivo (sin extensión)",
                    },
                    "voice": {
                        "type": "string",
                        "description": "Nombre de la voz a utilizar (ej: Monica, Jorge, Siri, Angélica)",
                        "default": "monica",
                    },
                    "type": {
                        "type": "string",
                        "description": "Forzar variante específica de voz (normal/enhanced/premium/siri). Útil para voces con múltiples variantes como Marisol (Enhanced + Premium)",
                        "enum": ["normal", "enhanced", "premium", "siri"],
                    },
                },
                "required": ["text", "filename"],
            },
        ),
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
            return [TextContent(type="text", text=f"Herramienta desconocida: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error al ejecutar {name}: {str(e)}")]


async def speak_text(arguments: dict) -> list[TextContent]:
    """
    Reproduce el texto usando TTS de macOS con búsqueda flexible de voces
    """
    text = arguments["text"]
    voice_query = arguments.get("voice", "monica")
    rate = arguments.get("rate", 175)
    voice_type = arguments.get("type")

    # Buscar la voz en el sistema
    voice_name = find_voice_in_system(voice_query)

    # Si se especificó tipo, buscar variante específica
    if voice_type and voice_name:
        categorias = categorize_voices()
        for cat, voices_list in categorias.items():
            for voice_real_name, _ in voices_list:
                if voice_real_name.lower() == voice_name.lower():
                    if voice_type.lower() == "normal" and cat == "espanol":
                        voice_name = voice_real_name
                        break
                    elif voice_type.lower() == "enhanced" and cat == "enhanced":
                        voice_name = voice_real_name
                        break
                    elif voice_type.lower() == "premium" and cat == "premium":
                        voice_name = voice_real_name
                        break
                    elif voice_type.lower() == "siri" and cat == "siri":
                        voice_name = voice_real_name
                        break

    # Construir comando
    cmd = ["say", "-v", voice_name, "-r", str(rate), text]

    # Ejecutar de forma asíncrona
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return [
            TextContent(
                type="text",
                text=f"✅ Audio reproducido exitosamente\nVoz: {voice_name}\nVelocidad: {rate} palabras/min",
            )
        ]
    else:
        error_msg = stderr.decode() if stderr else "Error desconocido"
        return [
            TextContent(type="text", text=f"❌ Error al reproducir audio: {error_msg}")
        ]


async def list_voices() -> list[TextContent]:
    """
    Lista todas las voces disponibles categorizadas por tipo
    """
    categorias = categorize_voices()

    if not categorias:
        return [
            TextContent(
                type="text", text="❌ No se pudo obtener la lista de voces del sistema"
            )
        ]

    voices_info = "🎙️ **VOCES DISPONIBLES EN EL SISTEMA**\n\n"

    # Voces en Español
    if categorias["espanol"]:
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        voices_info += f"📍 **VOCES EN ESPAÑOL** ({len(categorias['espanol'])})\n"
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        for nombre, info in sorted(categorias["espanol"])[
            :10
        ]:  # Limitar a 10 para no saturar
            voices_info += f"• **{nombre}**: {info[len(nombre) :].strip()}\n"
        if len(categorias["espanol"]) > 10:
            voices_info += f"\n_... y {len(categorias['espanol']) - 10} más_\n"
        voices_info += "\n"

    # Voces Enhanced/Premium
    enhanced_premium = list(
        set([(v[0], v[1]) for v in categorias["enhanced"] + categorias["premium"]])
    )
    if enhanced_premium:
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        voices_info += f"⭐ **VOCES ENHANCED/PREMIUM** ({len(enhanced_premium)})\n"
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        for nombre, info in sorted(enhanced_premium)[:10]:
            voices_info += f"• **{nombre}**: {info[len(nombre) :].strip()}\n"
        if len(enhanced_premium) > 10:
            voices_info += f"\n_... y {len(enhanced_premium) - 10} más_\n"
        voices_info += "\n"

    # Voces de Siri
    if categorias["siri"]:
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        voices_info += f"🤖 **VOCES DE SIRI** ({len(categorias['siri'])})\n"
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        for nombre, info in sorted(categorias["siri"]):
            voices_info += f"• **{nombre}**: {info[len(nombre) :].strip()}\n"
        voices_info += "\n"
    else:
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        voices_info += "🤖 **VOCES DE SIRI**\n"
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        voices_info += "ℹ️ No hay voces de Siri instaladas\n\n"
        voices_info += "💡 Instala desde: System Preferences → Accessibility → Spoken Content → System Voices\n\n"

    # Total
    total_voces = len(SYSTEM_VOICES)
    voices_info += f"**Total de voces detectadas: {total_voces}**\n\n"
    voices_info += "💡 **Uso:** Puedes usar cualquier nombre de voz (ej: Monica, Jorge, Siri, Angélica)\n"
    voices_info += "🔍 **Búsqueda flexible:** También funciona con búsqueda parcial (ej: 'siri' encuentra voces Siri)\n"

    return [TextContent(type="text", text=voices_info)]


async def save_audio(arguments: dict) -> list[TextContent]:
    """
    Guarda el texto como archivo de audio con búsqueda flexible de voces
    """
    text = arguments["text"]
    filename = arguments["filename"]
    voice_query = arguments.get("voice", "monica")
    voice_type = arguments.get("type")

    # Buscar la voz en el sistema
    voice_name = find_voice_in_system(voice_query)

    # Si se especificó tipo, buscar variante específica
    if voice_type and voice_name:
        categorias = categorize_voices()
        for cat, voices_list in categorias.items():
            for voice_real_name, _ in voices_list:
                if voice_real_name.lower() == voice_name.lower():
                    if voice_type.lower() == "normal" and cat == "espanol":
                        voice_name = voice_real_name
                        break
                    elif voice_type.lower() == "enhanced" and cat == "enhanced":
                        voice_name = voice_real_name
                        break
                    elif voice_type.lower() == "premium" and cat == "premium":
                        voice_name = voice_real_name
                        break
                    elif voice_type.lower() == "siri" and cat == "siri":
                        voice_name = voice_real_name
                        break

    # Asegurar extensión .aiff
    if not filename.endswith(".aiff"):
        filename += ".aiff"

    # Ruta completa (guardar en el directorio home del usuario)
    output_path = f"/Users/{subprocess.getoutput('whoami')}/Desktop/{filename}"

    # Comando para guardar
    cmd = ["say", "-v", voice_name, "-o", output_path, text]

    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return [
            TextContent(
                type="text",
                text=f"✅ Audio guardado exitosamente\nArchivo: {output_path}\nVoz: {voice_name}",
            )
        ]
    else:
        error_msg = stderr.decode() if stderr else "Error desconocido"
        return [
            TextContent(type="text", text=f"❌ Error al guardar audio: {error_msg}")
        ]


async def main():
    """
    Punto de entrada principal del servidor
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
