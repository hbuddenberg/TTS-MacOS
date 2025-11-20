"""
Voice System for TTS Notify v2

This module provides unified voice management across all TTS engines.
Handles voice detection, searching, categorization, and filtering with caching.
"""

import asyncio
import subprocess
import unicodedata
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any, Callable
import re
import time
import logging

from .models import Voice, Gender, VoiceQuality, Language
from .exceptions import VoiceDetectionError, VoiceNotFoundError, ValidationError
from .config_manager import config_manager

logger = logging.getLogger(__name__)


class VoiceFilter:
    """Voice filtering utility with enhanced logic from v1.5.0"""

    def __init__(self):
        self._gender_patterns = {
            Gender.MALE: [
                r'\bmale\b', r'\bman\b', r'\bboy\b', r'\bhombre\b', r'\bmasculino\b',
                # Spanish male voices from v1.5.0
                r'\bjorge\b', r'\bjuan\b', r'\bdiego\b', r'\bcarlos\b', r'\balberto\b',
                r'\brey\b', r'\brocko\b', r'\breed\b', r'\bgrandpa\b'
            ],
            Gender.FEMALE: [
                r'\bfemale\b', r'\bwoman\b', r'\bgirl\b', r'\blady\b', r'\bmujer\b', r'\bfemenino\b',
                # Spanish female voices from v1.5.0
                r'\bmonica\b', r'\bpaulina\b', r'\bangelica\b', r'\bmaria\b', r'\bsandy\b',
                r'\bflo\b', r'\bshelley\b', r'\bgrandma\b', r'\bmarisol\b', r'\bisabela\b',
                r'\bsoledad\b', r'\bfrancisca\b', r'\bmónica\b', r'\bjimena\b', r'\bangélica\b'
            ]
        }

        self._quality_patterns = {
            VoiceQuality.ENHANCED: [r'\benhanced\b'],
            VoiceQuality.PREMIUM: [r'\bpremium\b'],
            VoiceQuality.SIRI: [r'\bsiri\b'],
            VoiceQuality.NEURAL: [r'\bneural\b', r'\bneural2\b']
        }

        self._language_patterns = {
            Language.SPANISH: [
                r'\bspanish\b', r'\bespañol\b',
                # Spanish locale patterns
                r'\bes_es\b', r'\bspain\b', r'\bespaña\b',
                r'\bes_mx\b', r'\bmexico\b', r'\bméxico\b',
                r'\bes_ar\b', r'\bargentina\b',
                r'\bes_cl\b', r'\bchile\b',
                r'\bes_co\b', r'\bcolombia\b'
            ],
            Language.ENGLISH: [
                r'\benglish\b', r'\ben_us\b', r'\bunited\b'
            ]
        }

    def filter_by_gender(self, voices: List[Voice], gender: Gender) -> List[Voice]:
        """Filter voices by gender with enhanced patterns"""
        if gender == Gender.UNKNOWN:
            return voices

        filtered_voices = []
        patterns = self._gender_patterns.get(gender, [])

        for voice in voices:
            # Direct gender match
            if voice.gender == gender:
                filtered_voices.append(voice)
                continue

            # Pattern matching in description
            voice_text = f"{voice.name} {voice.description or ''}".lower()
            if any(re.search(pattern, voice_text, re.IGNORECASE) for pattern in patterns):
                filtered_voices.append(voice)

        return filtered_voices

    def filter_by_language(self, voices: List[Voice], language: Language) -> List[Voice]:
        """Filter voices by language"""
        if language == Language.UNKNOWN:
            return voices

        filtered_voices = []
        patterns = self._language_patterns.get(language, [])

        for voice in voices:
            # Direct language match
            if voice.language == language:
                filtered_voices.append(voice)
                continue

            # Pattern matching in description
            voice_text = f"{voice.name} {voice.description or ''}".lower()
            if any(re.search(pattern, voice_text, re.IGNORECASE) for pattern in patterns):
                filtered_voices.append(voice)

        return filtered_voices

    def filter_by_locale(self, voices: List[Voice], locale: str) -> List[Voice]:
        """Filter voices by locale with improved pattern matching"""
        if not locale:
            return voices

        # Normalize locale format
        locale = locale.replace('-', '_').lower()

        filtered_voices = []
        for voice in voices:
            if voice.locale:
                voice_locale = voice.locale.lower()
                if voice_locale == locale or voice_locale.startswith(locale.split('_')[0]):
                    filtered_voices.append(voice)

        return filtered_voices

    def filter_by_quality(self, voices: List[Voice], quality: VoiceQuality) -> List[Voice]:
        """Filter voices by quality"""
        if quality == VoiceQuality.BASIC:
            return voices

        filtered_voices = []
        patterns = self._quality_patterns.get(quality, [])

        for voice in voices:
            # Direct quality match
            if voice.quality == quality:
                filtered_voices.append(voice)
                continue

            # Pattern matching in description
            voice_text = f"{voice.name} {voice.description or ''}".lower()
            if any(re.search(pattern, voice_text, re.IGNORECASE) for pattern in patterns):
                filtered_voices.append(voice)

        return filtered_voices


class VoiceDetector(ABC):
    """Abstract base class for voice detectors"""

    @abstractmethod
    async def detect_voices(self) -> List[Voice]:
        """Detect available voices"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the detector is available on the current system"""
        pass


class MacOSVoiceDetector(VoiceDetector):
    """Voice detector for macOS native TTS with enhanced v1.5.0 logic"""

    def __init__(self, cache_ttl: int = 300):
        self._say_command = "say"
        self._cache_ttl = cache_ttl
        self._cache = None
        self._cache_timestamp = 0

    def is_available(self) -> bool:
        """Check if say command is available"""
        try:
            subprocess.run([self._say_command, "-v", "?"],
                         capture_output=True, timeout=5, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    async def detect_voices(self) -> List[Voice]:
        """Detect macOS system voices with caching"""
        current_time = time.time()

        # Check cache
        if (self._cache and
            current_time - self._cache_timestamp < self._cache_ttl):
            logger.debug("Using cached voice list")
            return self._cache.copy()

        try:
            # Run say -v ? to get voice list
            process = await asyncio.create_subprocess_exec(
                self._say_command, "-v", "?",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise VoiceDetectionError("macOS TTS", stderr.decode() if stderr else "Unknown error")

            voices = self._parse_voice_list(stdout.decode())

            # Update cache
            self._cache = voices
            self._cache_timestamp = current_time

            logger.info(f"Detected {len(voices)} voices on macOS")
            return voices

        except Exception as e:
            if isinstance(e, VoiceDetectionError):
                raise
            raise VoiceDetectionError("macOS TTS", str(e))

    def _parse_voice_list(self, voice_output: str) -> List[Voice]:
        """Parse voice list from say command output with enhanced v1.5.0 logic"""
        voices = []
        lines = voice_output.strip().split('\n')

        for line in lines:
            if not line.strip():
                continue

            # Parse voice line format: "Voice_Name    # Description    language"
            parts = line.strip().split(None, 2)
            if len(parts) < 2:
                continue

            voice_id = parts[0]
            description = parts[2] if len(parts) > 2 else ""

            # Extract language and locale information (enhanced from v1.5.0)
            language = Language.UNKNOWN
            locale = None

            # Look for language indicators in description
            desc_lower = description.lower()

            # Spanish detection with enhanced patterns
            if 'spanish' in desc_lower or 'español' in desc_lower:
                language = Language.SPANISH
                # Enhanced locale detection
                if any(pattern in desc_lower for pattern in ['es_es', 'spain', 'españa']):
                    locale = 'es_ES'
                elif any(pattern in desc_lower for pattern in ['es_mx', 'mexico', 'méxico']):
                    locale = 'es_MX'
                elif any(pattern in desc_lower for pattern in ['es_ar', 'argentina']):
                    locale = 'es_AR'
                elif any(pattern in desc_lower for pattern in ['es_cl', 'chile']):
                    locale = 'es_CL'
                elif any(pattern in desc_lower for pattern in ['es_co', 'colombia']):
                    locale = 'es_CO'

            # English detection
            elif 'english' in desc_lower:
                language = Language.ENGLISH
                if any(pattern in desc_lower for pattern in ['en_us', 'united']):
                    locale = 'en_US'

            # Determine voice quality (enhanced from v1.5.0)
            quality = VoiceQuality.BASIC
            if 'enhanced' in desc_lower:
                quality = VoiceQuality.ENHANCED
            elif 'premium' in desc_lower:
                quality = VoiceQuality.PREMIUM
            elif 'neural' in desc_lower or 'neural2' in desc_lower:
                quality = VoiceQuality.NEURAL

            # Determine gender (enhanced from v1.5.0 patterns)
            gender = self._detect_gender_from_name_and_description(voice_id, description)

            # Create voice object
            voice = Voice(
                id=voice_id,
                name=self._format_voice_name(voice_id),
                language=language,
                locale=locale,
                gender=gender,
                quality=quality,
                description=description,
                engine_name="macos",
                supported_formats=["aiff"],
                metadata={
                    "raw_description": description,
                    "detection_timestamp": time.time()
                }
            )

            voices.append(voice)

        return voices

    def _detect_gender_from_name_and_description(self, voice_id: str, description: str) -> Gender:
        """Detect gender from voice name and description using v1.5.0 patterns"""
        voice_id_lower = voice_id.lower()
        desc_lower = description.lower()
        combined_text = f"{voice_id_lower} {desc_lower}"

        # Male patterns from v1.5.0
        male_patterns = [
            'jorge', 'juan', 'diego', 'carlos', 'alberto', 'rey', 'rocko', 'reed', 'grandpa',
            'male', 'man', 'boy', 'hombre', 'masculino'
        ]

        # Female patterns from v1.5.0
        female_patterns = [
            'monica', 'paulina', 'angelica', 'maria', 'sandy', 'flo', 'shelley', 'grandma',
            'marisol', 'isabela', 'soledad', 'francisca', 'jimena', 'mónica', 'angélica',
            'female', 'woman', 'girl', 'lady', 'mujer', 'femenino'
        ]

        # Check for male indicators
        if any(pattern in combined_text for pattern in male_patterns):
            return Gender.MALE

        # Check for female indicators
        if any(pattern in combined_text for pattern in female_patterns):
            return Gender.FEMALE

        return Gender.UNKNOWN

    def _format_voice_name(self, voice_id: str) -> str:
        """Format voice ID to readable name"""
        # Convert underscores to spaces and capitalize
        return voice_id.replace('_', ' ').title()

    def invalidate_cache(self):
        """Invalidate the voice cache"""
        self._cache = None
        self._cache_timestamp = 0


class VoiceManager:
    """Unified voice management system with caching and enhanced search"""

    def __init__(self, cache_ttl: int = 300):
        self._detectors: List[VoiceDetector] = []
        self._voices_cache: Optional[List[Voice]] = None
        self._cache_valid = False
        self._cache_ttl = cache_ttl
        self._cache_timestamp = 0
        self._filter = VoiceFilter()

        # Register default detectors
        self._register_default_detectors()

    def _register_default_detectors(self):
        """Register default voice detectors"""
        # macOS detector
        macos_detector = MacOSVoiceDetector(cache_ttl=self._cache_ttl)
        if macos_detector.is_available():
            self._detectors.append(macos_detector)
            logger.info("Registered macOS voice detector")

    def register_detector(self, detector: VoiceDetector):
        """Register a custom voice detector"""
        self._detectors.append(detector)
        self._invalidate_cache()
        logger.info(f"Registered custom voice detector: {detector.__class__.__name__}")

    def _invalidate_cache(self):
        """Invalidate the voice cache"""
        self._cache_valid = False
        self._voices_cache = None
        self._cache_timestamp = 0

    async def refresh_voices(self, force_refresh: bool = False) -> None:
        """Refresh the voice cache"""
        current_time = time.time()

        # Check if we need to refresh
        if (not force_refresh and
            self._cache_valid and
            self._voices_cache is not None and
            current_time - self._cache_timestamp < self._cache_ttl):
            logger.debug("Using cached voices (refresh not needed)")
            return

        voices = []
        detector_count = 0

        for detector in self._detectors:
            try:
                detector_voices = await detector.detect_voices()
                voices.extend(detector_voices)
                detector_count += 1
                logger.debug(f"Detector {detector.__class__.__name__} found {len(detector_voices)} voices")
            except VoiceDetectionError as e:
                logger.warning(f"Failed to detect voices with {detector.__class__.__name__}: {e}")

        # Remove duplicates (same voice ID) - prioritize first occurrence
        unique_voices = {}
        for voice in voices:
            if voice.id not in unique_voices:
                unique_voices[voice.id] = voice

        self._voices_cache = list(unique_voices.values())
        self._cache_valid = True
        self._cache_timestamp = current_time

        logger.info(f"Voice refresh complete: {len(self._voices_cache)} unique voices from {detector_count} detectors")

    async def get_all_voices(self, force_refresh: bool = False) -> List[Voice]:
        """Get all available voices"""
        if not self._cache_valid or force_refresh or self._voices_cache is None:
            await self.refresh_voices(force_refresh)

        return self._voices_cache.copy() if self._voices_cache else []

    async def search_voices(
        self,
        query: Optional[str] = None,
        language: Optional[Language] = None,
        locale: Optional[str] = None,
        gender: Optional[Gender] = None,
        quality: Optional[VoiceQuality] = None,
        engine_name: Optional[str] = None,
        fuzzy: bool = True
    ) -> List[Voice]:
        """Search voices with multiple filters"""
        voices = await self.get_all_voices()

        # Apply filters
        if language:
            voices = self._filter.filter_by_language(voices, language)

        if locale:
            voices = self._filter.filter_by_locale(voices, locale)

        if gender:
            voices = self._filter.filter_by_gender(voices, gender)

        if quality:
            voices = self._filter.filter_by_quality(voices, quality)

        if engine_name:
            voices = [v for v in voices if v.engine_name == engine_name]

        # Apply query search (enhanced from v1.5.0)
        if query:
            voices = [v for v in voices if v.matches_query(query, fuzzy)]

        return voices

    async def find_voice(
        self,
        voice_id: str,
        fuzzy: bool = True,
        fallback_language: Optional[Language] = Language.SPANISH
    ) -> Voice:
        """Find a specific voice by ID or name with enhanced 3-tier search"""
        voices = await self.get_all_voices()

        # Tier 1: Exact match (case-insensitive)
        for voice in voices:
            if voice.id.lower() == voice_id.lower() or voice.name.lower() == voice_id.lower():
                logger.debug(f"Found exact match for voice '{voice_id}': {voice.id}")
                return voice

        if fuzzy:
            # Tier 2: Prefix match (prioritized)
            normalized_query = self._normalize_text(voice_id.lower())

            for voice in voices:
                normalized_name = self._normalize_text(voice.name.lower())
                normalized_vid = self._normalize_text(voice.id.lower())
                if normalized_name.startswith(normalized_query) or normalized_vid.startswith(normalized_query):
                    logger.debug(f"Found prefix match for voice '{voice_id}': {voice.id}")
                    return voice

            # Tier 3: Partial match
            for voice in voices:
                if normalized_query in self._normalize_text(voice.name.lower()):
                    logger.debug(f"Found partial match for voice '{voice_id}': {voice.id}")
                    return voice

        # Tier 4: Fallback to language
        if fallback_language:
            fallback_voices = await self.search_voices(language=fallback_language)
            if fallback_voices:
                logger.debug(f"Using fallback voice for language '{fallback_language}': {fallback_voices[0].id}")
                return fallback_voices[0]

        # Tier 5: Last resort - first available voice
        if voices:
            logger.warning(f"No match found for '{voice_id}', using first available: {voices[0].id}")
            return voices[0]

        raise VoiceNotFoundError(voice_id, [v.id for v in voices])

    async def get_voice_categories(self) -> Dict[str, List[Voice]]:
        """Get voices categorized by type (enhanced from v1.5.0)"""
        voices = await self.get_all_voices()

        categories = {
            "spanish": [],
            "english": [],
            "other": [],
            "enhanced": [],
            "premium": [],
            "siri": [],
            "neural": [],
            "male": [],
            "female": []
        }

        for voice in voices:
            # Language categories
            if voice.language == Language.SPANISH:
                categories["spanish"].append(voice)
            elif voice.language == Language.ENGLISH:
                categories["english"].append(voice)
            else:
                categories["other"].append(voice)

            # Quality categories
            if voice.quality == VoiceQuality.ENHANCED:
                categories["enhanced"].append(voice)
            elif voice.quality == VoiceQuality.PREMIUM:
                categories["premium"].append(voice)
            elif voice.quality == VoiceQuality.SIRI:
                categories["siri"].append(voice)
            elif voice.quality == VoiceQuality.NEURAL:
                categories["neural"].append(voice)

            # Gender categories
            if voice.gender == Gender.MALE:
                categories["male"].append(voice)
            elif voice.gender == Gender.FEMALE:
                categories["female"].append(voice)

        # Log summary
        logger.info(f"Voice categories: { {k: len(v) for k, v in categories.items()} }")

        return categories

    def get_available_engines(self) -> List[str]:
        """Get list of available TTS engines"""
        engines = set()
        for detector in self._detectors:
            if hasattr(detector, 'engine_name'):
                engines.add(detector.engine_name)
            else:
                engines.append(detector.__class__.__name__.replace('VoiceDetector', '').lower())
        return sorted(list(engines))

    async def validate_voice(self, voice_id: str) -> bool:
        """Validate that a voice exists and is usable"""
        try:
            await self.find_voice(voice_id, fuzzy=False)
            return True
        except VoiceNotFoundError:
            return False

    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache information"""
        return {
            "cache_valid": self._cache_valid,
            "cache_timestamp": self._cache_timestamp,
            "cache_age_seconds": time.time() - self._cache_timestamp if self._cache_timestamp else 0,
            "cached_voices_count": len(self._voices_cache) if self._voices_cache else 0,
            "cache_ttl": self._cache_ttl
        }

    def invalidate_cache(self):
        """Invalidate the voice cache"""
        self._invalidate_cache()
        logger.info("Voice cache invalidated")

    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison (remove accents, etc.)"""
        # Normalize to NFD (separate base characters from accents)
        nfd = unicodedata.normalize("NFD", text)
        # Remove non-spacing marks (accents)
        without_accents = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
        return without_accents.lower()

    async def get_voice_statistics(self) -> Dict[str, Any]:
        """Get detailed voice statistics"""
        voices = await self.get_all_voices()
        categories = await self.get_voice_categories()

        stats = {
            "total_voices": len(voices),
            "by_language": {},
            "by_quality": {},
            "by_gender": {},
            "engines": self.get_available_engines(),
            "cache_info": self.get_cache_info()
        }

        # Language statistics
        languages = {}
        for voice in voices:
            lang = voice.language.value
            languages[lang] = languages.get(lang, 0) + 1
        stats["by_language"] = languages

        # Quality statistics
        qualities = {}
        for voice in voices:
            quality = voice.quality.value
            qualities[quality] = qualities.get(quality, 0) + 1
        stats["by_quality"] = qualities

        # Gender statistics
        genders = {}
        for voice in voices:
            gender = voice.gender.value
            genders[gender] = genders.get(gender, 0) + 1
        stats["by_gender"] = genders

        return stats