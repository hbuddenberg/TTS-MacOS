"""
System detection utilities for TTS Notify v2

This module provides system detection and capability checking.
"""

import platform
import subprocess
from typing import Dict, Any, List, Optional
import logging

from .file_manager import file_manager

logger = logging.getLogger(__name__)


class SystemDetector:
    """System detection and capability checking"""

    def __init__(self):
        self._system = platform.system()
        self._version = platform.version()
        self._architecture = platform.machine()
        self._platform = platform.platform()
        self._capabilities_cache: Dict[str, Any] = {}

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get comprehensive system information.

        Returns:
            Dictionary with system information
        """
        info = {
            "system": self._system,
            "version": self._version,
            "architecture": self._architecture,
            "platform": self._platform,
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "user": file_manager.get_current_user(),
            "home_directory": str(file_manager._user_home),
            "desktop_directory": str(file_manager._desktop_path),
        }

        # Add system-specific information
        if self._system == "Darwin":  # macOS
            info.update(self._get_macos_info())
        elif self._system == "Windows":
            info.update(self._get_windows_info())
        else:  # Linux and others
            info.update(self._get_linux_info())

        return info

    def _get_macos_info(self) -> Dict[str, Any]:
        """Get macOS-specific information"""
        info = {}

        try:
            # Get macOS version details
            result = subprocess.run(["sw_vers", "-productVersion"],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                info["macos_version"] = result.stdout.strip()

            # Check for Siri voices
            info["siri_voices_available"] = self._check_siri_voices()

            # Check for VoiceOver utility
            result = subprocess.run(["which", "VoiceOver"],
                                  capture_output=True, text=True, timeout=5)
            info["voiceover_available"] = result.returncode == 0

            # Check for accessibility features
            info["accessibility_features"] = self._check_accessibility_features()

        except Exception as e:
            logger.warning(f"Failed to get macOS info: {e}")

        return info

    def _get_windows_info(self) -> Dict[str, Any]:
        """Get Windows-specific information"""
        info = {}

        try:
            # Get Windows version
            info["windows_version"] = platform.win32_ver()[1] if hasattr(platform, 'win32_ver') else "Unknown"

            # Check for SAPI (Speech API)
            info["sapi_available"] = self._check_sapi_availability()

            # Check for Windows speech engines
            info["speech_engines"] = self._get_windows_speech_engines()

        except Exception as e:
            logger.warning(f"Failed to get Windows info: {e}")

        return info

    def _get_linux_info(self) -> Dict[str, Any]:
        """Get Linux-specific information"""
        info = {}

        try:
            # Get distribution info
            if hasattr(platform, 'freedesktop_release'):
                info["distribution"] = platform.freedesktop_release()
            elif hasattr(platform, 'linux_distribution'):
                info["distribution"] = platform.linux_distribution()

            # Check for speech synthesis tools
            info["speech_tools"] = self._check_linux_speech_tools()

            # Check for audio systems
            info["audio_systems"] = self._check_audio_systems()

        except Exception as e:
            logger.warning(f"Failed to get Linux info: {e}")

        return info

    def _check_siri_voices(self) -> bool:
        """Check if Siri voices are available on macOS"""
        try:
            result = subprocess.run(["say", "-v", "?"],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return "siri" in result.stdout.lower()
        except Exception:
            pass
        return False

    def _check_accessibility_features(self) -> List[str]:
        """Check for macOS accessibility features"""
        features = []

        try:
            # Check for VoiceOver
            if subprocess.run(["which", "VoiceOver"], capture_output=True, timeout=5).returncode == 0:
                features.append("voiceover")

            # Check for other accessibility tools
            accessibility_tools = ["say", "osascript"]
            for tool in accessibility_tools:
                if subprocess.run(["which", tool], capture_output=True, timeout=5).returncode == 0:
                    features.append(tool)

        except Exception:
            pass

        return features

    def _check_sapi_availability(self) -> bool:
        """Check if Windows SAPI is available"""
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            return True
        except Exception:
            return False

    def _get_windows_speech_engines(self) -> List[str]:
        """Get available Windows speech engines"""
        engines = []

        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            voices = speaker.GetVoices()
            for i in range(voices.Count):
                engines.append(voices.Item(i).GetDescription())
        except Exception:
            pass

        return engines

    def _check_linux_speech_tools(self) -> List[str]:
        """Check for Linux speech synthesis tools"""
        tools = []

        speech_tools = ["festival", "espeak", "mbrola", "rhvoice", "pico"]
        for tool in speech_tools:
            if subprocess.run(["which", tool], capture_output=True, timeout=5).returncode == 0:
                tools.append(tool)

        return tools

    def _check_audio_systems(self) -> List[str]:
        """Check for available audio systems on Linux"""
        systems = []

        audio_systems = ["pulseaudio", "alsa", "jackd", "pipewire"]
        for system in audio_systems:
            if subprocess.run(["which", system], capture_output=True, timeout=5).returncode == 0:
                systems.append(system)

        return systems

    def check_tts_capabilities(self) -> Dict[str, Any]:
        """
        Check TTS capabilities for the current system.

        Returns:
            Dictionary with TTS capability information
        """
        capabilities = {
            "native_tts_available": False,
            "native_command": None,
            "supported_formats": [],
            "voice_count": 0,
            "engine_available": False
        }

        if self._system == "Darwin":  # macOS
            capabilities.update(self._check_macos_tts_capabilities())
        elif self._system == "Windows":
            capabilities.update(self._check_windows_tts_capabilities())
        else:  # Linux
            capabilities.update(self._check_linux_tts_capabilities())

        return capabilities

    def _check_macos_tts_capabilities(self) -> Dict[str, Any]:
        """Check macOS TTS capabilities"""
        capabilities = {}

        try:
            # Check if say command is available
            result = subprocess.run(["which", "say"],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                capabilities["native_tts_available"] = True
                capabilities["native_command"] = "say"
                capabilities["supported_formats"] = ["aiff"]

                # Get voice count
                voice_result = subprocess.run(["say", "-v", "?"],
                                           capture_output=True, text=True, timeout=10)
                if voice_result.returncode == 0:
                    voice_count = len([line for line in voice_result.stdout.split('\n') if line.strip()])
                    capabilities["voice_count"] = voice_count

                capabilities["engine_available"] = True

        except Exception as e:
            logger.warning(f"Failed to check macOS TTS capabilities: {e}")

        return capabilities

    def _check_windows_tts_capabilities(self) -> Dict[str, Any]:
        """Check Windows TTS capabilities"""
        capabilities = {}

        try:
            # Check SAPI availability
            if self._check_sapi_availability():
                capabilities["native_tts_available"] = True
                capabilities["native_command"] = "sapi"
                capabilities["supported_formats"] = ["wav"]

                # Get voice count
                engines = self._get_windows_speech_engines()
                capabilities["voice_count"] = len(engines)

                capabilities["engine_available"] = True

        except Exception as e:
            logger.warning(f"Failed to check Windows TTS capabilities: {e}")

        return capabilities

    def _check_linux_tts_capabilities(self) -> Dict[str, Any]:
        """Check Linux TTS capabilities"""
        capabilities = {}

        tools = self._check_linux_speech_tools()
        if tools:
            capabilities["native_tts_available"] = True
            capabilities["available_tools"] = tools
            capabilities["supported_formats"] = ["wav"]  # Common format for Linux tools
            capabilities["engine_available"] = True

        return capabilities

    def get_recommended_configuration(self) -> Dict[str, Any]:
        """
        Get recommended configuration for the current system.

        Returns:
            Dictionary with recommended settings
        """
        config = {}

        if self._system == "Darwin":  # macOS
            config.update({
                "TTS_NOTIFY_VOICE": "monica",
                "TTS_NOTIFY_RATE": 175,
                "TTS_NOTIFY_LANGUAGE": "es",
                "TTS_NOTIFY_QUALITY": "enhanced",
                "TTS_NOTIFY_OUTPUT_FORMAT": "aiff",
                "TTS_NOTIFY_CACHE_ENABLED": True,
                "TTS_NOTIFY_MAX_CONCURRENT": 5
            })
        elif self._system == "Windows":
            config.update({
                "TTS_NOTIFY_VOICE": "Microsoft David",
                "TTS_NOTIFY_RATE": 150,
                "TTS_NOTIFY_LANGUAGE": "en",
                "TTS_NOTIFY_OUTPUT_FORMAT": "wav",
                "TTS_NOTIFY_CACHE_ENABLED": True,
                "TTS_NOTIFY_MAX_CONCURRENT": 3
            })
        else:  # Linux
            config.update({
                "TTS_NOTIFY_VOICE": "default",
                "TTS_NOTIFY_RATE": 150,
                "TTS_NOTIFY_LANGUAGE": "en",
                "TTS_NOTIFY_OUTPUT_FORMAT": "wav",
                "TTS_NOTIFY_CACHE_ENABLED": True,
                "TTS_NOTIFY_MAX_CONCURRENT": 3
            })

        # Add system-specific recommendations
        if self._architecture == "arm64":
            config["TTS_NOTIFY_MAX_CONCURRENT"] = 3  # Conservative for ARM

        return config

    def validate_system_requirements(self) -> Dict[str, Any]:
        """
        Validate system requirements for TTS Notify.

        Returns:
            Dictionary with validation results
        """
        validation = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "recommendations": []
        }

        # Check Python version
        python_version = platform.python_version_tuple()
        if python_version < (3, 10):
            validation["errors"].append(f"Python {python_version[0]}.{python_version[1]} is not supported. Requires Python 3.10+")
            validation["valid"] = False

        # Check TTS capabilities
        tts_caps = self.check_tts_capabilities()
        if not tts_caps["native_tts_available"]:
            validation["errors"].append("No native TTS engine found on this system")
            validation["valid"] = False

        # Check file system permissions
        try:
            test_file = file_manager._desktop_path / ".tts_notify_test"
            test_file.write_text("test")
            test_file.unlink()
        except Exception as e:
            validation["errors"].append(f"Cannot write to Desktop directory: {e}")
            validation["valid"] = False

        # Check memory availability (basic check)
        try:
            import psutil
            memory_gb = psutil.virtual_memory().total / (1024**3)
            if memory_gb < 1:  # Less than 1GB
                validation["warnings"].append("Low memory availability detected")
        except ImportError:
            validation["recommendations"].append("Install psutil for better system monitoring")

        return validation


# Global system detector instance
system_detector = SystemDetector()