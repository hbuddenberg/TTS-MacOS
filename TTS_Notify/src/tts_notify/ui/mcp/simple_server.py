#!/usr/bin/env python3
"""
TTS Notify v2.0.0 - Simple MCP Server

Simple MCP server implementation that uses macOS say command directly.
This bypasses complex import issues and provides reliable TTS functionality.
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from mcp.server.fastmcp import FastMCP
    from mcp.types import TextContent
except ImportError as e:
    logger.error(f"MCP library not available: {e}")
    logger.error("Please install with: pip install mcp>=1.0.0")
    sys.exit(1)

# Create FastMCP server instance
app = FastMCP("tts-notify")


@app.tool()
async def speak_text(text: str, voice: Optional[str] = None, rate: Optional[int] = None) -> str:
    """
    Speak text using macOS TTS.

    Args:
        text: The text to speak
        voice: The voice to use (optional, defaults to system default)
        rate: The speech rate in words per minute (optional, 100-300)

    Returns:
        Success message with voice used
    """
    try:
        logger.info(f"Speaking text: {text[:50]}...")

        # Build say command
        cmd = ['say']

        if voice:
            cmd.extend(['-v', voice])

        if rate:
            cmd.extend(['-r', str(rate)])

        cmd.append(text)

        # Execute TTS
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            voice_used = voice or "system default"
            logger.info(f"Text spoken successfully with voice: {voice_used}")
            return f"✅ Text spoken successfully with voice: {voice_used}"
        else:
            error_msg = stderr.decode() if stderr else 'Unknown error'
            logger.error(f"Error speaking text: {error_msg}")
            return f"❌ Error speaking text: {error_msg}"

    except Exception as e:
        logger.error(f"Exception in speak_text: {e}")
        return f"❌ Exception: {str(e)}"


@app.tool()
async def list_voices() -> str:
    """
    List all available TTS voices on the system.

    Returns:
        JSON string with available voices
    """
    try:
        logger.info("Listing system voices...")

        process = await asyncio.create_subprocess_exec(
            'say', '-v', '?',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            voices_output = stdout.decode()

            # Parse voices and format as JSON
            voices = []
            for line in voices_output.split('\n'):
                if line.strip():
                    voices.append(line.strip())

            logger.info(f"Found {len(voices)} voices")

            result = {
                "total_voices": len(voices),
                "voices": voices
            }

            return json.dumps(result, indent=2)
        else:
            error_msg = stderr.decode() if stderr else 'Unknown error'
            logger.error(f"Error listing voices: {error_msg}")
            return f"❌ Error listing voices: {error_msg}"

    except Exception as e:
        logger.error(f"Exception in list_voices: {e}")
        return f"❌ Exception: {str(e)}"


@app.tool()
async def save_audio(text: str, output_path: str, voice: Optional[str] = None, rate: Optional[int] = None) -> str:
    """
    Save text as audio file.

    Args:
        text: The text to convert to audio
        output_path: The path where to save the audio file
        voice: The voice to use (optional)
        rate: The speech rate (optional)

    Returns:
        Success message with file path
    """
    try:
        logger.info(f"Saving audio to: {output_path}")

        # Build say command for output
        cmd = ['say']

        if voice:
            cmd.extend(['-v', voice])

        if rate:
            cmd.extend(['-r', str(rate)])

        cmd.extend(['-o', output_path, text])

        # Execute
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            logger.info(f"Audio saved successfully to: {output_path}")
            return f"✅ Audio saved successfully to: {output_path}"
        else:
            error_msg = stderr.decode() if stderr else 'Unknown error'
            logger.error(f"Error saving audio: {error_msg}")
            return f"❌ Error saving audio: {error_msg}"

    except Exception as e:
        logger.error(f"Exception in save_audio: {e}")
        return f"❌ Exception: {str(e)}"


async def main():
    """Main entry point for the MCP server"""
    logger.info("🤖 TTS Notify MCP Server v2.0.0 starting...")
    logger.info("📍 Using macOS native TTS (say command)")
    logger.info("🔧 Ready to serve Claude Desktop requests")

    # Use FastMCP's built-in server which handles all the transport
    await app.run()


def sync_main():
    """Synchronous main entry point for subprocess calls"""
    try:
        # Check if we're already in an async context
        try:
            loop = asyncio.get_running_loop()
            # If we get here, there's already a running loop
            logger.info("Detected running asyncio loop, creating new task")
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(lambda: asyncio.run(main()))
                future.result()
        except RuntimeError:
            # No running loop, safe to use asyncio.run()
            asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("MCP Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    sync_main()