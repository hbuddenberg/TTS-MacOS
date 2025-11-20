"""
Custom exceptions for TTS Notify v2

This module defines all custom exceptions used throughout the TTS Notify system.
"""

from typing import Optional, Dict, Any


class TTSNotifyError(Exception):
    """Base exception for all TTS Notify errors"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class VoiceError(TTSNotifyError):
    """Exception raised for voice-related errors"""

    def __init__(self, message: str, voice_id: Optional[str] = None, **kwargs):
        super().__init__(message, kwargs)
        self.voice_id = voice_id


class VoiceNotFoundError(VoiceError):
    """Exception raised when a requested voice is not found"""

    def __init__(self, voice_id: str, available_voices: Optional[list] = None):
        message = f"Voice '{voice_id}' not found"
        if available_voices:
            message += f". Available voices: {', '.join(available_voices[:10])}"
        super().__init__(message, voice_id=voice_id, available_voices=available_voices)


class VoiceDetectionError(VoiceError):
    """Exception raised when voice detection fails"""

    def __init__(self, engine_name: str, original_error: Optional[Exception] = None):
        message = f"Failed to detect voices using engine '{engine_name}'"
        if original_error:
            message += f": {str(original_error)}"
        super().__init__(message, engine_name=engine_name, original_error=str(original_error))


class TTSError(TTSNotifyError):
    """Exception raised for TTS engine errors"""

    def __init__(self, message: str, engine_name: Optional[str] = None, **kwargs):
        super().__init__(message, kwargs)
        self.engine_name = engine_name


class EngineNotAvailableError(TTSError):
    """Exception raised when a TTS engine is not available"""

    def __init__(self, engine_name: str, reason: Optional[str] = None):
        message = f"TTS engine '{engine_name}' is not available"
        if reason:
            message += f": {reason}"
        super().__init__(message, engine_name=engine_name, reason=reason)


class AudioProcessingError(TTSNotifyError):
    """Exception raised for audio processing errors"""

    def __init__(self, message: str, file_path: Optional[str] = None, **kwargs):
        super().__init__(message, kwargs)
        self.file_path = file_path


class ConfigurationError(TTSNotifyError):
    """Exception raised for configuration errors"""

    def __init__(self, message: str, config_key: Optional[str] = None, **kwargs):
        super().__init__(message, kwargs)
        self.config_key = config_key


class InstallationError(TTSNotifyError):
    """Exception raised during installation"""

    def __init__(self, message: str, component: Optional[str] = None, **kwargs):
        super().__init__(message, kwargs)
        self.component = component


class PluginError(TTSNotifyError):
    """Exception raised for plugin-related errors"""

    def __init__(self, message: str, plugin_name: Optional[str] = None, **kwargs):
        super().__init__(message, kwargs)
        self.plugin_name = plugin_name


class ValidationError(TTSNotifyError):
    """Exception raised for input validation errors"""

    def __init__(self, message: str, field: Optional[str] = None, value: Optional[Any] = None, **kwargs):
        super().__init__(message, kwargs)
        self.field = field
        self.value = value