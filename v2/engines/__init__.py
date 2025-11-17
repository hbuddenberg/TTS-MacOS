"""
TTS Engines Module - Pluggable architecture for multiple TTS engines

This module provides a unified interface for different TTS engines:
- NativeEngine: OS-native TTS (macOS say, Linux espeak-ng)
- AIEngine: Coqui TTS with XTTS-v2 for voice cloning
- EngineSelector: Automatic selection based on requirements
"""

from .ai_engine import AIEngine
from .native import NativeEngine
from .selector import EngineSelector

__all__ = ["NativeEngine", "AIEngine", "EngineSelector"]
