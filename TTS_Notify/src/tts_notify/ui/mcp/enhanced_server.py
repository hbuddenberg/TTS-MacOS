#!/usr/bin/env python3
"""
TTS Notify v2.0.0 - Enhanced MCP Server

Enhanced MCP server implementation with maximum compatibility
for different MCP clients (Claude Desktop, Continue.dev, Cline, etc.)
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

class EnhancedTTSNotifyMCPServer:
    """Enhanced MCP server with maximum compatibility"""

    def __init__(self, debug=False):
        self.debug = debug
        self.initialized = False
        self.request_count = 0

        # Enhanced tool schemas for better compatibility
        self.tools = {
            "speak_text": {
                "name": "speak_text",
                "description": "Speak text using macOS TTS with optional voice and rate",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to speak",
                            "minLength": 1,
                            "maxLength": 10000
                        },
                        "voice": {
                            "type": "string",
                            "description": "Voice name (optional, uses system default if not specified)",
                            "default": None
                        },
                        "rate": {
                            "type": "integer",
                            "description": "Speech rate in words per minute (100-300)",
                            "minimum": 100,
                            "maximum": 300,
                            "default": 175
                        }
                    },
                    "required": ["text"]
                }
            },
            "list_voices": {
                "name": "list_voices",
                "description": "List all available TTS voices on the system",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            },
            "save_audio": {
                "name": "save_audio",
                "description": "Save text as audio file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to convert",
                            "minLength": 1
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Output file path (will use .aiff format)",
                            "minLength": 1
                        },
                        "voice": {
                            "type": "string",
                            "description": "Voice name (optional)",
                            "default": None
                        },
                        "rate": {
                            "type": "integer",
                            "description": "Speech rate (optional)",
                            "minimum": 100,
                            "maximum": 300,
                            "default": 175
                        }
                    },
                    "required": ["text", "output_path"]
                }
            }
        }

        if self.debug:
            logger.setLevel(logging.DEBUG)
            print("🐛 Enhanced MCP Server started in DEBUG mode")

    def log_debug(self, message: str):
        """Debug logging helper"""
        if self.debug:
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] DEBUG: {message}", file=sys.stderr)

    def speak_text(self, text: str, voice: Optional[str] = None, rate: Optional[int] = None) -> str:
        """Speak text using macOS TTS"""
        try:
            self.log_debug(f"Speaking text: '{text[:50]}...' with voice: {voice or 'default'}")

            cmd = ['say']

            if voice and voice.strip():
                cmd.extend(['-v', voice.strip()])

            if rate and isinstance(rate, int):
                # Validate rate range
                rate = max(100, min(300, rate))
                cmd.extend(['-r', str(rate)])

            cmd.append(text)

            self.log_debug(f"Executing command: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                voice_used = voice or "system default"
                self.log_debug(f"TTS execution successful")
                return f"✅ Text spoken successfully with voice: {voice_used}"
            else:
                error_msg = result.stderr if result.stderr else 'Unknown TTS error'
                self.log_debug(f"TTS execution failed: {error_msg}")
                return f"❌ TTS Error: {error_msg}"

        except subprocess.TimeoutExpired:
            self.log_debug("TTS execution timed out")
            return "❌ TTS Error: Speech synthesis timed out"
        except Exception as e:
            self.log_debug(f"TTS exception: {str(e)}")
            return f"❌ TTS Exception: {str(e)}"

    def list_voices(self) -> str:
        """List all available TTS voices"""
        try:
            self.log_debug("Listing system voices...")

            result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                voices_output = result.stdout

                voices = []
                for line in voices_output.split('\n'):
                    if line.strip():
                        voices.append(line.strip())

                self.log_debug(f"Found {len(voices)} voices")

                result_data = {
                    "total_voices": len(voices),
                    "voices": voices,
                    "sample_spanish_voices": [v for v in voices if any(x in v.lower() for x in ['es_', 'spanish', 'español', 'mónica', 'jorge', 'paulina'])][:5]
                }

                return json.dumps(result_data, indent=2, ensure_ascii=False)
            else:
                error_msg = result.stderr if result.stderr else 'Unknown error'
                self.log_debug(f"Voice listing failed: {error_msg}")
                return f"❌ Error listing voices: {error_msg}"

        except subprocess.TimeoutExpired:
            self.log_debug("Voice listing timed out")
            return "❌ Error listing voices: Timeout"
        except Exception as e:
            self.log_debug(f"Voice listing exception: {str(e)}")
            return f"❌ Exception: {str(e)}"

    def save_audio(self, text: str, output_path: str, voice: Optional[str] = None, rate: Optional[int] = None) -> str:
        """Save text as audio file"""
        try:
            self.log_debug(f"Saving audio to: {output_path}")

            # Ensure .aiff extension
            if not output_path.lower().endswith('.aiff'):
                output_path += '.aiff'

            cmd = ['say']

            if voice and voice.strip():
                cmd.extend(['-v', voice.strip()])

            if rate and isinstance(rate, int):
                rate = max(100, min(300, rate))
                cmd.extend(['-r', str(rate)])

            cmd.extend(['-o', output_path, text])

            self.log_debug(f"Audio save command: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                self.log_debug(f"Audio saved successfully to: {output_path}")
                return f"✅ Audio saved successfully to: {output_path}"
            else:
                error_msg = result.stderr if result.stderr else 'Unknown error'
                self.log_debug(f"Audio save failed: {error_msg}")
                return f"❌ Error saving audio: {error_msg}"

        except subprocess.TimeoutExpired:
            self.log_debug("Audio save timed out")
            return "❌ Error saving audio: Timeout"
        except Exception as e:
            self.log_debug(f"Audio save exception: {str(e)}")
            return f"❌ Exception: {str(e)}"

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP JSON-RPC request with enhanced error handling"""

        self.request_count += 1
        request_id = request.get("id", self.request_count)

        self.log_debug(f"Request #{self.request_count}: {request.get('method', 'unknown')}")

        # Validate basic JSON-RPC structure
        if "jsonrpc" not in request or request["jsonrpc"] != "2.0":
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32600,
                    "message": "Invalid Request: Missing or invalid jsonrpc version"
                },
                "id": request_id
            }

        if "method" not in request:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32600,
                    "message": "Invalid Request: Missing method"
                },
                "id": request_id
            }

        method = request["method"]
        params = request.get("params", {})

        try:
            # Handle initialization
            if method == "initialize":
                self.log_debug(f"Initializing with params: {params}")

                self.initialized = True

                # Enhanced server info for better compatibility
                server_info = {
                    "name": "TTS Notify",
                    "version": "2.0.0"
                }

                # Enhanced capabilities
                capabilities = {
                    "tools": {
                        "listChanged": True  # Some clients need this
                    },
                    "logging": {},  # Some clients expect this
                    "prompts": {    # Some clients expect this
                        "listChanged": True
                    }
                }

                response = {
                    "jsonrpc": "2.0",
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": capabilities,
                        "serverInfo": server_info
                    },
                    "id": request_id
                }

                self.log_debug("Initialization successful")
                return response

            # Check if initialized
            if not self.initialized and method not in ["initialize"]:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32002,
                        "message": "Server not initialized"
                    },
                    "id": request_id
                }

            # Handle notifications
            if method.startswith("notifications/"):
                self.log_debug(f"Received notification: {method}")
                return None  # Notifications don't require responses

            # Handle tools list
            elif method == "tools/list":
                tools_list = list(self.tools.values())

                response = {
                    "jsonrpc": "2.0",
                    "result": {
                        "tools": tools_list
                    },
                    "id": request_id
                }

                self.log_debug(f"Listed {len(tools_list)} tools")
                return response

            # Handle tool calls
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})

                self.log_debug(f"Calling tool: {tool_name} with args: {arguments}")

                if tool_name not in self.tools:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32601,
                            "message": f"Tool not found: {tool_name}"
                        },
                        "id": request_id
                    }

                # Validate arguments against schema
                tool_schema = self.tools[tool_name]["inputSchema"]
                validation_error = self.validate_arguments(tool_schema, arguments)

                if validation_error:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32602,
                            "message": f"Invalid arguments: {validation_error}"
                        },
                        "id": request_id
                    }

                # Execute tool
                if tool_name == "speak_text":
                    result = self.speak_text(**arguments)
                elif tool_name == "list_voices":
                    result = self.list_voices()
                elif tool_name == "save_audio":
                    result = self.save_audio(**arguments)
                else:
                    result = f"Unknown tool: {tool_name}"

                response = {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": result
                        }]
                    },
                    "id": request_id
                }

                self.log_debug(f"Tool {tool_name} executed successfully")
                return response

            # Handle prompts list (some clients expect this)
            elif method == "prompts/list":
                response = {
                    "jsonrpc": "2.0",
                    "result": {
                        "prompts": []
                    },
                    "id": request_id
                }

                self.log_debug("Prompts list requested (empty list)")
                return response

            # Handle unknown methods
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    },
                    "id": request_id
                }

        except Exception as e:
            error_msg = f"Internal error: {str(e)}"
            self.log_debug(f"Request handling failed: {error_msg}")

            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": error_msg
                },
                "id": request_id
            }

    def validate_arguments(self, schema: Dict, arguments: Dict) -> Optional[str]:
        """Validate arguments against JSON schema"""

        # Basic validation
        required = schema.get("required", [])
        properties = schema.get("properties", {})

        # Check required properties
        for req in required:
            if req not in arguments:
                return f"Missing required property: {req}"

        # Check property types
        for prop, value in arguments.items():
            if prop in properties:
                prop_schema = properties[prop]
                expected_type = prop_schema.get("type")

                if expected_type == "string":
                    if not isinstance(value, str):
                        return f"Property {prop} must be a string"

                    # Check minLength
                    min_len = prop_schema.get("minLength")
                    if min_len and len(value) < min_len:
                        return f"Property {prop} must be at least {min_len} characters"

                    # Check maxLength
                    max_len = prop_schema.get("maxLength")
                    if max_len and len(value) > max_len:
                        return f"Property {prop} must be at most {max_len} characters"

                elif expected_type == "integer":
                    if not isinstance(value, int):
                        return f"Property {prop} must be an integer"

                    # Check range
                    min_val = prop_schema.get("minimum")
                    if min_val is not None and value < min_val:
                        return f"Property {prop} must be >= {min_val}"

                    max_val = prop_schema.get("maximum")
                    if max_val is not None and value > max_val:
                        return f"Property {prop} must be <= {max_val}"

        return None

    def run_stdio_enhanced(self):
        """Run MCP server with enhanced stdio communication"""

        print("🤖 Enhanced TTS Notify MCP Server v2.0.0 starting...", file=sys.stderr)
        print("📍 Enhanced compatibility mode", file=sys.stderr)
        print("🔧 Ready for MCP client connections", file=sys.stderr)

        if self.debug:
            print("🐛 Debug mode enabled", file=sys.stderr)

        try:
            while True:
                try:
                    # Read line from stdin with timeout awareness
                    line = sys.stdin.readline()

                    if not line:
                        self.log_debug("EOF received, shutting down")
                        break

                    line = line.strip()
                    if not line:
                        continue

                    self.log_debug(f"Received: {line[:100]}...")

                    # Parse JSON-RPC request
                    try:
                        request = json.loads(line)
                    except json.JSONDecodeError as e:
                        self.log_debug(f"JSON decode error: {e}")
                        error_response = {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32700,
                                "message": f"Parse error: {str(e)}"
                            },
                            "id": None
                        }
                        print(json.dumps(error_response), flush=True)
                        continue

                    # Handle request
                    response = self.handle_request(request)

                    # Send response (notifications don't get responses)
                    if response is not None:
                        response_json = json.dumps(response, ensure_ascii=False)
                        print(response_json, flush=True)
                        self.log_debug(f"Sent response: {response.get('result', response.get('error', 'Unknown'))}")

                except KeyboardInterrupt:
                    self.log_debug("Interrupted by user")
                    break
                except Exception as e:
                    self.log_debug(f"Unexpected error: {e}")
                    # Try to send error response
                    try:
                        error_response = {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32603,
                                "message": f"Server error: {str(e)}"
                            },
                            "id": None
                        }
                        print(json.dumps(error_response), flush=True)
                    except:
                        pass  # If we can't even send error, just continue

        except KeyboardInterrupt:
            print("📋 Enhanced MCP Server stopped by user", file=sys.stderr)
        except Exception as e:
            print(f"❌ Fatal error in enhanced MCP server: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    """Main entry point"""
    debug = "--debug" in sys.argv
    server = EnhancedTTSNotifyMCPServer(debug=debug)
    server.run_stdio_enhanced()

if __name__ == "__main__":
    main()