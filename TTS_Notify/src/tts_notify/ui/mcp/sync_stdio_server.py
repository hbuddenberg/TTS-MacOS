#!/usr/bin/env python3
"""
TTS Notify v2.0.0 - Sync Stdio MCP Server

Synchronous MCP server implementation that works with stdio communication.
This server handles the MCP protocol correctly for Claude Desktop.
"""

import json
import logging
import subprocess
import sys
import threading
import time
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SyncTTSNotifyMCPServer:
    """Synchronous MCP server implementation"""

    def __init__(self):
        self.initialized = False
        self.tools = {
            "speak_text": {
                "name": "speak_text",
                "description": "Speak text using macOS TTS with optional voice and rate",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to speak"},
                        "voice": {"type": "string", "description": "Voice name (optional)"},
                        "rate": {"type": "integer", "description": "Speech rate 100-300 WPM (optional)"}
                    },
                    "required": ["text"]
                }
            },
            "list_voices": {
                "name": "list_voices",
                "description": "List all available TTS voices on the system",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            "save_audio": {
                "name": "save_audio",
                "description": "Save text as audio file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to convert"},
                        "output_path": {"type": "string", "description": "Output file path"},
                        "voice": {"type": "string", "description": "Voice name (optional)"},
                        "rate": {"type": "integer", "description": "Speech rate (optional)"}
                    },
                    "required": ["text", "output_path"]
                }
            }
        }

    def speak_text(self, text: str, voice: Optional[str] = None, rate: Optional[int] = None) -> str:
        """Speak text using macOS TTS"""
        try:
            logger.info(f"Speaking text: {text[:50]}...")

            cmd = ['say']

            if voice:
                cmd.extend(['-v', voice])

            if rate:
                cmd.extend(['-r', str(rate)])

            cmd.append(text)

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                voice_used = voice or "system default"
                logger.info(f"Text spoken successfully with voice: {voice_used}")
                return f"✅ Text spoken successfully with voice: {voice_used}"
            else:
                error_msg = result.stderr if result.stderr else 'Unknown error'
                logger.error(f"Error speaking text: {error_msg}")
                return f"❌ Error speaking text: {error_msg}"

        except Exception as e:
            logger.error(f"Exception in speak_text: {e}")
            return f"❌ Exception: {str(e)}"

    def list_voices(self) -> str:
        """List all available TTS voices"""
        try:
            logger.info("Listing system voices...")

            result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)

            if result.returncode == 0:
                voices_output = result.stdout

                voices = []
                for line in voices_output.split('\n'):
                    if line.strip():
                        voices.append(line.strip())

                logger.info(f"Found {len(voices)} voices")

                result_data = {
                    "total_voices": len(voices),
                    "voices": voices
                }

                return json.dumps(result_data, indent=2)
            else:
                error_msg = result.stderr if result.stderr else 'Unknown error'
                logger.error(f"Error listing voices: {error_msg}")
                return f"❌ Error listing voices: {error_msg}"

        except Exception as e:
            logger.error(f"Exception in list_voices: {e}")
            return f"❌ Exception: {str(e)}"

    def save_audio(self, text: str, output_path: str, voice: Optional[str] = None, rate: Optional[int] = None) -> str:
        """Save text as audio file"""
        try:
            logger.info(f"Saving audio to: {output_path}")

            cmd = ['say']

            if voice:
                cmd.extend(['-v', voice])

            if rate:
                cmd.extend(['-r', str(rate)])

            cmd.extend(['-o', output_path, text])

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"Audio saved successfully to: {output_path}")
                return f"✅ Audio saved successfully to: {output_path}"
            else:
                error_msg = result.stderr if result.stderr else 'Unknown error'
                logger.error(f"Error saving audio: {error_msg}")
                return f"❌ Error saving audio: {error_msg}"

        except Exception as e:
            logger.error(f"Exception in save_audio: {e}")
            return f"❌ Exception: {str(e)}"

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP JSON-RPC request"""

        if "method" not in request:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32600, "message": "Invalid Request"},
                "id": request.get("id")
            }

        method = request["method"]
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "initialize":
                self.initialized = True
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "TTS Notify",
                            "version": "2.0.0"
                        }
                    },
                    "id": request_id
                }

            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "tools": list(self.tools.values())
                    },
                    "id": request_id
                }

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})

                if tool_name not in self.tools:
                    return {
                        "jsonrpc": "2.0",
                        "error": {"code": -32601, "message": f"Tool not found: {tool_name}"},
                        "id": request_id
                    }

                if tool_name == "speak_text":
                    result = self.speak_text(**arguments)
                elif tool_name == "list_voices":
                    result = self.list_voices()
                elif tool_name == "save_audio":
                    result = self.save_audio(**arguments)
                else:
                    result = f"Unknown tool: {tool_name}"

                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": result
                        }]
                    },
                    "id": request_id
                }

            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32601, "message": f"Method not found: {method}"},
                    "id": request_id
                }

        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                "id": request_id
            }

    def run_stdio_sync(self):
        """Run MCP server with stdio communication (synchronous)"""
        logger.info("🤖 TTS Notify MCP Server v2.0.0 starting...")
        logger.info("📍 Using stdio communication")
        logger.info("🔧 Ready for Claude Desktop connections")

        try:
            while True:
                # Read line from stdin
                try:
                    line = sys.stdin.readline()
                except KeyboardInterrupt:
                    break

                if not line:
                    logger.info("EOF received, shutting down")
                    break

                line = line.strip()
                if not line:
                    continue

                try:
                    # Parse JSON-RPC request
                    request = json.loads(line)
                    logger.info(f"Received request: {request.get('method', 'unknown')}")

                    # Handle request
                    response = self.handle_request(request)

                    # Send response
                    response_json = json.dumps(response)
                    print(response_json, flush=True)
                    logger.info(f"Sent response: {response.get('result', response.get('error'))}")

                except json.JSONDecodeError as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {"code": -32700, "message": f"Parse error: {str(e)}"},
                        "id": None
                    }
                    print(json.dumps(error_response), flush=True)

        except KeyboardInterrupt:
            logger.info("MCP Server stopped by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            sys.exit(1)

def main():
    """Main entry point"""
    server = SyncTTSNotifyMCPServer()
    server.run_stdio_sync()

if __name__ == "__main__":
    main()