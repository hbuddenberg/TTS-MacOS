#!/bin/bash

# TTS-MacOS v2 - Enhanced Installation Script with MCP Configuration
# Supports macOS and Linux with automatic Claude Desktop configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_NAME="tts-macos-v2"
VENV_NAME="venv-v2"

echo -e "${BLUE}🚀 TTS-MacOS v2 - Complete Installation with MCP Configuration${NC}"
echo "=========================================================================="

# Interactive mode prompt
INTERACTIVE_MODE=true
if [ "$1" = "--non-interactive" ]; then
    INTERACTIVE_MODE=false
    echo -e "${CYAN}🤖 Running in non-interactive mode${NC}"
fi

ask_yes_no() {
    if [ "$INTERACTIVE_MODE" = false ]; then
        # Default to yes in non-interactive mode
        return 0
    fi

    local prompt="$1"
    local default="${2:-N}"

    while true; do
        if [ "$default" = "Y" ]; then
            read -p "$prompt [Y/n]: " -r response
            case "$response" in
                [nN][oO]|[nN]) return 1 ;;
                ""|[yY]|[yY][eE][sS]) return 0 ;;
            esac
        else
            read -p "$prompt [y/N]: " -r response
            case "$response" in
                [yY]|[yY][eE][sS]) return 0 ;;
                ""|[nN][oO]|[nN]) return 1 ;;
            esac
        fi
    done
}

# Detect platform
PLATFORM=$(uname)
ARCH=$(uname -m)

echo -e "${BLUE}🖥️  Platform detected:${NC} $PLATFORM ($ARCH)"

# Check Python availability
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 is required but not installed${NC}"
    if [ "$PLATFORM" = "Darwin" ]; then
        echo "Install with: brew install python3"
    elif [ "$PLATFORM" = "Linux" ]; then
        echo "Install with: sudo apt-get install python3 python3-pip python3-venv"
    fi
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${BLUE}🐍 Python version:${NC} $PYTHON_VERSION"

# Check minimum Python version (3.8+)
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${GREEN}✅ Python version is compatible${NC}"
else
    echo -e "${RED}❌ Error: Python 3.8+ is required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

# Platform-specific setup
echo -e "${BLUE}🔧 Setting up platform-specific dependencies...${NC}"

if [ "$PLATFORM" = "Darwin" ]; then
    # macOS setup
    echo -e "${YELLOW}🍎 macOS detected${NC}"

    # Check for Homebrew
    if ! command -v brew &> /dev/null; then
        if ask_yes_no "Homebrew not found. Install it?" "Y"; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        else
            echo -e "${YELLOW}⚠️  Homebrew is required for macOS dependencies${NC}"
            exit 1
        fi
    fi

    # Install macOS dependencies
    echo "Installing macOS dependencies..."
    brew install libsndfile pkg-config

    # Check for Xcode Command Line Tools
    if ! xcode-select -p &> /dev/null; then
        echo "Installing Xcode Command Line Tools..."
        xcode-select --install
    fi

elif [ "$PLATFORM" = "Linux" ]; then
    # Linux setup
    echo -e "${YELLOW}🐧 Linux detected${NC}"

    # Detect Linux distribution
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        echo "Detected Debian/Ubuntu-based distribution"

        # Update package list
        sudo apt-get update

        # Install system dependencies
        echo "Installing system dependencies..."
        sudo apt-get install -y \
            python3-dev \
            python3-pip \
            python3-venv \
            libsndfile1 \
            espeak-ng \
            espeak \
            portaudio19-dev \
            python3-pyaudio \
            build-essential \
            git \
            wget \
            curl

    elif [ -f /etc/redhat-release ]; then
        # RHEL/CentOS/Fedora
        echo "Detected Red Hat-based distribution"

        # Install system dependencies
        echo "Installing system dependencies..."
        sudo yum install -y \
            python3-devel \
            python3-pip \
            libsndfile \
            espeak-ng \
            portaudio-devel \
            gcc \
            gcc-c++ \
            make \
            git \
            wget \
            curl

    elif [ -f /etc/arch-release ]; then
        # Arch Linux
        echo "Detected Arch Linux"

        # Install system dependencies
        echo "Installing system dependencies..."
        sudo pacman -S --needed \
            python \
            python-pip \
            libsndfile \
            espeak-ng \
            portaudio \
            base-devel \
            git \
            wget \
            curl
    else
        echo -e "${YELLOW}⚠️  Unknown Linux distribution. Manual dependency installation may be required.${NC}"
        echo "Please install: python3-dev, python3-pip, libsndfile1, espeak-ng"
    fi

    # Check for CUDA (optional)
    if command -v nvidia-smi &> /dev/null; then
        echo -e "${GREEN}🔥 NVIDIA GPU detected - CUDA acceleration available${NC}"
        nvidia-smi --query-gpu=name,driver_version --format=csv,noheader,nounits
    else
        echo -e "${YELLOW}⚠️  No NVIDIA GPU detected - will use CPU inference${NC}"
    fi
else
    echo -e "${RED}❌ Unsupported platform: $PLATFORM${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${BLUE}📦 Creating Python virtual environment...${NC}"

if [ -d "$VENV_NAME" ]; then
    if ask_yes_no "Virtual environment already exists. Recreate it?"; then
        echo -e "${YELLOW}⚠️  Removing existing virtual environment...${NC}"
        rm -rf "$VENV_NAME"
    else
        echo -e "${YELLOW}⚠️  Using existing virtual environment${NC}"
    fi
fi

if [ ! -d "$VENV_NAME" ]; then
    python3 -m venv "$VENV_NAME"
fi

# Activate virtual environment
echo -e "${BLUE}🔌 Activating virtual environment...${NC}"
source "$VENV_NAME/bin/activate"

# Upgrade pip and install wheel
echo "Upgrading pip and installing wheel..."
python -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo -e "${BLUE}📚 Installing Python dependencies...${NC}"

# Core dependencies
echo "Installing core dependencies..."
pip install mcp>=1.0.0 fastmcp>=0.2.0 pydantic>=2.0.0

# Audio processing dependencies
echo "Installing audio processing dependencies..."
pip install soundfile>=0.12.0 librosa>=0.10.0

# TTS dependencies (will install torch as dependency)
echo "Installing TTS engine..."
pip install TTS>=0.22.0

# Optional NLP dependencies for smart features
echo "Installing NLP dependencies for smart features..."
pip install langdetect textblob || echo -e "${YELLOW}⚠️  NLP dependencies failed to install (optional)${NC}"

# GPU acceleration (optional)
if [ "$PLATFORM" = "Linux" ] && command -v nvidia-smi &> /dev/null; then
    if ask_yes_no "Install GPU acceleration for NVIDIA GPUs?" "Y"; then
        echo -e "${YELLOW}🔥 Installing GPU acceleration...${NC}"
        pip install torch-audio --index-url https://download.pytorch.org/whl/cu118 || echo -e "${YELLOW}⚠️  GPU acceleration installation failed${NC}"
    else
        echo -e "${YELLOW}💭 CPU-only version installed${NC}"
    fi
else
    echo -e "${YELLOW}💭 CPU-only version installed (GPU not detected or not on Linux)${NC}"
fi

# Test installation
echo -e "${BLUE}🧪 Testing installation...${NC}"

python -c "
import sys
import importlib

# Test core dependencies
modules_to_test = [
    ('mcp', 'MCP Framework'),
    ('fastmcp', 'FastMCP'),
    ('pydantic', 'Pydantic'),
    ('torch', 'PyTorch'),
    ('soundfile', 'SoundFile'),
    ('librosa', 'Librosa')
]

failed_modules = []
for module, name in modules_to_test:
    try:
        importlib.import_module(module)
        print(f'✅ {name}')
    except ImportError as e:
        print(f'❌ {name}: {e}')
        failed_modules.append(name)

# Test TTS
try:
    import TTS
    print('✅ Coqui TTS')

    # Check device availability
    import torch
    if torch.cuda.is_available():
        print(f'🔥 CUDA available: {torch.cuda.get_device_name(0)}')
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        print('🍎 Metal (Apple Silicon) available')
    else:
        print('💭 CPU inference only')

except ImportError as e:
    print(f'❌ Coqui TTS: {e}')
    failed_modules.append('Coqui TTS')

if failed_modules:
    print(f'\\n⚠️  Some modules failed to install: {failed_modules}')
    sys.exit(1)
else:
    print('\\n🎉 All dependencies installed successfully!')
"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Installation test failed${NC}"
    exit 1
fi

# Create activation script
cat > activate-tts-v2.sh << 'EOF'
#!/bin/bash
# TTS-MacOS v2 Environment Activation Script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "$SCRIPT_DIR/venv-v2/bin/activate"
echo "🎯 TTS-MacOS v2 environment activated!"
echo "🐍 Python: $(python --version)"
echo "🔧 To test: python -c 'from v2.engines import EngineSelector; print(\"TTS-MacOS v2 ready!\")'"
EOF

chmod +x activate-tts-v2.sh

# Create CLI launcher
cat > tts-macos-v2 << 'EOF'
#!/bin/bash
# TTS-MacOS v2 CLI Launcher
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "$SCRIPT_DIR/venv-v2/bin/activate"
cd "$SCRIPT_DIR"
python -m v2.cli.main "$@"
EOF

chmod +x tts-macos-v2

# Create MCP server launcher
cat > mcp-server-v2 << 'EOF'
#!/bin/bash
# TTS-MacOS v2 MCP Server Launcher
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "$SCRIPT_DIR/venv-v2/bin/activate"
cd "$SCRIPT_DIR"
python mcp_server_v2.py "$@"
EOF

chmod +x mcp-server-v2

# Create MCP configuration tool launcher
cat > mcp-config << 'EOF'
#!/bin/bash
# TTS-MacOS v2 MCP Configuration Tool
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "$SCRIPT_DIR/venv-v2/bin/activate"
cd "$SCRIPT_DIR"
python mcp_config_tool.py "$@"
EOF

chmod +x mcp-config

# === MCP Configuration Installation ===
echo -e "${PURPLE}🔧 Claude Desktop MCP Configuration${NC}"
echo "========================================="

# Check if user wants to install MCP configuration
if ask_yes_no "Install TTS-MacOS v2 MCP server in Claude Desktop?" "Y"; then

    echo -e "${BLUE}🔍 Detecting Claude Desktop installation...${NC}"

    # Detect Claude Desktop
    CLAUDE_CONFIG_DIR=""
    if [ "$PLATFORM" = "Darwin" ]; then
        CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    elif [ "$PLATFORM" = "Linux" ]; then
        CLAUDE_CONFIG_DIR="$HOME/.config/claude"
    fi

    if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
        echo -e "${RED}❌ Claude Desktop not found${NC}"
        echo -e "${YELLOW}Please install Claude Desktop and run it once to create configuration directory${NC}"
    else
        echo -e "${GREEN}✅ Claude Desktop configuration found: $CLAUDE_CONFIG_DIR${NC}"

        # Check if user wants legacy server too
        INSTALL_LEGACY=false
        if [ -f "legacy/server.py" ]; then
            if ask_yes_no "Also install legacy v1.x server for compatibility?" "Y"; then
                INSTALL_LEGACY=true
                echo -e "${YELLOW}🔄 Will install both v2 and legacy servers${NC}"
            fi
        fi

        # Backup existing configuration
        CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
        if [ -f "$CONFIG_FILE" ]; then
            BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
            cp "$CONFIG_FILE" "$BACKUP_FILE"
            echo -e "${YELLOW}⚠️  Existing configuration backed up: $BACKUP_FILE${NC}"
        fi

        # Create configuration directory if it doesn't exist
        mkdir -p "$CLAUDE_CONFIG_DIR"

        # Generate new configuration
        SERVER_PATH="$SCRIPT_DIR/mcp-server-v2"
        PYTHON_PATH="$SCRIPT_DIR/$VENV_NAME/bin/python"

        echo -e "${BLUE}📝 Generating Claude Desktop configuration...${NC}"

        cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "tts-macos-v2": {
      "command": "$PYTHON_PATH",
      "args": ["$SERVER_PATH"],
      "env": {
        "PYTHONPATH": "$SCRIPT_DIR",
        "TTS_MACOS_V2": "1"
      }
EOF

        # Add legacy server if requested
        if [ "$INSTALL_LEGACY" = true ]; then
            LEGACY_SERVER_PATH="$SCRIPT_DIR/legacy/server.py"
            cat >> "$CONFIG_FILE" << EOF
    },
    "tts-macos-legacy": {
      "command": "$PYTHON_PATH",
      "args": ["$LEGACY_SERVER_PATH", "--legacy"],
      "env": {
        "PYTHONPATH": "$SCRIPT_DIR/legacy",
        "TTS_MACOS_LEGACY": "1"
      }
EOF
        fi

        cat >> "$CONFIG_FILE" << EOF
    }
  }
}
EOF

        echo -e "${GREEN}✅ Claude Desktop configuration updated${NC}"

        if [ "$INSTALL_LEGACY" = true ]; then
            echo -e "${GREEN}✅ Both v2 and legacy MCP servers installed${NC}"
            echo -e "${BLUE}📋 Installed servers:${NC}"
            echo -e "${CYAN}  • tts-macos-v2${NC}: Full v2.0 features with AI voices and cloning"
            echo -e "${CYAN}  • tts-macos-legacy${NC}: v1.x compatibility mode"
        else
            echo -e "${GREEN}✅ v2 MCP server installed${NC}"
            echo -e "${BLUE}📋 Server: tts-macos-v2 (full v2.0 features)${NC}"
        fi

        echo -e "${PURPLE}🔄 Next steps:${NC}"
        echo "  1. ${YELLOW}Restart Claude Desktop completely${NC} (Cmd+Q on macOS)"
        echo "  2. Test with: 'List available tools' in Claude"
        echo "  3. Try: tts_speak(text='Hello from TTS-MacOS v2!')"
    fi
else
    echo -e "${YELLOW}⚠️  MCP configuration skipped${NC}"
    echo -e "${BLUE}💡 You can configure it later with:${NC}"
    echo "  ./mcp-config install --v2"
fi

# Test the installation
echo -e "${BLUE}🧪 Testing TTS-MacOS v2 installation...${NC}"

python -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')

try:
    from v2.engines import EngineSelector
    print('✅ Engine selector works')

    from v2.core.config import TTSConfig
    print('✅ Configuration system works')

    from v2.cli.main import EnhancedCLI
    print('✅ Enhanced CLI works')

    print('\\n🎉 TTS-MacOS v2 installation successful!')

except Exception as e:
    print(f'❌ Installation test failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Installation test failed${NC}"
    exit 1
fi

# Installation complete
echo ""
echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
echo ""
echo -e "${BLUE}📋 Quick Start:${NC}"
echo "1. Activate environment:"
echo "   source activate-tts-v2.sh"
echo ""
echo "2. Test the system:"
echo "   python -c 'from v2.engines import EngineSelector; print(\"TTS-MacOS v2 ready!\")'"
echo ""
echo "3. Start MCP server:"
echo "   ./mcp-server-v2"
echo ""
echo "4. Use CLI:"
echo "   ./tts-macos-v2 --help"
echo ""
echo "5. Configure MCP (if skipped during installation):"
echo "   ./mcp-config install --v2"
echo ""
echo "6. Run demo:"
echo "   ./demo.sh"
echo ""
echo -e "${BLUE}📁 Installation location:${NC} $SCRIPT_DIR"
echo -e "${BLUE}🔧 Virtual environment:${NC} $VENV_NAME"
echo -e "${BLUE}⚙️  Claude Desktop config:${NC} ${CLAUDE_CONFIG_DIR:-'Not installed'}"
echo ""
echo -e "${GREEN}✨ TTS-MacOS v2 is ready to use!${NC}"

# Create summary information
cat > INSTALLATION_SUMMARY.md << EOF
# TTS-MacOS v2 Installation Summary

## Installation Details
- **Platform**: $PLATFORM ($ARCH)
- **Python**: $PYTHON_VERSION
- **Location**: $SCRIPT_DIR
- **Virtual Environment**: $VENV_NAME

## Installed Components
- ✅ Core TTS engines (Native + AI)
- ✅ Enhanced CLI with dual-engine support
- ✅ Legacy compatibility layer
- ✅ MCP server for Claude Desktop
- ✅ Configuration management tools

## MCP Configuration
EOF

if [ -f "$CLAUDE_CONFIG_DIR/claude_desktop_config.json" ]; then
    cat >> INSTALLATION_SUMMARY.md << EOF
- ✅ Claude Desktop configured
- 📂 Config file: $CLAUDE_CONFIG_DIR/claude_desktop_config.json
EOF
else
    cat >> INSTALLATION_SUMMARY.md << EOF
- ❌ Claude Desktop not configured
- 💡 Run: ./mcp-config install --v2
EOF
fi

cat >> INSTALLATION_SUMMARY.md << EOF

## Next Steps
1. Restart Claude Desktop (if MCP was configured)
2. Test with: ./demo.sh
3. Read documentation: README.md
4. See migration guide: MIGRATION.md

## Troubleshooting
- Issues? Check: ./mcp-config detect
- Test: ./mcp-config test
- Status: ./mcp-config status

Generated: $(date)
EOF

echo -e "${BLUE}📄 Installation summary created: INSTALLATION_SUMMARY.md${NC}"

# Optional: Add to PATH
if ask_yes_no "Would you like to add TTS-MacOS v2 to your PATH?" "N"; then
    SHELL_RC="$HOME/.bashrc"
    if [ "$SHELL" = "/bin/zsh" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ "$SHELL" = "/bin/fish" ]; then
        SHELL_RC="$HOME/.config/fish/config.fish"
    fi

    echo "" >> "$SHELL_RC"
    echo "# TTS-MacOS v2" >> "$SHELL_RC"
    echo "export PATH=\"\$PATH:$SCRIPT_DIR\"" >> "$SHELL_RC"

    echo -e "${GREEN}✅ Added to PATH in $SHELL_RC${NC}"
    echo -e "${YELLOW}💡 Run 'source $SHELL_RC' or restart your terminal to use${NC}"
fi

# Create install-mcp command for quick JSON generation
cat > install-mcp << 'EOF'
#!/bin/bash
# TTS-MacOS v2 - Quick MCP JSON Generator
# Generates ready-to-use JSON configuration for Claude Desktop

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🔧 TTS-MacOS v2 - MCP JSON Generator${NC}"
echo "========================================="

if [ -f "generate_mcp_json.py" ]; then
    source "$VENV_NAME/bin/activate" 2>/dev/null || true
    python generate_mcp_json.py --v2 --legacy --pretty "$@"
else
    echo "❌ Error: generate_mcp_json.py not found"
    echo "💡 Please run the main installation first"
    exit 1
fi
EOF

chmod +x install-mcp
echo -e "${GREEN}✅ Created install-mcp command for quick JSON generation${NC}"
echo -e "${CYAN}💡 Usage: ./install-mcp --help${NC}"

echo ""
echo -e "${BLUE}📚 For more information:${NC}"
echo "   - 📖 Documentation: README.md"
echo "   - 🔄 Migration guide: MIGRATION.md"
echo "   - 🎭 Demo: ./demo.sh"
echo "   - ⚙️  MCP config: ./mcp-config --help"
echo "   - 🔧 Quick MCP JSON: ./install-mcp"
echo ""
echo -e "${PURPLE}🎉 Thank you for installing TTS-MacOS v2! 🎤✨${NC}"
