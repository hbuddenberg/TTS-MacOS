"""
Text normalization utilities for TTS Notify v2

This module provides text normalization functions for better voice recognition
and text processing.
"""

import unicodedata
import re
from typing import Optional


class TextNormalizer:
    """Text normalization utility with enhanced support for multiple languages"""

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text by removing accents and converting to lowercase.

        Args:
            text: Text to normalize

        Returns:
            Normalized text
        """
        if not text:
            return ""

        # Normalize to NFD (separate base characters from accents)
        nfd = unicodedata.normalize("NFD", text)

        # Remove non-spacing marks (accents)
        without_accents = "".join(c for c in nfd if unicodedata.category(c) != "Mn")

        # Convert to lowercase
        return without_accents.lower()

    @staticmethod
    def remove_code_blocks(text: str) -> str:
        """
        Remove code blocks from text for TTS processing.

        Args:
            text: Text to process

        Returns:
            Text with code blocks removed
        """
        # Remove inline code
        text = re.sub(r'`[^`]+`', '', text)

        # Remove code blocks
        text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Remove markdown formatting
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic*
        text = re.sub(r'__([^_]+)__', r'\1', text)        # __bold__
        text = re.sub(r'_([^_]+)_', r'\1', text)          # _italic_

        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    @staticmethod
    def truncate_text(text: str, max_length: int, ellipsis: str = "...") -> str:
        """
        Truncate text to maximum length with ellipsis.

        Args:
            text: Text to truncate
            max_length: Maximum length
            ellipsis: Ellipsis string to add

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text

        return text[:max_length - len(ellipsis)] + ellipsis

    @staticmethod
    def clean_for_tts(text: str, max_length: Optional[int] = None) -> str:
        """
        Clean text for TTS processing by removing code blocks and normalizing.

        Args:
            text: Text to clean
            max_length: Optional maximum length

        Returns:
            Cleaned text ready for TTS
        """
        # Remove code blocks and formatting
        cleaned = TextNormalizer.remove_code_blocks(text)

        # Normalize text
        cleaned = TextNormalizer.normalize_text(cleaned)

        # Truncate if needed
        if max_length:
            cleaned = TextNormalizer.truncate_text(cleaned, max_length)

        return cleaned

    @staticmethod
    def extract_text_from_markdown(text: str) -> str:
        """
        Extract readable text from markdown content.

        Args:
            text: Markdown text

        Returns:
            Plain text content
        """
        # Remove headers
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)

        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

        # Remove images
        text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)

        # Remove lists but keep content
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)

        # Remove blockquotes
        text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)

        # Clean up the result
        return TextNormalizer.clean_for_tts(text)

    @staticmethod
    def sanitize_filename(text: str) -> str:
        """
        Sanitize text for use as a filename.

        Args:
            text: Text to sanitize

        Returns:
            Sanitized filename
        """
        # Remove or replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '', text)
        sanitized = re.sub(r'\s+', '_', sanitized)
        sanitized = sanitized.strip('._')

        # Ensure it's not empty
        if not sanitized:
            sanitized = "untitled"

        return sanitized

    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Format duration in seconds to human-readable string.

        Args:
            seconds: Duration in seconds

        Returns:
            Formatted duration string
        """
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds:.1f}s"
        else:
            hours = int(seconds // 3600)
            remaining_minutes = int((seconds % 3600) // 60)
            return f"{hours}h {remaining_minutes}m"