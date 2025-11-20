#!/usr/bin/env python3
"""
MCP server entry point for TTS Notify v2

This module provides the entry point when using:
python -m ui.mcp
"""

from .server import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())