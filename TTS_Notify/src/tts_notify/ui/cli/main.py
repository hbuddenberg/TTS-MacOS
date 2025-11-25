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
from ...core.tts_engine import engine_registry, bootstrap_engines
from ...core.models import TTSRequest, AudioFormat, TTSEngineType, Voice
from ...core.exceptions import TTSNotifyError, VoiceNotFoundError, ValidationError, TTSError, EngineNotAvailableError
from ...utils.logger import setup_logging, get_logger


class TTSNotifyCLI:
    """Main CLI class for TTS Notify v2"""

    def __init__(self):
        self.config_manager = config_manager
        self.voice_manager = VoiceManager()
        self.logger = None
        self._engines_initialized = False

    async def initialize_engines(self):
        """Initialize TTS engines based on configuration"""
        if not self._engines_initialized:
            config = self.config_manager.get_config()
            await bootstrap_engines(config)
            self._engines_initialized = True
            if self.logger:
                self.logger.info("TTS engines initialized successfully")

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
Ejemplos (v2.0.0 + v3.0.0 CoquiTTS):
  tts-notify "Hola mundo"
  tts-notify "Hola mundo" --voice monica --rate 200
  tts-notify "Hello world" --engine coqui --language en
  tts-notify "Bonjour le monde" --engine coqui --model xtts_v2 --language fr
  tts-notify --list
  tts-notify --list-languages              # Listar idiomas CoquiTTS
  tts-notify --download-language fr        # Descargar idioma francés
  tts-notify --model-status                # Estado de modelos CoquiTTS
  tts-notify --list --compact
  tts-notify --list --gen female
  tts-notify --list --lang es_ES
  tts-notify "Test" --save output_file
  tts-notify --mcp-config                 # Mostrar configuración MCP para Claude Desktop

Para búsqueda flexible de voces:
  tts-notify "Test" --voice angelica     # Encuentra Angélica
  tts-notify "Test" --voice "jorge enhanced"  # Variante Enhanced
  tts-notify "Test" --voice siri         # Siri si está instalada

CoquiTTS (v3.0.0+):
  tts-notify "Hello" --engine coqui --voice Daniel --language en
  tts-notify "Hola" --engine coqui --language es --force-language
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

        # Engine selection (v3.0.0+)
        parser.add_argument(
            "--engine", "-e",
            choices=["macos", "coqui"],
            help="Motor TTS a utilizar (default: configurado en TTS_NOTIFY_ENGINE)"
        )
        parser.add_argument(
            "--model", "-m",
            help="Modelo CoquiTTS específico (default: xtts_v2)"
        )
        parser.add_argument(
            "--language", "-L",
            choices=["auto", "en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "zh", "ja", "ko"],
            help="Idioma para CoquiTTS (auto=detección automática)"
        )
        parser.add_argument(
            "--force-language",
            action="store_true",
            help="Forzar idioma específico ignorando detección automática"
        )

        # CoquiTTS management commands (v3.0.0+)
        parser.add_argument(
            "--list-languages",
            action="store_true",
            help="Listar idiomas disponibles en CoquiTTS"
        )
        parser.add_argument(
            "--download-language",
            metavar="LANG",
            choices=["en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "zh", "ja", "ko"],
            help="Descargar modelo para idioma específico de CoquiTTS"
        )
        parser.add_argument(
            "--model-status",
            action="store_true",
            help="Mostrar estado de los modelos CoquiTTS"
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
            "--lang",
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
            version="%(prog)s 3.0.0 (Phase A - CoquiTTS Integration)"
        )

        return parser

    async def list_voices(self, compact: bool = False, gender: Optional[str] = None,
                         language: Optional[str] = None, engine: Optional[str] = None) -> None:
        """List available voices with optional filtering"""
        try:
            # Initialize engines first
            await self.initialize_engines()

            if engine == "coqui":
                # For CoquiTTS, list available speakers for the current model
                await self._list_coqui_voices()
                return

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

    async def _list_coqui_voices(self) -> None:
        """List CoquiTTS available voices/speakers"""
        try:
            coqui_engine = engine_registry.get("coqui")
            if coqui_engine:
                voices = await coqui_engine.get_supported_voices()

                print("\n🤖 VOCES COQUITTS:")
                print("=" * 40)

                if voices:
                    for voice in sorted(voices, key=lambda v: v.name):
                        gender_symbol = "♂" if voice.gender and voice.gender.value == "male" else "♀"
                        lang = voice.language.value if voice.language else "unknown"
                        quality = voice.quality.value if voice.quality else "basic"
                        print(f"  {gender_symbol} {voice.name} ({lang}, {quality})")
                        if voice.description:
                            print(f"      {voice.description}")
                    print(f"\nTotal: {len(voices)} voces CoquiTTS")
                else:
                    print("  No se encontraron voces CoquiTTS disponibles")
                    print("  Ejecute: tts-notify --model-status para verificar el estado")
            else:
                print("❌ Motor CoquiTTS no disponible")
                print("   Instale con: pip install coqui-tts o configure TTS_NOTIFY_ENGINE=coqui")

        except EngineNotAvailableError:
            print("❌ Motor CoquiTTS no disponible")
            print("   Instale con: pip install coqui-tts")
        except Exception as e:
            print(f"❌ Error listando voces CoquiTTS: {e}")

    async def list_languages(self) -> None:
        """List available CoquiTTS languages"""
        try:
            coqui_engine = engine_registry.get("coqui")
            if coqui_engine and hasattr(coqui_engine, 'multi_language_models'):
                print("\n🌍 IDIOMAS DISPONIBLES EN COQUITTS:")
                print("=" * 50)

                current_model = coqui_engine.model_name
                model_info = coqui_engine.multi_language_models.get(current_model)

                if model_info:
                    print(f"\nModelo actual: {current_model}")
                    print(f"Idiomas soportados: {len(model_info.languages)}")
                    print(f"Calidad: {model_info.quality}")
                    print(f"Locutores: {model_info.speakers}")
                    print(f"Tamaño: ~{model_info.size_gb}GB")

                    print(f"\n📋 Idiomas disponibles:")
                    for i, lang in enumerate(model_info.languages, 1):
                        lang_names = {
                            "en": "Inglés", "es": "Español", "fr": "Francés",
                            "de": "Alemán", "it": "Italiano", "pt": "Portugués",
                            "nl": "Neerlandés", "pl": "Polaco", "ru": "Ruso",
                            "zh": "Chino", "ja": "Japonés", "ko": "Coreano"
                        }
                        lang_name = lang_names.get(lang, lang.upper())
                        print(f"  {i:2d}. {lang} ({lang_name})")
                else:
                    print("❌ Información del modelo no disponible")
            else:
                print("❌ Motor CoquiTTS no disponible o no soporta multi-idioma")

        except Exception as e:
            print(f"❌ Error listando idiomas: {e}")

    async def download_language(self, language: str) -> None:
        """Download CoquiTTS language model"""
        try:
            print(f"📥 Descargando idioma '{language}' para CoquiTTS...")

            coqui_engine = engine_registry.get("coqui")
            if coqui_engine and hasattr(coqui_engine, 'ensure_language_available'):
                success = await coqui_engine.ensure_language_available(language)

                if success:
                    print(f"✅ Idioma '{language}' descargado y disponible")
                else:
                    print(f"❌ Error descargando idioma '{language}'")
                    print("   Verifique su conexión a internet y espacio en disco")
            else:
                print("❌ Motor CoquiTTS no disponible")

        except Exception as e:
            print(f"❌ Error descargando idioma: {e}")

    async def show_model_status(self) -> None:
        """Show CoquiTTS model status"""
        try:
            config = self.config_manager.get_config()

            print("\n🤖 ESTADO DE MODELOS COQUITTS:")
            print("=" * 50)

            # Check CoquiTTS availability
            try:
                coqui_engine = engine_registry.get("coqui")
                if coqui_engine:
                    current_model = coqui_engine.model_name
                    model_info = coqui_engine.multi_language_models.get(current_model)

                    print(f"✅ Motor CoquiTTS disponible")
                    print(f"📍 Modelo actual: {current_model}")

                    if model_info:
                        print(f"📊 Estado del modelo:")
                        print(f"   • Idiomas: {len(model_info.languages)}")
                        print(f"   • Locutores: {model_info.speakers}")
                        print(f"   • Calidad: {model_info.quality}")
                        print(f"   • Tamaño: ~{model_info.size_gb}GB")
                        print(f"   • GPU: {'Sí' if coqui_engine.use_gpu else 'No'}")

                        # Check model download status
                        if hasattr(coqui_engine, 'is_model_downloaded'):
                            downloaded = coqui_engine.is_model_downloaded()
                            print(f"   • Descargado: {'Sí' if downloaded else 'No'}")
                    else:
                        print("⚠️  Información del modelo no disponible")
                else:
                    print("❌ Motor CoquiTTS no registrado")

            except EngineNotAvailableError:
                print("❌ Motor CoquiTTS no disponible")

            # Configuration
            print(f"\n⚙️  Configuración:")
            print(f"   • Motor por defecto: {config.TTS_NOTIFY_ENGINE}")
            print(f"   • Auto-descargar modelos: {config.TTS_NOTIFY_AUTO_DOWNLOAD_MODELS}")
            print(f"   • Modo offline: {config.TTS_NOTIFY_COQUI_OFFLINE_MODE}")
            print(f"   • Usar GPU: {config.TTS_NOTIFY_COQUI_USE_GPU}")
            print(f"   • Cache modelos: {config.TTS_NOTIFY_COQUI_CACHE_MODELS}")

            # Installation suggestion
            if not engine_registry.get("coqui"):
                print(f"\n💡 Instalación:")
                print(f"   pip install coqui-tts torchaudio soundfile")
                print(f"   O bien:")
                print(f"   pip install -e .[coqui]")

        except Exception as e:
            print(f"❌ Error obteniendo estado de modelos: {e}")

    async def speak_text(self, text: str, voice: Optional[str] = None,
                        rate: Optional[int] = None, pitch: Optional[float] = None,
                        volume: Optional[float] = None, engine: Optional[str] = None,
                        model: Optional[str] = None, language: Optional[str] = None,
                        force_language: bool = False) -> None:
        """Speak text using TTS engine (v3.0.0 with CoquiTTS support)"""
        try:
            # Initialize engines first
            await self.initialize_engines()

            # Get configuration
            config = self.config_manager.get_config()

            # Determine engine to use
            engine_name = engine or config.TTS_NOTIFY_ENGINE

            if engine_name == "coqui":
                await self._speak_with_coqui(text, voice, rate, pitch, volume, model, language, force_language, config)
            else:
                # Default to macOS engine
                await self._speak_with_macos(text, voice, rate, pitch, volume, config)

        except (VoiceNotFoundError, ValidationError, TTSError, EngineNotAvailableError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error inesperado: {e}")
            if self.logger:
                self.logger.exception("Unexpected error in speak_text")
            sys.exit(1)

    async def _speak_with_macos(self, text: str, voice: Optional[str] = None,
                               rate: Optional[int] = None, pitch: Optional[float] = None,
                               volume: Optional[float] = None, config=None) -> None:
        """Speak text using macOS TTS engine"""
        try:
            # Get voice from voice manager
            voice_name = voice or config.TTS_NOTIFY_VOICE
            voice_obj = await self.voice_manager.find_voice(voice_name)
            if not voice_obj:
                voice_obj = await self.voice_manager.find_voice("monica")  # fallback

            # Create TTS request
            request = TTSRequest(
                text=text,
                voice=voice_obj,
                rate=rate or config.TTS_NOTIFY_RATE,
                pitch=pitch or config.TTS_NOTIFY_PITCH,
                volume=volume or config.TTS_NOTIFY_VOLUME,
                output_format=AudioFormat.AIFF
            )

            # Use engine registry
            macos_engine = engine_registry.get("macos")
            response = await macos_engine.speak(request)

            if response.success:
                if self.logger:
                    self.logger.info(f"Text spoken successfully with macOS engine: {text[:50]}...")
                engine_used = f"macOS ({voice_obj.name})"
                print(f"✅ Texto reproducido con motor: {engine_used}")
            else:
                print(f"❌ Error: {response.error}")
                sys.exit(1)

        except Exception as e:
            # Fallback to direct subprocess if engine fails
            import subprocess
            voice_to_use = voice or config.TTS_NOTIFY_VOICE
            rate_to_use = str(rate or config.TTS_NOTIFY_RATE)

            cmd = ['say', '-v', voice_to_use, '-r', rate_to_use]
            cmd.append(text)

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ Texto reproducido con voz: {voice_to_use} (fallback directo)")
            else:
                print(f"❌ Error: {result.stderr}")
                sys.exit(1)

    async def _speak_with_coqui(self, text: str, voice: Optional[str] = None,
                              rate: Optional[int] = None, pitch: Optional[float] = None,
                              volume: Optional[float] = None, model: Optional[str] = None,
                              language: Optional[str] = None, force_language: bool = False,
                              config=None) -> None:
        """Speak text using CoquiTTS engine"""
        try:
            coqui_engine = engine_registry.get("coqui")
            if not coqui_engine:
                print("❌ Motor CoquiTTS no disponible. Instale con: pip install coqui-tts")
                sys.exit(1)

            # For CoquiTTS, we need to handle voice differently since it uses speaker names
            # For now, we'll use the default voice from the engine
            voices = await coqui_engine.get_supported_voices()
            voice_obj = None

            if voice:
                # Try to find matching voice in CoquiTTS voices
                for v in voices:
                    if v.name.lower() == voice.lower() or v.id.lower() == voice.lower():
                        voice_obj = v
                        break

            if not voice_obj and voices:
                voice_obj = voices[0]  # Use first available voice

            if not voice_obj:
                print("❌ No hay voces CoquiTTS disponibles")
                sys.exit(1)

            # Create TTS request with CoquiTTS specific parameters
            request = TTSRequest(
                text=text,
                voice=voice_obj,
                rate=rate or config.TTS_NOTIFY_RATE,
                pitch=pitch or config.TTS_NOTIFY_PITCH,
                volume=volume or config.TTS_NOTIFY_VOLUME,
                engine_type=TTSEngineType.COQUI,
                language=language or config.TTS_NOTIFY_DEFAULT_LANGUAGE,
                force_language=force_language,
                model_name=model or config.TTS_NOTIFY_COQUI_MODEL,
                auto_download=config.TTS_NOTIFY_AUTO_DOWNLOAD_MODELS,
                output_format=AudioFormat.WAV  # CoquiTTS typically uses WAV
            )

            response = await coqui_engine.speak(request)

            if response.success:
                if self.logger:
                    self.logger.info(f"Text spoken successfully with CoquiTTS: {text[:50]}...")
                engine_used = f"CoquiTTS ({voice_obj.name})"
                lang_used = language or "auto"
                print(f"✅ Texto reproducido con motor: {engine_used} [idioma: {lang_used}]")
            else:
                print(f"❌ Error CoquiTTS: {response.error}")
                sys.exit(1)

        except Exception as e:
            print(f"❌ Error con motor CoquiTTS: {e}")
            if "No module named 'TTS'" in str(e):
                print("   💡 Instale CoquiTTS: pip install coqui-tts torchaudio soundfile")
            sys.exit(1)

    async def save_audio(self, text: str, filename: str, voice: Optional[str] = None,
                        rate: Optional[int] = None, pitch: Optional[float] = None,
                        volume: Optional[float] = None, audio_format: str = "aiff",
                        engine: Optional[str] = None, model: Optional[str] = None,
                        language: Optional[str] = None, force_language: bool = False) -> None:
        """Save text as audio file (v3.0.0 with CoquiTTS support)"""
        try:
            # Initialize engines first
            await self.initialize_engines()

            # Get configuration
            config = self.config_manager.get_config()

            # Determine output path
            output_path = Path(filename)
            if not output_path.suffix:
                output_path = output_path.with_suffix(f".{audio_format}")

            if not output_path.is_absolute():
                output_dir = Path(getattr(config, 'TTS_NOTIFY_OUTPUT_DIR', Path.home() / "Desktop"))
                output_path = output_dir / output_path

            # Determine engine to use
            engine_name = engine or config.TTS_NOTIFY_ENGINE

            if engine_name == "coqui":
                await self._save_with_coqui(text, output_path, voice, rate, pitch, volume,
                                         audio_format, model, language, force_language, config)
            else:
                await self._save_with_macos(text, output_path, voice, rate, pitch, volume,
                                          audio_format, config)

        except (VoiceNotFoundError, ValidationError, TTSError, EngineNotAvailableError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error inesperado: {e}")
            if self.logger:
                self.logger.exception("Unexpected error in save_audio")
            sys.exit(1)

    async def _save_with_macos(self, text: str, output_path: Path, voice: Optional[str] = None,
                              rate: Optional[int] = None, pitch: Optional[float] = None,
                              volume: Optional[float] = None, audio_format: str = "aiff",
                              config=None) -> None:
        """Save audio using macOS TTS engine"""
        try:
            # Get voice from voice manager
            voice_name = voice or config.TTS_NOTIFY_VOICE
            voice_obj = await self.voice_manager.find_voice(voice_name)
            if not voice_obj:
                voice_obj = await self.voice_manager.find_voice("monica")  # fallback

            # Create TTS request
            request = TTSRequest(
                text=text,
                voice=voice_obj,
                rate=rate or config.TTS_NOTIFY_RATE,
                pitch=pitch or config.TTS_NOTIFY_PITCH,
                volume=volume or config.TTS_NOTIFY_VOLUME,
                output_format=AudioFormat(audio_format),
                output_path=output_path
            )

            # Use engine registry
            macos_engine = engine_registry.get("macos")
            response = await macos_engine.save(request, output_path)

            if response.success:
                print(f"✅ Audio guardado en: {output_path} (macOS)")
                if self.logger:
                    self.logger.info(f"Audio saved with macOS engine: {output_path}")
            else:
                print(f"❌ Error: {response.error}")
                sys.exit(1)

        except Exception as e:
            print(f"❌ Error guardando audio con macOS: {e}")
            sys.exit(1)

    async def _save_with_coqui(self, text: str, output_path: Path, voice: Optional[str] = None,
                             rate: Optional[int] = None, pitch: Optional[float] = None,
                             volume: Optional[float] = None, audio_format: str = "wav",
                             model: Optional[str] = None, language: Optional[str] = None,
                             force_language: bool = False, config=None) -> None:
        """Save audio using CoquiTTS engine"""
        try:
            coqui_engine = engine_registry.get("coqui")
            if not coqui_engine:
                print("❌ Motor CoquiTTS no disponible. Instale con: pip install coqui-tts")
                sys.exit(1)

            # Get CoquiTTS voice (similar to _speak_with_coqui)
            voices = await coqui_engine.get_supported_voices()
            voice_obj = None

            if voice:
                for v in voices:
                    if v.name.lower() == voice.lower() or v.id.lower() == voice.lower():
                        voice_obj = v
                        break

            if not voice_obj and voices:
                voice_obj = voices[0]

            if not voice_obj:
                print("❌ No hay voces CoquiTTS disponibles")
                sys.exit(1)

            # Create TTS request with CoquiTTS parameters
            request = TTSRequest(
                text=text,
                voice=voice_obj,
                rate=rate or config.TTS_NOTIFY_RATE,
                pitch=pitch or config.TTS_NOTIFY_PITCH,
                volume=volume or config.TTS_NOTIFY_VOLUME,
                engine_type=TTSEngineType.COQUI,
                language=language or config.TTS_NOTIFY_DEFAULT_LANGUAGE,
                force_language=force_language,
                model_name=model or config.TTS_NOTIFY_COQUI_MODEL,
                auto_download=config.TTS_NOTIFY_AUTO_DOWNLOAD_MODELS,
                output_format=AudioFormat(audio_format),
                output_path=output_path
            )

            response = await coqui_engine.save(request, output_path)

            if response.success:
                lang_used = language or "auto"
                print(f"✅ Audio guardado en: {output_path} (CoquiTTS [idioma: {lang_used}])")
                if self.logger:
                    self.logger.info(f"Audio saved with CoquiTTS engine: {output_path}")
            else:
                print(f"❌ Error CoquiTTS: {response.error}")
                sys.exit(1)

        except Exception as e:
            print(f"❌ Error guardando audio con CoquiTTS: {e}")
            if "No module named 'TTS'" in str(e):
                print("   💡 Instale CoquiTTS: pip install coqui-tts torchaudio soundfile")
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
        """Main CLI execution method (v3.0.0 with CoquiTTS support)"""
        # Load configuration profile if specified
        if args.profile:
            self.config_manager.reload_config(args.profile)

        # Setup logging
        self.setup_logging()

        # Handle MCP configuration request
        if args.mcp_config:
            self.show_mcp_config()
            return

        # Handle CoquiTTS management commands
        if args.list_languages:
            await self.list_languages()
            return

        if args.download_language:
            await self.download_language(args.download_language)
            return

        if args.model_status:
            await self.show_model_status()
            return

        # Handle voice listing with engine support
        if args.list:
            await self.list_voices(
                compact=args.compact,
                gender=args.gen,
                language=args.lang,
                engine=args.engine
            )
            return

        # Handle save command with CoquiTTS support
        if args.save:
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
                audio_format=args.format,
                engine=args.engine,
                model=args.model,
                language=args.language,
                force_language=args.force_language
            )
            return

        # Handle speak command with CoquiTTS support
        if args.text:
            await self.speak_text(
                text=args.text,
                voice=args.voice,
                rate=args.rate,
                pitch=args.pitch,
                volume=args.volume,
                engine=args.engine,
                model=args.model,
                language=args.language,
                force_language=args.force_language
            )
            return

        # No valid command provided
        print("Error: Se requiere texto o alguna de las opciones disponibles")
        print("Use --help para ver todas las opciones disponibles")
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