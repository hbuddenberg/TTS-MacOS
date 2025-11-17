"""
TTS-MacOS v2 - Dual Engine Text-to-Speech System

A hybrid TTS system that combines:
- Native OS TTS engines (macOS say, Linux espeak-ng)
- AI-powered TTS engines (Coqui TTS with XTTS-v2)

Features:
- Voice cloning from audio samples
- Cross-platform compatibility (macOS/Linux)
- Backward compatibility with v1.x
- MCP server integration
- Advanced CLI interface
"""

__version__ = "2.0.0"
__author__ = "TTS-MacOS Development Team"

from .engines import EngineSelector
from .core.config import TTSConfig

__all__ = ["EngineSelector", "TTSConfig"]
