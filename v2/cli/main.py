"""
TTS-MacOS v2 - Enhanced CLI Interface

Advanced command-line interface supporting dual-engine architecture:
- Native and AI engine selection
- Voice cloning commands
- Multi-platform support
- Comprehensive voice management
- Batch processing capabilities
- Interactive voice preview

Features:
- Intelligent engine selection
- Voice cloning and management
- Cross-platform compatibility
- Progress indicators
- Configuration management
- Voice quality testing
"""

import argparse
import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..core.config import AudioFormat, Quality, TTSConfig, TTSRequest

# Import v2 components
from ..engines import EngineSelector, EngineType
from ..legacy.cli import LegacyCLI


class EnhancedCLI:
    """
    Enhanced CLI for TTS-MacOS v2 with dual-engine support
    """

    def __init__(self):
        self.config = TTSConfig()
        self.engine_selector = EngineSelector()
        self.legacy_cli = LegacyCLI()  # For backward compatibility

    def create_parser(self) -> argparse.ArgumentParser:
        """Create comprehensive argument parser"""
        parser = argparse.ArgumentParser(
            prog="tts-macos-v2",
            description="TTS-MacOS v2 - Dual-Engine Text-to-Speech with AI Voice Cloning",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Basic synthesis
  %(prog)s "Hello world" --engine auto
  %(prog)s "Hola mundo" --voice monica --language es

  # Voice cloning
  %(prog)s clone-voice my_voice.wav --name "My Voice"
  %(prog)s "Cloned speech" --voice "My Voice" --engine ai

  # Save to file
  %(prog)s "Save this" --output speech.wav --format wav

  # Voice management
  %(prog)s list-voices --engine all
  %(prog)s preview-voice monica --language es

  # Batch processing
  %(prog)s batch *.txt --output-dir ./audio/

  # Configuration
  %(prog)s config --show
  %(prog)s config --set default_engine=ai
            """,
        )

        # Subcommands
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Main synthesis command (default)
        synthesize_parser = subparsers.add_parser(
            "synthesize", help="Synthesize speech (default)"
        )
        self._add_synthesize_args(synthesize_parser)

        # Voice cloning
        clone_parser = subparsers.add_parser(
            "clone-voice", help="Clone voice from audio sample"
        )
        self._add_clone_args(clone_parser)

        # Voice listing
        list_parser = subparsers.add_parser("list-voices", help="List available voices")
        self._add_list_args(list_parser)

        # Voice preview
        preview_parser = subparsers.add_parser("preview-voice", help="Preview a voice")
        self._add_preview_args(preview_parser)

        # Batch processing
        batch_parser = subparsers.add_parser(
            "batch", help="Process multiple text files"
        )
        self._add_batch_args(batch_parser)

        # Configuration
        config_parser = subparsers.add_parser("config", help="Manage configuration")
        self._add_config_args(config_parser)

        # System info
        info_parser = subparsers.add_parser("info", help="Show system information")

        # Legacy mode
        legacy_parser = subparsers.add_parser("legacy", help="Use v1.x legacy commands")
        self._add_legacy_args(legacy_parser)

        return parser

    def _add_synthesize_args(self, parser):
        """Add synthesis arguments"""
        parser.add_argument("text", nargs="?", help="Text to synthesize")

        parser.add_argument(
            "-e",
            "--engine",
            choices=["auto", "native", "ai"],
            default="auto",
            help="TTS engine to use (default: auto)",
        )

        parser.add_argument(
            "-v", "--voice", help="Voice name or path to audio file for cloning"
        )

        parser.add_argument(
            "-l",
            "--language",
            default="en",
            help="Language code (es, en, fr, de, it, pt, etc.)",
        )

        parser.add_argument(
            "-r",
            "--rate",
            type=float,
            default=1.0,
            help="Speech rate multiplier (0.5-2.0, default: 1.0)",
        )

        parser.add_argument(
            "--volume",
            type=float,
            default=1.0,
            help="Volume level (0.0-2.0, default: 1.0)",
        )

        parser.add_argument(
            "--pitch", type=float, help="Pitch adjustment (0.5-2.0, AI engine only)"
        )

        parser.add_argument("-o", "--output", help="Output file path")

        parser.add_argument(
            "-f",
            "--format",
            choices=["wav", "mp3", "aiff"],
            default="wav",
            help="Audio format (default: wav)",
        )

        parser.add_argument(
            "-q",
            "--quality",
            choices=["fast", "balanced", "premium"],
            default="balanced",
            help="Quality vs speed preference (default: balanced)",
        )

        parser.add_argument(
            "--speaker-wav", help="Path to WAV file for voice cloning (AI engine)"
        )

        parser.add_argument(
            "--model", help="Specific TTS model (xtts_v2, glow_tts, etc.)"
        )

        parser.add_argument(
            "--play", action="store_true", help="Play audio after synthesis"
        )

        parser.add_argument(
            "--no-play", action="store_true", help="Don't play audio (override --play)"
        )

    def _add_clone_args(self, parser):
        """Add voice cloning arguments"""
        parser.add_argument(
            "speaker_wav", help="Path to WAV audio file (6+ seconds recommended)"
        )

        parser.add_argument(
            "-n", "--name", required=True, help="Name for the cloned voice"
        )

        parser.add_argument("-d", "--description", help="Description of the voice")

        parser.add_argument(
            "-l", "--language", default="en", help="Primary language for the voice"
        )

        parser.add_argument(
            "--preview",
            action="store_true",
            help="Preview the cloned voice after creation",
        )

    def _add_list_args(self, parser):
        """Add voice listing arguments"""
        parser.add_argument(
            "-e",
            "--engine",
            choices=["all", "native", "ai"],
            default="all",
            help="Filter by engine (default: all)",
        )

        parser.add_argument("-l", "--language", help="Filter by language code")

        parser.add_argument(
            "--include-clones",
            action="store_true",
            default=True,
            help="Include voice clones in results",
        )

        parser.add_argument(
            "--compact", action="store_true", help="Show compact listing"
        )

    def _add_preview_args(self, parser):
        """Add voice preview arguments"""
        parser.add_argument("voice", help="Voice name to preview")

        parser.add_argument(
            "-e",
            "--engine",
            choices=["auto", "native", "ai"],
            default="auto",
            help="Engine choice (default: auto)",
        )

        parser.add_argument("-l", "--language", default="en", help="Language code")

        parser.add_argument(
            "-t",
            "--text",
            help="Custom text for preview (uses default if not provided)",
        )

    def _add_batch_args(self, parser):
        """Add batch processing arguments"""
        parser.add_argument("files", nargs="+", help="Text files to process")

        parser.add_argument(
            "-o",
            "--output-dir",
            default="./batch_output/",
            help="Output directory (default: ./batch_output/)",
        )

        parser.add_argument(
            "-e",
            "--engine",
            choices=["auto", "native", "ai"],
            default="auto",
            help="TTS engine to use",
        )

        parser.add_argument("-v", "--voice", help="Voice name")

        parser.add_argument("-l", "--language", default="en", help="Language code")

        parser.add_argument(
            "-f",
            "--format",
            choices=["wav", "mp3", "aiff"],
            default="wav",
            help="Audio format",
        )

        parser.add_argument(
            "--parallel",
            type=int,
            default=1,
            help="Number of parallel processes (default: 1)",
        )

        parser.add_argument("--progress", action="store_true", help="Show progress bar")

    def _add_config_args(self, parser):
        """Add configuration arguments"""
        parser.add_argument(
            "--show", action="store_true", help="Show current configuration"
        )

        parser.add_argument(
            "--set", metavar="KEY=VALUE", help="Set configuration value"
        )

        parser.add_argument(
            "--reset", action="store_true", help="Reset configuration to defaults"
        )

        parser.add_argument(
            "--clear-cache", action="store_true", help="Clear model cache"
        )

    def _add_legacy_args(self, parser):
        """Add legacy mode arguments"""
        parser.add_argument(
            "legacy_args",
            nargs=argparse.REMAINDER,
            help="Arguments to pass to legacy CLI",
        )

    async def run_command(self, args) -> int:
        """Execute the specified command"""
        try:
            if args.command == "synthesize" or not args.command:
                return await self.cmd_synthesize(args)
            elif args.command == "clone-voice":
                return await self.cmd_clone_voice(args)
            elif args.command == "list-voices":
                return await self.cmd_list_voices(args)
            elif args.command == "preview-voice":
                return await self.cmd_preview_voice(args)
            elif args.command == "batch":
                return await self.cmd_batch(args)
            elif args.command == "config":
                return self.cmd_config(args)
            elif args.command == "info":
                return await self.cmd_info()
            elif args.command == "legacy":
                return self.cmd_legacy(args)
            else:
                print(f"Unknown command: {args.command}")
                return 1

        except KeyboardInterrupt:
            print("\\nOperation cancelled by user")
            return 130
        except Exception as e:
            print(f"Error: {e}")
            return 1

    async def cmd_synthesize(self, args) -> int:
        """Execute synthesis command"""
        if not args.text:
            print("Error: Text is required for synthesis")
            return 1

        # Create synthesis request
        request = TTSRequest(
            text=args.text,
            engine=EngineType(args.engine),
            voice=args.voice,
            language=args.language,
            rate=args.rate,
            volume=args.volume,
            pitch_adjustment=args.pitch,
            format=AudioFormat(args.format),
            quality=Quality(args.quality),
            speaker_wav=args.speaker_wav,
            model_name=args.model,
        )

        # Select engine
        tts_engine = self.engine_selector.select_engine(
            engine=request.engine,
            voice_cloning=bool(request.speaker_wav),
            language=request.language,
            quality=request.quality,
        )

        engine_type = "AI" if hasattr(tts_engine, "config") else "Native"
        print(f"🔊 Using {engine_type} engine...")

        # Synthesize
        start_time = time.time()

        try:
            output_path = tts_engine.synthesize(
                text=request.text,
                voice=request.voice,
                language=request.language,
                rate=request.rate,
                volume=request.volume,
                output_file=args.output,
                speaker_wav=request.speaker_wav,
                model_name=request.model_name,
                pitch_adjustment=request.pitch_adjustment,
            )

            synthesis_time = time.time() - start_time

            if output_path and Path(output_path).exists():
                file_size = Path(output_path).stat().st_size / (1024 * 1024)  # MB

                print(f"✅ Synthesis completed in {synthesis_time:.2f}s")
                print(f"📁 Output: {output_path}")
                print(f"💾 Size: {file_size:.2f} MB")

                # Play audio if requested
                play_audio = args.play and not args.no_play
                if play_audio:
                    print("🔊 Playing audio...")
                    self._play_audio_file(output_path)

            else:
                # Real-time synthesis (no file output)
                print(f"✅ Synthesis completed in {synthesis_time:.2f}s")

            return 0

        except Exception as e:
            print(f"❌ Synthesis failed: {e}")
            return 1

    async def cmd_clone_voice(self, args) -> int:
        """Execute voice cloning command"""
        if not Path(args.speaker_wav).exists():
            print(f"❌ Audio file not found: {args.speaker_wav}")
            return 1

        print(f"🎭 Cloning voice from: {args.speaker_wav}")

        try:
            # Get AI engine
            ai_engine = self.engine_selector.ai_engine
            if not ai_engine:
                print("❌ AI engine not available for voice cloning")
                return 1

            # Create clone
            clone_info = ai_engine.clone_voice(
                speaker_wav=args.speaker_wav,
                voice_name=args.name,
                description=args.description,
            )

            print(f"✅ Voice '{args.name}' cloned successfully!")
            print(f"📝 Description: {clone_info['description']}")
            print(f"🎵 Sample Rate: {clone_info['sample_rate']} Hz")

            # Preview if requested
            if args.preview:
                print("\\n🔊 Previewing cloned voice...")
                sample_text = f"Hello, this is {args.name} speaking. How do I sound?"

                await self._preview_voice_internal(
                    voice=args.name,
                    language=args.language,
                    text=sample_text,
                    engine="ai",
                )

            return 0

        except Exception as e:
            print(f"❌ Voice cloning failed: {e}")
            return 1

    async def cmd_list_voices(self, args) -> int:
        """Execute voice listing command"""
        voices_info = self.engine_selector.list_all_voices()

        if args.compact:
            self._print_compact_voices(voices_info, args)
        else:
            self._print_detailed_voices(voices_info, args)

        return 0

    async def cmd_preview_voice(self, args) -> int:
        """Execute voice preview command"""
        return await self._preview_voice_internal(
            voice=args.voice, language=args.language, text=args.text, engine=args.engine
        )

    async def cmd_batch(self, args) -> int:
        """Execute batch processing command"""
        # Validate input files
        files_to_process = []
        for pattern in args.files:
            if "*" in pattern or "?" in pattern:
                # Glob pattern
                import glob

                files_to_process.extend(glob.glob(pattern))
            else:
                # Direct file path
                if Path(pattern).exists():
                    files_to_process.append(pattern)
                else:
                    print(f"⚠️  File not found: {pattern}")

        if not files_to_process:
            print("❌ No files to process")
            return 1

        print(f"📁 Processing {len(files_to_process)} files...")

        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Process files
        success_count = 0
        total_files = len(files_to_process)

        for i, file_path in enumerate(files_to_process, 1):
            try:
                if args.progress:
                    percent = (i / total_files) * 100
                    print(
                        f"[{i}/{total_files}] {percent:.1f}% - {Path(file_path).name}"
                    )

                # Read text from file
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read().strip()

                if not text:
                    print(f"⚠️  Empty file: {file_path}")
                    continue

                # Generate output filename
                input_name = Path(file_path).stem
                output_file = output_dir / f"{input_name}.{args.format}"

                # Synthesize
                tts_engine = self.engine_selector.select_engine(
                    engine=EngineType(args.engine),
                    language=args.language,
                    quality=Quality.BALANCED,
                )

                await asyncio.get_event_loop().run_in_executor(
                    None,
                    tts_engine.synthesize,
                    text,
                    args.voice,
                    args.language,
                    1.0,  # rate
                    1.0,  # volume
                    str(output_file),
                )

                success_count += 1

            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")

        print(
            f"\\n✅ Batch processing complete: {success_count}/{total_files} files processed"
        )
        print(f"📁 Output directory: {output_dir}")

        return 0 if success_count > 0 else 1

    def cmd_config(self, args) -> int:
        """Execute configuration command"""
        if args.show:
            self._print_config()
        elif args.set:
            self._set_config(args.set)
        elif args.reset:
            self._reset_config()
        elif args.clear_cache:
            self._clear_cache()
        else:
            print("No configuration action specified. Use --help for options.")
            return 1

        return 0

    async def cmd_info(self) -> int:
        """Show system information"""
        print("🤖 TTS-MacOS v2 - System Information")
        print("=" * 50)

        # Engine information
        engine_info = self.engine_selector.get_engine_info()
        print("\\n🔧 Available Engines:")
        for engine_name, info in engine_info.items():
            status = "✅" if info["available"] else "❌"
            print(f"  {status} {engine_name.title()}: {info['type']}")

        # Platform information
        platform_info = self.config.get_platform_info()
        print(f"\\n💻 Platform:")
        print(f"  🖥️  System: {platform_info['system']}")
        print(f"  🏗️  Architecture: {platform_info['architecture']}")
        print(f"  🐍 Python: {platform_info['python_version']}")

        # Cache information
        cache_size = self.config.get_cache_size()
        print(f"\\n📦 Cache: {cache_size} MB")

        return 0

    def cmd_legacy(self, args) -> int:
        """Execute legacy command"""
        print("🔄 Using TTS-MacOS v1.x compatibility mode...")
        return self.legacy_cli.run(args.legacy_args if args.legacy_args else None)

    def _print_compact_voices(self, voices_info, args):
        """Print compact voice listing"""
        print("🎭 Available Voices (Compact)")
        print("-" * 30)

        if "native" in voices_info and args.engine in ["all", "native"]:
            native_voices = voices_info["native"]
            if "all" in native_voices:
                for voice in native_voices["all"][:10]:  # Limit output
                    print(f"  🍎 {voice['name']}")

        if "ai" in voices_info and args.engine in ["all", "ai"]:
            ai_voices = voices_info["ai"]
            print(f"  🤖 AI Voices: {len(ai_voices.get('languages', []))} languages")
            print(
                f"  🎭 Voice Cloning: {'✅' if ai_voices.get('cloning_support') else '❌'}"
            )

    def _print_detailed_voices(self, voices_info, args):
        """Print detailed voice listing"""
        print("🎭 Available Voices")
        print("=" * 50)

        # Native voices
        if "native" in voices_info and args.engine in ["all", "native"]:
            native_voices = voices_info["native"]
            if "error" not in native_voices:
                print(
                    f"\\n🍎 Native Engine Voices ({native_voices.get('total', 0)} total):"
                )

                for category in ["spanish", "enhanced", "premium", "other"]:
                    if category in native_voices and native_voices[category]:
                        print(
                            f"\\n  📂 {category.title()} ({len(native_voices[category])}):"
                        )
                        for voice in native_voices[category][:5]:
                            gender_icon = (
                                "👨" if voice.get("gender") == "Masculino" else "👩"
                            )
                            lang_flag = self._get_language_flag(
                                voice.get("language", "")
                            )
                            print(
                                f"    {gender_icon} {lang_flag} {voice['name']} - {voice.get('description', '')}"
                            )

                        if len(native_voices[category]) > 5:
                            print(
                                f"    ... and {len(native_voices[category]) - 5} more"
                            )

        # AI voices
        if "ai" in voices_info and args.engine in ["all", "ai"]:
            ai_voices = voices_info["ai"]
            print(f"\\n🤖 AI Engine Voices:")
            print(f"  🔧 Device: {ai_voices.get('device', 'Unknown')}")
            print(f"  🌐 Languages: {', '.join(ai_voices.get('languages', []))}")
            print(
                f"  🎭 Voice Cloning: {'✅' if ai_voices.get('cloning_support') else '❌'}"
            )

    def _print_config(self):
        """Print current configuration"""
        print("⚙️  Current Configuration:")
        print(json.dumps(self.config.config, indent=2))

    def _set_config(self, key_value):
        """Set configuration value"""
        try:
            key, value = key_value.split("=", 1)

            # Type conversion for known keys
            if key == "cache_size_mb":
                value = int(value)
            elif key in ["auto_download_models", "prefer_gpu"]:
                value = value.lower() in ("true", "1", "yes", "on")

            self.config.update_config({key: value})
            print(f"✅ Set {key} = {value}")

        except ValueError:
            print(f"❌ Invalid format. Use KEY=VALUE")

    def _reset_config(self):
        """Reset configuration to defaults"""
        # Remove config file to force defaults
        if self.config.config_file.exists():
            self.config.config_file.unlink()
            print("✅ Configuration reset to defaults")
        else:
            print("ℹ️  Configuration already at defaults")

    def _clear_cache(self):
        """Clear model cache"""
        self.config.clear_cache()
        print("✅ Model cache cleared")

    def _play_audio_file(self, file_path):
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
                print(f"⚠️  No audio player available for {system}")

        except Exception as e:
            print(f"⚠️  Could not play audio: {e}")

    def _get_language_flag(self, language_code):
        """Get emoji flag for language"""
        flags = {
            "es": "🇪🇸",
            "es-ES": "🇪🇸",
            "es-MX": "🇲🇽",
            "en": "🇺🇸",
            "en-US": "🇺🇸",
            "en-GB": "🇬🇧",
            "fr": "🇫🇷",
            "de": "🇩🇪",
            "it": "🇮🇹",
            "pt": "🇵🇹",
        }
        return flags.get(language_code, "🌍")

    async def _preview_voice_internal(self, voice, language, text, engine):
        """Internal voice preview implementation"""
        if not text:
            # Default sample texts
            samples = {
                "en": "Hello, this is a voice preview test.",
                "es": "Hola, esta es una prueba de voz.",
                "fr": "Bonjour, ceci est un test d'évaluation vocale.",
                "de": "Hallo, dies ist ein Sprachtest.",
                "it": "Ciao, questo è un test di valutazione vocale.",
            }
            text = samples.get(language, samples["en"])

        try:
            tts_engine = self.engine_selector.select_engine(
                engine=EngineType(engine), language=language
            )

            output_path = tts_engine.synthesize(
                text=text, voice=voice, language=language, output_file=None
            )

            if output_path:
                self._play_audio_file(output_path)
                print(f"✅ Voice preview complete: {voice}")

        except Exception as e:
            print(f"❌ Voice preview failed: {e}")


def main():
    """Main CLI entry point"""
    cli = EnhancedCLI()
    parser = cli.create_parser()
    args = parser.parse_args()

    # Run command asynchronously
    return asyncio.run(cli.run_command(args))


if __name__ == "__main__":
    sys.exit(main())
