#!/usr/bin/env python3
"""
Servidor MCP alternativo usando FastMCP para mejor compatibilidad
"""

import asyncio
import json
import subprocess
import unicodedata
from typing import Any, Dict, List, Tuple

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

# Crear instancia del servidor FastMCP
mcp = FastMCP("mcp-tts-macos-fast")


def normalize_text(text: str) -> str:
    """Normaliza texto removiendo acentos para comparación"""
    nfd = unicodedata.normalize("NFD", text)
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

            if "spanish" in linea_lower or "español" in linea_lower:
                categorias["espanol"].append((nombre_voz, linea.strip()))

            if "siri" in linea_lower:
                categorias["siri"].append((nombre_voz, linea.strip()))

            if "enhanced" in linea_lower:
                categorias["enhanced"].append((nombre_voz, linea.strip()))

            if "premium" in linea_lower:
                categorias["premium"].append((nombre_voz, linea.strip()))

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

        for linea in result.stdout.split("\n"):
            partes = linea.strip().split()
            if partes:
                nombre_voz = partes[0]
                if normalize_text(nombre_voz) == query_normalized:
                    return nombre_voz

        for linea in result.stdout.split("\n"):
            partes = linea.strip().split()
            if partes:
                nombre_voz = partes[0]
                if normalize_text(nombre_voz).startswith(query_normalized):
                    return nombre_voz

        for linea in result.stdout.split("\n"):
            if query_normalized in normalize_text(linea):
                partes = linea.strip().split()
                if partes:
                    return partes[0]

        for linea in result.stdout.split("\n"):
            if "spanish" in linea.lower() or "español" in linea.lower():
                partes = linea.strip().split()
                if partes:
                    return partes[0]

        return "Monica"
    except:
        return "Monica"


SYSTEM_VOICES = get_system_voices()


@mcp.tool()
async def speak_text(text: str, voice: str = "monica", rate: int = 175) -> str:
    """
    Convierte texto a voz y lo reproduce usando el TTS nativo de macOS.

    Args:
        text: El texto que deseas convertir a audio
        voice: Nombre de la voz a utilizar (ej: Monica, Jorge, Siri, Angélica)
        rate: Velocidad de lectura en palabras por minuto (100-300)
    """
    # Buscar la voz en el sistema
    voice_name = find_voice_in_system(voice)

    # Construir comando
    cmd = ["say", "-v", voice_name, "-r", str(rate), text]

    # Ejecutar de forma asíncrona
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return f"✅ Audio reproducido exitosamente\\nVoz: {voice_name}\\nVelocidad: {rate} palabras/min"
    else:
        error_msg = stderr.decode() if stderr else "Error desconocido"
        return f"❌ Error al reproducir audio: {error_msg}"


@mcp.tool()
async def list_voices() -> str:
    """
    Lista todas las voces disponibles en el sistema macOS categorizadas por tipo
    """
    categorias = categorize_voices()

    if not categorias:
        return "❌ No se pudo obtener la lista de voces del sistema"

    voices_info = "🎙️ **VOCES DISPONIBLES EN EL SISTEMA**\\n\\n"

    # Voces en Español
    if categorias["espanol"]:
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n"
        voices_info += f"📍 **VOCES EN ESPAÑOL** ({len(categorias['espanol'])})\\n"
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        for nombre, info in sorted(categorias["espanol"])[:10]:
            voices_info += f"• **{nombre}**: {info[len(nombre) :].strip()}\\n"
        if len(categorias["espanol"]) > 10:
            voices_info += f"\\n_... y {len(categorias['espanol']) - 10} más_\\n"
        voices_info += "\\n"

    # Voces Enhanced/Premium
    enhanced_premium = list(
        set([(v[0], v[1]) for v in categorias["enhanced"] + categorias["premium"]])
    )
    if enhanced_premium:
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n"
        voices_info += f"⭐ **VOCES ENHANCED/PREMIUM** ({len(enhanced_premium)})\\n"
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        for nombre, info in sorted(enhanced_premium)[:10]:
            voices_info += f"• **{nombre}**: {info[len(nombre) :].strip()}\\n"
        if len(enhanced_premium) > 10:
            voices_info += f"\\n_... y {len(enhanced_premium) - 10} más_\\n"
        voices_info += "\\n"

    # Voces de Siri
    if categorias["siri"]:
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n"
        voices_info += f"🤖 **VOCES DE SIRI** ({len(categorias['siri'])})\\n"
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        for nombre, info in sorted(categorias["siri"]):
            voices_info += f"• **{nombre}**: {info[len(nombre) :].strip()}\\n"
        voices_info += "\\n"
    else:
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n"
        voices_info += "🤖 **VOCES DE SIRI**\\n"
        voices_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        voices_info += "ℹ️ No hay voces de Siri instaladas\\n\\n"
        voices_info += "💡 Instala desde: System Preferences → Accessibility → Spoken Content → System Voices\\n\\n"

    # Total
    total_voces = len(SYSTEM_VOICES)
    voices_info += f"**Total de voces detectadas: {total_voces}**\\n\\n"
    voices_info += "💡 **Uso:** Puedes usar cualquier nombre de voz (ej: Monica, Jorge, Siri, Angélica)\\n"
    voices_info += "🔍 **Búsqueda flexible:** También funciona con búsqueda parcial (ej: 'siri' encuentra voces Siri)\\n"

    return voices_info


@mcp.tool()
async def save_audio(text: str, filename: str, voice: str = "monica") -> str:
    """
    Convierte texto a voz y lo guarda como archivo de audio (AIFF).

    Args:
        text: El texto a convertir
        filename: Nombre del archivo (sin extensión)
        voice: Nombre de la voz a utilizar (ej: Monica, Jorge, Siri, Angélica)
    """
    # Buscar la voz en el sistema
    voice_name = find_voice_in_system(voice)

    # Asegurar extensión .aiff
    if not filename.endswith(".aiff"):
        filename += ".aiff"

    # Ruta completa
    output_path = f"/Users/{subprocess.getoutput('whoami')}/Desktop/{filename}"

    # Comando para guardar
    cmd = ["say", "-v", voice_name, "-o", output_path, text]

    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return f"✅ Audio guardado exitosamente\\nArchivo: {output_path}\\nVoz: {voice_name}"
    else:
        error_msg = stderr.decode() if stderr else "Error desconocido"
        return f"❌ Error al guardar audio: {error_msg}"


if __name__ == "__main__":
    mcp.run()
