#!/usr/bin/env python3
"""
TTS-MacOS v2 - Quick MCP JSON Generator

Generates ready-to-use JSON configuration for Claude Desktop MCP integration.
Provides resolved paths and immediate JSON output for copy-paste installation.

Usage:
    python generate_mcp_json.py [--v2] [--legacy] [--pretty]
    python generate_mcp_json.py --install
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path


class MCPJSONGenerator:
    """Generates MCP configuration JSON with resolved paths"""

    def __init__(self):
        self.system = platform.system()
        self.script_dir = Path(__file__).parent.absolute()
        self.venv_dir = self.script_dir / "venv-v2"

        # Detect paths
        self.python_path = self._resolve_python_path()
        self.v2_server_path = self.script_dir / "mcp_server_v2.py"
        self.legacy_server_path = self.script_dir / "legacy" / "server.py"

        # Claude Desktop config directory
        if self.system == "Darwin":  # macOS
            self.claude_config_dir = (
                Path.home() / "Library" / "Application Support" / "Claude"
            )
        elif self.system == "Linux":
            self.claude_config_dir = Path.home() / ".config" / "claude"
        else:
            self.claude_config_dir = None

    def _resolve_python_path(self) -> Path:
        """Resolve the best Python path to use"""
        # Prefer virtual environment Python
        venv_python = self.venv_dir / "bin" / "python"
        if venv_python.exists():
            return venv_python

        # Fall back to system Python3
        try:
            result = subprocess.run(
                ["which", "python3"], capture_output=True, text=True
            )
            if result.returncode == 0:
                return Path(result.stdout.strip())
        except:
            pass

        # Fall back to current Python
        return Path(sys.executable)

    def validate_installation(self) -> dict:
        """Validate TTS-MacOS v2 installation"""
        validation = {
            "script_dir": self.script_dir,
            "python_path": self.python_path,
            "python_exists": self.python_path.exists(),
            "v2_server_exists": self.v2_server_path.exists(),
            "legacy_server_exists": self.legacy_server_path.exists(),
            "claude_config_exists": self.claude_config_dir.exists()
            if self.claude_config_dir
            else False,
            "venv_exists": self.venv_dir.exists(),
            "errors": [],
            "warnings": [],
        }

        if not validation["python_exists"]:
            validation["errors"].append("Python not found")

        if not validation["v2_server_exists"]:
            validation["errors"].append("v2 server not found")

        if not validation["venv_exists"]:
            validation["warnings"].append("Virtual environment not found")

        return validation

    def generate_config(
        self,
        include_v2: bool = True,
        include_legacy: bool = False,
        server_names: dict = None,
    ) -> dict:
        """Generate MCP configuration dictionary"""

        if server_names is None:
            server_names = {"v2": "tts-macos-v2", "legacy": "tts-macos-legacy"}

        config = {"mcpServers": {}}

        # v2 server configuration
        if include_v2:
            config["mcpServers"][server_names["v2"]] = {
                "command": str(self.python_path),
                "args": [str(self.v2_server_path)],
                "env": {"PYTHONPATH": str(self.script_dir), "TTS_MACOS_V2": "1"},
            }

        # Legacy server configuration
        if include_legacy and self.legacy_server_path.exists():
            config["mcpServers"][server_names["legacy"]] = {
                "command": str(self.python_path),
                "args": [str(self.legacy_server_path), "--legacy"],
                "env": {
                    "PYTHONPATH": str(self.script_dir / "legacy"),
                    "TTS_MACOS_LEGACY": "1",
                },
            }

        return config

    def format_json_output(
        self, config: dict, pretty: bool = True, include_comments: bool = False
    ) -> str:
        """Format JSON configuration for output"""

        if include_comments:
            # Create commented version
            lines = []
            lines.append("{")
            lines.append('  "mcpServers": {')

            for i, (server_name, server_config) in enumerate(
                config["mcpServers"].items()
            ):
                if i > 0:
                    lines.append("    },")

                lines.append(
                    f"    // TTS-MacOS {'v2' if 'v2' in server_name else 'Legacy'} Server"
                )
                lines.append(f'    "{server_name}": {{')
                lines.append(f'      "command": "{server_config["command"]}",')
                lines.append(f'      "args": {json.dumps(server_config["args"])},')
                lines.append('      "env": {')

                for j, (key, value) in enumerate(server_config["env"].items()):
                    comma = "," if j < len(server_config["env"]) - 1 else ""
                    lines.append(f'        "{key}": "{value}"{comma}')

                lines.append("      }")

            lines.append("    }")
            lines.append("  }")
            lines.append("}")

            return "\n".join(lines)
        else:
            # Standard JSON formatting
            if pretty:
                return json.dumps(config, indent=2, ensure_ascii=False)
            else:
                return json.dumps(config, ensure_ascii=False)

    def install_config(self, config: dict, backup: bool = True) -> dict:
        """Install configuration to Claude Desktop"""

        result = {
            "success": False,
            "backup_created": False,
            "backup_path": None,
            "config_file": None,
            "errors": [],
        }

        if not self.claude_config_dir:
            result["errors"].append("Claude Desktop config directory not found")
            return result

        try:
            # Create config directory
            self.claude_config_dir.mkdir(parents=True, exist_ok=True)

            config_file = self.claude_config_dir / "claude_desktop_config.json"
            result["config_file"] = str(config_file)

            # Backup existing configuration
            if backup and config_file.exists():
                backup_path = config_file.with_suffix(".json.backup")
                import shutil

                shutil.copy2(config_file, backup_path)
                result["backup_created"] = True
                result["backup_path"] = str(backup_path)

            # Write new configuration
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            result["success"] = True

        except Exception as e:
            result["errors"].append(f"Installation failed: {e}")

        return result

    def print_installation_guide(self, config: dict):
        """Print comprehensive installation guide"""

        print(f"\n📋 Installation Options:")
        print("=" * 50)

        # Option 1: Auto install
        print(f"\n1. 🚀 Auto-Installation (Recommended):")
        print(f"   python generate_mcp_json.py --install")

        # Option 2: MCP config tool
        print(f"\n2. 🔧 MCP Configuration Tool:")
        print(f"   ./mcp-config install --v2")

        # Option 3: Manual installation
        print(f"\n3. 📝 Manual Installation:")
        print(f"   a) Copy the JSON below")
        if self.claude_config_dir:
            print(f"   b) Edit: {self.claude_config_dir}/claude_desktop_config.json")
        else:
            print(
                f"   b) Create: ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)"
            )
            print(f"      or ~/.config/claude/claude_desktop_config.json (Linux)")
        print(f"   c) Paste the JSON")
        print(f"   d) Save and restart Claude Desktop")

        print(f"\n🧪 Testing After Installation:")
        print(f"   • Restart Claude Desktop completely")
        print(f"   • Try: 'List available tools'")
        print(f"   • Test: tts_speak(text='Hello from TTS-MacOS v2!')")

        if self.claude_config_dir:
            print(f"\n📁 Configuration File Location:")
            print(f"   {self.claude_config_dir}/claude_desktop_config.json")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate MCP configuration JSON for TTS-MacOS v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Generate v2 server config
  %(prog)s --legacy                   # Include legacy server
  %(prog)s --v2 --legacy            # Both servers
  %(prog)s --install                  # Auto-install to Claude Desktop
  %(prog)s --pretty --comments        # Pretty output with comments
        """,
    )

    parser.add_argument(
        "--v2", action="store_true", default=True, help="Include v2 server (default)"
    )
    parser.add_argument(
        "--no-v2", dest="v2", action="store_false", help="Skip v2 server"
    )
    parser.add_argument("--legacy", action="store_true", help="Include legacy server")
    parser.add_argument(
        "--install", action="store_true", help="Auto-install to Claude Desktop"
    )
    parser.add_argument(
        "--pretty", action="store_true", default=True, help="Pretty JSON formatting"
    )
    parser.add_argument(
        "--comments", action="store_true", help="Include comments in JSON"
    )
    parser.add_argument("--name-v2", help="Custom v2 server name")
    parser.add_argument("--name-legacy", help="Custom legacy server name")

    args = parser.parse_args()

    # Create generator
    generator = MCPJSONGenerator()

    # Validate installation
    validation = generator.validate_installation()

    if validation["errors"]:
        print("❌ Installation validation failed:")
        for error in validation["errors"]:
            print(f"   • {error}")
        return 1

    if validation["warnings"]:
        print("⚠️  Installation warnings:")
        for warning in validation["warnings"]:
            print(f"   • {warning}")
        print()

    # Show system information
    print(f"🖥️  System: {generator.system}")
    print(f"📁 Script Directory: {generator.script_dir}")
    print(f"🐍 Python Path: {generator.python_path}")
    print(f"🔧 v2 Server: {generator.v2_server_path}")
    if validation["legacy_server_exists"]:
        print(f"🔄 Legacy Server: {generator.legacy_server_path}")

    # Generate configuration
    server_names = {}
    if args.name_v2:
        server_names["v2"] = args.name_v2
    if args.name_legacy:
        server_names["legacy"] = args.name_legacy

    config = generator.generate_config(
        include_v2=args.v2,
        include_legacy=args.legacy and validation["legacy_server_exists"],
        server_names=server_names if server_names else None,
    )

    # Auto-install if requested
    if args.install:
        print(f"\n🚀 Auto-installing to Claude Desktop...")
        install_result = generator.install_config(config)

        if install_result["success"]:
            print(f"✅ Configuration installed successfully!")
            if install_result["backup_created"]:
                print(f"💾 Backup created: {install_result['backup_path']}")
            print(f"📁 Config file: {install_result['config_file']}")
            print(f"\n🔄 Restart Claude Desktop to use the new configuration")
        else:
            print(f"❌ Installation failed:")
            for error in install_result["errors"]:
                print(f"   • {error}")
            return 1

    # Output JSON configuration
    print(f"\n📝 MCP Configuration JSON:")
    print("=" * 50)

    json_output = generator.format_json_output(
        config, pretty=args.pretty, include_comments=args.comments
    )

    print(json_output)

    # Print installation guide if not auto-installed
    if not args.install:
        generator.print_installation_guide(config)

    return 0


if __name__ == "__main__":
    sys.exit(main())
