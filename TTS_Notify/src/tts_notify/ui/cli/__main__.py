#!/usr/bin/env python3
"""
CLI entry point for TTS Notify v2

This module provides the command-line entry point when using:
python -m ui.cli
"""

from .main import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())