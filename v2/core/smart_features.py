"""
Smart Features - Advanced AI-powered features for TTS-MacOS v2

Implements intelligent voice selection, content analysis, and optimization:
- Voice recommendation based on content analysis
- Automatic language detection
- Voice quality assessment and optimization
- Content-aware voice selection
- Performance optimization and caching

Features:
- AI-powered voice matching
- Content sentiment analysis
- Voice quality scoring
- Automatic parameter optimization
- Smart caching strategies
"""

import json
import logging
import re
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

# Text analysis libraries
try:
    from langdetect import DetectorFactory, detect
    from textblob import TextBlob

    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False
    print(
        "Warning: NLP libraries not available. Install with: pip install langdetect textblob"
    )

from ..core.config import Quality, TTSConfig


class VoiceRecommender:
    """
    AI-powered voice recommendation system
    """

    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self.logger = logging.getLogger(__name__)

        # Voice compatibility matrix
        self.voice_compatibility = self._build_voice_compatibility_matrix()

        # Content type patterns
        self.content_patterns = self._build_content_patterns()

        # Voice quality scores (cached)
        self.quality_cache = {}

        # Usage statistics
        self.usage_stats = defaultdict(int)

    def recommend_voice(
        self,
        text: str,
        language: str = "en",
        voice_type: str = "balanced",
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Recommend the best voice for given content

        Args:
            text: Text content to analyze
            language: Target language
            voice_type: Preferred voice type (natural/expressive/professional)
            context: Additional context (e.g., "audiobook", "news", "conversation")

        Returns:
            Voice recommendation with confidence score
        """
        try:
            # Analyze content
            content_analysis = self._analyze_content(text, language)

            # Score available voices
            voice_scores = self._score_voices(
                content_analysis, language, voice_type, context
            )

            # Get top recommendation
            if voice_scores:
                best_voice = voice_scores[0]

                recommendation = {
                    "voice": best_voice["name"],
                    "engine": best_voice["engine"],
                    "confidence": best_voice["score"],
                    "reasoning": best_voice["reasoning"],
                    "alternatives": voice_scores[1:4],  # Top 3 alternatives
                    "content_analysis": content_analysis,
                }

                # Log recommendation for learning
                self._log_recommendation(text, best_voice)

                return recommendation
            else:
                # Fallback recommendation
                return self._get_fallback_recommendation(language)

        except Exception as e:
            self.logger.error(f"Voice recommendation failed: {e}")
            return self._get_fallback_recommendation(language)

    def _analyze_content(self, text: str, language: str) -> Dict[str, Any]:
        """Analyze text content for voice selection"""
        analysis = {
            "length": len(text),
            "word_count": len(text.split()),
            "language": language,
            "detected_language": language,
            "sentiment": "neutral",
            "formality": "medium",
            "content_type": "general",
            "emotional_tone": "neutral",
            "complexity": "medium",
        }

        # Language detection (if NLP available)
        if NLP_AVAILABLE:
            try:
                detected = detect(text)
                analysis["detected_language"] = detected

                # Sentiment analysis
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity

                if polarity > 0.3:
                    analysis["sentiment"] = "positive"
                elif polarity < -0.3:
                    analysis["sentiment"] = "negative"
                else:
                    analysis["sentiment"] = "neutral"

            except:
                pass  # Fall back to defaults

        # Content type detection
        content_type = self._detect_content_type(text)
        analysis["content_type"] = content_type

        # Formality detection
        formal_indicators = [
            "therefore",
            "furthermore",
            "however",
            "consequently",
            "moreover",
        ]
        informal_indicators = ["hey", "yeah", "cool", "awesome", "gonna", "wanna"]

        formal_count = sum(
            1 for word in formal_indicators if word.lower() in text.lower()
        )
        informal_count = sum(
            1 for word in informal_indicators if word.lower() in text.lower()
        )

        if formal_count > informal_count:
            analysis["formality"] = "formal"
        elif informal_count > formal_count:
            analysis["formality"] = "informal"
        else:
            analysis["formality"] = "medium"

        # Complexity analysis
        avg_word_length = sum(len(word) for word in text.split()) / len(text.split())
        if avg_word_length > 6:
            analysis["complexity"] = "high"
        elif avg_word_length < 4:
            analysis["complexity"] = "low"

        return analysis

    def _detect_content_type(self, text: str) -> str:
        """Detect the type of content"""
        text_lower = text.lower()

        # Check for various content types
        if any(
            word in text_lower
            for word in ["chapter", "once upon a time", "the end", "character"]
        ):
            return "narrative"

        if any(
            word in text_lower
            for word in ["breaking", "according to", "reported", "announced"]
        ):
            return "news"

        if any(
            word in text_lower
            for word in ["recipe", "ingredients", "instructions", "preheat"]
        ):
            return "instructional"

        if any(
            word in text_lower
            for word in ["research", "study", "analysis", "according to research"]
        ):
            return "educational"

        if any(
            word in text_lower
            for word in ["buy now", "limited time", "special offer", "discount"]
        ):
            return "commercial"

        if any(
            word in text_lower
            for word in ["question", "how", "what", "why", "when", "where"]
        ):
            return "conversational"

        # Check for emotional content
        emotional_words = [
            "love",
            "hate",
            "happy",
            "sad",
            "angry",
            "excited",
            "worried",
            "beautiful",
        ]
        emotional_count = sum(1 for word in emotional_words if word in text_lower)

        if emotional_count > 2:
            return "emotional"

        return "general"

    def _score_voices(
        self,
        content_analysis: Dict[str, Any],
        language: str,
        voice_type: str,
        context: Optional[str],
    ) -> List[Dict[str, Any]]:
        """Score available voices based on content analysis"""
        scores = []

        # Get available voices from both engines
        from ..engines import EngineSelector

        engine_selector = EngineSelector()

        all_voices = engine_selector.list_all_voices()

        # Score native voices
        if "native" in all_voices:
            scores.extend(
                self._score_native_voices(
                    all_voices["native"], content_analysis, language, voice_type
                )
            )

        # Score AI voices
        if "ai" in all_voices:
            scores.extend(
                self._score_ai_voices(
                    all_voices["ai"], content_analysis, language, voice_type
                )
            )

        # Sort by score (descending)
        scores.sort(key=lambda x: x["score"], reverse=True)

        return scores

    def _score_native_voices(
        self,
        native_voices: Dict[str, Any],
        content_analysis: Dict[str, Any],
        language: str,
        voice_type: str,
    ) -> List[Dict[str, Any]]:
        """Score native voices"""
        scores = []

        for category, voices in native_voices.items():
            if isinstance(voices, list):
                for voice in voices:
                    score = self._calculate_voice_score(
                        voice, content_analysis, language, voice_type, "native"
                    )

                    if score > 0:
                        scores.append(
                            {
                                "name": voice["name"],
                                "engine": "native",
                                "score": score,
                                "reasoning": self._generate_reasoning(
                                    voice, content_analysis, score
                                ),
                                "category": category,
                            }
                        )

        return scores

    def _score_ai_voices(
        self,
        ai_voices: Dict[str, Any],
        content_analysis: Dict[str, Any],
        language: str,
        voice_type: str,
    ) -> List[Dict[str, Any]]:
        """Score AI voices"""
        scores = []

        # AI voices are more flexible - high base score for multilingual content
        base_score = 0.7

        # Boost for complex or emotional content
        if content_analysis.get("content_type") in ["narrative", "emotional"]:
            base_score += 0.2

        # Boost for non-English content
        if content_analysis.get("language") != "en":
            base_score += 0.2

        # Create AI voice entries
        ai_voice = {
            "name": "AI-TTS",
            "engine": "ai",
            "score": min(base_score, 1.0),
            "reasoning": f"AI TTS recommended for {content_analysis.get('content_type', 'general')} content",
        }

        scores.append(ai_voice)

        return scores

    def _calculate_voice_score(
        self,
        voice: Dict[str, Any],
        content_analysis: Dict[str, Any],
        language: str,
        voice_type: str,
        engine_type: str,
    ) -> float:
        """Calculate score for a specific voice"""
        score = 0.0

        # Language matching
        voice_language = voice.get("language", "").lower()
        if language in voice_language or voice_language in language:
            score += 0.4
        elif voice_language == "unknown":
            score += 0.1

        # Content type matching
        content_type = content_analysis.get("content_type", "general")
        if content_type == "narrative":
            if voice.get("type") in ["Premium", "Enhanced"]:
                score += 0.3
        elif content_type == "news":
            if voice.get("type") in ["Enhanced", "Standard"]:
                score += 0.2
        elif content_type == "conversational":
            if voice.get("gender") in ["Male", "Female"]:  # More natural voices
                score += 0.2

        # Voice type preference
        if voice_type == "expressive" and voice.get("type") == "Premium":
            score += 0.3
        elif voice_type == "professional" and voice.get("type") in [
            "Enhanced",
            "Premium",
        ]:
            score += 0.2
        elif voice_type == "natural" and voice.get("type") in ["Standard", "Enhanced"]:
            score += 0.1

        # Length consideration
        text_length = content_analysis.get("length", 0)
        if text_length > 1000:  # Long content
            if voice.get("type") in [
                "Premium",
                "Enhanced",
            ]:  # Better voices for long content
                score += 0.2

        # Sentiment matching
        sentiment = content_analysis.get("sentiment", "neutral")
        if sentiment != "neutral" and voice.get("type") == "Premium":
            score += 0.1  # Premium voices handle emotions better

        # Historical performance
        voice_name = voice.get("name", "")
        if voice_name in self.usage_stats:
            # Boost frequently used successful voices
            usage_boost = min(self.usage_stats[voice_name] / 100, 0.2)
            score += usage_boost

        return min(score, 1.0)

    def _generate_reasoning(
        self, voice: Dict[str, Any], content_analysis: Dict[str, Any], score: float
    ) -> str:
        """Generate reasoning for voice recommendation"""
        reasons = []

        # Language matching
        voice_language = voice.get("language", "")
        if voice_language and voice_language != "unknown":
            reasons.append(f"Language match ({voice_language})")

        # Voice quality
        voice_type = voice.get("type", "Standard")
        if voice_type in ["Premium", "Enhanced"]:
            reasons.append(f"High quality ({voice_type})")

        # Content type
        content_type = content_analysis.get("content_type", "general")
        if content_type != "general":
            reasons.append(f"Suitable for {content_type}")

        # Length consideration
        if content_analysis.get("length", 0) > 1000:
            reasons.append("Good for long content")

        return ", ".join(reasons) if reasons else "General purpose voice"

    def _get_fallback_recommendation(self, language: str) -> Dict[str, Any]:
        """Get fallback recommendation when scoring fails"""
        fallback_voices = {
            "es": {"name": "monica", "engine": "native", "confidence": 0.5},
            "en": {"name": "samantha", "engine": "native", "confidence": 0.5},
            "default": {"name": "AI-TTS", "engine": "ai", "confidence": 0.4},
        }

        voice = fallback_voices.get(language, fallback_voices["default"])

        return {
            "voice": voice["name"],
            "engine": voice["engine"],
            "confidence": voice["confidence"],
            "reasoning": "Fallback recommendation",
            "alternatives": [],
            "content_analysis": {"language": language},
        }

    def _log_recommendation(self, text: str, voice: Dict[str, Any]):
        """Log recommendation for learning and improvement"""
        voice_name = voice["name"]
        self.usage_stats[voice_name] += 1

    def _build_voice_compatibility_matrix(self) -> Dict[str, Dict[str, float]]:
        """Build voice compatibility matrix for different content types"""
        return {
            "narrative": {"premium": 0.9, "enhanced": 0.7, "standard": 0.5},
            "news": {"premium": 0.8, "enhanced": 0.9, "standard": 0.7},
            "conversational": {"premium": 0.7, "enhanced": 0.8, "standard": 0.9},
            "educational": {"premium": 0.8, "enhanced": 0.9, "standard": 0.6},
        }

    def _build_content_patterns(self) -> Dict[str, List[str]]:
        """Build regex patterns for content type detection"""
        return {
            "narrative": [
                r"chapter\s+\d+",
                r"once\s+upon\s+a\s+time",
                r"the\s+end",
                r"\w+\s+said",
            ],
            "news": [
                r"breaking\s+news",
                r"according\s+to",
                r"reported\s+that",
                r"announced\s+today",
            ],
            "instructional": [
                r"step\s+\d+",
                r"first,.*second,.*third",
                r"to\s+\w+,\s+you\s+should",
            ],
        }


class AutoLanguageDetector:
    """
    Automatic language detection with confidence scoring
    """

    def __init__(self):
        self.confidence_threshold = 0.8

        # Language mapping for TTS engines
        self.language_mapping = {
            "en": "en",
            "es": "es",
            "fr": "fr",
            "de": "de",
            "it": "it",
            "pt": "pt",
            "nl": "nl",
            "pl": "pl",
            "tr": "tr",
            "ru": "ru",
            "cs": "cs",
            "ar": "ar",
            "zh": "zh-cn",
            "ja": "ja",
            "hu": "hu",
            "ko": "ko",
        }

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language with confidence scoring

        Args:
            text: Text to analyze

        Returns:
            Detection result with language code and confidence
        """
        if not NLP_AVAILABLE:
            return self._fallback_detection(text)

        try:
            # Set seed for consistent results
            DetectorFactory.seed = 0

            # Detect language
            detected = detect(text)

            # Map to TTS language code
            tts_language = self.language_mapping.get(detected, detected)

            # Calculate confidence (simplified)
            confidence = self._calculate_confidence(text, detected)

            return {
                "detected_language": detected,
                "tts_language": tts_language,
                "confidence": confidence,
                "text_length": len(text),
                "word_count": len(text.split()),
                "method": "langdetect",
            }

        except Exception as e:
            return self._fallback_detection(text)

    def _calculate_confidence(self, text: str, language: str) -> float:
        """Calculate confidence score for language detection"""
        # Simple heuristic based on text length and language-specific patterns
        base_confidence = min(len(text) / 1000, 1.0) * 0.8

        # Boost confidence for longer texts
        if len(text) > 500:
            base_confidence += 0.1

        # Check for language-specific indicators
        language_indicators = {
            "es": ["el", "la", "los", "las", "que", "de", "en", "y", "con"],
            "fr": ["le", "la", "les", "que", "de", "et", "en", "avec"],
            "de": ["der", "die", "das", "dem", "den", "des", "und", "mit"],
            "it": ["il", "la", "lo", "le", "che", "di", "e", "con"],
        }

        if language in language_indicators:
            indicators = language_indicators[language]
            text_lower = text.lower()
            indicator_count = sum(
                1 for word in indicators if word in text_lower.split()
            )

            if indicator_count > 2:
                base_confidence += 0.1

        return min(base_confidence, 1.0)

    def _fallback_detection(self, text: str) -> Dict[str, Any]:
        """Fallback language detection using simple heuristics"""
        # Check for common language indicators
        text_lower = text.lower()

        language_scores = {"es": 0, "fr": 0, "de": 0, "it": 0, "pt": 0, "en": 0}

        # Spanish indicators
        spanish_words = [
            "el",
            "la",
            "que",
            "de",
            "en",
            "y",
            "con",
            "por",
            "para",
            "como",
            "más",
        ]
        language_scores["es"] = sum(1 for word in spanish_words if word in text_lower)

        # French indicators
        french_words = [
            "le",
            "la",
            "que",
            "de",
            "et",
            "en",
            "avec",
            "pour",
            "comme",
            "plus",
        ]
        language_scores["fr"] = sum(1 for word in french_words if word in text_lower)

        # German indicators
        german_words = [
            "der",
            "die",
            "das",
            "dem",
            "den",
            "des",
            "und",
            "mit",
            "für",
            "wie",
        ]
        language_scores["de"] = sum(1 for word in german_words if word in text_lower)

        # English indicators
        english_words = [
            "the",
            "and",
            "that",
            "for",
            "with",
            "from",
            "they",
            "have",
            "what",
        ]
        language_scores["en"] = sum(1 for word in english_words if word in text_lower)

        # Find best match
        best_language = max(language_scores, key=language_scores.get)
        max_score = language_scores[best_language]

        confidence = min(max_score / 10, 0.6)  # Lower confidence for fallback

        return {
            "detected_language": best_language,
            "tts_language": self.language_mapping.get(best_language, best_language),
            "confidence": confidence,
            "text_length": len(text),
            "word_count": len(text.split()),
            "method": "heuristic",
        }


class PerformanceOptimizer:
    """
    Performance optimization and smart caching
    """

    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self.cache_stats = {"hits": 0, "misses": 0, "total_requests": 0}

        # Performance benchmarks
        self.performance_benchmarks = {}

    def optimize_parameters(
        self, text: str, engine_type: str, quality_preference: Quality
    ) -> Dict[str, Any]:
        """
        Optimize TTS parameters based on content and requirements

        Args:
            text: Text to synthesize
            engine_type: Type of engine being used
            quality_preference: User's quality preference

        Returns:
            Optimized parameters
        """
        text_length = len(text)
        word_count = len(text.split())

        # Base parameters
        params = {
            "rate": 1.0,
            "volume": 1.0,
            "pitch_adjustment": 1.0,
            "model_name": None,
            "cache_enabled": True,
        }

        # Optimize based on text length
        if text_length > 5000:  # Very long text
            if quality_preference == Quality.FAST:
                params["rate"] = 1.2  # Slightly faster for long content
            params["cache_enabled"] = True  # Enable caching for long content

        elif text_length < 100:  # Short text
            if quality_preference == Quality.PREMIUM:
                params["pitch_adjustment"] = 1.1  # Slightly higher pitch for clarity

        # Engine-specific optimizations
        if engine_type == "ai":
            # AI engine optimizations
            if quality_preference == Quality.FAST:
                params["model_name"] = "glow_tts"  # Faster model
            elif quality_preference == Quality.PREMIUM:
                params["model_name"] = "xtts_v2"  # Highest quality
            else:
                params["model_name"] = "xtts_v2"  # Balanced default

        elif engine_type == "native":
            # Native engine optimizations
            if text_length > 2000:
                params["rate"] = 1.1  # Slightly faster for very long content

        return params

    def get_performance_recommendation(
        self, text_length: int, engine_type: str, quality_preference: Quality
    ) -> Dict[str, Any]:
        """Get performance recommendations"""
        recommendations = []

        # Text length considerations
        if text_length > 10000:
            recommendations.append(
                {
                    "type": "warning",
                    "message": "Very long text detected. Consider breaking into smaller segments.",
                    "priority": "medium",
                }
            )

        # Engine-specific recommendations
        if engine_type == "ai" and quality_preference == Quality.PREMIUM:
            recommendations.append(
                {
                    "type": "info",
                    "message": "AI Premium quality selected. Synthesis may take 10-30 seconds per minute of audio.",
                    "priority": "low",
                }
            )

        # Cache recommendations
        if self.cache_stats["total_requests"] > 10:
            hit_rate = self.cache_stats["hits"] / self.cache_stats["total_requests"]
            if hit_rate < 0.3:
                recommendations.append(
                    {
                        "type": "suggestion",
                        "message": f"Low cache hit rate ({hit_rate:.1%}). Consider reusing similar content.",
                        "priority": "low",
                    }
                )

        return {
            "recommendations": recommendations,
            "estimated_time": self._estimate_synthesis_time(
                text_length, engine_type, quality_preference
            ),
            "cache_hit_rate": self.cache_stats["hits"]
            / max(self.cache_stats["total_requests"], 1),
        }

    def _estimate_synthesis_time(
        self, text_length: int, engine_type: str, quality_preference: Quality
    ) -> float:
        """Estimate synthesis time in seconds"""
        # Base rates (seconds per character)
        base_rates = {"native": 0.01, "ai": 0.05}

        # Quality multipliers
        quality_multipliers = {
            Quality.FAST: 0.7,
            Quality.BALANCED: 1.0,
            Quality.PREMIUM: 1.5,
        }

        base_rate = base_rates.get(engine_type, 0.03)
        quality_multiplier = quality_multipliers.get(quality_preference, 1.0)

        estimated_time = text_length * base_rate * quality_multiplier

        return max(estimated_time, 0.5)  # Minimum 0.5 seconds

    def update_cache_stats(self, hit: bool):
        """Update cache statistics"""
        self.cache_stats["total_requests"] += 1
        if hit:
            self.cache_stats["hits"] += 1
        else:
            self.cache_stats["misses"] += 1

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total = self.cache_stats["total_requests"]
        hit_rate = self.cache_stats["hits"] / max(total, 1)

        return {
            "hits": self.cache_stats["hits"],
            "misses": self.cache_stats["misses"],
            "total_requests": total,
            "hit_rate": hit_rate,
            "miss_rate": 1 - hit_rate,
        }
