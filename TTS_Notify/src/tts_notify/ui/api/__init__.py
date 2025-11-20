"""
REST API interface for TTS Notify v2

FastAPI-based REST API for text-to-speech functionality.
"""

from .server import TTSNotifyAPIServer, main, api_server

__all__ = ["TTSNotifyAPIServer", "main", "api_server"]