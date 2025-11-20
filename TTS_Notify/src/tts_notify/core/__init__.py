"""
Core modules for TTS Notify v2

This package contains the core functionality for text-to-speech processing,
including voice management, TTS engines, and configuration.
"""

from .config_manager import TTSConfig, config_manager
from .voice_system import VoiceManager, VoiceFilter, MacOSVoiceDetector
from .tts_engine import TTSEngine, MacOSTTSEngine, engine_registry
from .models import Voice, TTSRequest, TTSResponse, Gender, VoiceQuality, Language, AudioFormat
from .exceptions import (
    TTSNotifyError, VoiceError, VoiceNotFoundError, VoiceDetectionError,
    TTSError, EngineNotAvailableError, AudioProcessingError,
    ConfigurationError, InstallationError, PluginError, ValidationError
)

__all__ = [
    # Configuration
    "TTSConfig",
    "config_manager",

    # Voice System
    "VoiceManager",
    "VoiceFilter",
    "MacOSVoiceDetector",

    # TTS Engine
    "TTSEngine",
    "MacOSTTSEngine",
    "engine_registry",

    # Models
    "Voice",
    "TTSRequest",
    "TTSResponse",
    "Gender",
    "VoiceQuality",
    "Language",
    "AudioFormat",

    # Exceptions
    "TTSNotifyError",
    "VoiceError",
    "VoiceNotFoundError",
    "VoiceDetectionError",
    "TTSError",
    "EngineNotAvailableError",
    "AudioProcessingError",
    "ConfigurationError",
    "InstallationError",
    "PluginError",
    "ValidationError",
]