"""
Engine Selector - Intelligent engine selection for TTS-MacOS v2

Automatically selects the best TTS engine based on:
- Available parameters (voice cloning, language requirements)
- System capabilities (GPU, memory, models available)
- User preferences (quality vs speed)
- Platform compatibility
"""

import os
import platform
from enum import Enum
from typing import Any, Dict, Optional

from .ai_engine import AIEngine
from .native import NativeEngine


class EngineType(Enum):
    NATIVE = "native"
    AI = "ai"
    AUTO = "auto"


class EngineSelector:
    """
    Intelligently selects the best TTS engine based on requirements
    """

    def __init__(self):
        self.native_engine = None
        self.ai_engine = None
        self._initialize_engines()

    def _initialize_engines(self):
        """Initialize available engines"""
        try:
            self.native_engine = NativeEngine()
        except Exception as e:
            print(f"Warning: Native engine not available: {e}")

        try:
            self.ai_engine = AIEngine()
        except Exception as e:
            print(f"Warning: AI engine not available: {e}")

    def select_engine(
        self,
        engine: EngineType = EngineType.AUTO,
        voice_cloning: bool = False,
        language: str = "en",
        quality: str = "balanced",
    ) -> Any:
        """
        Select the best engine for the given requirements

        Args:
            engine: Explicit engine choice or AUTO
            voice_cloning: Whether voice cloning is needed
            language: Target language code
            quality: Quality preference (fast/balanced/premium)

        Returns:
            Selected TTS engine instance
        """
        # Explicit engine choice
        if engine == EngineType.NATIVE and self.native_engine:
            return self.native_engine
        elif engine == EngineType.AI and self.ai_engine:
            return self.ai_engine

        # Voice cloning requires AI engine
        if voice_cloning and self.ai_engine:
            return self.ai_engine

        # Quality-based selection
        if quality == "premium" and self.ai_engine:
            return self.ai_engine
        elif quality == "fast" and self.native_engine:
            return self.native_engine

        # Language compatibility check
        if self._needs_ai_engine(language):
            return self.ai_engine if self.ai_engine else self.native_engine

        # Balanced approach - prefer native for speed, fallback to AI
        if self.native_engine and self.native_engine.is_available():
            return self.native_engine
        elif self.ai_engine:
            return self.ai_engine
        else:
            raise RuntimeError("No TTS engines available")

    def _needs_ai_engine(self, language: str) -> bool:
        """Check if language requires AI engine for better quality"""
        # Languages where AI engine provides significantly better quality
        ai_preferred_languages = {"ar", "zh-cn", "zh", "ja", "ko", "hi", "th", "vi"}
        return language.lower() in ai_preferred_languages

    def get_engine_info(self) -> Dict[str, Any]:
        """Get information about available engines"""
        info = {
            "native_engine": {
                "available": self.native_engine is not None,
                "type": "Native OS TTS",
                "platform": platform.system(),
                "voice_cloning": False,
            },
            "ai_engine": {
                "available": self.ai_engine is not None,
                "type": "Coqui TTS XTTS-v2",
                "voice_cloning": True,
                "models_loaded": self.ai_engine.get_loaded_models()
                if self.ai_engine
                else [],
            },
        }
        return info

    def list_all_voices(self) -> Dict[str, Any]:
        """List voices from all available engines"""
        voices = {}

        if self.native_engine:
            try:
                voices["native"] = self.native_engine.list_voices()
            except Exception as e:
                voices["native"] = {"error": str(e)}

        if self.ai_engine:
            try:
                voices["ai"] = self.ai_engine.list_voices()
            except Exception as e:
                voices["ai"] = {"error": str(e)}

        return voices
