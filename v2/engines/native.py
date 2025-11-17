"""
Native TTS Engine - OS-native text-to-speech

Provides cross-platform native TTS support:
- macOS: Uses built-in 'say' command
- Linux: Uses 'espeak-ng' command
- Fallback mechanisms for robustness

Maintains compatibility with existing v1.x functionality.
"""

import json
import os
import platform
import subprocess
import sys
from typing import Any, Dict, List, Optional


class NativeEngine:
    """
    Native OS TTS engine using system commands
    """

    def __init__(self):
        self.system = platform.system()
        self.voices_cache = None
        self.say_command = self._detect_tts_command()
        self._validate_availability()

    def _detect_tts_command(self) -> str:
        """Detect the appropriate TTS command for the current OS"""
        if self.system == "Darwin":  # macOS
            return "say"
        elif self.system == "Linux":
            # Check for espeak-ng first, then espeak
            if (
                subprocess.run(
                    ["which", "espeak-ng"], capture_output=True, text=True
                ).returncode
                == 0
            ):
                return "espeak-ng"
            elif (
                subprocess.run(
                    ["which", "espeak"], capture_output=True, text=True
                ).returncode
                == 0
            ):
                return "espeak"
            else:
                raise RuntimeError(
                    "No native TTS command found on Linux. Install espeak-ng."
                )
        else:
            raise RuntimeError(f"Unsupported platform: {self.system}")

    def _validate_availability(self):
        """Validate that the TTS command is actually available"""
        try:
            result = subprocess.run(
                [self.say_command, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                raise RuntimeError(f"TTS command '{self.say_command}' not working")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise RuntimeError(f"Cannot validate TTS command: {e}")

    def is_available(self) -> bool:
        """Check if the native engine is available"""
        try:
            self._validate_availability()
            return True
        except:
            return False

    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        rate: float = 1.0,
        volume: float = 1.0,
        output_file: Optional[str] = None,
        **kwargs,
    ) -> Optional[str]:
        """
        Synthesize speech using native TTS command

        Args:
            text: Text to synthesize
            voice: Voice name (platform-specific)
            rate: Speech rate (0.5-2.0)
            volume: Volume level (0.0-2.0)
            output_file: Path to save audio file

        Returns:
            Path to generated audio file if saved, None otherwise
        """
        # Build command based on platform
        cmd = [self.say_command]

        # Add platform-specific parameters
        if self.system == "Darwin":  # macOS
            if voice:
                cmd.extend(["-v", voice])
            if rate != 1.0:
                cmd.extend(["-r", str(int(rate * 200))])  # macOS uses WPM
            if volume != 1.0:
                # macOS uses volume 0-255
                volume_value = max(0, min(255, int(volume * 100)))
                cmd.extend(["--volume", str(volume_value)])
            if output_file:
                cmd.extend(["-o", output_file, "--data-format=LEF32@16000"])

        elif self.system == "Linux":  # espeak/espeak-ng
            if voice:
                cmd.extend(["-v", voice])
            if rate != 1.0:
                cmd.extend(["-s", str(int(rate * 175))])  # espeak uses WPM
            if volume != 1.0:
                volume_value = max(0, min(200, int(volume * 100)))
                cmd.extend(["-a", str(volume_value)])  # amplitude
            if output_file:
                cmd.extend(["-w", output_file])

        # Add text
        cmd.append(text)

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                raise RuntimeError(f"Native TTS failed: {result.stderr}")

            return output_file

        except subprocess.TimeoutExpired:
            raise RuntimeError("TTS synthesis timed out")
        except FileNotFoundError:
            raise RuntimeError(f"TTS command '{self.say_command}' not found")

    def list_voices(self) -> Dict[str, Any]:
        """List available voices for the current platform"""
        if self.voices_cache:
            return self.voices_cache

        voices = {}

        if self.system == "Darwin":  # macOS
            voices = self._list_macos_voices()
        elif self.system == "Linux":
            voices = self._list_linux_voices()

        self.voices_cache = voices
        return voices

    def _list_macos_voices(self) -> Dict[str, Any]:
        """List macOS voices using say -v '?'"""
        try:
            result = subprocess.run(
                ["say", "-v", "?"], capture_output=True, text=True, timeout=10
            )

            voices = {
                "total": 0,
                "spanish": [],
                "enhanced": [],
                "premium": [],
                "siri": [],
                "other": [],
                "all": [],
            }

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")

                for line in lines:
                    if line.strip():
                        # Parse voice line format
                        parts = line.split()
                        if parts:
                            voice_name = parts[0]
                            rest = " ".join(parts[1:])

                            voice_info = {
                                "name": voice_name,
                                "description": rest,
                                "language": self._extract_language(rest),
                                "gender": self._extract_gender(rest),
                                "type": self._determine_voice_type(rest),
                            }

                            voices["all"].append(voice_info)
                            voices["total"] += 1

                            # Categorize voice
                            if voice_info["type"] == "spanish":
                                voices["spanish"].append(voice_info)
                            elif voice_info["type"] == "enhanced":
                                voices["enhanced"].append(voice_info)
                            elif voice_info["type"] == "premium":
                                voices["premium"].append(voice_info)
                            elif voice_info["type"] == "siri":
                                voices["siri"].append(voice_info)
                            else:
                                voices["other"].append(voice_info)

            return voices

        except Exception as e:
            return {"error": f"Failed to list macOS voices: {e}"}

    def _list_linux_voices(self) -> Dict[str, Any]:
        """List Linux voices using espeak-ng --voices"""
        try:
            # Try espeak-ng --voices first
            if self.say_command == "espeak-ng":
                result = subprocess.run(
                    ["espeak-ng", "--voices"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
            else:
                result = subprocess.run(
                    ["espeak", "--voices"], capture_output=True, text=True, timeout=10
                )

            voices = {"total": 0, "all": []}

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                # Skip header line
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 5:
                            voice_info = {
                                "name": parts[4],
                                "language": parts[1],
                                "gender": parts[2],
                                "age": parts[3] if parts[3] != "-" else None,
                                "description": " ".join(parts[5:])
                                if len(parts) > 5
                                else "",
                            }
                            voices["all"].append(voice_info)
                            voices["total"] += 1

            return voices

        except Exception as e:
            return {"error": f"Failed to list Linux voices: {e}"}

    def _extract_language(self, description: str) -> str:
        """Extract language code from voice description"""
        desc_lower = description.lower()
        if "spanish" in desc_lower or "español" in desc_lower:
            if "mexico" in desc_lower or "méxico" in desc_lower:
                return "es-MX"
            elif "spain" in desc_lower or "españa" in desc_lower:
                return "es-ES"
            else:
                return "es"
        elif "english" in desc_lower:
            if "united" in desc_lower and "states" in desc_lower:
                return "en-US"
            elif "britain" in desc_lower or "uk" in desc_lower:
                return "en-GB"
            else:
                return "en"
        else:
            return "unknown"

    def _extract_gender(self, description: str) -> str:
        """Extract gender from voice description"""
        desc_lower = description.lower()
        if any(word in desc_lower for word in ["female", "woman", "mujer"]):
            return "female"
        elif any(word in desc_lower for word in ["male", "man", "hombre"]):
            return "male"
        else:
            return "unknown"

    def _determine_voice_type(self, description: str) -> str:
        """Determine voice category based on description"""
        desc_lower = description.lower()

        # Check for Spanish voices
        if "spanish" in desc_lower or "español" in desc_lower:
            return "spanish"

        # Check for premium/enhanced voices
        if any(word in desc_lower for word in ["premium", "enhanced", "enhanced"]):
            return "premium"

        # Check for Siri voices
        if "siri" in desc_lower:
            return "siri"

        return "other"

    def get_voice_info(self, voice_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific voice"""
        voices = self.list_voices()

        for voice in voices.get("all", []):
            if voice["name"].lower() == voice_name.lower():
                return voice

        return None

    def test_voice(
        self, voice_name: str, test_text: str = "Hello, this is a test."
    ) -> bool:
        """Test if a specific voice is working"""
        try:
            result = self.synthesize(text=test_text, voice=voice_name)
            return True
        except:
            return False
