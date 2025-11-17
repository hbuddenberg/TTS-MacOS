"""
TTS-MacOS v2 - Unified MCP Server

Advanced MCP server supporting dual-engine architecture:
- Native engine for fast OS-level TTS
- AI engine for high-quality voice cloning
- Intelligent engine selection
- Comprehensive JSON parameter support
- Cross-platform compatibility (macOS/Linux)

Features:
- Automatic engine selection based on requirements
- Voice cloning from audio samples
- Multi-language support (16+ languages)
- Advanced audio parameters (pitch, emphasis, speed)
- Real-time voice preview and testing
- Session management and caching
"""

import asyncio
import json
import logging
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from .core.config import AudioFormat, Quality, TTSConfig, TTSRequest
from .engines import EngineSelector, EngineType
from .legacy import LegacyMCPServer


class UnifiedMCPServer:
    """
    Unified MCP server for TTS-MacOS v2 with dual-engine support
    """

    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self.mcp = FastMCP("tts-macos-v2")

        # Initialize engine selector
        self.engine_selector = EngineSelector()

        # Session management
        self.session_preferences = {}
        self.session_stats = {
            "total_synthesis": 0,
            "engine_usage": {"native": 0, "ai": 0},
            "start_time": time.time(),
        }

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Register MCP tools
        self._register_tools()

        self.logger.info("TTS-MacOS v2 MCP Server initialized")

    def _register_tools(self):
        """Register all MCP tools"""

        @self.mcp.tool()
        def tts_speak(
            text: str,
            engine: str = "auto",
            voice: Optional[str] = None,
            language: str = "en",
            rate: float = 1.0,
            volume: float = 1.0,
            pitch_adjustment: Optional[float] = None,
            format: str = "wav",
            quality: str = "balanced",
            speaker_wav: Optional[str] = None,
            model_name: Optional[str] = None,
            emphasis: str = "moderate",
            speed: Optional[float] = None,
        ) -> str:
            """
            🎯 Primary TTS synthesis with intelligent engine selection

            Automatically selects the best engine based on requirements:
            - Native engine: Fast synthesis, OS-level integration
            - AI engine: High quality, voice cloning, multilingual

            Args:
                text: Text to synthesize (required)
                engine: Engine choice (auto/native/ai)
                voice: Voice name or path to audio file for cloning
                language: Language code (es, en, fr, de, it, pt, etc.)
                rate: Speech rate (0.5-2.0, default 1.0)
                volume: Audio volume (0.0-2.0, default 1.0)
                pitch_adjustment: Pitch multiplier (0.5-2.0, AI engine only)
                format: Output format (wav/mp3/aiff)
                quality: Quality preference (fast/balanced/premium)
                speaker_wav: Path to WAV file for voice cloning (AI engine)
                model_name: Specific TTS model (xtts_v2, glow_tts, etc.)
                emphasis: Emphasis level (none/moderate/strong, AI engine)
                speed: Alternative speed control (0.5-2.0)

            Returns:
                Detailed synthesis result with engine used and audio info
            """
            try:
                # Create synthesis request
                request = TTSRequest(
                    text=text,
                    engine=EngineType(engine),
                    voice=voice,
                    language=language,
                    rate=rate,
                    volume=volume,
                    pitch_adjustment=pitch_adjustment,
                    format=AudioFormat(format),
                    quality=Quality(quality),
                    speaker_wav=speaker_wav,
                    model_name=model_name,
                    emphasis=emphasis,
                    speed=speed or rate,
                )

                # Select appropriate engine
                tts_engine = self.engine_selector.select_engine(
                    engine=request.engine,
                    voice_cloning=bool(request.speaker_wav),
                    language=request.language,
                    quality=request.quality,
                )

                # Determine engine type for logging
                engine_type = (
                    "ai"
                    if hasattr(tts_engine, "synthesize")
                    and hasattr(tts_engine, "config")
                    else "native"
                )

                # Synthesize speech
                start_time = time.time()

                if engine_type == "ai":
                    output_path = tts_engine.synthesize(
                        text=request.text,
                        voice=request.voice,
                        language=request.language,
                        rate=request.rate,
                        volume=request.volume,
                        output_file=None,  # Don't save file for speak
                        speaker_wav=request.speaker_wav,
                        model_name=request.model_name,
                        pitch_adjustment=request.pitch_adjustment,
                        emphasis=request.emphasis,
                        speed=request.speed,
                    )

                    # For AI engine, we need to play the audio
                    if output_path and Path(output_path).exists():
                        self._play_audio_file(output_path)

                else:
                    # Native engine synthesis and playback
                    output_path = tts_engine.synthesize(
                        text=request.text,
                        voice=request.voice,
                        rate=int(request.rate * 175)
                        if hasattr(tts_engine, "synthesize")
                        else request.rate,
                        volume=request.volume,
                        output_file=None,
                    )

                synthesis_time = time.time() - start_time

                # Update session stats
                self.session_stats["total_synthesis"] += 1
                self.session_stats["engine_usage"][engine_type] += 1

                # Store voice preference for session
                if request.voice:
                    self.session_preferences["last_voice"] = request.voice
                    self.session_preferences["last_language"] = request.language

                # Prepare result
                engine_name = (
                    "AI (Coqui TTS)"
                    if engine_type == "ai"
                    else f"Native ({tts_engine.system})"
                )
                voice_used = request.voice or "Default"

                result = (
                    f"✅ TTS Synthesis Complete\\n"
                    f"🔊 Engine: {engine_name}\\n"
                    f"🎤 Voice: {voice_used}\\n"
                    f"🌍 Language: {request.language}\\n"
                    f"⚡ Rate: {request.rate}x\\n"
                    f"🔊 Volume: {request.volume}x\\n"
                    f"📊 Quality: {request.quality.value}\\n"
                    f"⏱️  Time: {synthesis_time:.2f}s\\n"
                    f'📝 Text: "{request.text[:100]}{"..." if len(request.text) > 100 else ""}"'
                )

                if request.speaker_wav:
                    result += f"\\n🎭 Voice Cloning: {request.speaker_wav}"

                if request.pitch_adjustment and request.pitch_adjustment != 1.0:
                    result += f"\\n🎵 Pitch: {request.pitch_adjustment}x"

                return result

            except Exception as e:
                error_msg = f"❌ TTS synthesis failed: {str(e)}"
                self.logger.error(
                    f"TTS synthesis error: {e}\\n{traceback.format_exc()}"
                )
                return error_msg

        @self.mcp.tool()
        def tts_clone(
            speaker_wav: str,
            voice_name: str,
            description: Optional[str] = None,
            language: str = "en",
        ) -> str:
            """
            🎭 Create a voice clone from audio sample

            Creates a high-quality voice clone using just 6+ seconds of audio.
            The cloned voice can speak any language supported by XTTS-v2.

            Args:
                speaker_wav: Path to WAV audio file (6+ seconds recommended)
                voice_name: Name for the cloned voice
                description: Optional description of the voice
                language: Primary language for the voice

            Returns:
                Clone creation result with voice information
            """
            try:
                # Validate speaker WAV file
                if not Path(speaker_wav).exists():
                    return f"❌ Audio file not found: {speaker_wav}"

                # Get AI engine for cloning
                ai_engine = self.engine_selector.ai_engine
                if not ai_engine:
                    return "❌ AI engine not available for voice cloning"

                # Create voice clone
                clone_info = ai_engine.clone_voice(
                    speaker_wav=speaker_wav,
                    voice_name=voice_name,
                    description=description,
                )

                # Format result
                result = (
                    f"✅ Voice Clone Created Successfully\\n"
                    f"🎭 Voice Name: {clone_info['name']}\\n"
                    f"📁 Original File: {clone_info['original_file']}\\n"
                    f"🔧 Processed File: {clone_info['processed_file']}\\n"
                    f"📝 Description: {clone_info['description']}\\n"
                    f"🤖 Model: {clone_info['model']}\\n"
                    f"🎵 Sample Rate: {clone_info['sample_rate']} Hz"
                )

                return result

            except Exception as e:
                error_msg = f"❌ Voice cloning failed: {str(e)}"
                self.logger.error(f"Voice cloning error: {e}")
                return error_msg

        @self.mcp.tool()
        def tts_list_voices(
            engine: str = "all",
            language: Optional[str] = None,
            include_clones: bool = True,
        ) -> str:
            """
            📋 List available voices from all engines

            Comprehensive voice listing with categorization and filtering.

            Args:
                engine: Filter by engine (all/native/ai)
                language: Filter by language code (es, en, fr, etc.)
                include_clones: Include voice clones in results

            Returns:
                Detailed voice listing with engine information
            """
            try:
                voices_info = {"engines": {}}

                # Native engine voices
                if engine in ["all", "native"] and self.engine_selector.native_engine:
                    native_voices = self.engine_selector.native_engine.list_voices()
                    voices_info["engines"]["native"] = native_voices

                # AI engine voices
                if engine in ["all", "ai"] and self.engine_selector.ai_engine:
                    ai_voices = self.engine_selector.ai_engine.list_voices()
                    voices_info["engines"]["ai"] = ai_voices

                # Voice clones
                if include_clones and self.engine_selector.ai_engine:
                    clones = self.engine_selector.ai_engine.list_voice_clones()
                    if clones:
                        voices_info["clones"] = clones

                # Format output
                result_lines = [f"🎭 TTS-MacOS v2 - Available Voices\\n"]

                # Native voices
                if "native" in voices_info["engines"]:
                    native = voices_info["engines"]["native"]
                    if "error" not in native:
                        result_lines.append(
                            f"\\n🍎 Native Engine Voices ({native.get('total', 0)} total):"
                        )

                        for category, voices in native.items():
                            if (
                                category in ["spanish", "enhanced", "premium", "other"]
                                and voices
                            ):
                                result_lines.append(
                                    f"  📂 {category.title()} ({len(voices)}):"
                                )
                                for voice in voices[:5]:  # Limit to first 5 for brevity
                                    gender_icon = (
                                        "👨"
                                        if voice.get("gender") == "Masculino"
                                        else "👩"
                                    )
                                    result_lines.append(
                                        f"    {gender_icon} {voice['name']} - {voice.get('description', '')}"
                                    )

                                if len(voices) > 5:
                                    result_lines.append(
                                        f"    ... and {len(voices) - 5} more"
                                    )

                # AI voices
                if "ai" in voices_info["engines"]:
                    ai = voices_info["engines"]["ai"]
                    result_lines.append(f"\\n🤖 AI Engine Voices:")
                    result_lines.append(f"  🔧 Device: {ai.get('device', 'Unknown')}")
                    result_lines.append(
                        f"  🌐 Languages: {', '.join(ai.get('languages', []))}"
                    )
                    result_lines.append(
                        f"  🎭 Voice Cloning: {'✅' if ai.get('cloning_support') else '❌'}"
                    )

                    if ai.get("models"):
                        result_lines.append(f"\\n  📊 Available Models:")
                        for model_name, model_info in ai["models"].items():
                            status = (
                                "✅ Loaded"
                                if model_info.get("loaded")
                                else "📦 Available"
                            )
                            cloning = "🎭" if model_info.get("supports_cloning") else ""
                            result_lines.append(
                                f"    {status} {model_info['name']} {cloning} ({model_info['quality']})"
                            )

                # Voice clones
                if "clones" in voices_info:
                    clones = voices_info["clones"]
                    result_lines.append(f"\\n🎭 Custom Voice Clones ({len(clones)}):")
                    for clone in clones:
                        result_lines.append(
                            f"  🔊 {clone['name']} - {clone.get('description', 'No description')}"
                        )

                # Session stats
                result_lines.append(f"\\n📊 Session Statistics:")
                result_lines.append(
                    f"  🔊 Total Synthesis: {self.session_stats['total_synthesis']}"
                )
                result_lines.append(
                    f"  🍎 Native Engine: {self.session_stats['engine_usage']['native']}"
                )
                result_lines.append(
                    f"  🤖 AI Engine: {self.session_stats['engine_usage']['ai']}"
                )

                # Last used voice
                if self.session_preferences.get("last_voice"):
                    result_lines.append(
                        f"  🎤 Last Voice: {self.session_preferences['last_voice']}"
                    )

                return "\\n".join(result_lines)

            except Exception as e:
                return f"❌ Error listing voices: {str(e)}"

        @self.mcp.tool()
        def tts_save(
            text: str,
            filename: str,
            engine: str = "auto",
            voice: Optional[str] = None,
            language: str = "en",
            format: str = "wav",
            quality: str = "balanced",
            speaker_wav: Optional[str] = None,
        ) -> str:
            """
            💾 Save synthesized audio to file

            High-quality audio synthesis with file output support.

            Args:
                text: Text to synthesize
                filename: Output filename (without extension)
                engine: Engine choice (auto/native/ai)
                voice: Voice name or cloning audio path
                language: Language code
                format: Audio format (wav/mp3/aiff)
                quality: Quality preference
                speaker_wav: Path for voice cloning

            Returns:
                File save result with path and information
            """
            try:
                # Create output path
                output_dir = Path.home() / "Desktop" / "TTS-MacOS-v2"
                output_dir.mkdir(parents=True, exist_ok=True)

                output_file = output_dir / f"{filename}.{format}"

                # Create synthesis request
                request = TTSRequest(
                    text=text,
                    engine=EngineType(engine),
                    voice=voice,
                    language=language,
                    format=AudioFormat(format),
                    quality=quality,
                    speaker_wav=speaker_wav,
                    output_path=str(output_file),
                )

                # Select engine and synthesize
                tts_engine = self.engine_selector.select_engine(
                    engine=request.engine,
                    voice_cloning=bool(request.speaker_wav),
                    language=request.language,
                    quality=request.quality,
                )

                # Synthesize to file
                if hasattr(tts_engine, "config"):  # AI engine
                    result_path = tts_engine.synthesize(
                        text=request.text,
                        voice=request.voice,
                        language=request.language,
                        output_file=str(output_file),
                        speaker_wav=request.speaker_wav,
                        format=request.format.value,
                    )
                else:  # Native engine
                    result_path = tts_engine.synthesize(
                        text=request.text,
                        voice=request.voice,
                        output_file=str(output_file),
                    )

                if result_path and Path(result_path).exists():
                    # Get file info
                    file_stat = Path(result_path).stat()
                    file_size_mb = file_stat.st_size / (1024 * 1024)

                    engine_type = "AI" if hasattr(tts_engine, "config") else "Native"

                    result = (
                        f"✅ Audio Saved Successfully\\n"
                        f"📁 File: {result_path}\\n"
                        f"🔊 Engine: {engine_type}\\n"
                        f"🎤 Voice: {request.voice or 'Default'}\\n"
                        f"🌍 Language: {request.language}\\n"
                        f"📊 Format: {request.format.value.upper()}\\n"
                        f"💾 Size: {file_size_mb:.2f} MB\\n"
                        f'📝 Text: "{request.text[:100]}{"..." if len(request.text) > 100 else ""}"'
                    )

                    if request.speaker_wav:
                        result += f"\\n🎭 Voice Cloning: {request.speaker_wav}"

                    return result
                else:
                    return "❌ Audio file was not created"

            except Exception as e:
                return f"❌ Error saving audio: {str(e)}"

        @self.mcp.tool()
        def tts_preview(
            voice: str,
            engine: str = "auto",
            language: str = "en",
            sample_text: Optional[str] = None,
        ) -> str:
            """
            🔊 Preview a voice with sample text

            Test how a voice sounds with a short sample.

            Args:
                voice: Voice name to test
                engine: Engine choice (auto/native/ai)
                language: Language code
                sample_text: Custom text (optional, uses default if not provided)

            Returns:
                Preview result with voice information
            """
            try:
                # Default sample text based on language
                if not sample_text:
                    samples = {
                        "en": "Hello, this is a voice preview test. The quick brown fox jumps over the lazy dog.",
                        "es": "Hola, esta es una prueba de voz. El veloz murciélago hindú comía feliz cardillo y kiwi.",
                        "fr": "Bonjour, ceci est un test d'évaluation vocale. La cigogne et le singe sont dans le bain.",
                        "de": "Hallo, dies ist ein Sprachtest. Falsches Üben von Xylophonmusik jagt alle Gespenster weg.",
                        "it": "Ciao, questo è un test di valutazione vocale. In quel luogo di Tony attese gli altri e gli chiese aiuto.",
                    }
                    sample_text = samples.get(language, samples["en"])

                # Create short preview request
                request = TTSRequest(
                    text=sample_text,
                    engine=EngineType(engine),
                    voice=voice,
                    language=language,
                    quality=Quality.BALANCED,
                )

                # Select and test engine
                tts_engine = self.engine_selector.select_engine(
                    engine=request.engine, language=request.language
                )

                engine_type = "AI" if hasattr(tts_engine, "config") else "Native"

                # Test voice availability
                if hasattr(tts_engine, "get_voice_info"):
                    voice_info = tts_engine.get_voice_info(voice)
                    if voice_info:
                        voice_details = f" ({voice_info.get('description', '')})"
                    else:
                        voice_details = " (not found)"
                else:
                    voice_details = ""

                # Perform synthesis
                start_time = time.time()

                if engine_type == "ai":
                    output_path = tts_engine.synthesize(
                        text=request.text,
                        voice=request.voice,
                        language=request.language,
                        output_file=None,
                    )
                    if output_path:
                        self._play_audio_file(output_path)
                else:
                    tts_engine.synthesize(
                        text=request.text, voice=request.voice, output_file=None
                    )

                synthesis_time = time.time() - start_time

                result = (
                    f"🔊 Voice Preview Complete\\n"
                    f"🎤 Voice: {voice}{voice_details}\\n"
                    f"🔊 Engine: {engine_type}\\n"
                    f"🌍 Language: {language}\\n"
                    f"⏱️  Time: {synthesis_time:.2f}s\\n"
                    f'📝 Text: "{request.text}"'
                )

                return result

            except Exception as e:
                return f"❌ Voice preview failed: {str(e)}"

        @self.mcp.tool()
        def tts_info() -> str:
            """
            ℹ️ Get TTS-MacOS v2 system information

            Returns detailed system information including:
            - Available engines and their status
            - Platform information
            - Model cache status
            - Session statistics

            Returns:
                Comprehensive system information
            """
            try:
                info_lines = ["🤖 TTS-MacOS v2 - System Information\\n"]

                # Engine information
                engine_info = self.engine_selector.get_engine_info()
                info_lines.append("🔧 Available Engines:")

                for engine_name, info in engine_info.items():
                    status = "✅" if info["available"] else "❌"
                    info_lines.append(
                        f"  {status} {engine_name.title()}: {info['type']}"
                    )

                    if engine_name == "ai_engine" and info["available"]:
                        info_lines.append(
                            f"    🎭 Voice Cloning: {info['voice_cloning']}"
                        )
                        info_lines.append(
                            f"    📦 Models: {', '.join(info['models_loaded'])}"
                        )

                # Platform information
                platform_info = self.config.get_platform_info()
                info_lines.append(f"\\n💻 Platform Information:")
                info_lines.append(f"  🖥️  System: {platform_info['system']}")
                info_lines.append(f"  🏗️  Architecture: {platform_info['architecture']}")
                info_lines.append(f"  🐍 Python: {platform_info['python_version']}")

                if "cuda_available" in platform_info:
                    info_lines.append(
                        f"  🔥 CUDA: {'✅' if platform_info['cuda_available'] else '❌'}"
                    )

                # Cache information
                cache_size = self.config.get_cache_size()
                info_lines.append(f"\\n📦 Cache Information:")
                info_lines.append(f"  💾 Size: {cache_size} MB")
                info_lines.append(f"  📁 Location: {self.config.cache_dir}")

                # List cached models
                cached_models = []
                for model_name in self.config.models.keys():
                    if self.config.is_model_cached(model_name):
                        cached_models.append(model_name)

                if cached_models:
                    info_lines.append(f"  🎯 Cached Models: {', '.join(cached_models)}")

                # Session statistics
                session_time = time.time() - self.session_stats["start_time"]
                info_lines.append(f"\\n📊 Session Statistics:")
                info_lines.append(f"  ⏱️  Duration: {session_time:.1f}s")
                info_lines.append(
                    f"  🔊 Total Synthesis: {self.session_stats['total_synthesis']}"
                )
                info_lines.append(
                    f"  🍎 Native Engine: {self.session_stats['engine_usage']['native']}"
                )
                info_lines.append(
                    f"  🤖 AI Engine: {self.session_stats['engine_usage']['ai']}"
                )

                return "\\n".join(info_lines)

            except Exception as e:
                return f"❌ Error getting system info: {str(e)}"

    def _play_audio_file(self, file_path: str):
        """Play audio file using system player"""
        try:
            import platform
            import subprocess

            system = platform.system()

            if system == "Darwin":  # macOS
                subprocess.run(["afplay", file_path], check=True)
            elif system == "Linux":
                subprocess.run(["aplay", file_path], check=True)
            else:
                self.logger.warning(f"No audio player available for {system}")

        except Exception as e:
            self.logger.warning(f"Could not play audio file {file_path}: {e}")

    def get_server(self) -> FastMCP:
        """Get the MCP server instance"""
        return self.mcp

    async def run(self):
        """Start the MCP server"""
        await self.mcp.run()


# Legacy compatibility
class LegacyMCPServerWrapper:
    """Wrapper for legacy v1.4.4 MCP server"""

    def __init__(self):
        self.legacy_server = LegacyMCPServer()

    async def run(self):
        """Run legacy server for backward compatibility"""
        await self.legacy_server.run()


# Factory function
def create_server(version: str = "v2") -> Any:
    """Create appropriate MCP server version"""
    if version == "v2":
        return UnifiedMCPServer()
    elif version == "legacy" or version == "v1":
        return LegacyMCPServerWrapper()
    else:
        raise ValueError(f"Unknown server version: {version}")


# Main function
async def main():
    """Main entry point for the MCP server"""
    import sys

    # Check for legacy mode
    if len(sys.argv) > 1 and sys.argv[1] == "--legacy":
        server = create_server("legacy")
    else:
        server = create_server("v2")

    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
