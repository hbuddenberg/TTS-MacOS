"""
Legacy Module - Preserves TTS-MacOS v1.4.4 functionality

This module contains the complete v1.4.4 implementation preserved for:
- Backward compatibility
- Migration assistance
- Fallback functionality
- Reference for existing behavior

All v1.x features are maintained unchanged:
- macOS say command integration
- Dynamic voice detection and categorization
- Flexible voice search with accent normalization
- MCP server with FastMCP framework
- CLI tool with comprehensive options
- Hooks integration for Claude Code
"""

from .cli import LegacyCLI
from .server import LegacyMCPServer
from .voice_detector import LegacyVoiceDetector

__all__ = ["LegacyMCPServer", "LegacyCLI", "LegacyVoiceDetector"]

# Version information for legacy compatibility
LEGACY_VERSION = "1.4.4"
LEGACY_STATUS = "preserved"
