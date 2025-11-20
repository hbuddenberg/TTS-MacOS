"""
MCP server interface for TTS Notify v2

Model Context Protocol server integration for Claude Desktop.
"""

# Don't import at module level to avoid import issues
# Import will be done lazily when needed

def get_main():
    """Get the main function with proper error handling"""
    try:
        from .simple_server import main as simple_main
        return simple_main
    except ImportError:
        try:
            from .server import main as complex_main
            return complex_main
        except ImportError:
            raise ImportError("No MCP server implementation available")

def get_server_class():
    """Get the server class with proper error handling"""
    try:
        from .simple_server import FastMCP
        return FastMCP
    except ImportError:
        try:
            from .server import TTSNotifyMCPServer
            return TTSNotifyMCPServer
        except ImportError:
            raise ImportError("No MCP server implementation available")

__all__ = ["get_main", "get_server_class"]