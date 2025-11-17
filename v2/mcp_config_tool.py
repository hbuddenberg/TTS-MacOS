#!/usr/bin/env python3
"""
TTS-MacOS v2 - MCP Configuration Tool

Command-line tool for installing and configuring TTS-MacOS v2 MCP server in Claude Desktop.
Provides automated detection, configuration, and testing of MCP integration.

Usage:
    python mcp_config_tool.py install [--v2] [--legacy] [--name SERVER_NAME]
    python mcp_config_tool.py detect
    python mcp_config_tool.py test
    python mcp_config_tool.py uninstall [--server SERVER_NAME]
    python mcp_config_tool.py status
"""

import argparse
import json
import sys
from pathlib import Path

from mcp_installer import MCPInstaller


def print_section(title: str, color: str = "\033[1;34m"):
    """Print a formatted section header"""
    print(f"\n{color}🔧 {title}\033[0m")
    print("=" * (len(title) + 4))


def print_success(message: str):
    """Print success message"""
    print(f"✅ {message}")


def print_error(message: str):
    """Print error message"""
    print(f"❌ {message}")


def print_warning(message: str):
    """Print warning message"""
    print(f"⚠️  {message}")


def print_info(message: str):
    """Print info message"""
    print(f"ℹ️  {message}")


def format_json_output(data: dict, indent: int = 2) -> str:
    """Format dictionary as pretty JSON"""
    return json.dumps(data, indent=indent, ensure_ascii=False)


def cmd_detect(args):
    """Detect Claude Desktop installation and TTS-MacOS setup"""
    installer = MCPInstaller()

    print_section("Claude Desktop Detection")

    # Detect Claude installation
    claude_info = installer.detect_claude_installation()

    print(
        f"Claude Desktop Installed: {'✅' if claude_info['claude_installed'] else '❌'}"
    )
    print(
        f"Config Directory Exists: {'✅' if claude_info['config_dir_exists'] else '❌'}"
    )
    print(f"Config File Exists: {'✅' if claude_info['config_file_exists'] else '❌'}")
    print(f"Config Valid: {'✅' if claude_info['config_valid'] else '❌'}")

    if claude_info["existing_servers"]:
        print(f"\n📋 Existing TTS Servers:")
        for server in claude_info["existing_servers"]:
            print(f"  • {server['name']}: {server['command']}")

    if claude_info["recommendations"]:
        print(f"\n💡 Recommendations:")
        for rec in claude_info["recommendations"]:
            print(f"  • {rec}")

    print_section("TTS-MacOS v2 Installation Validation")

    # Validate TTS-MacOS installation
    validation = installer.validate_installation()

    print(f"Python Available: {'✅' if validation['python_available'] else '❌'}")
    if validation.get("python_version"):
        print(f"Python Version: {validation['python_version']}")

    print(f"v2 Server Exists: {'✅' if validation['v2_server_exists'] else '❌'}")
    print(
        f"v2 Server Executable: {'✅' if validation['v2_server_executable'] else '❌'}"
    )
    print(
        f"Dependencies Available: {'✅' if validation['dependencies_available'] else '❌'}"
    )
    print(
        f"Legacy Server Available: {'✅' if validation['legacy_available'] else '❌'}"
    )

    if validation["recommendations"]:
        print(f"\n⚠️  Installation Recommendations:")
        for rec in validation["recommendations"]:
            print(f"  • {rec}")

    return (
        0 if (claude_info["claude_installed"] and validation["v2_server_exists"]) else 1
    )


def cmd_install(args):
    """Install MCP server configuration"""
    installer = MCPInstaller()

    print_section("MCP Server Installation")

    # Validate installation first
    validation = installer.validate_installation()
    if not validation["v2_server_exists"] or not validation["dependencies_available"]:
        print_error("TTS-MacOS v2 installation validation failed")
        for rec in validation["recommendations"]:
            print_warning(rec)
        return 1

    # Generate configuration
    try:
        config_result = installer.generate_mcp_config(
            install_v2=args.v2,
            install_legacy=args.legacy,
            v2_server_name=args.name
            if args.name and not args.name.startswith("tts-macos-legacy")
            else "tts-macos-v2",
            legacy_server_name=args.name
            if args.name and args.name.startswith("tts-macos-legacy")
            else "tts-macos-legacy",
            python_path=args.python_path,
        )

        print_success("Configuration generated successfully")
        print(f"Servers to install: {', '.join(config_result['servers_installed'])}")
        print(f"Python path: {config_result['python_path']}")

    except Exception as e:
        print_error(f"Configuration generation failed: {e}")
        return 1

    # Install configuration
    try:
        install_result = installer.install_mcp_config(
            config_result["config"],
            backup_existing=not args.no_backup,
            merge_with_existing=args.merge,
        )

        if install_result["success"]:
            print_success("MCP configuration installed successfully")

            if install_result["backup_created"]:
                print_info(f"Backup created: {install_result['backup_path']}")

            print_success(
                f"Servers added: {', '.join(install_result['servers_added'])}"
            )

        else:
            print_error("MCP configuration installation failed")
            for error in install_result["errors"]:
                print_warning(error)
            return 1

    except Exception as e:
        print_error(f"Installation failed: {e}")
        return 1

    # Show recommendations
    if config_result["recommendations"]:
        print_section("Recommendations")
        for rec in config_result["recommendations"]:
            print_info(rec)

    print_section("Installation Complete")
    print_success("🎉 TTS-MacOS v2 MCP server installed!")
    print_info("Restart Claude Desktop for changes to take effect")
    print_info("Test with: 'List available tools' in Claude")

    return 0


def cmd_test(args):
    """Test MCP installation"""
    installer = MCPInstaller()

    print_section("MCP Installation Testing")

    # Test installation
    test_results = installer.test_mcp_installation()

    print(f"Python Path Test: {'✅' if test_results['python_path_test'] else '❌'}")
    if test_results.get("python_version"):
        print(f"Python Version: {test_results['python_version']}")

    print(f"v2 Server Test: {'✅' if test_results['v2_server_test'] else '❌'}")
    print(f"Legacy Server Test: {'✅' if test_results['legacy_server_test'] else '❌'}")

    if test_results["errors"]:
        print_section("Test Errors")
        for error in test_results["errors"]:
            print_warning(error)
        return 1

    print_success("All tests passed!")

    # Show current configuration
    print_section("Current Configuration")
    current_config = installer.get_current_config()

    if current_config["exists"]:
        print(f"Configuration file: {installer.config_file}")
        print(f"MCP servers: {current_config['server_count']}")

        if current_config["mcp_servers"]:
            print("\nConfigured servers:")
            for name, config in current_config["mcp_servers"].items():
                if "tts" in name.lower():
                    print(f"  • {name}: {config.get('command', 'No command')}")
    else:
        print_warning("No configuration file found")

    return 0


def cmd_uninstall(args):
    """Uninstall MCP server configuration"""
    installer = MCPInstaller()

    print_section("MCP Server Uninstallation")

    # Determine servers to uninstall
    if args.server:
        servers_to_remove = [args.server]
    else:
        # Default: remove all TTS-MacOS servers
        current_config = installer.get_current_config()
        if current_config["exists"]:
            servers_to_remove = [
                name
                for name in current_config["mcp_servers"].keys()
                if "tts" in name.lower() and "macos" in name.lower()
            ]
        else:
            print_error("No configuration file found")
            return 1

    if not servers_to_remove:
        print_warning("No TTS-MacOS servers found to uninstall")
        return 0

    print_info(f"Servers to remove: {', '.join(servers_to_remove)}")

    # Confirm uninstallation
    if not args.force:
        response = input(
            f"\n⚠️  Are you sure you want to remove {len(servers_to_remove)} server(s)? [y/N]: "
        )
        if response.lower() not in ["y", "yes"]:
            print_info("Uninstallation cancelled")
            return 0

    # Perform uninstallation
    try:
        uninstall_result = installer.uninstall_mcp_config(
            servers_to_remove, backup_existing=not args.no_backup
        )

        if uninstall_result["success"]:
            print_success("Uninstallation completed successfully")

            if uninstall_result["backup_created"]:
                print_info(f"Backup created: {uninstall_result['backup_path']}")

            if uninstall_result["servers_removed"]:
                print_success(
                    f"Servers removed: {', '.join(uninstall_result['servers_removed'])}"
                )

            print_info("Restart Claude Desktop for changes to take effect")

        else:
            print_error("Uninstallation failed")
            for error in uninstall_result["errors"]:
                print_warning(error)
            return 1

    except Exception as e:
        print_error(f"Uninstallation failed: {e}")
        return 1

    return 0


def cmd_status(args):
    """Show current status and configuration"""
    installer = MCPInstaller()

    print_section("TTS-MacOS v2 MCP Status")

    # Show Claude detection
    claude_info = installer.detect_claude_installation()
    print(
        f"Claude Desktop: {'✅ Installed' if claude_info['claude_installed'] else '❌ Not found'}"
    )
    print(
        f"Configuration: {'✅ Valid' if claude_info['config_valid'] else '❌ Invalid/Missing'}"
    )

    # Show current configuration
    current_config = installer.get_current_config()

    if current_config["exists"] and current_config["mcp_servers"]:
        tts_servers = {
            name: config
            for name, config in current_config["mcp_servers"].items()
            if "tts" in name.lower()
        }

        if tts_servers:
            print(f"\n📋 Configured TTS Servers ({len(tts_servers)}):")
            for name, config in tts_servers.items():
                print(f"  • {name}")
                print(f"    Command: {config.get('command', 'N/A')}")
                print(f"    Args: {config.get('args', [])}")
                if "env" in config:
                    print(f"    Environment: {len(config['env'])} variables")
        else:
            print("\n📋 No TTS servers configured")
    else:
        print("\n📋 No configuration file found")

    # Show validation status
    validation = installer.validate_installation()
    print(f"\n🔧 Installation Status:")
    print(f"  Python: {'✅' if validation['python_available'] else '❌'}")
    print(f"  v2 Server: {'✅' if validation['v2_server_executable'] else '❌'}")
    print(f"  Dependencies: {'✅' if validation['dependencies_available'] else '❌'}")
    print(f"  Legacy: {'✅' if validation['legacy_available'] else '❌'}")

    # Show test results
    test_results = installer.test_mcp_installation()
    print(f"\n🧪 Test Results:")
    print(f"  Python Path: {'✅' if test_results['python_path_test'] else '❌'}")
    print(f"  v2 Server: {'✅' if test_results['v2_server_test'] else '❌'}")
    print(f"  Legacy Server: {'✅' if test_results['legacy_server_test'] else '❌'}")

    return 0


def cmd_generate_script(args):
    """Generate standalone installation script"""
    installer = MCPInstaller()

    print_section("Generating Installation Script")

    try:
        script_path = installer.create_installation_script(args.output)
        print_success(f"Installation script generated: {script_path}")
        print_info(f"Run: bash {script_path}")
        return 0

    except Exception as e:
        print_error(f"Script generation failed: {e}")
        return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        prog="mcp_config_tool",
        description="TTS-MacOS v2 MCP Configuration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s detect                    # Detect Claude Desktop and installation
  %(prog)s install --v2              # Install v2 server only
  %(prog)s install --v2 --legacy    # Install both v2 and legacy servers
  %(prog)s install --name my-tts    # Install with custom server name
  %(prog)s test                      # Test MCP installation
  %(prog)s status                    # Show current status
  %(prog)s uninstall --server tts-macos-v2  # Uninstall specific server
  %(prog)s generate-script --output install_mcp.sh  # Generate script
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Install command
    install_parser = subparsers.add_parser(
        "install", help="Install MCP server configuration"
    )
    install_parser.add_argument(
        "--v2", action="store_true", default=True, help="Install v2 server (default)"
    )
    install_parser.add_argument(
        "--no-v2", dest="v2", action="store_false", help="Skip v2 server"
    )
    install_parser.add_argument(
        "--legacy", action="store_true", help="Install legacy server"
    )
    install_parser.add_argument("--name", help="Custom server name")
    install_parser.add_argument("--python-path", help="Custom Python path")
    install_parser.add_argument(
        "--no-backup", action="store_true", help="Skip configuration backup"
    )
    install_parser.add_argument(
        "--merge", action="store_true", default=True, help="Merge with existing config"
    )
    install_parser.add_argument(
        "--no-merge", dest="merge", action="store_false", help="Replace existing config"
    )

    # Detect command
    detect_parser = subparsers.add_parser(
        "detect", help="Detect Claude Desktop and installation"
    )

    # Test command
    test_parser = subparsers.add_parser("test", help="Test MCP installation")

    # Uninstall command
    uninstall_parser = subparsers.add_parser(
        "uninstall", help="Uninstall MCP server configuration"
    )
    uninstall_parser.add_argument("--server", help="Specific server name to uninstall")
    uninstall_parser.add_argument(
        "--force", action="store_true", help="Skip confirmation"
    )
    uninstall_parser.add_argument(
        "--no-backup", action="store_true", help="Skip configuration backup"
    )

    # Status command
    status_parser = subparsers.add_parser(
        "status", help="Show current status and configuration"
    )

    # Generate script command
    generate_parser = subparsers.add_parser(
        "generate-script", help="Generate standalone installation script"
    )
    generate_parser.add_argument("--output", required=True, help="Output script path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    try:
        if args.command == "detect":
            return cmd_detect(args)
        elif args.command == "install":
            return cmd_install(args)
        elif args.command == "test":
            return cmd_test(args)
        elif args.command == "uninstall":
            return cmd_uninstall(args)
        elif args.command == "status":
            return cmd_status(args)
        elif args.command == "generate-script":
            return cmd_generate_script(args)
        else:
            print_error(f"Unknown command: {args.command}")
            return 1

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        return 130
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if "--debug" in sys.argv:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
