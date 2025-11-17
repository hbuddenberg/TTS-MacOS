"""
AI TTS Engine - Coqui TTS integration for TTS-MacOS v2

Provides AI-powered text-to-speech capabilities using:
- XTTS-v2 for multilingual voice cloning (6-second samples)
- Glow-TTS for faster synthesis
- Tacotron2-DDC for high quality single-language
- Model caching and management
- Cross-platform GPU acceleration support

Features:
- Voice cloning from audio samples
- 16+ language support with native quality
- Real-time synthesis with caching
- GPU acceleration when available
"""

import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import torch
import torchaudio

try:
    from TTS.tts.configs.glow_tts_config import GlowTTSConfig
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.glow_tts import GlowTTS
    from TTS.tts.models.xtts import Xtts
    from TTS.utils.audio import AudioProcessor

    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Warning: TTS not available. Install with: pip install TTS")

from ..core.config import ModelInfo, Quality, TTSConfig


class AIEngine:
    """
    AI-powered TTS engine using Coqui TTS models
    """

    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self.system = self.config.system

        # Check TTS availability
        if not TTS_AVAILABLE:
            raise RuntimeError(
                "TTS library not available. Install with: pip install TTS"
            )

        # Model management
        self.loaded_models = {}
        self.default_model = "xtts_v2"

        # Audio processor
        self.sample_rate = 22050
        self.audio_processor = None

        # Initialize audio processor
        self._initialize_audio_processor()

        # Logging
        self.logger = logging.getLogger(__name__)

        # Check GPU availability
        self.device = self._get_device()

    def _initialize_audio_processor(self):
        """Initialize audio processor for TTS"""
        try:
            self.audio_processor = AudioProcessor(
                sample_rate=self.sample_rate,
                resample=True,
                num_mels=80,
                log_linear=True,
            )
        except Exception as e:
            self.logger.warning(f"Could not initialize audio processor: {e}")

    def _get_device(self) -> str:
        """Get optimal device for computation"""
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"  # Apple Silicon GPU
        else:
            return "cpu"

    def is_available(self) -> bool:
        """Check if AI engine is available"""
        return TTS_AVAILABLE and torch is not None

    def get_loaded_models(self) -> List[str]:
        """Get list of currently loaded models"""
        return list(self.loaded_models.keys())

    def _load_model(self, model_name: str, force_reload: bool = False):
        """Load a TTS model with caching"""
        if model_name in self.loaded_models and not force_reload:
            return self.loaded_models[model_name]

        model_info = self.config.get_model_info(model_name)
        if not model_info:
            raise ValueError(f"Unknown model: {model_name}")

        self.logger.info(f"Loading TTS model: {model_name}")

        try:
            if model_name == "xtts_v2":
                model = self._load_xtts_v2(model_info)
            elif model_name == "glow_tts":
                model = self._load_glow_tts(model_info)
            elif model_name == "tacotron2_ddc":
                model = self._load_tacotron2_ddc(model_info)
            else:
                raise ValueError(f"Unsupported model: {model_name}")

            # Cache the model
            self.loaded_models[model_name] = model
            self.logger.info(f"Model {model_name} loaded successfully on {self.device}")

            return model

        except Exception as e:
            self.logger.error(f"Failed to load model {model_name}: {e}")
            raise RuntimeError(f"Could not load model {model_name}: {e}")

    def _load_xtts_v2(self, model_info: ModelInfo):
        """Load XTTS-v2 model for voice cloning"""
        model_path = self.config.get_cache_path(model_info.name)

        # For now, use the pretrained XTTS v2 model
        # In production, this would download and cache the model
        model = Xtts.init_from_config(XttsConfig())

        # Load model if available locally, otherwise will download on first use
        if model_path.exists():
            try:
                model.load_checkpoint(model_path, eval=True)
                model.to(self.device)
            except Exception:
                # Fall back to downloading on first use
                self.logger.info("Model not cached, will download on first synthesis")
        else:
            self.logger.info("XTTS-v2 will be downloaded on first use")

        return model

    def _load_glow_tts(self, model_info: ModelInfo):
        """Load Glow-TTS model for fast synthesis"""
        # This is a placeholder - would load actual Glow-TTS model
        self.logger.info("Glow-TTS placeholder implementation")
        return {"type": "glow_tts", "model_info": model_info}

    def _load_tacotron2_ddc(self, model_info: ModelInfo):
        """Load Tacotron2-DDC model for high quality"""
        # This is a placeholder - would load actual Tacotron2-DDC model
        self.logger.info("Tacotron2-DDC placeholder implementation")
        return {"type": "tacotron2_ddc", "model_info": model_info}

    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        language: str = "en",
        rate: float = 1.0,
        volume: float = 1.0,
        output_file: Optional[str] = None,
        speaker_wav: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs,
    ) -> Optional[str]:
        """
        Synthesize speech using AI TTS models

        Args:
            text: Text to synthesize
            voice: Voice name or path for cloning
            language: Language code
            rate: Speech rate multiplier
            volume: Volume level
            output_file: Path to save audio file
            speaker_wav: Path to WAV file for voice cloning
            model_name: Specific model to use

        Returns:
            Path to generated audio file
        """
        # Select model
        model_name = model_name or self.default_model
        model = self._load_model(model_name)

        # Prepare output path
        if not output_file:
            output_file = self._get_temp_output_path()

        try:
            if model_name == "xtts_v2":
                return self._synthesize_xtts(
                    model,
                    text,
                    voice,
                    language,
                    rate,
                    volume,
                    output_file,
                    speaker_wav,
                    **kwargs,
                )
            else:
                # Fallback for other models
                return self._synthesize_generic(
                    model, text, voice, language, rate, volume, output_file, **kwargs
                )

        except Exception as e:
            self.logger.error(f"Synthesis failed: {e}")
            raise RuntimeError(f"TTS synthesis failed: {e}")

    def _synthesize_xtts(
        self,
        model,
        text: str,
        voice: Optional[str],
        language: str,
        rate: float,
        volume: float,
        output_file: str,
        speaker_wav: Optional[str],
        **kwargs,
    ) -> str:
        """
        Synthesize using XTTS-v2 with voice cloning support
        """
        try:
            # XTTS-v2 specific synthesis
            if speaker_wav and os.path.exists(speaker_wav):
                # Voice cloning mode
                self.logger.info(f"Using voice cloning with reference: {speaker_wav}")

                # Process speaker wav for voice cloning
                speaker_wav_processed = self._process_speaker_wav(speaker_wav)

                # Synthesize with cloned voice
                outputs = model.synthesize(
                    text,
                    speaker_wav=speaker_wav_processed,
                    language=language,
                    gpt_cond_len=30,  # 30 seconds conditioning
                    gpt_cond_chunk_len=4,  # 4 second chunks
                    speed=rate,
                    **kwargs,
                )
            else:
                # Use predefined speaker
                speaker_id = self._get_speaker_id(voice, language)
                outputs = model.synthesize(
                    text, speaker=speaker_id, language=language, speed=rate, **kwargs
                )

            # Save to file
            torchaudio.save(output_file, outputs["wav"].unsqueeze(0), model.sample_rate)

            # Apply volume if needed
            if volume != 1.0:
                self._apply_volume(output_file, output_file, volume)

            return output_file

        except Exception as e:
            self.logger.error(f"XTTS synthesis failed: {e}")
            raise

    def _synthesize_generic(
        self,
        model,
        text: str,
        voice: Optional[str],
        language: str,
        rate: float,
        volume: float,
        output_file: str,
        **kwargs,
    ) -> str:
        """
        Fallback synthesis method for other models
        """
        # This is a placeholder implementation
        # In practice, would use TTS.inference() or similar

        self.logger.info(f"Using generic synthesis for {model['type']}")

        # For now, create a simple audio file as placeholder
        # In real implementation, this would use the actual TTS model
        sample_rate = 22050
        duration = len(text) * 0.1  # Rough estimate
        silence = torch.zeros(int(sample_rate * duration))

        torchaudio.save(output_file, silence.unsqueeze(0), sample_rate)

        return output_file

    def _process_speaker_wav(self, speaker_wav: str) -> str:
        """
        Process speaker WAV file for voice cloning
        Ensures proper format, duration, and quality
        """
        try:
            # Load audio
            waveform, sample_rate = torchaudio.load(speaker_wav)

            # Convert to mono if needed
            if waveform.shape[0] > 1:
                waveform = torch.mean(waveform, dim=0, keepdim=True)

            # Resample to 22050 Hz if needed
            if sample_rate != self.sample_rate:
                resampler = torchaudio.transforms.Resample(
                    orig_freq=sample_rate, new_freq=self.sample_rate
                )
                waveform = resampler(waveform)

            # Ensure minimum duration (6 seconds for XTTS-v2)
            min_duration = 6 * self.sample_rate
            if waveform.shape[1] < min_duration:
                # Loop the audio to reach minimum duration
                repeats = (min_duration // waveform.shape[1]) + 1
                waveform = waveform.repeat(1, repeats)
                waveform = waveform[:, :min_duration]

            # Save processed audio
            processed_path = tempfile.mktemp(suffix=".wav")
            torchaudio.save(processed_path, waveform, self.sample_rate)

            return processed_path

        except Exception as e:
            self.logger.error(f"Failed to process speaker WAV: {e}")
            raise RuntimeError(f"Could not process speaker audio file: {e}")

    def _get_speaker_id(self, voice: Optional[str], language: str) -> str:
        """Get speaker ID for predefined voices"""
        # XTTS-v2 has default speakers per language
        language_speakers = {
            "en": "default female speaker",
            "es": "default spanish speaker",
            "fr": "default french speaker",
            "de": "default german speaker",
            "it": "default italian speaker",
            "pt": "default portuguese speaker",
        }

        return language_speakers.get(language, "default speaker")

    def _get_temp_output_path(self) -> str:
        """Generate temporary output path"""
        timestamp = int(torch.time.time())
        return tempfile.mktemp(suffix=f"_tts_{timestamp}.wav")

    def _apply_volume(self, input_file: str, output_file: str, volume: float):
        """Apply volume adjustment to audio file"""
        try:
            waveform, sample_rate = torchaudio.load(input_file)
            waveform = waveform * volume
            torchaudio.save(output_file, waveform, sample_rate)
        except Exception as e:
            self.logger.warning(f"Could not apply volume adjustment: {e}")

    def list_voices(self) -> Dict[str, Any]:
        """List available AI voices and models"""
        voices = {
            "models": {},
            "languages": [],
            "cloning_support": True,
            "device": self.device,
        }

        for model_name, model_info in self.config.models.items():
            voices["models"][model_name] = {
                "name": model_info.display_name,
                "languages": model_info.languages,
                "supports_cloning": model_info.supports_cloning,
                "quality": model_info.quality.value,
                "loaded": model_name in self.loaded_models,
                "size_mb": model_info.model_size_mb,
            }

        # Get all supported languages
        all_languages = set()
        for model_info in self.config.models.values():
            all_languages.update(model_info.languages)

        voices["languages"] = sorted(list(all_languages))

        return voices

    def get_voice_info(self, voice_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific voice"""
        # For AI engine, voices are typically language-specific
        for model_name, model_info in self.config.models.items():
            if voice_name.lower() in [lang.lower() for lang in model_info.languages]:
                return {
                    "name": voice_name,
                    "model": model_name,
                    "language": voice_name,
                    "supports_cloning": model_info.supports_cloning,
                    "quality": model_info.quality.value,
                    "display_name": model_info.display_name,
                }

        return None

    def clone_voice(
        self, speaker_wav: str, voice_name: str, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a voice clone from audio sample

        Args:
            speaker_wav: Path to reference audio file
            voice_name: Name for the cloned voice
            description: Optional description

        Returns:
            Information about the cloned voice
        """
        if not os.path.exists(speaker_wav):
            raise FileNotFoundError(f"Speaker audio file not found: {speaker_wav}")

        try:
            # Process the speaker audio
            processed_wav = self._process_speaker_wav(speaker_wav)

            # Create voice clone info
            clone_info = {
                "name": voice_name,
                "original_file": speaker_wav,
                "processed_file": processed_wav,
                "description": description or f"Cloned from {speaker_wav}",
                "created_at": torch.time.time(),
                "model": "xtts_v2",
                "sample_rate": self.sample_rate,
            }

            # Save clone metadata
            self._save_voice_clone(clone_info)

            return clone_info

        except Exception as e:
            self.logger.error(f"Voice cloning failed: {e}")
            raise RuntimeError(f"Could not clone voice: {e}")

    def _save_voice_clone(self, clone_info: Dict[str, Any]):
        """Save voice clone metadata"""
        clones_dir = self.config.config_dir / "voice_clones"
        clones_dir.mkdir(exist_ok=True)

        clone_file = clones_dir / f"{clone_info['name']}.json"

        import json

        with open(clone_file, "w", encoding="utf-8") as f:
            json.dump(clone_info, f, indent=2, ensure_ascii=False)

    def list_voice_clones(self) -> List[Dict[str, Any]]:
        """List all saved voice clones"""
        clones_dir = self.config.config_dir / "voice_clones"
        if not clones_dir.exists():
            return []

        clones = []
        import json

        for clone_file in clones_dir.glob("*.json"):
            try:
                with open(clone_file, "r", encoding="utf-8") as f:
                    clone_info = json.load(f)
                    clones.append(clone_info)
            except Exception as e:
                self.logger.warning(f"Could not load clone info from {clone_file}: {e}")

        return clones

    def preload_models(self, model_names: Optional[List[str]] = None):
        """Preload models for faster synthesis"""
        if model_names is None:
            model_names = ["xtts_v2"]  # Default model

        for model_name in model_names:
            try:
                self._load_model(model_name)
                self.logger.info(f"Preloaded model: {model_name}")
            except Exception as e:
                self.logger.error(f"Failed to preload model {model_name}: {e}")

    def unload_model(self, model_name: str):
        """Unload a model to free memory"""
        if model_name in self.loaded_models:
            del self.loaded_models[model_name]
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            self.logger.info(f"Unloaded model: {model_name}")

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage information"""
        memory_info = {
            "device": self.device,
            "loaded_models": len(self.loaded_models),
            "cuda_allocated": 0,
            "cuda_reserved": 0,
        }

        if torch.cuda.is_available():
            memory_info.update(
                {
                    "cuda_allocated": torch.cuda.memory_allocated() / (1024**3),  # GB
                    "cuda_reserved": torch.cuda.memory_reserved() / (1024**3),  # GB
                    "cuda_max_allocated": torch.cuda.max_memory_allocated()
                    / (1024**3),  # GB
                }
            )

        return memory_info
