"""
MCP server interface for TTS Notify v2

Model Context Protocol server integration for Claude Desktop.
"""

from .server import TTSNotifyMCPServer, main

__all__ = ["TTSNotifyMCPServer", "main"]