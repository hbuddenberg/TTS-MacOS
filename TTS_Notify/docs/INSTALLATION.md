# Installation Guide - TTS Notify v2.0.0

Comprehensive installation guide for TTS Notify v2.0.0 modular text-to-speech system.

## 🎯 Installation Options

### Option 1: Complete Installation (Recommended)

Installs all components: CLI, MCP server, and REST API with all dependencies.

```bash
git clone https://github.com/yourusername/tts-notify.git
cd tts-notify
./installers/install.sh all
```

### Option 2: Development Mode

Creates development environment with all dependencies and dev tools.

```bash
git clone https://github.com/yourusername/tts-notify.git
cd tts-notify
./installers/install.sh development
source venv/bin/activate
```

### Option 3: Production CLI

Installs CLI globally for system-wide usage.

```bash
git clone https://github.com/yourusername/tts-notify.git
cd tts-notify
./installers/install.sh production
```

### Option 4: MCP Server Only

Installs and configures MCP server for Claude Desktop integration.

```bash
git clone https://github.com/yourusername/tts-notify.git
cd tts-notify
./installers/install.sh mcp
```

### Option 5: UVX Mode (Quick Test)

Run without installation using UV package manager.

```bash
# Install UV if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run TTS Notify
uvx --from tts-notify tts-notify "Hello world"
```

## 📋 Platform-Specific Installers

### macOS & Linux

```bash
# Main installer (interactive menu)
./installers/install.sh

# Direct mode selection
./installers/install.sh development
./installers/install.sh production
./installers/install.sh mcp
./installers/install.sh all
```

### Windows

**Command Prompt (Batch)**
```cmd
installers\install.bat development
installers\install.bat production
installers\install.bat mcp
installers\install.bat all
```

**PowerShell**
```powershell
.\installers\install.ps1 -Mode development
.\installers\install.ps1 -Mode production
.\installers\install.ps1 -Mode mcp
.\installers\install.ps1 -Mode all
```

## 🔧 Manual Installation

### Prerequisites

#### System Requirements
- **macOS 10.14 (Mojave) or superior** - Required for `say` command
- **Linux** - Supported with appropriate TTS engine
- **Windows** - Supported with appropriate TTS engine
- **Python 3.10+** - Minimum required version

#### Python Dependencies
```bash
# Core dependencies
pip install pydantic>=2.0.0 pyyaml>=6.0

# MCP server support
pip install mcp>=1.0.0

# REST API support
pip install "fastapi>=0.104.0" "uvicorn[standard]>=0.24.0" "python-multipart>=0.0.6"

# Development dependencies
pip install "pytest>=7.0.0" "pytest-asyncio>=0.21.0" "black>=23.0.0" "isort>=5.12.0" "mypy>=1.0.0"
```

### Installation Steps

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/tts-notify.git
cd tts-notify
```

2. **Install Package**
```bash
# Development mode
pip install -e ".[dev]"

# Specific modes
pip install -e ".[mcp]"     # MCP only
pip install -e ".[api]"      # API only
pip install -e ".[all]"      # All features
```

3. **Verify Installation**
```bash
# Test CLI
python -m tts_notify "Hello world"

# Test help
python -m tts_notify --help

# Test voice detection
python -m tts_notify --list
```

## 🚀 Quick Verification

After installation, verify that everything works:

### CLI Verification
```bash
# Basic functionality
tts-notify "Installation test successful"

# Voice listing
tts-notify --list

# System information
tts-notify --info
```

### MCP Server Verification
```bash
# Start MCP server
tts-notify --mode mcp

# Should show MCP server starting up
# Claude Desktop will auto-configure if installed
```

### API Server Verification
```bash
# Start API server
tts-notify --mode api

# Test endpoints (in another terminal)
curl http://localhost:8000/status
curl http://localhost:8000/docs
```

## ⚙️ Configuration

### Environment Setup

Create configuration file:
```bash
# Default location
mkdir -p ~/.config/tts-notify
cp config/default.yaml ~/.config/tts-notify/
cp config/profiles.yaml ~/.config/tts-notify/
```

### Environment Variables

Create `.env` file:
```bash
# Voice Settings
TTS_NOTIFY_VOICE=monica
TTS_NOTIFY_RATE=175
TTS_NOTIFY_LANGUAGE=es

# Functionality
TTS_NOTIFY_ENABLED=true
TTS_NOTIFY_CACHE_ENABLED=true

# Logging
TTS_NOTIFY_LOG_LEVEL=INFO
```

## 🔍 Troubleshooting

### Common Issues

#### UV Installation Failed
```bash
# Try manual UV installation
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
```

#### Voice Not Found
```bash
# Check system voices
say -v "?"

# Verify TTS capability
python -c "
import subprocess
result = subprocess.run(['say', '-v', '?'], capture_output=True)
print('TTS available' if result.returncode == 0 else 'TTS not available')
"
```

#### MCP Server Not Connecting
```bash
# Check Claude Desktop configuration
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Restart Claude Desktop completely (Cmd+Q)
```

#### API Server Port Conflicts
```bash
# Use different port
export TTS_NOTIFY_API_PORT=8080
tts-notify --mode api

# Or kill existing processes
lsof -i :8000 | xargs kill -9
```

### Uninstallation

```bash
# Run uninstaller
./installers/install.sh uninstall

# Or manual removal
rm -rf venv ~/.config/tts-notify
# Remove MCP configuration from Claude Desktop
```

## 📖 Next Steps

After successful installation:

1. **Read [USAGE.md](USAGE.md)** - Comprehensive usage guide
2. **Read [VOICES.md](VOICES.md)** - Complete voice reference
3. **Check [CHANGELOG-v2.md](../CHANGELOG-v2.md)** - Version history

## 🤝 Getting Help

- **Issues**: https://github.com/yourusername/tts-notify/issues
- **Documentation**: https://github.com/yourusername/tts-notify#readme
- **Discussions**: https://github.com/yourusername/tts-notify/discussions

---

**TTS Notify v2.0.0** - Installation should be straightforward and error-free. If you encounter any issues, please check the troubleshooting section or create an issue on GitHub.