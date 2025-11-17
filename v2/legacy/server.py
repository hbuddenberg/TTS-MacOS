"""
Legacy MCP Server - Preserves TTS-MacOS v1.4.4 MCP functionality

This module maintains the exact MCP server implementation from v1.4.4
for complete backward compatibility.
"""

import asyncio
import json
import logging
import subprocess
import unicodedata
from typing import Any, Dict, List, Tuple

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from .voice_detector import LegacyVoiceDetector


class LegacyMCPServer:
    """
    Preserves v1.4.4 MCP server functionality for backward compatibility
    """

    def __init__(self):
        self.version = "1.4.4"
        self.mcp = FastMCP("mcp-tts-macos-legacy")
        self.voice_detector = LegacyVoiceDetector()
        self.session_voices = {}  # Track voice preferences per session

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Register MCP tools
        self._register_tools()

    def normalize_text(self, text: str) -> str:
        """Normaliza texto removiendo acentos para comparación"""
        # Normalizar a NFD (separa caracteres base de acentos)
        nfd = unicodedata.normalize("NFD", text)
        # Filtrar los acentos (categoría Mn = Nonspacing Mark)
        without_accents = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
        return without_accents.lower()

    def get_system_voices(self) -> Dict[str, str]:
        """Obtiene todas las voces disponibles en el sistema"""
        return self.voice_detector.get_system_voices()

    def _register_tools(self):
        """Registra las herramientas MCP según la lógica v1.4.4"""

        @self.mcp.tool()
        def speak_text(
            text: str, voice: str = "monica", rate: int = 175, type: str = "normal"
        ) -> str:
            """
            Reproduce texto usando voz nativa de macOS con soporte para variantes

            Args:
                text: Texto a reproducir (requerido)
                voice: Nombre de la voz (ej: monica, angelica, jorge)
                rate: Velocidad en palabras por minuto (100-300)
                type: Variante de voz (normal/enhanced/premium/siri)

            Returns:
                Mensaje de confirmación con detalles de reproducción
            """
            try:
                # Validar rate
                if not (100 <= rate <= 300):
                    return "❌ Error: La velocidad debe estar entre 100 y 300 WPM"

                # Obtener voces del sistema
                system_voices = self.get_system_voices()

                # Construir nombre completo de la voz según variante
                voice_with_type = self._build_voice_name(voice, type, system_voices)
                voice_name = self._find_best_voice_match(voice_with_type, system_voices)

                if not voice_name:
                    # Fallback a Monica español
                    voice_name = self._find_best_voice_match("monica", system_voices)
                    if not voice_name:
                        return "❌ Error: No se encontraron voces en el sistema"

                # Comando say según variante
                cmd = ["say", "-v", voice_name]

                # Agregar rate si no es default
                if rate != 175:
                    cmd.extend(["-r", str(rate)])

                # Agregar texto
                cmd.append(text)

                # Ejecutar en segundo plano para no bloquear
                process = asyncio.create_subprocess_exec(
                    *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )

                # Guardar preferencia de voz para esta sesión
                self.session_voices["default"] = voice_name

                # Ejecutar y esperar resultado
                proc = asyncio.run(process)
                stdout, stderr = asyncio.run(proc.communicate())

                if proc.returncode == 0:
                    # Determinar info de la voz utilizada
                    voice_info = self._get_voice_info(voice_name, system_voices)
                    emoji = self._get_voice_emoji(voice_info)

                    return (
                        f"✅ {emoji} Reproduciendo con voz: {voice_name}\\n"
                        f'📝 Texto: "{text}"\\n'
                        f"⚡ Velocidad: {rate} WPM\\n"
                        f"🎭 Tipo: {type}\\n"
                        f"🎯 Voz detectada: {voice_info.get('language', 'Desconocido')}"
                    )
                else:
                    return f"❌ Error ejecutando say: {stderr.decode()}"

            except Exception as e:
                return f"❌ Error en speak_text: {str(e)}"

        @self.mcp.tool()
        def speak(text: str, voice: str = "monica", rate: int = 175) -> str:
            """
            Alias simple para speak_text (compatibilidad)

            Args:
                text: Texto a reproducir
                voice: Nombre de la voz
                rate: Velocidad en palabras por minuto

            Returns:
                Mensaje de confirmación
            """
            return speak_text(text=text, voice=voice, rate=rate, type="normal")

        @self.mcp.tool()
        def list_voices() -> str:
            """
            Lista todas las voces disponibles categorizadas por tipo

            Returns:
                Listado detallado de voces disponibles
            """
            try:
                # Obtener y categorizar voces
                result = subprocess.run(
                    ["say", "-v", "?"], capture_output=True, text=True, check=True
                )

                voices_by_type = {
                    "Español": [],
                    "Enhanced": [],
                    "Premium": [],
                    "Siri": [],
                    "Otras": [],
                }

                total_count = 0

                for line in result.stdout.split("\\n"):
                    if not line.strip():
                        continue

                    parts = line.strip().split()
                    if not parts:
                        continue

                    voice_name = parts[0]
                    description = " ".join(parts[1:])
                    line_lower = line.lower()

                    # Contador total
                    total_count += 1

                    # Determinar categoría
                    category = "Otras"
                    if any(word in line_lower for word in ["spanish", "español"]):
                        category = "Español"
                    elif "enhanced" in line_lower:
                        category = "Enhanced"
                    elif "premium" in line_lower:
                        category = "Premium"
                    elif "siri" in line_lower:
                        category = "Siri"

                    voices_by_type[category].append(
                        {"name": voice_name, "description": description}
                    )

                # Formatear salida
                output = [f"🎭 VOCES DISPONIBLES ({total_count} total)\\n"]

                for category, voices in voices_by_type.items():
                    if voices:
                        output.append(f"\\n📂 {category.upper()} ({len(voices)}):")
                        for voice in voices:
                            output.append(
                                f"  • {voice['name']} - {voice['description']}"
                            )

                output.append(
                    f"\\n💾 Última voz usada: {self.session_voices.get('default', 'Ninguna')}"
                )

                return "\\n".join(output)

            except subprocess.CalledProcessError as e:
                return f"❌ Error obteniendo voces: {e}"

        @self.mcp.tool()
        def save_audio(
            text: str, filename: str, voice: str = "monica", rate: int = 175
        ) -> str:
            """
            Guarda texto como archivo de audio AIFF en el escritorio

            Args:
                text: Texto a convertir
                filename: Nombre del archivo (sin extensión)
                voice: Voz a utilizar
                rate: Velocidad en palabras por minuto

            Returns:
                Confirmación con ruta del archivo guardado
            """
            try:
                # Validar filename
                if not filename or not filename.strip():
                    return "❌ Error: Debes proporcionar un nombre de archivo válido"

                # Construir ruta completa al escritorio
                import subprocess as sp

                username = sp.getoutput("whoami").strip()
                output_path = f"/Users/{username}/Desktop/{filename}.aiff"

                # Obtener voces y encontrar la mejor
                system_voices = self.get_system_voices()
                voice_name = self._find_best_voice_match(voice, system_voices)

                if not voice_name:
                    return f"❌ Error: No se encontró la voz '{voice}'"

                # Construir comando say para archivo
                cmd = [
                    "say",
                    "-v",
                    voice_name,
                    "-r",
                    str(rate),
                    "-o",
                    output_path,
                    "--data-format=LEF32@16000",
                    text,
                ]

                # Ejecutar comando
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    file_size = subprocess.run(
                        ["ls", "-lh", output_path], capture_output=True, text=True
                    ).stdout.split()[4]

                    return (
                        f"✅ Audio guardado exitosamente\\n"
                        f"📁 Archivo: {output_path}\\n"
                        f"🎤 Voz: {voice_name}\\n"
                        f"⚡ Velocidad: {rate} WPM\\n"
                        f"💾 Tamaño: {file_size}\\n"
                        f'📝 Texto: "{text}"'
                    )
                else:
                    return f"❌ Error guardando audio: {result.stderr}"

            except Exception as e:
                return f"❌ Error en save_audio: {str(e)}"

    def _build_voice_name(
        self, base_voice: str, voice_type: str, system_voices: Dict[str, str]
    ) -> str:
        """Construye nombre completo de voz según variante solicitada"""
        # Para voces españolas ya tienen variantes predefinidas
        spanish_variants = {
            "monica": {
                "normal": "Monica",
                "enhanced": "Monica-enhanced",
                "premium": "Monica-premium",
            },
            "jorge": {
                "normal": "Jorge",
                "enhanced": "Jorge-enhanced",
                "premium": "Jorge-premium",
            },
            "angelica": {
                "normal": "Angelica",
                "enhanced": "Angelica-enhanced",
                "premium": "Angelica-premium",
            },
        }

        base_lower = base_voice.lower()
        if (
            base_lower in spanish_variants
            and voice_type in spanish_variants[base_lower]
        ):
            return spanish_variants[base_lower][voice_type]

        # Para otras voces, agregar sufijo si existe
        if voice_type != "normal":
            variant_name = f"{base_voice}-{voice_type}"
            if variant_name in system_voices:
                return variant_name

        return base_voice

    def _find_best_voice_match(
        self, requested_voice: str, system_voices: Dict[str, str]
    ) -> str:
        """Encuentra la mejor coincidencia de voz usando el algoritmo v1.4.4"""
        if not requested_voice or not system_voices:
            return None

        # Estrategia 1: Búsqueda exacta
        if requested_voice in system_voices:
            return requested_voice

        # Estrategia 2: Búsqueda normalizada (sin acentos)
        normalized = self.normalize_text(requested_voice)
        if normalized in system_voices:
            return normalized

        # Estrategia 3: Búsqueda por primera letra
        if len(requested_voice) >= 1:
            first_char = requested_voice[0].upper()
            for voice_name in system_voices:
                if voice_name and voice_name[0].upper() == first_char:
                    return voice_name

        # Estrategia 4: Búsqueda parcial
        for voice_name in system_voices:
            if normalized in self.normalize_text(voice_name):
                return voice_name

        return None

    def _get_voice_info(
        self, voice_name: str, system_voices: Dict[str, str]
    ) -> Dict[str, str]:
        """Extrae información detallada de la voz"""
        if voice_name in system_voices:
            description = system_voices[voice_name].lower()

            language = "Desconocido"
            if "spanish" in description or "español" in description:
                language = "Español"
            elif "english" in description:
                language = "Inglés"

            return {
                "name": voice_name,
                "language": language,
                "description": system_voices[voice_name],
            }

        return {"name": voice_name, "language": "Desconocido", "description": ""}

    def _get_voice_emoji(self, voice_info: Dict[str, str]) -> str:
        """Retorna emoji apropiado para la voz"""
        language = voice_info.get("language", "").lower()

        if "español" in language or "spanish" in language:
            return "🇪🇸"
        elif "inglés" in language or "english" in language:
            return "🇺🇸"
        else:
            return "🎤"

    def get_server(self) -> FastMCP:
        """Retorna la instancia del servidor MCP"""
        return self.mcp

    async def run(self):
        """Inicia el servidor MCP legacy"""
        await self.mcp.run()


# Función para compatibilidad con v1.4.4
async def main():
    """Función principal que mantiene compatibilidad con v1.4.4"""
    server = LegacyMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
