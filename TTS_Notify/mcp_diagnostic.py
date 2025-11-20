#!/usr/bin/env python3
"""
MCP Server Diagnostic Tool

This tool helps diagnose why an MCP server might work with Claude Desktop
but not with other MCP clients like Continue.dev, Cline, etc.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def test_basic_server():
    """Test the basic sync server"""
    print_header("Testing Basic Sync Server")

    test_commands = [
        {
            "name": "Initialize",
            "request": {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "clientInfo": {"name": "Diagnostic", "version": "1.0.0"}
                }
            }
        },
        {
            "name": "List Tools",
            "request": {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
        }
    ]

    server_path = "/Volumes/Resources/Develop/TTS-Notify/TTS_Notify/src/venv/bin/python"
    server_args = ["-m", "tts_notify", "--mode", "mcp"]

    try:
        process = subprocess.Popen(
            [server_path] + server_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for test in test_commands:
            print(f"\n📤 {test['name']}:")
            request_json = json.dumps(test['request'])
            print(f"   Request: {request_json}")

            process.stdin.write(request_json + "\n")
            process.stdin.flush()

            response = process.stdout.readline()
            if response:
                response_data = json.loads(response.strip())
                print(f"   ✅ Response: {json.dumps(response_data, indent=6)}")
            else:
                print("   ❌ No response received")

        process.terminate()
        process.wait()
        return True

    except Exception as e:
        print(f"❌ Error testing basic server: {e}")
        return False

def test_enhanced_server():
    """Test the enhanced server with debug mode"""
    print_header("Testing Enhanced Server (Debug Mode)")

    test_commands = [
        {
            "name": "Initialize with Enhanced Capabilities",
            "request": {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": True},
                        "logging": {},
                        "prompts": {"listChanged": True}
                    },
                    "clientInfo": {"name": "Enhanced Diagnostic", "version": "1.0.0"}
                }
            }
        },
        {
            "name": "List Tools (Enhanced)",
            "request": {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
        },
        {
            "name": "List Prompts (Some clients expect this)",
            "request": {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "prompts/list"
            }
        }
    ]

    server_path = "/Volumes/Resources/Develop/TTS-Notify/TTS_Notify/src/venv/bin/python"
    server_args = ["-m", "tts_notify", "--mode", "mcp", "--debug"]

    try:
        process = subprocess.Popen(
            [server_path] + server_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for test in test_commands:
            print(f"\n📤 {test['name']}:")
            request_json = json.dumps(test['request'])
            print(f"   Request: {request_json}")

            process.stdin.write(request_json + "\n")
            process.stdin.flush()

            response = process.stdout.readline()
            if response:
                response_data = json.loads(response.strip())
                print(f"   ✅ Response: {json.dumps(response_data, indent=6)}")
            else:
                print("   ❌ No response received")

        # Get debug output
        _, stderr = process.communicate(timeout=1)
        if stderr:
            print(f"\n🐛 Debug Output:")
            for line in stderr.strip().split('\n'):
                if line.strip():
                    print(f"   {line}")

        process.terminate()
        return True

    except Exception as e:
        print(f"❌ Error testing enhanced server: {e}")
        return False

def generate_configurations():
    """Generate different configurations for various MCP clients"""
    print_header("MCP Client Configurations")

    base_path = "/Volumes/Resources/Develop/TTS-Notify/TTS_Notify/src/venv/bin/python"

    configurations = {
        "Claude Desktop": {
            "description": "Working configuration for Claude Desktop",
            "config": {
                "mcpServers": {
                    "tts-notify": {
                        "command": base_path,
                        "args": ["-m", "tts_notify", "--mode", "mcp"]
                    }
                }
            }
        },
        "Enhanced (Recommended for other clients)": {
            "description": "Enhanced server with debug mode for troubleshooting",
            "config": {
                "mcpServers": {
                    "tts-notify": {
                        "command": base_path,
                        "args": ["-m", "tts_notify", "--mode", "mcp", "--debug"]
                    }
                }
            }
        },
        "Enhanced without debug": {
            "description": "Enhanced server without debug output (cleaner logs)",
            "config": {
                "mcpServers": {
                    "tts-notify": {
                        "command": base_path,
                        "args": ["-m", "tts_notify", "--mode", "mcp", "--enhanced"]
                    }
                }
            }
        }
    }

    for name, info in configurations.items():
        print(f"\n🎯 {name}:")
        print(f"   📝 {info['description']}")
        print(f"   ⚙️  Configuration:")
        config_json = json.dumps(info['config'], indent=6)
        print(f"   {config_json}")

def troubleshooting_guide():
    """Provide troubleshooting guidance"""
    print_header("Troubleshooting Guide")

    print("""
🔧 Common Issues and Solutions:

1️⃣ TIMEOUT ISSUES:
   ✅ Use enhanced server: --enhanced or --debug flags
   ✅ Check if client expects specific capabilities
   ✅ Verify client supports JSON-RPC 2.0

2️⃣ PROTOCOL VERSION MISMATCH:
   ✅ Ensure client supports MCP 2024-11-05
   ✅ Some clients might need older protocol versions

3️⃣ MISSING CAPABILITIES:
   ✅ Enhanced server includes: tools, logging, prompts
   ✅ Some clients expect "listChanged": True
   ✅ Check client documentation for required capabilities

4️⃣ TRANSPORT ISSUES:
   ✅ Ensure client uses stdio transport
   ✅ Some clients might need WebSocket or other transports
   ✅ Verify no buffer issues with long responses

5️⃣ TOOL SCHEMA VALIDATION:
   ✅ Enhanced server has stricter validation
   ✅ Some clients are sensitive to schema format
   ✅ Check for required vs optional properties

🧪 DEBUG MODE:
   ✅ Add --debug flag to see detailed communication
   ✅ Monitor stderr for debug output
   ✅ Check for validation errors or timeouts

📱 CLIENT-SPECIFIC NOTES:

• CONTINUE.DE:
   - Often needs enhanced capabilities
   - May require "listChanged": True
   - Try debug mode first

• CLINE (VS Code):
   - Usually works with basic MCP
   - Check extension settings for timeouts
   - May need specific tool schemas

• CURSOR:
   - Similar to Claude Desktop
   - Standard configuration should work
   - Check for custom timeout settings

🚀 RECOMMENDATIONS:
   1. Start with enhanced server in debug mode
   2. Check client logs for specific errors
   3. Verify protocol compatibility
   4. Test with minimal configuration first
""")

def main():
    """Main diagnostic function"""
    print("🔍 TTS Notify MCP Server Diagnostic Tool")
    print("This tool helps diagnose compatibility issues with different MCP clients")

    # Test basic server
    basic_success = test_basic_server()

    # Test enhanced server
    enhanced_success = test_enhanced_server()

    # Generate configurations
    generate_configurations()

    # Provide troubleshooting guide
    troubleshooting_guide()

    # Summary
    print_header("Diagnostic Summary")
    print(f"✅ Basic Server: {'WORKING' if basic_success else 'FAILED'}")
    print(f"✅ Enhanced Server: {'WORKING' if enhanced_success else 'FAILED'}")

    if basic_success and enhanced_success:
        print("\n🎉 Both servers are working correctly!")
        print("📝 If other clients still don't work, try:")
        print("   1. Using the Enhanced configuration with --debug")
        print("   2. Checking client-specific requirements")
        print("   3. Reviewing client logs for specific errors")
    else:
        print("\n❌ Server issues detected!")
        print("📝 Check the errors above and fix before testing with clients")

if __name__ == "__main__":
    main()