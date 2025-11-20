"""
TTS Notify v2 - Modular Text-to-Speech notification system for macOS

This package provides a modular architecture for text-to-speech functionality
with support for CLI, API, and MCP interfaces.
"""

__version__ = "2.0.0"
__author__ = "TTS Notify Project"
__license__ = "MIT"

# Core components
from core.config_manager import TTSConfig, config_manager
from core.voice_system import VoiceManager, VoiceFilter, MacOSVoiceDetector
from core.tts_engine import TTSEngine, MacOSTTSEngine, engine_registry
from core.models import Voice, TTSRequest, TTSResponse, Gender, VoiceQuality, Language, AudioFormat
from core.exceptions import (
    TTSNotifyError, VoiceError, VoiceNotFoundError, VoiceDetectionError,
    TTSError, EngineNotAvailableError, AudioProcessingError,
    ConfigurationError, InstallationError, PluginError, ValidationError
)

# Utilities
from utils import (
    TextNormalizer, FileManager, file_manager,
    setup_logging, get_logger, get_audit_logger, configure_logging_from_config,
    SystemDetector, AsyncUtils
)

# Main Orchestrator and User Interfaces
from main import TTSNotifyOrchestrator, main as orchestrator_main
from ui.cli.main import TTSNotifyCLI, main as cli_main
from ui.mcp.server import TTSNotifyMCPServer, main as mcp_main
from ui.api.server import TTSNotifyAPIServer, main as api_main, api_server

# Version information
def get_version():
    """Get the current TTS Notify version"""
    return __version__

def get_version_info():
    """Get detailed version information"""
    return {
        "version": __version__,
        "author": __author__,
        "license": __license__,
        "description": "Modular Text-to-Speech notification system for macOS"
    }

# Export main classes and functions
__all__ = [
    # Version
    "get_version",
    "get_version_info",

    # Main Orchestrator
    "TTSNotifyOrchestrator",
    "orchestrator_main",

    # User Interfaces
    "TTSNotifyCLI",
    "cli_main",
    "TTSNotifyMCPServer",
    "mcp_main",
    "TTSNotifyAPIServer",
    "api_main",
    "api_server",

    # Core
    "TTSConfig",
    "config_manager",
    "VoiceManager",
    "VoiceFilter",
    "MacOSVoiceDetector",
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

    # Utilities
    "TextNormalizer",
    "FileManager",
    "file_manager",
    "setup_logging",
    "get_logger",
    "get_audit_logger",
    "configure_logging_from_config",
    "SystemDetector",
    "AsyncUtils",
]

# Configure logging when package is imported
try:
    import os
    # Try to load configuration from environment
    config = config_manager.get_config()
    configure_logging_from_config(config.to_dict())
except Exception:
    # Fallback to default logging configuration
    setup_logging()