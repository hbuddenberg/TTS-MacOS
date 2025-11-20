#!/usr/bin/env python3
"""
TTS Notify v2 - MCP Server

Modular MCP server for Claude Desktop integration using the new core architecture.
Maintains full feature parity with v1.5.0 while using the modular backend.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

# Import from the new modular architecture
from core.config_manager import config_manager
from core.voice_system import VoiceManager, VoiceFilter
from core.tts_engine import MacOSTTSEngine
from core.models import TTSRequest, AudioFormat
from core.exceptions import TTSNotifyError, VoiceNotFoundError, ValidationError
from utils.logger import setup_logging, get_logger


class TTSNotifyMCPServer:
    """MCP Server for TTS Notify v2"""

    def __init__(self):
        self.config_manager = config_manager
        self.voice_manager = VoiceManager()
        self.tts_engine = MacOSTTSEngine()
        self.logger = None

        # Load configuration for MCP context
        self.config = self.config_manager.get_config()

        # Setup logging
        self._setup_logging()

        # Create FastMCP instance
        self.mcp = FastMCP("tts-notify")

        # Register tools
        self._register_tools()

    def _setup_logging(self):
        """Setup logging based on configuration"""
        setup_logging(
            level=getattr(self.config, 'TTS_NOTIFY_LOG_LEVEL', 'INFO'),
            verbose=getattr(self.config, 'TTS_NOTIFY_VERBOSE', False)
        )
        self.logger = get_logger(__name__)

        if self.logger:
            self.logger.info("TTS Notify MCP Server v2.0.0 starting up")

    def _register_tools(self):
        """Register MCP tools with FastMCP"""

        @self.mcp.tool()
        async def speak_text(
            text: str,
            voice: Optional[str] = None,
            rate: Optional[int] = None,
            pitch: Optional[float] = None,
            volume: Optional[float] = None
        ) -> List[TextContent]:
            """
            Reproduce texto en voz alta usando el motor TTS de macOS

            Args:
                text: Texto a reproducir
                voice: Voz a utilizar (búsqueda flexible, ej: 'monica', 'angelica' -> 'Angélica')
                rate: Velocidad de habla (100-300 palabras por minuto)
                pitch: Tono de la voz (0.5-2.0, donde 1.0 es normal)
                volume: Volumen (0.0-1.0, donde 1.0 es máximo)

            Returns:
                Lista de TextContent con el resultado
            """
            try:
                # Use configuration defaults if not specified
                voice_name = voice or getattr(self.config, 'TTS_NOTIFY_VOICE', 'monica')
                speech_rate = rate or getattr(self.config, 'TTS_NOTIFY_RATE', 175)
                speech_pitch = pitch or getattr(self.config, 'TTS_NOTIFY_PITCH', 1.0)
                speech_volume = volume or getattr(self.config, 'TTS_NOTIFY_VOLUME', 1.0)

                # Create TTS request
                request = TTSRequest(
                    text=text,
                    voice_name=voice_name,
                    rate=speech_rate,
                    pitch=speech_pitch,
                    volume=speech_volume,
                    language=getattr(self.config, 'TTS_NOTIFY_LANGUAGE', 'es')
                )

                # Validate request
                validation_errors = request.validate()
                if validation_errors:
                    error_msg = "Errores de validación: " + "; ".join(validation_errors)
                    if self.logger:
                        self.logger.warning(f"MCP validation error: {error_msg}")
                    return [TextContent(type="text", text=f"❌ Error: {error_msg}")]

                # Speak text
                response = await self.tts_engine.speak(request)

                result_msg = f"✅ Texto reproducido con voz '{response.voice_used}' a {response.actual_rate} WPM"
                if self.logger:
                    self.logger.info(f"MCP speak_text: {text[:50]}... -> {response.voice_used}")

                return [TextContent(type="text", text=result_msg)]

            except (VoiceNotFoundError, ValidationError, TTSError) as e:
                error_msg = f"❌ Error TTS: {e}"
                if self.logger:
                    self.logger.error(f"MCP TTS error: {e}")
                return [TextContent(type="text", text=error_msg)]

            except Exception as e:
                error_msg = f"❌ Error inesperado: {e}"
                if self.logger:
                    self.logger.exception("MCP speak_text unexpected error")
                return [TextContent(type="text", text=error_msg)]

        @self.mcp.tool()
        async def list_voices(
            gender: Optional[str] = None,
            language: Optional[str] = None,
            compact: Optional[bool] = False
        ) -> List[TextContent]:
            """
            Lista todas las voces disponibles del sistema con categorización

            Args:
                gender: Filtrar por género ('male' o 'female')
                language: Filtrar por idioma (ej: 'es', 'en', 'es_ES', 'es_MX')
                compact: Si es True, muestra solo nombres en formato compacto

            Returns:
                Lista de TextContent con la lista de voces formateada
            """
            try:
                # Get all voices
                voices = await self.voice_manager.get_all_voices()

                # Apply filters if specified
                if gender or language:
                    voice_filter = VoiceFilter()
                    voices = voice_filter.filter_voices(voices, gender=gender, language=language)

                if not voices:
                    no_voices_msg = "No se encontraron voces con los filtros especificados"
                    if self.logger:
                        self.logger.info("MCP list_voices: no voices found with filters")
                    return [TextContent(type="text", text=no_voices_msg)]

                # Format output
                if compact:
                    # Compact format - just names
                    voice_names = sorted([voice.name for voice in voices])
                    voices_text = "\n".join(voice_names)
                    header = f"🎵 VOCES DISPONIBLES ({len(voices)}):\n"
                    result_text = header + voices_text
                else:
                    # Detailed format with categorization (v1.5.0 style)
                    result_text = self._format_voices_categorized(voices)

                if self.logger:
                    self.logger.info(f"MCP list_voices: returned {len(voices)} voices")

                return [TextContent(type="text", text=result_text)]

            except TTSNotifyError as e:
                error_msg = f"❌ Error listando voces: {e}"
                if self.logger:
                    self.logger.error(f"MCP list_voices error: {e}")
                return [TextContent(type="text", text=error_msg)]

            except Exception as e:
                error_msg = f"❌ Error inesperado: {e}"
                if self.logger:
                    self.logger.exception("MCP list_voices unexpected error")
                return [TextContent(type="text", text=error_msg)]

        @self.mcp.tool()
        async def save_audio(
            text: str,
            filename: str,
            voice: Optional[str] = None,
            rate: Optional[int] = None,
            format: Optional[str] = "aiff"
        ) -> List[TextContent]:
            """
            Guarda texto como archivo de audio en el escritorio

            Args:
                text: Texto a convertir
                filename: Nombre del archivo (sin extensión, se añadirá automáticamente)
                voice: Voz a utilizar (búsqueda flexible)
                rate: Velocidad de habla (100-300 palabras por minuto)
                format: Formato de audio ('aiff', 'wav', 'mp3', 'ogg', 'm4a', 'flac')

            Returns:
                Lista de TextContent con el resultado
            """
            try:
                # Validate format
                try:
                    audio_format = AudioFormat(format)
                except ValueError:
                    return [TextContent(type="text", text=f"❌ Formato no soportado: {format}")]

                # Determine output path
                output_dir = Path(getattr(self.config, 'TTS_NOTIFY_OUTPUT_DIR', Path.home() / "Desktop"))
                output_path = output_dir / f"{filename}.{audio_format.value}"

                # Use configuration defaults if not specified
                voice_name = voice or getattr(self.config, 'TTS_NOTIFY_VOICE', 'monica')
                speech_rate = rate or getattr(self.config, 'TTS_NOTIFY_RATE', 175)

                # Create TTS request
                request = TTSRequest(
                    text=text,
                    voice_name=voice_name,
                    rate=speech_rate,
                    pitch=getattr(self.config, 'TTS_NOTIFY_PITCH', 1.0),
                    volume=getattr(self.config, 'TTS_NOTIFY_VOLUME', 1.0),
                    language=getattr(self.config, 'TTS_NOTIFY_LANGUAGE', 'es'),
                    output_format=audio_format,
                    output_path=str(output_path)
                )

                # Validate request
                validation_errors = request.validate()
                if validation_errors:
                    error_msg = "Errores de validación: " + "; ".join(validation_errors)
                    if self.logger:
                        self.logger.warning(f"MCP save_audio validation error: {error_msg}")
                    return [TextContent(type="text", text=f"❌ Error: {error_msg}")]

                # Save audio
                response = await self.tts_engine.synthesize(request)

                result_msg = f"✅ Audio guardado en: {output_path}"
                if self.logger:
                    self.logger.info(f"MCP save_audio: {text[:50]}... -> {output_path}")

                return [TextContent(type="text", text=result_msg)]

            except (VoiceNotFoundError, ValidationError, TTSError) as e:
                error_msg = f"❌ Error TTS: {e}"
                if self.logger:
                    self.logger.error(f"MCP save_audio TTS error: {e}")
                return [TextContent(type="text", text=error_msg)]

            except Exception as e:
                error_msg = f"❌ Error inesperado: {e}"
                if self.logger:
                    self.logger.exception("MCP save_audio unexpected error")
                return [TextContent(type="text", text=error_msg)]

        @self.mcp.tool()
        async def get_mcp_config() -> List[TextContent]:
            """
            Obtiene la configuración actual del servidor MCP y variables de entorno

            Returns:
                Lista de TextContent con la configuración actual
            """
            try:
                # Get MCP environment variables
                mcp_vars = self.config_manager.get_mcp_environment_variables()

                # Format configuration info
                config_lines = [
                    "🔧 CONFIGURACIÓN ACTUAL DEL SERVIDOR MCP:",
                    "",
                    f"Voz por defecto: {mcp_vars.get('TTS_NOTIFY_VOICE', 'N/A')}",
                    f"Velocidad por defecto: {mcp_vars.get('TTS_NOTIFY_RATE', 'N/A')} WPM",
                    f"Idioma por defecto: {mcp_vars.get('TTS_NOTIFY_LANGUAGE', 'N/A')}",
                    f"Calidad por defecto: {mcp_vars.get('TTS_NOTIFY_QUALITY', 'N/A')}",
                    f"TTS habilitado: {mcp_vars.get('TTS_NOTIFY_ENABLED', 'N/A')}",
                    f"Caché habilitado: {mcp_vars.get('TTS_NOTIFY_CACHE_ENABLED', 'N/A')}",
                    f"Confirmación habilitada: {mcp_vars.get('TTS_NOTIFY_CONFIRMATION', 'N/A')}",
                    f"Nivel de logging: {mcp_vars.get('TTS_NOTIFY_LOG_LEVEL', 'N/A')}",
                    f"Largo máximo de texto: {mcp_vars.get('TTS_NOTIFY_MAX_TEXT_LENGTH', 'N/A')}",
                    f"Formato de salida: {mcp_vars.get('TTS_NOTIFY_OUTPUT_FORMAT', 'N/A')}",
                    f"Perfil actual: {mcp_vars.get('TTS_NOTIFY_PROFILE', 'N/A')}",
                    "",
                    "📝 Variables de entorno activas:",
                ]

                # Add active environment variables
                active_vars = self.config.get_active_vars()
                if active_vars:
                    for var in active_vars:
                        config_lines.append(f"  ✅ {var}")
                else:
                    config_lines.append("  (Ninguna variable de entorno personalizada)")

                config_text = "\n".join(config_lines)

                if self.logger:
                    self.logger.info("MCP get_mcp_config: configuration retrieved")

                return [TextContent(type="text", text=config_text)]

            except Exception as e:
                error_msg = f"❌ Error obteniendo configuración: {e}"
                if self.logger:
                    self.logger.error(f"MCP get_mcp_config error: {e}")
                return [TextContent(type="text", text=error_msg)]

    def _format_voices_categorized(self, voices) -> str:
        """Format voices organized by category like v1.5.0"""
        # Categorize voices
        espanol = []
        enhanced = []
        siri = []
        other = []

        for voice in voices:
            voice_name_lower = voice.name.lower()

            if any(espanol_marker in voice_name_lower for espanol_marker in
                   ['espanol', 'español', 'spain', 'mexico', 'mexico', 'argentina', 'colombia', 'chile']):
                espanol.append(voice)
            elif 'siri' in voice_name_lower:
                siri.append(voice)
            elif 'enhanced' in voice_name_lower or 'premium' in voice_name_lower:
                enhanced.append(voice)
            else:
                other.append(voice)

        # Build output
        output_lines = [f"🎵 VOCES DISPONIBLES ({len(voices)}):"]

        if espanol:
            output_lines.append("\n🇪🇸  VOCES ESPAÑOL:")
            for voice in sorted(espanol, key=lambda v: v.name):
                gender_symbol = "♂" if voice.gender and voice.gender.value == "male" else "♀"
                quality = voice.quality.value if voice.quality else "basic"
                output_lines.append(f"  {gender_symbol} {voice.name} ({quality})")

        if enhanced:
            output_lines.append("\n✨ VOCES ENHANCED:")
            for voice in sorted(enhanced, key=lambda v: v.name):
                gender_symbol = "♂" if voice.gender and voice.gender.value == "male" else "♀"
                quality = voice.quality.value if voice.quality else "enhanced"
                output_lines.append(f"  {gender_symbol} {voice.name} ({quality})")

        if siri:
            output_lines.append("\n🍎 VOCES SIRI:")
            for voice in sorted(siri, key=lambda v: v.name):
                gender_symbol = "♂" if voice.gender and voice.gender.value == "male" else "♀"
                output_lines.append(f"  {gender_symbol} {voice.name}")

        if other:
            output_lines.append("\n🌍 OTRAS VOCES:")
            for voice in sorted(other, key=lambda v: v.name):
                gender_symbol = "♂" if voice.gender and voice.gender.value == "male" else "♀"
                lang = voice.language.value if voice.language else "unknown"
                output_lines.append(f"  {gender_symbol} {voice.name} ({lang})")

        return "\n".join(output_lines)

    async def run(self):
        """Run the MCP server"""
        if self.logger:
            self.logger.info("Starting TTS Notify MCP Server v2.0.0")

        # Run the FastMCP server
        await self.mcp.run()


async def main():
    """Main entry point for MCP server"""
    server = TTSNotifyMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())