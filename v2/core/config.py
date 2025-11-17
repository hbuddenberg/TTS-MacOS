"""
TTS-MacOS v2 Core Configuration and Utilities

Central configuration management for the dual-engine TTS system including:
- Model configuration and paths
- Platform detection and optimization
- Parameter validation
- Caching system management
"""

import json
import os
import platform
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


class EngineType(str, Enum):
    NATIVE = "native"
    AI = "ai"
    AUTO = "auto"


class AudioFormat(str, Enum):
    WAV = "wav"
    MP3 = "mp3"
    AIFF = "aiff"
    OGG = "ogg"


class Quality(str, Enum):
    FAST = "fast"
    BALANCED = "balanced"
    PREMIUM = "premium"


class LanguageCode(str, Enum):
    SPANISH = "es"
    ENGLISH = "en"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    POLISH = "pl"
    TURKISH = "tr"
    RUSSIAN = "ru"
    DUTCH = "nl"
    CZECH = "cs"
    ARABIC = "ar"
    CHINESE = "zh-cn"
    JAPANESE = "ja"
    HUNGARIAN = "hu"
    KOREAN = "ko"


class TTSRequest(BaseModel):
    """
    Comprehensive TTS request validation using Pydantic
    """

    text: str = Field(
        ..., min_length=1, max_length=10000, description="Text to synthesize"
    )
    engine: EngineType = Field(EngineType.AUTO, description="TTS engine to use")
    voice: Optional[str] = Field(
        None, description="Voice name or path to audio file for cloning"
    )
    language: LanguageCode = Field(LanguageCode.ENGLISH, description="Target language")
    rate: float = Field(1.0, ge=0.5, le=2.0, description="Speech rate multiplier")
    volume: float = Field(1.0, ge=0.0, le=2.0, description="Volume level")
    pitch_adjustment: Optional[float] = Field(
        1.0, ge=0.5, le=2.0, description="Pitch adjustment"
    )
    format: AudioFormat = Field(AudioFormat.WAV, description="Output audio format")
    quality: Quality = Field(
        Quality.BALANCED, description="Quality vs speed preference"
    )
    output_path: Optional[str] = Field(None, description="Custom output file path")
    speaker_wav: Optional[str] = Field(
        None, description="Path to WAV file for voice cloning"
    )
    model_name: Optional[str] = Field(None, description="Specific TTS model to use")

    # Advanced options
    emphasis: Optional[str] = Field("moderate", regex="^(none|moderate|strong)$")
    speed: Optional[float] = Field(1.0, ge=0.5, le=2.0)

    @validator("speaker_wav")
    def validate_speaker_wav(cls, v, values):
        if v and not os.path.exists(v):
            raise ValueError(f"Speaker WAV file not found: {v}")
        return v

    @validator("output_path")
    def validate_output_path(cls, v):
        if v:
            # Ensure directory exists
            Path(v).parent.mkdir(parents=True, exist_ok=True)
        return v


@dataclass
class ModelInfo:
    """Information about available TTS models"""

    name: str
    display_name: str
    languages: List[str]
    supports_cloning: bool
    quality: Quality
    model_size_mb: int
    download_url: Optional[str] = None
    local_path: Optional[str] = None


class TTSConfig:
    """
    Central configuration management for TTS-MacOS v2
    """

    def __init__(self):
        self.system = platform.system()
        self.home_dir = Path.home()
        self.config_dir = self.home_dir / ".config" / "tts-macos-v2"
        self.cache_dir = self.home_dir / ".cache" / "tts-macos-v2"
        self.models_dir = self.cache_dir / "models"

        # Create directories
        self._ensure_directories()

        # Load or create configuration
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()

        # Initialize model registry
        self.models = self._initialize_model_registry()

    def _ensure_directories(self):
        """Create necessary directories"""
        for directory in [self.config_dir, self.cache_dir, self.models_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create defaults"""
        default_config = {
            "version": "2.0.0",
            "default_engine": "auto",
            "default_language": "en",
            "default_quality": "balanced",
            "cache_size_mb": 2048,
            "auto_download_models": True,
            "prefer_gpu": True,
            "output_format": "wav",
            "native_engine": {
                "enabled": True,
                "preferred_voices": {
                    "es": "monica",
                    "en": "samantha",
                    "fr": "aurelie",
                    "de": "anna",
                },
            },
            "ai_engine": {
                "enabled": True,
                "default_model": "xtts_v2",
                "cache_models": True,
                "model_timeout": 300,
            },
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    # Merge with defaults for any missing keys
                    return {**default_config, **loaded_config}
            except Exception as e:
                print(f"Warning: Could not load config file, using defaults: {e}")

        # Save default config
        self._save_config(default_config)
        return default_config

    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")

    def _initialize_model_registry(self) -> Dict[str, ModelInfo]:
        """Initialize registry of available TTS models"""
        models = {
            "xtts_v2": ModelInfo(
                name="xtts_v2",
                display_name="XTTS v2",
                languages=[
                    "en",
                    "es",
                    "fr",
                    "de",
                    "it",
                    "pt",
                    "pl",
                    "tr",
                    "ru",
                    "nl",
                    "cs",
                    "ar",
                    "zh-cn",
                    "ja",
                    "hu",
                    "ko",
                ],
                supports_cloning=True,
                quality=Quality.PREMIUM,
                model_size_mb=2400,
                download_url="https://coqui.gateway.scarf.sh/hf-coqui/XTTS-v2/main XTTS-v2.tar.gz",
            ),
            "glow_tts": ModelInfo(
                name="glow_tts",
                display_name="Glow-TTS",
                languages=["en", "es", "fr", "de", "it", "pt"],
                supports_cloning=False,
                quality=Quality.BALANCED,
                model_size_mb=100,
            ),
            "tacotron2_ddc": ModelInfo(
                name="tacotron2_ddc",
                display_name="Tacotron2-DDC",
                languages=["en"],
                supports_cloning=False,
                quality=Quality.PREMIUM,
                model_size_mb=150,
            ),
        }

        return models

    def get_default_voice(
        self, language: str, engine: EngineType = EngineType.AUTO
    ) -> Optional[str]:
        """Get default voice for language and engine"""
        if engine == EngineType.NATIVE or engine == EngineType.AUTO:
            native_voices = self.config.get("native_engine", {}).get(
                "preferred_voices", {}
            )
            if language in native_voices:
                return native_voices[language]

        # For AI engine, return generic speaker
        if engine == EngineType.AI:
            return "default"

        return None

    def get_model_info(self, model_name: str) -> Optional[ModelInfo]:
        """Get information about a specific model"""
        return self.models.get(model_name)

    def list_available_models(self, language: str = None) -> List[ModelInfo]:
        """List available models, optionally filtered by language"""
        models = list(self.models.values())

        if language:
            models = [m for m in models if language in m.languages]

        return models

    def get_cache_path(self, model_name: str) -> Path:
        """Get cache path for a specific model"""
        return self.models_dir / model_name

    def is_model_cached(self, model_name: str) -> bool:
        """Check if a model is already cached"""
        model_path = self.get_cache_path(model_name)
        return model_path.exists() and any(model_path.iterdir())

    def get_cache_size(self) -> int:
        """Get total cache size in MB"""
        total_size = 0
        try:
            for item in self.cache_dir.rglob("*"):
                if item.is_file():
                    total_size += item.stat().st_size / (1024 * 1024)  # Convert to MB
        except Exception:
            pass
        return int(total_size)

    def clear_cache(self, model_name: str = None):
        """Clear cache for specific model or all models"""
        if model_name:
            model_path = self.get_cache_path(model_name)
            if model_path.exists():
                import shutil

                shutil.rmtree(model_path)
        else:
            import shutil

            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                self._ensure_directories()

    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        self.config = {**self.config, **updates}
        self._save_config(self.config)

    def get_platform_info(self) -> Dict[str, Any]:
        """Get platform-specific information"""
        info = {
            "system": self.system,
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }

        if self.system == "Darwin":  # macOS
            info.update(
                {
                    "macos_version": platform.mac_ver()[0],
                    "metal_available": True,  # Apple Silicon or recent Intel Macs
                }
            )
        elif self.system == "Linux":
            # Check for CUDA
            try:
                import torch

                info.update(
                    {
                        "cuda_available": torch.cuda.is_available(),
                        "cuda_version": torch.version.cuda
                        if torch.cuda.is_available()
                        else None,
                    }
                )
            except ImportError:
                info.update({"cuda_available": False})

        return info
