#!/bin/bash

# TTS-MacOS v2 - MCP Configuration Generator
# Generates ready-to-use JSON configuration for Claude Desktop

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 TTS-MacOS v2 - MCP Configuration Generator${NC}"
echo "=================================================="

# Get current script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_DIR="$SCRIPT_DIR/venv-v2"

# Check if we're in the right directory
if [ ! -f "mcp_server_v2" ]; then
    echo -e "${RED}❌ Error: Please run this script from the TTS-MacOS v2 directory${NC}"
    echo "Expected files: mcp_server_v2, v2/ directory"
    exit 1
fi

# Detect platform
PLATFORM=$(uname)
echo -e "${CYAN}🖥️  Platform:${NC} $PLATFORM"

# Resolve Python path
if [ -f "$VENV_DIR/bin/python" ]; then
    PYTHON_PATH="$VENV_DIR/bin/python"
    echo -e "${GREEN}✅ Virtual environment Python found:${NC} $PYTHON_PATH"
elif command -v python3 &> /dev/null; then
    PYTHON_PATH="$(command -v python3)"
    echo -e "${YELLOW}⚠️  Using system Python (venv not found):${NC} $PYTHON_PATH"
    echo -e "${YELLOW}💡 Run ./install.sh first to create virtual environment${NC}"
else
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

# Resolve Claude Desktop config directory
if [ "$PLATFORM" = "Darwin" ]; then
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    echo -e "${CYAN}🍎 macOS detected${NC}"
elif [ "$PLATFORM" = "Linux" ]; then
    CLAUDE_CONFIG_DIR="$HOME/.config/claude"
    echo -e "${CYAN}🐧 Linux detected${NC}"
else
    echo -e "${RED}❌ Unsupported platform: $PLATFORM${NC}"
    exit 1
fi

echo -e "${CYAN}📂 Claude Desktop config directory:${NC} $CLAUDE_CONFIG_DIR"

# Check if Claude Desktop directory exists
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    echo -e "${YELLOW}⚠️  Claude Desktop config directory not found${NC}"
    echo -e "${YELLOW}💡 Please install and run Claude Desktop once to create it${NC}"
    echo ""
    echo "The JSON configuration below will still work once Claude Desktop is installed."
    echo ""
fi

# Resolve server paths
V2_SERVER_PATH="$SCRIPT_DIR/mcp_server_v2"
LEGACY_SERVER_PATH="$SCRIPT_DIR/legacy/server.py"

# Check server files
echo -e "${BLUE}🔍 Checking server files...${NC}"

if [ -f "$V2_SERVER_PATH" ]; then
    echo -e "${GREEN}✅ v2 server found:${NC} $V2_SERVER_PATH"
else
    echo -e "${RED}❌ v2 server not found:${NC} $V2_SERVER_PATH"
    exit 1
fi

if [ -f "$LEGACY_SERVER_PATH" ]; then
    echo -e "${GREEN}✅ Legacy server found:${NC} $LEGACY_SERVER_PATH"
    LEGACY_AVAILABLE=true
else
    echo -e "${YELLOW}⚠️  Legacy server not found:${NC} $LEGACY_SERVER_PATH"
    LEGACY_AVAILABLE=false
fi

# Make servers executable
chmod +x "$V2_SERVER_PATH"
if [ "$LEGACY_AVAILABLE" = true ]; then
    chmod +x "$LEGACY_SERVER_PATH"
fi

echo ""
echo -e "${BLUE}📝 Generating MCP Configuration JSON${NC}"
echo "========================================"

# Generate JSON configuration
echo -e "${CYAN}🎯 For claude_desktop_config.json:${NC}"
echo ""

cat << 'EOF'
{
  "mcpServers": {
EOF

# v2 server configuration
echo "    \"tts-macos-v2\": {"
echo "      \"command\": \"$PYTHON_PATH\","
echo "      \"args\": [\"$V2_SERVER_PATH\"],"
echo "      \"env\": {"
echo "        \"PYTHONPATH\": \"$SCRIPT_DIR\","
echo "        \"TTS_MACOS_V2\": \"1\""
echo "      }"
echo "    }"

# Add legacy server if available
if [ "$LEGACY_AVAILABLE" = true ]; then
    echo "    },"
    echo "    \"tts-macos-legacy\": {"
    echo "      \"command\": \"$PYTHON_PATH\","
    echo "      \"args\": [\"$LEGACY_SERVER_PATH\", \"--legacy\"],"
    echo "      \"env\": {"
    echo "        \"PYTHONPATH\": \"$SCRIPT_DIR/legacy\","
    echo "        \"TTS_MACOS_LEGACY\": \"1\""
    echo "      }"
    echo "    }"
else
    echo ""
fi

cat << 'EOF'
  }
}
EOF

echo ""
echo -e "${BLUE}📋 Installation Instructions${NC}"
echo "==============================="

if [ -d "$CLAUDE_CONFIG_DIR" ]; then
    echo -e "${GREEN}1. Auto-Installation (Recommended):${NC}"
    echo "   ./mcp-config install --v2"
    if [ "$LEGACY_AVAILABLE" = true ]; then
        echo "   ./mcp-config install --v2 --legacy"
    fi
    echo ""
fi

echo -e "${GREEN}2. Manual Installation:${NC}"
echo "   a) Copy the JSON above"
echo "   b) Open: $CLAUDE_CONFIG_DIR/claude_desktop_config.json"
echo "   c) Paste the JSON configuration"
echo "   d) Save the file"
echo "   e) Restart Claude Desktop completely"

echo ""
echo -e "${GREEN}3. Alternative - Use MCP Config Tool:${NC}"
echo "   ./mcp-config install --v2 --name 'my-tts-server'"

echo ""
echo -e "${BLUE}🧪 Testing Configuration${NC}"
echo "========================"

echo -e "${CYAN}Test installation:${NC}"
echo "  ./mcp-config detect"
echo "  ./mcp-config test"

echo ""
echo -e "${CYAN}Test in Claude Desktop (after restart):${NC}"
echo "  • Type: 'List available tools'"
echo "  • Try: tts_speak(text='Hello from TTS-MacOS v2!')"

echo ""
echo -e "${BLUE}📁 File Locations${NC}"
echo "=================="
echo -e "${CYAN}Script directory:${NC}     $SCRIPT_DIR"
echo -e "${CYAN}Virtual environment:${NC}  $VENV_DIR"
echo -e "${CYAN}Python executable:${NC}    $PYTHON_PATH"
echo -e "${CYAN}v2 server:${NC}           $V2_SERVER_PATH"
if [ "$LEGACY_AVAILABLE" = true ]; then
    echo -e "${CYAN}Legacy server:${NC}        $LEGACY_SERVER_PATH"
fi
echo -e "${CYAN}Claude config:${NC}        $CLAUDE_CONFIG_DIR/claude_desktop_config.json"

echo ""
echo -e "${BLUE}🔧 Available Commands${NC}"
echo "===================="
echo -e "${CYAN}• Full installation:${NC}     ./install.sh"
echo -e "${CYAN}• MCP management:${NC}        ./mcp-config"
echo -e "${CYAN}• CLI testing:${NC}           ./tts-macos-v2 --help"
echo -e "${CYAN}• Demo:${NC}                  ./demo.sh"

echo ""
echo -e "${GREEN}🎉 Configuration ready!${NC}"
echo "========================"
echo -e "${YELLOW}💡 Tips:${NC}"
echo "  • Restart Claude Desktop completely after configuration"
echo "  • Use 'tts_speak' in Claude to test TTS functionality"
echo "  • Try voice cloning with 'tts_clone' if you have audio samples"
echo "  • Use 'tts_list_voices' to see all available voices"

echo ""
echo -e "${BLUE}✨ TTS-MacOS v2 MCP Configuration Complete! 🎤${NC}"
