#!/usr/bin/env python3
"""
TTS Notify v2 - CLI Interface

Modular command-line interface for TTS Notify v2 using the new core architecture.
Maintains full feature parity with v1.5.0 while using the modular backend.
"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Optional

# Import from the new modular architecture
from ...core.config_manager import config_manager
from ...core.voice_system import VoiceManager, VoiceFilter
from ...core.tts_engine import MacOSTTSEngine
from ...core.models import TTSRequest, AudioFormat
from ...core.exceptions import TTSNotifyError, VoiceNotFoundError, ValidationError, TTSError
from ...utils.logger import setup_logging, get_logger


class TTSNotifyCLI:
    """Main CLI class for TTS Notify v2"""

    def __init__(self):
        self.config_manager = config_manager
        self.voice_manager = VoiceManager()
        self.tts_engine = MacOSTTSEngine()
        self.logger = None

    def setup_logging(self):
        """Setup logging based on configuration"""
        config = self.config_manager.get_config()
        setup_logging(
            level=getattr(config, 'TTS_NOTIFY_LOG_LEVEL', 'INFO')
        )
        self.logger = get_logger(__name__)

    def create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser"""
        parser = argparse.ArgumentParser(
            prog="tts-notify",
            description="TTS Notify v2 - Sistema de notificaciones Text-to-Speech para macOS",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Ejemplos:
  tts-notify "Hola mundo"
  tts-notify "Hola mundo" --voice monica --rate 200
  tts-notify --list
  tts-notify --list --compact
  tts-notify --list --gen female
  tts-notify --list --lang es_ES
  tts-notify "Test" --save output_file
  tts-notify --mcp-config                 # Mostrar configuración MCP para Claude Desktop

Para búsqueda flexible de voces:
  tts-notify "Test" --voice angelica     # Encuentra Angélica
  tts-notify "Test" --voice "jorge enhanced"  # Variante Enhanced
  tts-notify "Test" --voice siri         # Siri si está instalada
            """
        )

        # Text argument
        parser.add_argument(
            "text",
            nargs="?",
            help="Texto a reproducir en voz alta"
        )

        # Voice options
        parser.add_argument(
            "--voice", "-v",
            help="Voz a utilizar (búsqueda flexible: exacta, parcial, sin acentos)"
        )
        parser.add_argument(
            "--rate", "-r",
            type=int,
            help="Velocidad de habla (palabras por minuto, 100-300)"
        )
        parser.add_argument(
            "--pitch",
            type=float,
            help="Tono de la voz (0.5-2.0, donde 1.0 es normal)"
        )
        parser.add_argument(
            "--volume",
            type=float,
            help="Volumen (0.0-1.0, donde 1.0 es máximo)"
        )

        # Listing options
        parser.add_argument(
            "--list", "-l",
            action="store_true",
            help="Listar todas las voces disponibles del sistema"
        )
        parser.add_argument(
            "--compact",
            action="store_true",
            help="Formato compacto para listar voces (solo nombres)"
        )
        parser.add_argument(
            "--gen", "--gender",
            choices=["male", "female"],
            help="Filtrar voces por género"
        )
        parser.add_argument(
            "--lang", "--language",
            help="Filtrar voces por idioma (ej: es, en, es_ES, es_MX)"
        )

        # Output options
        parser.add_argument(
            "--save", "-s",
            help="Guardar audio en archivo en lugar de reproducir"
        )
        parser.add_argument(
            "--format",
            choices=["aiff", "wav", "mp3", "ogg", "m4a", "flac"],
            default="aiff",
            help="Formato de audio para archivo de salida (default: aiff)"
        )

        # Configuration options
        parser.add_argument(
            "--profile",
            help="Usar perfil de configuración predefinido"
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Mostrar información detallada"
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Mostrar información de depuración"
        )

        # MCP configuration
        parser.add_argument(
            "--mcp-config",
            action="store_true",
            help="Mostrar configuración MCP para Claude Desktop con rutas reales"
        )

        # Version
        parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s 2.0.0"
        )

        return parser

    async def list_voices(self, compact: bool = False, gender: Optional[str] = None,
                         language: Optional[str] = None) -> None:
        """List available voices with optional filtering"""
        try:
            voices = await self.voice_manager.get_all_voices()

            # Apply filters
            if gender or language:
                voice_filter = VoiceFilter()
                voices = voice_filter.filter_voices(voices, gender=gender, language=language)

            if not voices:
                print("No se encontraron voces con los filtros especificados.")
                return

            if compact:
                # Compact format - just names
                for voice in sorted(voices, key=lambda v: v.name):
                    print(voice.name)
            else:
                # Detailed format with categorization
                self._print_voices_categorized(voices)

        except TTSNotifyError as e:
            print(f"Error listando voces: {e}")
            sys.exit(1)

    def _print_voices_categorized(self, voices) -> None:
        """Print voices organized by category like v1.5.0"""
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

        # Print by category
        if espanol:
            print("\n🇪🇸  VOCES ESPAÑOL:")
            for voice in sorted(espanol, key=lambda v: v.name):
                gender_symbol = "♂" if voice.gender and voice.gender.value == "male" else "♀"
                quality = voice.quality.value if voice.quality else "basic"
                print(f"  {gender_symbol} {voice.name} ({quality})")

        if enhanced:
            print("\n✨ VOCES ENHANCED:")
            for voice in sorted(enhanced, key=lambda v: v.name):
                gender_symbol = "♂" if voice.gender and voice.gender.value == "male" else "♀"
                quality = voice.quality.value if voice.quality else "enhanced"
                print(f"  {gender_symbol} {voice.name} ({quality})")

        if siri:
            print("\n🍎 VOCES SIRI:")
            for voice in sorted(siri, key=lambda v: v.name):
                gender_symbol = "♂" if voice.gender and voice.gender.value == "male" else "♀"
                print(f"  {gender_symbol} {voice.name}")

        if other:
            print("\n🌍 OTRAS VOCES:")
            for voice in sorted(other, key=lambda v: v.name):
                gender_symbol = "♂" if voice.gender and voice.gender.value == "male" else "♀"
                lang = voice.language.value if voice.language else "unknown"
                print(f"  {gender_symbol} {voice.name} ({lang})")

        print(f"\nTotal: {len(voices)} voces disponibles")

    async def speak_text(self, text: str, voice: Optional[str] = None,
                        rate: Optional[int] = None, pitch: Optional[float] = None,
                        volume: Optional[float] = None) -> None:
        """Speak text using TTS engine"""
        try:
            # Get configuration
            config = self.config_manager.get_config()

            # Simple TTS execution using macOS say command directly
            import subprocess

            voice_to_use = voice or getattr(config, 'TTS_NOTIFY_VOICE', 'monica')
            rate_to_use = str(rate or getattr(config, 'TTS_NOTIFY_RATE', 175))
            pitch_to_use = str(pitch or getattr(config, 'TTS_NOTIFY_PITCH', 1.0))

            # Build say command
            cmd = ['say', '-v', voice_to_use, '-r', rate_to_use]

            # Only add pitch if different from 1.0
            if pitch_to_use != '1.0':
                cmd.extend(['-p', pitch_to_use])

            cmd.append(text)

            # Execute TTS
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                if self.logger:
                    self.logger.info(f"Text spoken successfully: {text[:50]}...")
                print(f"✅ Texto reproducido con voz: {voice_to_use}")
            else:
                print(f"❌ Error: {result.stderr}")
                sys.exit(1)

        except (VoiceNotFoundError, ValidationError, TTSError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error inesperado: {e}")
            if self.logger:
                self.logger.exception("Unexpected error in speak_text")
            sys.exit(1)

    async def save_audio(self, text: str, filename: str, voice: Optional[str] = None,
                        rate: Optional[int] = None, pitch: Optional[float] = None,
                        volume: Optional[float] = None, audio_format: str = "aiff") -> None:
        """Save text as audio file"""
        try:
            # Get configuration
            config = self.config_manager.get_config()

            # Determine output path
            output_path = Path(filename)
            if not output_path.suffix:
                output_path = output_path.with_suffix(f".{audio_format}")

            if not output_path.is_absolute():
                output_dir = Path(getattr(config, 'TTS_NOTIFY_OUTPUT_DIR', Path.home() / "Desktop"))
                output_path = output_dir / output_path

            # Create TTS request
            request = TTSRequest(
                text=text,
                voice_name=voice or getattr(config, 'TTS_NOTIFY_VOICE', 'monica'),
                rate=rate or getattr(config, 'TTS_NOTIFY_RATE', 175),
                pitch=pitch or getattr(config, 'TTS_NOTIFY_PITCH', 1.0),
                volume=volume or getattr(config, 'TTS_NOTIFY_VOLUME', 1.0),
                language=getattr(config, 'TTS_NOTIFY_LANGUAGE', 'es'),
                output_format=AudioFormat(audio_format),
                output_path=str(output_path)
            )

            # Save audio
            response = await self.tts_engine.synthesize(request)

            print(f"✅ Audio guardado en: {output_path}")

            if self.logger:
                self.logger.info(f"Audio saved successfully: {output_path}")

        except (VoiceNotFoundError, ValidationError, TTSError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error inesperado: {e}")
            if self.logger:
                self.logger.exception("Unexpected error in save_audio")
            sys.exit(1)

    def show_mcp_config(self) -> None:
        """Show MCP configuration for Claude Desktop with real paths"""
        import json
        import subprocess
        import sys
        from pathlib import Path

        try:
            # Get the current Python executable path
            if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                # Virtual environment detected
                python_exe = sys.executable
            else:
                # Try to find a virtual environment in common locations
                project_root = Path(__file__).parent.parent.parent.parent
                venv_paths = [
                    project_root / "src" / "venv" / "bin" / "python",
                    project_root / "venv" / "bin" / "python",
                    Path.home() / ".local" / "share" / "tts-notify" / "venv" / "bin" / "python",
                ]

                python_exe = None
                for path in venv_paths:
                    if path.exists():
                        python_exe = str(path)
                        break

                if not python_exe:
                    python_exe = sys.executable

            # Get the MCP server script path
            current_dir = Path(__file__).parent.parent.parent.parent
            mcp_server_paths = [
                current_dir / "src" / "tts_notify" / "ui" / "mcp" / "server.py",
                current_dir / "src" / "mcp_server.py",
                Path("/Volumes/Resources/Develop/TTS-Notify/TTS_Notify/src/tts_notify/ui/mcp/server.py"),
            ]

            mcp_server_path = None
            for path in mcp_server_paths:
                if path.exists():
                    mcp_server_path = str(path)
                    break

            if not mcp_server_path:
                # Fallback: assume it's installed as a module
                mcp_server_path = "-m tts_notify.ui.mcp.server"

            # Create MCP configuration - use the orchestrator with mode mcp
            mcp_config = {
                "mcpServers": {
                    "tts-notify": {
                        "command": python_exe,
                        "args": ["-m", "tts_notify", "--mode", "mcp"]
                    }
                }
            }

            # Pretty print JSON configuration
            print("📋 Configuración MCP para Claude Desktop")
            print("=" * 50)
            print("Copie y pegue este JSON en su archivo de configuración:")
            print()
            print("📍 Ruta del archivo de configuración:")
            print("   ~/Library/Application Support/Claude/claude_desktop_config.json")
            print()
            print("📝 Configuración JSON:")
            print(json.dumps(mcp_config, indent=2))
            print()
            print("💡 Notas:")
            print("   • Asegúrese de que TTS Notify esté instalado correctamente")
            print("   • Reinicie Claude Desktop después de modificar la configuración")
            print("   • Las rutas mostradas son las rutas reales en su sistema")

            if self.logger:
                self.logger.info("MCP configuration displayed")

        except Exception as e:
            print(f"❌ Error generando configuración MCP: {e}")
            if self.logger:
                self.logger.error(f"Error generating MCP config: {e}")

    async def run(self, args: argparse.Namespace) -> None:
        """Main CLI execution method"""
        # Load configuration profile if specified
        if args.profile:
            self.config_manager.reload_config(args.profile)

        # Setup logging
        self.setup_logging()

        # Handle MCP configuration request
        if args.mcp_config:
            self.show_mcp_config()
            return

        # Handle different commands
        if args.list:
            await self.list_voices(
                compact=args.compact,
                gender=args.gen,
                language=args.lang
            )
        elif args.save:
            if not args.text:
                print("Error: Se requiere texto para guardar archivo de audio")
                sys.exit(1)
            await self.save_audio(
                text=args.text,
                filename=args.save,
                voice=args.voice,
                rate=args.rate,
                pitch=args.pitch,
                volume=args.volume,
                audio_format=args.format
            )
        elif args.text:
            await self.speak_text(
                text=args.text,
                voice=args.voice,
                rate=args.rate,
                pitch=args.pitch,
                volume=args.volume
            )
        else:
            print("Error: Se requiere texto o la opción --list")
            sys.exit(1)


async def main():
    """Main entry point for CLI"""
    cli = TTSNotifyCLI()
    parser = cli.create_parser()
    args = parser.parse_args()

    try:
        await cli.run(args)
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)


def sync_main():
    """Synchronous main entry point for CLI scripts"""
    cli = TTSNotifyCLI()
    parser = cli.create_parser()
    args = parser.parse_args()

    try:
        # Run the async main function
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    sync_main()