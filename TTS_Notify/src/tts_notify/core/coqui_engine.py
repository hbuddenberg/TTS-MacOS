"""
CoquiTTS Engine for TTS Notify v3

This module provides a comprehensive CoquiTTS engine with multi-language support,
intelligent model management, and voice cloning capabilities.
"""

import asyncio
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
import tempfile
import shutil

try:
    import torch
    import numpy as np
    COQUI_AVAILABLE = True
except ImportError:
    COQUI_AVAILABLE = False

try:
    from TTS.api import TTS
    TTS_API_AVAILABLE = True
except ImportError:
    TTS_API_AVAILABLE = False

from .models import (
    TTSRequest, TTSResponse, Voice, AudioFormat, Language,
    Gender, VoiceQuality, TTSEngineType,
    VoiceCloningRequest, VoiceCloningResponse, VoiceProfile
)
from .exceptions import TTSError, EngineNotAvailableError, ValidationError
from .config_manager import ConfigManager
from .voice_cloner import VoiceCloner, voice_cloner
from .audio_pipeline import AudioProcessor, audio_processor

logger = logging.getLogger(__name__)


@dataclass
class LanguageAvailability:
    """Language availability information"""
    available: bool
    source: str  # loaded_model, cached_model, downloadable, download_specific, not_supported
    model: Optional[str] = None
    download_required: bool = False
    size_gb: Optional[float] = None
    download_time_est: Optional[int] = None


@dataclass
class ModelInfo:
    """Model information for language support"""
    languages: List[str]
    size_gb: float
    speakers: int
    quality: str
    streaming: bool = True


class CoquiTTSEngine:
    """CoquiTTS-based TTS engine with multi-language and model management"""

    def __init__(self, model_name: str = "tts_models/es/multi-dataset/xtts_v2"):
        self.name = "coqui"
        self.model_name = model_name
        self._tts = None
        self._initialized = False
        self._device = "cpu"

        # Multi-language model capabilities based on research
        self.multi_language_models = {
            "tts_models/es/multi-dataset/xtts_v2": ModelInfo(
                languages=["en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "zh", "ja", "ko", "cs", "ar", "tr", "hu", "fi"],
                size_gb=2.0,
                speakers=17,
                quality="enhanced",
                streaming=True
            ),
            "tts_models/multilingual/multi-dataset/xtts_v2": ModelInfo(
                languages=["en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "zh", "ja", "ko"],
                size_gb=2.2,
                speakers=16,
                quality="enhanced",
                streaming=True
            )
        }

        # Single-language models
        self.single_language_models = {
            "es": ["tts_models/esu/fairseq/vits", "tts_models/es/css10/vits"],
            "en": ["tts_models/en/ljspeech/tacotron2-DDC", "tts_models/en/vctk/vits"],
            "fr": ["tts_models/fr/multi-dataset/xtts_v2"],
            "de": ["tts_models/de/thorsten-vits"],
            "it": ["tts_models/it/mai_female_vits", "tts_models/it/mai_male"],
            "pt": ["tts_models/pt/male/female_vits"],
            "nl": ["tts_models/nl/male/female_vits"],
            "pl": ["tts_models/pl/male/female_vits"],
            "tr": ["tts_models/tr/common-voice-gpu_vits"],
            "cs": ["tts_models/cs/cv-vits"],
            "ar": ["tts_models/ar/kokoro-vits"],
            "hu": ["tts_models/hu/bemea_vits"],
            "fi": ["tts_models/fi/sami_tts_vits"],
            "ja": ["tts_models/ja/kokoro-tacotron2-DDC"],
            "ko": ["tts_models/ko/kokoro-vits"],
            "zh": ["tts_models/zh/baker/tacotron2-DDC-GST"],
            "ru": ["tts_models/ru/multi-dataset/xtts_v2"],
        }

        # Cache directory
        self.config_manager = ConfigManager()
        self.cache_dir = self._get_cache_directory()

        # Supported formats
        self._supported_formats = [AudioFormat.WAV, AudioFormat.AIFF]

    def is_available(self) -> bool:
        """Check if CoquiTTS is available"""
        return COQUI_AVAILABLE and TTS_API_AVAILABLE

    async def initialize(self) -> None:
        """Initialize CoquiTTS with device detection"""
        if self._initialized:
            return

        if not self.is_available():
            raise EngineNotAvailableError(
                "CoquiTTS",
                "CoquiTTS not available. Install with: pip install coqui-tts"
            )

        try:
            config = self.config_manager.get_config()

            # Device detection with fallback
            if config.TTS_NOTIFY_COQUI_USE_GPU and torch.cuda.is_available():
                self._device = "cuda"
                logger.info("CoquiTTS: Using CUDA GPU acceleration")
            else:
                self._device = "cpu"
                if config.TTS_NOTIFY_COQUI_USE_GPU:
                    logger.info("CoquiTTS: GPU requested but not available, using CPU")
                else:
                    logger.info("CoquiTTS: Using CPU")

            # Asynchronous model loading
            logger.info(f"CoquiTTS: Loading model {self.model_name}...")
            self._tts = await asyncio.to_thread(
                TTS,
                model_name=self.model_name,
                progress_bar=False
            )

            self._initialized = True
            logger.info(f"CoquiTTS: Model {self.model_name} loaded successfully on {self._device}")

        except Exception as e:
            error_msg = f"Failed to initialize CoquiTTS: {str(e)}"
            logger.error(error_msg)
            raise EngineNotAvailableError("CoquiTTS", error_msg)

    async def cleanup(self) -> None:
        """Cleanup CoquiTTS resources"""
        if self._tts:
            self._tts = None
        self._initialized = False
        logger.info("CoquiTTS: Engine cleaned up")

    async def get_supported_voices(self) -> List[Voice]:
        """Get available voices from CoquiTTS model"""
        if not self._initialized:
            await self.initialize()

        voices = []

        try:
            # Multi-speaker model support
            if hasattr(self._tts, 'speakers') and self._tts.speakers:
                for i, speaker in enumerate(self._tts.speakers):
                    voices.append(Voice(
                        id=f"coqui_{speaker.lower().replace(' ', '_')}",
                        name=f"Coqui {speaker}",
                        language=self._infer_language(speaker),
                        gender=self._infer_gender(speaker),
                        quality=VoiceQuality.ENHANCED,
                        engine_name="coqui",
                        metadata={
                            "speaker_index": i,
                            "speaker_name": speaker,
                            "model": self.model_name,
                            "multi_lingual": getattr(self._tts, 'is_multi_lingual', False),
                            "engine_type": TTSEngineType.COQUI.value
                        }
                    ))

            # Single-speaker model fallback
            if not voices:
                model_info = self._get_model_info(self.model_name)
                languages = model_info.languages if model_info else ["en"]
                primary_lang = languages[0] if languages else "en"

                voices.append(Voice(
                    id="coqui_default",
                    name="Coqui Default",
                    language=self._get_language_enum(primary_lang),
                    gender=Gender.UNKNOWN,
                    quality=VoiceQuality.ENHANCED,
                    engine_name="coqui",
                    metadata={
                        "model": self.model_name,
                        "multi_lingual": False,
                        "languages": languages,
                        "engine_type": TTSEngineType.COQUI.value
                    }
                ))

            logger.info(f"CoquiTTS: Found {len(voices)} voices")
            return voices

        except Exception as e:
            logger.error(f"Failed to get voices from CoquiTTS: {str(e)}")
            # Return minimal voice list as fallback
            return [Voice(
                id="coqui_fallback",
                name="Coqui Fallback",
                language=Language.ENGLISH,
                gender=Gender.UNKNOWN,
                quality=VoiceQuality.BASIC,
                engine_name="coqui",
                metadata={"engine_type": TTSEngineType.COQUI.value}
            )]

    async def check_language_availability(self, language: str) -> LanguageAvailability:
        """Check if language is available and model status"""

        # Check loaded model
        if self._initialized and hasattr(self._tts, 'is_multi_lingual') and self._tts.is_multi_lingual:
            supported_langs = getattr(self._tts, 'supported_languages', [])
            if hasattr(self._tts, 'languages'):
                supported_langs = self._tts.languages

            if language in supported_langs:
                return LanguageAvailability(
                    available=True,
                    source="loaded_model",
                    model=self.model_name,
                    download_required=False
                )

        # Check multi-language models
        for model_name, model_info in self.multi_language_models.items():
            if language in model_info.languages:
                if self._model_exists_locally(model_name):
                    return LanguageAvailability(
                        available=True,
                        source="cached_model",
                        model=model_name,
                        download_required=False,
                        size_gb=model_info.size_gb
                    )
                else:
                    return LanguageAvailability(
                        available=False,
                        source="downloadable",
                        model=model_name,
                        download_required=True,
                        size_gb=model_info.size_gb,
                        download_time_est=self._estimate_download_time(model_info.size_gb)
                    )

        # Check single-language models
        if language in self.single_language_models:
            for model_name in self.single_language_models[language]:
                if self._model_exists_locally(model_name):
                    return LanguageAvailability(
                        available=True,
                        source="specific_model",
                        model=model_name,
                        download_required=False
                    )
                else:
                    return LanguageAvailability(
                        available=False,
                        source="download_specific",
                        model=model_name,
                        download_required=True
                    )

        return LanguageAvailability(
            available=False,
            source="not_supported"
        )

    async def ensure_language_available(self, language: str) -> bool:
        """Ensure language is available (download if necessary)"""
        availability = await self.check_language_availability(language)

        if availability.available:
            return True

        config = self.config_manager.get_config()
        if config.TTS_NOTIFY_COQUI_OFFLINE_MODE:
            logger.warning(f"Language {language} not available and offline mode is enabled")
            return False

        if availability.source in ["downloadable", "download_specific"]:
            try:
                logger.info(f"Downloading model for language {language}: {availability.model}")
                return await self._download_model(availability.model)
            except Exception as e:
                logger.error(f"Failed to download model for {language}: {str(e)}")
                return False

        return False

    async def speak(self, request: TTSRequest) -> TTSResponse:
        """Convert text to speech and play it using CoquiTTS"""
        start_time = time.time()
        self.validate_request(request)

        try:
            # Handle language and model selection
            language = await self._determine_language_for_request(request)
            await self.ensure_language_available(language)

            # Get speaker for the language
            speaker = await self._get_speaker_for_request(request, language)

            # Synthesize speech
            if request.output_path:
                save_response = await self._save_to_file(request, speaker, language)
            else:
                audio_data = await self._synthesize_audio(request.text, speaker, language)
                save_response = TTSResponse(
                    success=True,
                    audio_data=audio_data,
                    duration=time.time() - start_time,
                    format=AudioFormat.WAV,
                    metadata={
                        "engine": "coqui",
                        "model": self.model_name,
                        "language": language,
                        "speaker": speaker,
                        "engine_type": TTSEngineType.COQUI.value
                    }
                )

            if save_response.success:
                logger.info(f"Successfully generated speech using CoquiTTS (language: {language}, speaker: {speaker})")

            return save_response

        except Exception as e:
            error_msg = f"Failed to generate speech with CoquiTTS: {str(e)}"
            logger.error(error_msg)
            return TTSResponse(success=False, error=error_msg)

    async def synthesize(self, request: TTSRequest) -> TTSResponse:
        """Convert text to speech and return audio data"""
        # For synthesize, we always return audio data
        request.output_path = None  # Ensure we don't save to file
        return await self.speak(request)

    async def save(self, request: TTSRequest, output_path: Path) -> TTSResponse:
        """Convert text to speech and save to file"""
        request.output_path = output_path
        return await self.speak(request)

    async def get_engine_info(self) -> Dict[str, Any]:
        """Get detailed engine information"""
        config = self.config_manager.get_config()

        base_info = {
            "name": self.name,
            "available": self.is_available(),
            "initialized": self._initialized,
            "model_name": self.model_name,
            "device": self._device,
            "engine_type": TTSEngineType.COQUI.value,
            "supports_multi_language": True,
            "supported_languages": [],
            "cache_dir": str(self.cache_dir),
            "auto_download": config.TTS_NOTIFY_AUTO_DOWNLOAD_MODELS,
            "offline_mode": config.TTS_NOTIFY_COQUI_OFFLINE_MODE
        }

        if self._initialized:
            try:
                # Add model-specific information
                model_info = self._get_model_info(self.model_name)
                if model_info:
                    base_info.update({
                        "supported_languages": model_info.languages,
                        "speakers_count": model_info.speakers,
                        "model_quality": model_info.quality,
                        "supports_streaming": model_info.streaming
                    })

                # Add supported formats
                base_info["supported_formats"] = [fmt.value for fmt in await self.get_supported_formats()]

                # Add voices count
                voices = await self.get_supported_voices()
                base_info["supported_voices_count"] = len(voices)

            except Exception as e:
                base_info["error"] = str(e)

        return base_info

    async def get_supported_formats(self) -> List[AudioFormat]:
        """Get supported audio formats"""
        return self._supported_formats

    def validate_request(self, request: TTSRequest) -> None:
        """Validate TTS request for CoquiTTS"""
        # Basic validation (parent class logic)
        if not isinstance(request, TTSRequest):
            raise ValidationError("Request must be a TTSRequest instance")

        # Validate format compatibility
        supported_formats = asyncio.run(self.get_supported_formats())
        if request.output_format not in supported_formats:
            raise ValidationError(
                f"Format '{request.output_format.value}' is not supported by CoquiTTS",
                field="output_format",
                value=request.output_format.value
            )

    # Private methods

    def _get_cache_directory(self) -> Path:
        """Get the cache directory for models"""
        config = self.config_manager.get_config()

        if config.TTS_NOTIFY_COQUI_MODEL_CACHE_DIR:
            cache_dir = Path(config.TTS_NOTIFY_COQUI_MODEL_CACHE_DIR)
        else:
            # Default CoquiTTS cache location
            cache_dir = Path.home() / ".local" / "share" / "tts"

        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def _model_exists_locally(self, model_name: str) -> bool:
        """Check if model exists locally"""
        try:
            model_path = self.cache_dir / model_name
            return model_path.exists() and any(model_path.iterdir())
        except Exception:
            return False

    async def _download_model(self, model_name: str) -> bool:
        """Download a model (simplified - CoquiTTS handles downloads automatically)"""
        try:
            config = self.config_manager.get_config()

            if not config.TTS_NOTIFY_AUTO_DOWNLOAD_MODELS:
                logger.info(f"Auto-download disabled, skipping download of {model_name}")
                return False

            # The actual download will be handled by CoquiTTS when we try to load the model
            # We'll validate by attempting to load it
            logger.info(f"Downloading model {model_name}...")

            # Try to load the model, which will trigger download if needed
            temp_tts = await asyncio.to_thread(TTS, model_name=model_name, progress_bar=False)

            # Clean up temporary instance
            del temp_tts

            logger.info(f"Model {model_name} downloaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to download model {model_name}: {str(e)}")
            return False

    def _estimate_download_time(self, size_gb: float) -> int:
        """Estimate download time in seconds"""
        # Assume 2.5MB/s average download speed
        mb_per_second = 2.5
        size_mb = size_gb * 1024
        return int(size_mb / mb_per_second)

    def _get_model_info(self, model_name: str) -> Optional[ModelInfo]:
        """Get model information"""
        return self.multi_language_models.get(model_name)

    async def _determine_language_for_request(self, request: TTSRequest) -> str:
        """Determine language based on request and configuration"""
        config = self.config_manager.get_config()

        # 1. Use language from request if specified
        if request.language and request.language != "auto":
            return request.language

        # 2. Use forced language from config
        if config.TTS_NOTIFY_FORCE_LANGUAGE and config.TTS_NOTIFY_DEFAULT_LANGUAGE != "auto":
            return config.TTS_NOTIFY_DEFAULT_LANGUAGE

        # 3. Use preferred language from config
        if config.TTS_NOTIFY_DEFAULT_LANGUAGE != "auto":
            return config.TTS_NOTIFY_DEFAULT_LANGUAGE

        # 4. Auto-detection (let CoquiTTS handle)
        return "auto"

    async def _get_speaker_for_request(self, request: TTSRequest, language: str) -> str:
        """Get appropriate speaker for request"""
        config = self.config_manager.get_config()

        # Use specified speaker if available
        if config.TTS_NOTIFY_COQUI_SPEAKER and self._tts and hasattr(self._tts, 'speakers'):
            speakers = self._tts.speakers
            if config.TTS_NOTIFY_COQUI_SPEAKER in speakers:
                return config.TTS_NOTIFY_COQUI_SPEAKER

        # Use voice from request if it maps to a Coqui voice
        if request.voice and hasattr(request.voice, 'metadata') and request.voice.metadata.get('engine_type') == TTSEngineType.COQUI.value:
            speaker_name = request.voice.metadata.get('speaker_name')
            if speaker_name:
                return speaker_name

        # Default: first available speaker
        if self._tts and hasattr(self._tts, 'speakers') and self._tts.speakers:
            return self._tts.speakers[0]

        return "default"

    def _infer_language(self, speaker_name: str) -> Language:
        """Infer language from speaker name"""
        speaker_lower = speaker_name.lower()

        # Language indicators in speaker names
        language_indicators = {
            'spanish': Language.SPANISH,
            'español': Language.SPANISH,
            'es': Language.SPANISH,
            'english': Language.ENGLISH,
            'en': Language.ENGLISH,
            'french': Language.FRENCH,
            'français': Language.FRENCH,
            'fr': Language.FRENCH,
            'german': Language.GERMAN,
            'deutsch': Language.GERMAN,
            'de': Language.GERMAN,
            'italian': Language.ITALIAN,
            'italiano': Language.ITALIAN,
            'it': Language.ITALIAN,
            'portuguese': Language.PORTUGUESE,
            'português': Language.PORTUGUESE,
            'pt': Language.PORTUGUESE,
            'japanese': Language.JAPANESE,
            '日本語': Language.JAPANESE,
            'ja': Language.JAPANESE,
            'chinese': Language.CHINESE,
            '中文': Language.CHINESE,
            'zh': Language.CHINESE,
            'korean': Language.KOREAN,
            '한국어': Language.KOREAN,
            'ko': Language.KOREAN,
            'russian': Language.RUSSIAN,
            'русский': Language.RUSSIAN,
            'ru': Language.RUSSIAN,
            'polish': Language.RUSSIAN,
            'polski': Language.RUSSIAN,
            'pl': Language.RUSSIAN,
            'dutch': Language.RUSSIAN,
            'nederlands': Language.RUSSIAN,
            'nl': Language.RUSSIAN,
        }

        for indicator, lang in language_indicators.items():
            if indicator in speaker_lower:
                return lang

        # Default to English if no indicator found
        return Language.ENGLISH

    def _infer_gender(self, speaker_name: str) -> Gender:
        """Infer gender from speaker name"""
        speaker_lower = speaker_name.lower()

        # Female indicators
        female_indicators = ['female', 'woman', 'girl', 'female_', 'fem', 'woma', 'women']

        # Male indicators
        male_indicators = ['male', 'man', 'boy', 'male_', 'men']

        for indicator in female_indicators:
            if indicator in speaker_lower:
                return Gender.FEMALE

        for indicator in male_indicators:
            if indicator in speaker_lower:
                return Gender.MALE

        # Check specific name patterns
        if any(name in speaker_lower for name in ['maria', 'ana', 'lucia', 'sofia', 'isabella', 'sarah', 'emma']):
            return Gender.FEMALE

        if any(name in speaker_lower for name in ['john', 'david', 'michael', 'james', 'robert', 'william']):
            return Gender.MALE

        return Gender.UNKNOWN

    def _get_language_enum(self, language_code: str) -> Language:
        """Convert language code to Language enum"""
        language_map = {
            'en': Language.ENGLISH,
            'es': Language.SPANISH,
            'fr': Language.FRENCH,
            'de': Language.GERMAN,
            'it': Language.ITALIAN,
            'pt': Language.PORTUGUESE,
            'ja': Language.JAPANESE,
            'zh': Language.CHINESE,
            'ko': Language.KOREAN,
            'ru': Language.RUSSIAN,
            'pl': Language.RUSSIAN,  # Using existing enum
            'nl': Language.RUSSIAN,  # Using existing enum
        }

        return language_map.get(language_code.lower(), Language.ENGLISH)

    async def _synthesize_audio(self, text: str, speaker: str, language: str) -> bytes:
        """Synthesize audio using CoquiTTS"""
        try:
            # For CoquiTTS, we synthesize to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = Path(temp_file.name)

            # Generate speech
            self._tts.tts_to_file(
                text=text,
                speaker=speaker,
                language=language if language != "auto" else None,
                file_path=str(temp_path)
            )

            # Read and return audio data
            audio_data = temp_path.read_bytes()

            # Clean up
            temp_path.unlink(missing_ok=True)

            return audio_data

        except Exception as e:
            logger.error(f"Failed to synthesize audio: {str(e)}")
            raise TTSError(f"Audio synthesis failed: {str(e)}")

    # Phase C: Audio Pipeline Integration

    async def process_audio_pipeline(self, audio_data: bytes, source_format: AudioFormat,
                                   target_format: AudioFormat, language: Optional[str] = None,
                                   quality_level: Optional[str] = None) -> Tuple[bytes, Dict[str, Any]]:
        """
        Process audio through the advanced audio pipeline
        """
        try:
            config = self.config_manager.get_config()

            # Check if pipeline processing is enabled
            if not config.TTS_NOTIFY_COQUI_CONVERSION_ENABLED:
                # If disabled, only do basic format conversion if needed
                if source_format != target_format:
                    return await audio_processor._convert_format(audio_data, source_format, target_format), {}
                return audio_data, {}

            logger.info(f"Processing audio pipeline: {source_format.value} -> {target_format.value}")

            # Process through audio pipeline
            processed_audio, metrics = await audio_processor.process_audio(
                audio_data=audio_data,
                source_format=source_format,
                target_format=target_format,
                language=language,
                quality_level=quality_level
            )

            # Convert metrics to serializable format
            metrics_dict = {
                "processing_time": metrics.processing_time,
                "input_size_bytes": metrics.input_size_bytes,
                "output_size_bytes": metrics.output_size_bytes,
                "compression_ratio": metrics.compression_ratio,
                "peak_level_dbfs": metrics.peak_level_dbfs,
                "rms_level_dbfs": metrics.rms_level_dbfs,
                "dynamic_range_db": metrics.dynamic_range_dbfs,
                "spectral_centroid": metrics.spectral_centroid,
                "zero_crossing_rate": metrics.zero_crossing_rate,
                "stages_completed": [stage.value for stage in metrics.stages_completed],
                "warnings": metrics.warnings,
                "language": language,
                "quality_level": quality_level
            }

            logger.info(f"Audio pipeline completed in {metrics.processing_time:.2f}s")
            return processed_audio, metrics_dict

        except Exception as e:
            error_msg = f"Audio pipeline processing failed: {str(e)}"
            logger.error(error_msg)
            raise TTSError(error_msg)

    async def get_pipeline_capabilities(self) -> Dict[str, Any]:
        """Get audio pipeline processing capabilities"""
        try:
            capabilities = audio_processor.get_processing_capabilities()

            # Add engine-specific information
            config = self.config_manager.get_config()
            capabilities.update({
                "engine_name": self.name,
                "engine_available": self.is_available(),
                "engine_initialized": self._initialized,
                "pipeline_enabled": config.TTS_NOTIFY_COQUI_CONVERSION_ENABLED,
                "auto_clean_audio": config.TTS_NOTIFY_COQUI_AUTO_CLEAN_AUDIO,
                "auto_trim_silence": config.TTS_NOTIFY_COQUI_AUTO_TRIM_SILENCE,
                "noise_reduction": config.TTS_NOTIFY_COQUI_NOISE_REDUCTION,
                "target_formats": config.TTS_NOTIFY_COQUI_TARGET_FORMATS.split(',') if config.TTS_NOTIFY_COQUI_TARGET_FORMATS else ["wav"],
                "embedding_cache": config.TTS_NOTIFY_COQUI_EMBEDDING_CACHE,
                "embedding_format": config.TTS_NOTIFY_COQUI_EMBEDDING_FORMAT,
                "diarization": config.TTS_NOTIFY_COQUI_DIARIZATION
            })

            return capabilities

        except Exception as e:
            logger.error(f"Failed to get pipeline capabilities: {e}")
            return {"error": str(e)}

    async def _save_to_file(self, request: TTSRequest, speaker: str, language: str) -> TTSResponse:
        """Save synthesized audio to file"""
        try:
            # Ensure output directory exists
            output_path = request.output_path or Path.home() / "Desktop" / "coqui_output.wav"
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate and save audio
            self._tts.tts_to_file(
                text=request.text,
                speaker=speaker,
                language=language if language != "auto" else None,
                file_path=str(output_path)
            )

            return TTSResponse(
                success=True,
                file_path=output_path,
                format=AudioFormat.WAV,
                metadata={
                    "engine": "coqui",
                    "model": self.model_name,
                    "language": language,
                    "speaker": speaker,
                    "file_size": output_path.stat().st_size,
                    "engine_type": TTSEngineType.COQUI.value
                }
            )

        except Exception as e:
            logger.error(f"Failed to save audio to file: {str(e)}")
            return TTSResponse(
                success=False,
                error=f"Failed to save audio: {str(e)}"
            )

      # Phase B: Voice Cloning Methods

    async def clone_voice(self, request: VoiceCloningRequest) -> VoiceCloningResponse:
        """
        Clone a voice using the integrated voice cloning system
        """
        try:
            # Check if cloning is enabled
            config = self.config_manager.get_config()
            if not config.TTS_NOTIFY_COQUI_ENABLE_CLONING:
                return VoiceCloningResponse(
                    success=False,
                    error="Voice cloning is disabled. Set TTS_NOTIFY_COQUI_ENABLE_CLONING=true"
                )

            logger.info(f"Starting voice cloning in CoquiTTS: {request.voice_name}")

            # Delegate to voice cloner
            response = await voice_cloner.clone_voice(request)

            if response.success and response.voice:
                # Register the cloned voice with the engine
                await self._register_cloned_voice(response.voice)

            return response

        except Exception as e:
            error_msg = f"Voice cloning failed in CoquiTTS: {str(e)}"
            logger.error(error_msg)
            return VoiceCloningResponse(
                success=False,
                error=error_msg
            )

    async def _register_cloned_voice(self, voice: Voice) -> None:
        """
        Register a cloned voice with the engine
        """
        try:
            # Add to internal voice cache
            if not hasattr(self, '_cloned_voices'):
                self._cloned_voices = []

            self._cloned_voices.append(voice)
            logger.info(f"Cloned voice registered: {voice.name} ({voice.id})")

        except Exception as e:
            logger.warning(f"Failed to register cloned voice {voice.name}: {e}")

    async def get_cloned_voices(self) -> List[Voice]:
        """
        Get list of cloned voices
        """
        try:
            # Get from voice cloner
            return await voice_cloner.list_cloned_voices()

        except Exception as e:
            logger.error(f"Failed to get cloned voices: {e}")
            return []

    async def delete_cloned_voice(self, voice_id: str) -> bool:
        """
        Delete a cloned voice
        """
        try:
            success = await voice_cloner.delete_cloned_voice(voice_id)

            if success and hasattr(self, '_cloned_voices'):
                # Remove from internal cache
                self._cloned_voices = [
                    v for v in self._cloned_voices
                    if v.id != voice_id and not v.id.startswith(f"cloned_{voice_id}")
                ]

            return success

        except Exception as e:
            logger.error(f"Failed to delete cloned voice {voice_id}: {e}")
            return False

    async def get_cloning_status(self) -> Dict[str, Any]:
        """
        Get voice cloning system status
        """
        try:
            # Get basic status from voice cloner
            cloning_status = await voice_cloner.get_cloning_status()

            # Add engine-specific information
            cloning_status.update({
                "engine_available": self.is_available(),
                "engine_initialized": self._initialized,
                "model_name": self.model_name,
                "supports_cloning": True,
                "engine_type": "coqui"
            })

            return cloning_status

        except Exception as e:
            logger.error(f"Failed to get cloning status: {e}")
            return {"error": str(e)}

    def is_model_downloaded(self) -> bool:
        """
        Check if the primary model is downloaded
        """
        return self._model_exists_locally(self.model_name)

    async def get_supported_formats(self) -> List[AudioFormat]:
        """Get supported audio formats"""
        base_formats = self._supported_formats

        # Add additional formats for cloned voices if available
        if hasattr(self, '_cloned_voices') and self._cloned_voices:
            # Cloned voices might support more formats
            extended_formats = base_formats.copy()
            if AudioFormat.MP3 not in extended_formats:
                extended_formats.append(AudioFormat.MP3)
            if AudioFormat.OGG not in extended_formats:
                extended_formats.append(AudioFormat.OGG)
            return extended_formats

        return base_formats

    async def speak_with_cloned_voice(self, request: TTSRequest, cloned_voice: Voice) -> TTSResponse:
        """
        Speak using a cloned voice with enhanced processing
        """
        try:
            if not cloned_voice.is_cloned:
                return await self.speak(request)

            # Enhanced processing for cloned voices
            logger.info(f"Using cloned voice: {cloned_voice.name}")

            # Load voice profile if available
            if hasattr(cloned_voice, 'profile_path') and cloned_voice.profile_path:
                profile_path = Path(cloned_voice.profile_path)
                if profile_path.exists():
                    # Apply voice-specific optimizations
                    request.metadata["cloned_voice"] = True
                    request.metadata["voice_id"] = cloned_voice.id
                    request.metadata["optimization_score"] = cloned_voice.optimization_score

            # Generate speech with cloned voice
            response = await self.speak(request)

            if response.success:
                response.metadata["cloned_voice_name"] = cloned_voice.name
                response.metadata["cloned_voice_quality"] = cloned_voice.cloning_quality

            return response

        except Exception as e:
            error_msg = f"Failed to speak with cloned voice {cloned_voice.name}: {str(e)}"
            logger.error(error_msg)
            return TTSResponse(success=False, error=error_msg)

    async def validate_cloning_request(self, request: VoiceCloningRequest) -> List[str]:
        """
        Validate a voice cloning request
        """
        errors = []

        try:
            # Check if cloning is enabled
            config = self.config_manager.get_config()
            if not config.TTS_NOTIFY_COQUI_ENABLE_CLONING:
                errors.append("Voice cloning is disabled")

            # Validate source file
            if not request.source_audio_path.exists():
                errors.append(f"Source audio file not found: {request.source_audio_path}")

            # Validate audio duration
            try:
                import librosa
                duration = librosa.get_duration(filename=str(request.source_audio_path))
                min_duration = config.TTS_NOTIFY_COQUI_MIN_SAMPLE_SECONDS
                max_duration = config.TTS_NOTIFY_COQUI_MAX_SAMPLE_SECONDS

                if duration < min_duration:
                    errors.append(f"Audio too short: {duration:.2f}s (minimum: {min_duration}s)")
                if duration > max_duration:
                    errors.append(f"Audio too long: {duration:.2f}s (maximum: {max_duration}s)")
            except Exception as e:
                errors.append(f"Failed to analyze audio duration: {e}")

            # Validate voice name
            if not request.voice_name or len(request.voice_name.strip()) < 2:
                errors.append("Voice name must be at least 2 characters long")

            # Validate language support
            model_info = self._get_model_info(self.model_name)
            if model_info and request.language not in model_info.languages:
                errors.append(f"Language '{request.language}' not supported by model {self.model_name}")

        except Exception as e:
            errors.append(f"Validation error: {e}")

        return errors

    def __repr__(self) -> str:
        return f"CoquiTTSEngine(model='{self.model_name}', device='{self._device}', initialized={self._initialized})"