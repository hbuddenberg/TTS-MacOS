"""
TTS-MacOS v2 - MCP Installation and Configuration Manager

Handles automatic installation and configuration of the MCP server in Claude Desktop:
- Automatic Claude Desktop detection
- JSON configuration generation
- Multiple server support
- Cross-platform paths
- Backup and recovery
- Validation and testing

Features:
- Automatic Claude Desktop config detection
- Multi-server installation (v1.x + v2)
- Path resolution and validation
- Configuration backup and restore
- Installation testing and validation
"""

import os
import json
import sys
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import shutil
import tempfile


class MCPInstaller:
    """
    MCP server installation and configuration manager
    """

    def __init__(self):
        self.system = platform.system()
        self.home_dir = Path.home()
        self.claude_config_dir = self._get_claude_config_dir()
        self.config_file = self.claude_config_dir / "claude_desktop_config.json"

        # Get current script directory
        self.script_dir = Path(__file__).parent.absolute()
        self.v2_server_path = self.script_dir / "mcp_server_v2"
        self.legacy_server_path = self.script_dir / "legacy" / "server.py" if (self.script_dir / "legacy").exists() else None

    def _get_claude_config_dir(self) -> Path:
        """Get Claude Desktop configuration directory based on platform"""
        if self.system == "Darwin":  # macOS
            return self.home_dir / "Library" / "Application Support" / "Claude"
        elif self.system == "Linux":
            return self.home_dir / ".config" / "claude"
        else:
            raise RuntimeError(f"Unsupported platform: {self.system}")

    def detect_claude_installation(self) -> Dict[str, Any]:
        """Detect Claude Desktop installation and configuration"""
        result = {
            "claude_installed": False,
            "config_dir_exists": False,
            "config_file_exists": False,
            "config_valid": False,
            "existing_servers": [],
            "recommendations": []
        }

        # Check if Claude config directory exists
        if self.claude_config_dir.exists():
            result["config_dir_exists"] = True
            result["claude_installed"] = True

            # Check if config file exists
            if self.config_file.exists():
                result["config_file_exists"] = True

                try:
                    # Validate and parse existing config
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)

                    result["config_valid"] = True

                    # Extract existing TTS servers
                    if "mcpServers" in config:
                        for server_name, server_config in config["mcpServers"].items():
                            if "tts" in server_name.lower():
                                result["existing_servers"].append({
                                    "name": server_name,
                                    "command": server_config.get("command", ""),
                                    "args": server_config.get("args", [])
                                })

                except (json.JSONDecodeError, Exception) as e:
                    result["config_valid"] = False
                    result["error"] = str(e)
                    result["recommendations"].append("Config file is corrupted and needs to be recreated")

        # Add recommendations based on detection
        if not result["claude_installed"]:
            result["recommendations"].append("Claude Desktop is not installed. Please install Claude Desktop first.")
        elif not result["config_dir_exists"]:
            result["recommendations"].append("Claude Desktop config directory not found. Run Claude Desktop once to create it.")
        elif not result["config_file_exists"]:
            result["recommendations"].append("Claude Desktop config file not found. A new one will be created.")
        elif result["existing_servers"]:
            existing_names = [s["name"] for s in result["existing_servers"]]
            result["recommendations"].append(f"Existing TTS servers found: {', '.join(existing_names)}")

        return result

    def validate_installation(self) -> Dict[str, Any]:
        """Validate TTS-MacOS v2 installation"""
        validation = {
            "v2_server_exists": False,
            "v2_server_executable": False,
            "python_available": False,
            "dependencies_available": False,
            "legacy_available": False,
            "recommendations": []
        }

        # Check Python availability
        try:
            python_version = sys.version_info
            if python_version >= (3, 8):
                validation["python_available"] = True
                validation["python_version"] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
            else:
                validation["recommendations"].append("Python 3.8+ required")
        except Exception:
            validation["recommendations"].append("Python not available in PATH")

        # Check v2 server
        if self.v2_server_path.exists():
            validation["v2_server_exists"] = True

            # Check if executable
            if os.access(self.v2_server_path, os.X_OK):
                validation["v2_server_executable"] = True
            else:
                validation["recommendations"].append(f"v2 server file not executable: {self.v2_server_path}")
        else:
            validation["recommendations"].append(f"v2 server not found: {self.v2_server_path}")

        # Check legacy server
        if self.legacy_server_path and self.legacy_server_path.exists():
            validation["legacy_available"] = True

        # Test dependencies
        if validation["python_available"]:
            try:
                # Test import in subprocess to avoid affecting current environment
                test_script = f'''
import sys
sys.path.insert(0, "{self.script_dir}")
try:
    from v2.engines import EngineSelector
    print("DEPENDENCIES_OK")
except ImportError as e:
    print(f"DEPENDENCY_ERROR: {{e}}")
'''

                result = subprocess.run([
                    sys.executable, "-c", test_script
                ], capture_output=True, text=True, timeout=10)

                if "DEPENDENCIES_OK" in result.stdout:
                    validation["dependencies_available"] = True
                else:
                    validation["recommendations"].append("Dependencies not available. Run install script first.")

            except Exception as e:
                validation["recommendations"].append(f"Could not test dependencies: {e}")

        return validation

    def generate_mcp_config(
        self,
        install_v2: bool = True,
        install_legacy: bool = False,
        v2_server_name: str = "tts-macos-v2",
        legacy_server_name: str = "tts-macos-legacy",
        python_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate MCP server configuration JSON"""

        # Use current Python or provided path
        if not python_path:
            python_path = sys.executable

        # Validate paths
        if not Path(python_path).exists():
            raise ValueError(f"Python not found at: {python_path}")

        if install_v2 and not self.v2_server_path.exists():
            raise FileNotFoundError(f"v2 server not found: {self.v2_server_path}")

        if install_legacy and (not self.legacy_server_path or not self.legacy_server_path.exists()):
            raise FileNotFoundError(f"Legacy server not found: {self.legacy_server_path}")

        # Generate server configurations
        mcp_servers = {}

        if install_v2:
            mcp_servers[v2_server_name] = {
                "command": python_path,
                "args": [str(self.v2_server_path)],
                "env": {
                    "PYTHONPATH": str(self.script_dir),
                    "TTS_MACOS_V2": "1"
                }
            }

        if install_legacy:
            mcp_servers[legacy_server_name] = {
                "command": python_path,
                "args": [str(self.legacy_server_path), "--legacy"],
                "env": {
                    "PYTHONPATH": str(self.script_dir / "legacy"),
                    "TTS_MACOS_LEGACY": "1"
                }
            }

        # Generate complete configuration
        config = {
            "mcpServers": mcp_servers
        }

        return {
            "config": config,
            "servers_installed": list(mcp_servers.keys()),
            "python_path": python_path,
            "recommendations": self._generate_config_recommendations(install_v2, install_legacy)
        }

    def _generate_config_recommendations(self, install_v2: bool, install_legacy: bool) -> List[str]:
        """Generate recommendations based on installation choices"""
        recommendations = []

        if install_v2 and install_legacy:
            recommendations.append("Both v2 and legacy servers installed. You can switch between them in Claude.")
            recommendations.append("Use 'tts-macos-v2' for new features, 'tts-macos-legacy' for v1.x compatibility.")
        elif install_v2:
            recommendations.append("v2 server installed with full feature set including AI voices and cloning.")
            recommendations.append("Legacy v1.x commands available via 'tts_speak' tool in legacy mode.")
        elif install_legacy:
            recommendations.append("Legacy server installed for v1.x compatibility only.")
            recommendations.append("Consider installing v2 server for AI voices and voice cloning features.")

        recommendations.append("Restart Claude Desktop after configuration changes.")
        recommendations.append("Test MCP tools in Claude with: 'List available tools' or use tts_speak.")

        return recommendations

    def install_mcp_config(
        self,
        config: Dict[str, Any],
        backup_existing: bool = True,
        merge_with_existing: bool = True
    ) -> Dict[str, Any]:
        """Install MCP configuration to Claude Desktop"""

        result = {
            "success": False,
            "backup_created": False,
            "config_updated": False,
            "backup_path": None,
            "servers_added": [],
            "errors": []
        }

        try:
            # Create config directory if it doesn't exist
            self.claude_config_dir.mkdir(parents=True, exist_ok=True)

            # Backup existing configuration
            if backup_existing and self.config_file.exists():
                backup_path = self.config_file.with_suffix('.json.backup')
                shutil.copy2(self.config_file, backup_path)
                result["backup_created"] = True
                result["backup_path"] = str(backup_path)

            # Load or create existing configuration
            existing_config = {}
            if merge_with_existing and self.config_file.exists():
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        existing_config = json.load(f)
                except (json.JSONDecodeError, Exception) as e:
                    result["errors"].append(f"Warning: Could not parse existing config: {e}")
                    existing_config = {}

            # Merge configurations
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}

            # Add new servers
            new_servers = config.get("config", {}).get("mcpServers", {})
            for server_name, server_config in new_servers.items():
                if server_name in existing_config["mcpServers"]:
                    result["errors"].append(f"Warning: Server '{server_name}' already exists, overwriting")

                existing_config["mcpServers"][server_name] = server_config
                result["servers_added"].append(server_name)

            # Write updated configuration
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(existing_config, f, indent=2, ensure_ascii=False)

            result["config_updated"] = True
            result["success"] = True

        except Exception as e:
            result["errors"].append(f"Installation failed: {e}")

        return result

    def test_mcp_installation(self) -> Dict[str, Any]:
        """Test MCP installation by running servers"""
        test_results = {
            "v2_server_test": False,
            "legacy_server_test": False,
            "python_path_test": False,
            "errors": []
        }

        # Test Python path
        try:
            result = subprocess.run([
                sys.executable, "--version"
            ], capture_output=True, text=True, timeout=5)

            if result.returncode == 0:
                test_results["python_path_test"] = True
                test_results["python_version"] = result.stdout.strip()
            else:
                test_results["errors"].append("Python test failed")

        except Exception as e:
            test_results["errors"].append(f"Python path test failed: {e}")

        # Test v2 server
        if self.v2_server_path.exists():
            try:
                # Quick syntax check
                result = subprocess.run([
                    sys.executable, "-m", "py_compile", str(self.v2_server_path)
                ], capture_output=True, text=True, timeout=10)

                if result.returncode == 0:
                    test_results["v2_server_test"] = True
                else:
                    test_results["errors"].append(f"v2 server syntax error: {result.stderr}")

            except Exception as e:
                test_results["errors"].append(f"v2 server test failed: {e}")

        # Test legacy server
        if self.legacy_server_path and self.legacy_server_path.exists():
            try:
                result = subprocess.run([
                    sys.executable, "-m", "py_compile", str(self.legacy_server_path)
                ], capture_output=True, text=True, timeout=10)

                if result.returncode == 0:
                    test_results["legacy_server_test"] = True
                else:
                    test_results["errors"].append(f"Legacy server syntax error: {result.stderr}")

            except Exception as e:
                test_results["errors"].append(f"Legacy server test failed: {e}")

        return test_results

    def uninstall_mcp_config(
        self,
        server_names: List[str],
        backup_existing: bool = True
    ) -> Dict[str, Any]:
        """Uninstall specific MCP servers from configuration"""

        result = {
            "success": False,
            "servers_removed": [],
            "backup_created": False,
            "backup_path": None,
            "errors": []
        }

        try:
            if not self.config_file.exists():
                result["errors"].append("Configuration file not found")
                return result

            # Backup existing configuration
            if backup_existing:
                backup_path = self.config_file.with_suffix('.json.uninstall_backup')
                shutil.copy2(self.config_file, backup_path)
                result["backup_created"] = True
                result["backup_path"] = str(backup_path)

            # Load configuration
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Remove specified servers
            if "mcpServers" in config:
                for server_name in server_names:
                    if server_name in config["mcpServers"]:
                        del config["mcpServers"][server_name]
                        result["servers_removed"].append(server_name)
                    else:
                        result["errors"].append(f"Server '{server_name}' not found in configuration")

            # Write updated configuration
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            result["success"] = True

        except Exception as e:
            result["errors"].append(f"Uninstallation failed: {e}")

        return result

    def get_current_config(self) -> Dict[str, Any]:
        """Get current Claude Desktop MCP configuration"""
        if not self.config_file.exists():
            return {
                "exists": False,
                "config": {},
                "error": "Configuration file not found"
            }

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            return {
                "exists": True,
                "config": config,
                "mcp_servers": config.get("mcpServers", {}),
                "server_count": len(config.get("mcpServers", {}))
            }

        except Exception as e:
            return {
                "exists": True,
                "config": {},
                "error": f"Could not parse configuration: {e}"
            }

    def create_installation_script(self, output_path: str) -> str:
        """Create a standalone installation script"""

        script_content = f'''#!/bin/bash

# TTS-MacOS v2 - MCP Installation Script
# Generated automatically for Claude Desktop configuration

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="{self.script_dir}"
V2_SERVER="{self.v2_server_path}"
LEGACY_SERVER="{self.legacy_server_path or ''}"
PYTHON_PATH="{sys.executable}"
CLAUDE_CONFIG="{self.claude_config_dir}"
CONFIG_FILE="{self.config_file}"

echo -e "${{BLUE}}🔧 TTS-MacOS v2 MCP Installation${NC}"
echo "=================================="

# Check Claude Desktop
if [ ! -d "$CLAUDE_CONFIG" ]; then
    echo -e "${{RED}}❌ Claude Desktop not found${NC}"
    echo "Please install Claude Desktop and run it once to create configuration directory."
    exit 1
fi

echo -e "${{GREEN}}✅ Claude Desktop configuration found${NC}"

# Check v2 server
if [ ! -f "$V2_SERVER" ]; then
    echo -e "${{RED}}❌ v2 server not found: $V2_SERVER${NC}"
    exit 1
fi

echo -e "${{GREEN}}✅ v2 server found${NC}}"

# Make servers executable
chmod +x "$V2_SERVER"
if [ -f "$LEGACY_SERVER" ]; then
    chmod +x "$LEGACY_SERVER"
    echo -e "${{GREEN}}✅ Legacy server found and made executable${NC}"
fi

# Create configuration directory
mkdir -p "$CLAUDE_CONFIG"

# Backup existing configuration
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${{YELLOW}}⚠️  Existing configuration backed up${NC}"
fi

# Generate new configuration
cat > "$CONFIG_FILE" << 'EOF'
{{
    "mcpServers": {{
        "tts-macos-v2": {{
            "command": "{sys.executable}",
            "args": ["{self.v2_server_path}"],
            "env": {{
                "PYTHONPATH": "{self.script_dir}",
                "TTS_MACOS_V2": "1"
            }}
        }}'''

# Add legacy server if available
if self.legacy_server_path and self.legacy_server_path.exists():
            script_content += f''',
        "tts-macos-legacy": {{
            "command": "{sys.executable}",
            "args": ["{self.legacy_server_path}", "--legacy"],
            "env": {{
                "PYTHONPATH": "{self.script_dir}/legacy",
                "TTS_MACOS_LEGACY": "1"
            }}
        }}'''

        script_content += '''
    }
}
EOF

echo -e "${GREEN}✅ Claude Desktop configuration updated${NC}"

echo ""
echo -e "${{BLUE}}🎉 Installation Complete!${NC}"
echo "========================="
echo ""
echo "📋 Installed Servers:"
echo "  • tts-macos-v2: Full v2.0 features with AI voices and cloning"
if self.legacy_server_path and self.legacy_server_path.exists():
            echo "  • tts-macos-legacy: v1.x compatibility mode"
echo ""
echo "🔄 Next Steps:"
echo "  1. Restart Claude Desktop completely"
echo "  2. Test with: 'List available tools' in Claude"
echo "  3. Try: tts_speak(text='Hello from TTS-MacOS v2!')"
echo ""
echo -e "${{YELLOW}}⚠️  Important: Restart Claude Desktop for changes to take effect${NC}"
'''

        # Write script to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

        # Make executable
        os.chmod(output_path, 0o755)

        return output_path
