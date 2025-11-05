"""
TTS macOS - Text-to-Speech para macOS usando TTS nativo

CLI tool y servidor MCP para convertir texto a voz.
"""

__version__ = "1.4.3"
__author__ = "TTS macOS Project"
__license__ = "MIT"

from .cli import main, hablar, guardar, listar_voces, VOCES

__all__ = ["main", "hablar", "guardar", "listar_voces", "VOCES"]
