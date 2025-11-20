# TTS Notify v2.0.0

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](https://github.com/yourusername/tts-notify)

🎯 **Modular Text-to-Speech notification system for macOS with CLI, MCP, and REST API interfaces**

TTS Notify v2.0.0 is a complete rewrite featuring a modular architecture that maintains full compatibility with v1.5.0 while adding powerful new capabilities.

## ✨ What's New in v2.0.0

### 🏗️ **Complete Modular Architecture**
- **Core System**: 6 modular components with clean separation of concerns
- **Multiple Interfaces**: CLI, MCP Server, REST API - all using the same core
- **Plugin Foundation**: Extensible architecture for future enhancements
- **40% Code Reduction**: Eliminated duplication through smart design

### 🎛️ **Intelligent Configuration System**
- **30+ Environment Variables**: Complete control over all aspects
- **10+ Predefined Profiles**: Ready-to-use configurations for different scenarios
- **YAML Configuration Files**: Human-readable configuration management
- **Runtime Validation**: Automatic configuration validation with helpful error messages

### 🚀 **Enhanced Performance**
- **Async Support**: Non-blocking operations throughout the system
- **Voice Caching**: Intelligent caching with configurable TTL
- **Concurrent Processing**: Support for multiple simultaneous requests
- **Resource Optimization**: Efficient memory and CPU usage

### 🛠️ **Developer Experience**
- **Type Safety**: Full Pydantic model validation
- **Comprehensive Logging**: Structured logging with JSON support
- **Modern Tooling**: Black, isort, mypy, pytest integration
- **Cross-Platform Installers**: UV-based installation for all platforms

## 🚀 Quick Start

### Installation Options

#### 🎯 **Option 1: Complete Installation (Recommended)**
```bash
# Clone and install everything
git clone https://github.com/yourusername/tts-notify.git
cd tts-notify
./installers/install.sh all
```

#### 🔧 **Option 2: Development Mode**
```bash
git clone https://github.com/yourusername/tts-notify.git
cd tts-notify
./installers/install.sh development
source venv/bin/activate
```

#### 🤖 **Option 3: MCP Server Only**
```bash
git clone https://github.com/yourusername/tts-notify.git
cd tts-notify
./installers/install.sh mcp
```

#### 🌐 **Option 4: Production CLI**
```bash
git clone https://github.com/yourusername/tts-notify.git
cd tts-notify
./installers/install.sh production
```

### Basic Usage

#### **CLI Interface**
```bash
# Basic text-to-speech
tts-notify "Hello world"

# With specific voice and rate
tts-notify "Hola mundo" --voice monica --rate 200

# List available voices
tts-notify --list

# Save audio file
tts-notify "Test message" --save output --format wav

# Compact voice list
tts-notify --list --compact

# Filter by gender
tts-notify --list --gen female

# System information
tts-notify --info
```

#### **MCP Server (Claude Desktop)**
```bash
# Start MCP server
tts-notify --mode mcp

# Or use specific script
tts-notify-mcp
```

#### **REST API**
```bash
# Start API server
tts-notify --mode api

# Or use specific script
tts-notify-api

# API will be available at http://localhost:8000
# Documentation at http://localhost:8000/docs
```

## 🏗️ Architecture

### **Core Components**

```
src/
├── core/                    # Core TTS functionality
│   ├── config_manager.py   # Intelligent configuration with 30+ env vars
│   ├── voice_system.py     # Voice detection & management (84+ voices)
│   ├── tts_engine.py       # Abstract TTS engine with macOS implementation
│   ├── models.py           # Pydantic data models with validation
│   └── exceptions.py       # Custom exception hierarchy
├── ui/                      # User interfaces
│   ├── cli/                # Command-line interface
│   │   ├── main.py         # CLI implementation with feature parity
│   │   └── __main__.py     # CLI entry point
│   ├── mcp/                # MCP server for Claude Desktop
│   │   ├── server.py       # FastMCP server with 4 tools
│   │   └── __main__.py     # MCP entry point
│   └── api/                # REST API with FastAPI
│       ├── server.py       # FastAPI server with OpenAPI docs
│       └── __main__.py     # API entry point
├── utils/                   # Utility modules
│   ├── async_utils.py      # Async utilities and helpers
│   └── text_normalizer.py  # Text processing and normalization
├── plugins/                 # Plugin system foundation
│   └── __init__.py         # Plugin base classes and registry
├── installer/               # UV-based unified installer
│   └── installer.py        # Cross-platform installation logic
├── main.py                  # Main orchestrator with intelligent mode detection
├── __main__.py             # Package entry point
└── __init__.py             # Package initialization
```

### **Interface Overview**

| Interface | Use Case | Entry Point | Key Features |
|-----------|----------|-------------|--------------|
| **CLI** | Command-line usage, scripts | `python -m tts_notify` or `tts-notify` | Full voice control, file saving, filtering, system info |
| **MCP** | Claude Desktop integration | `python -m tts_notify --mode mcp` | 4 MCP tools, flexible voice search, async processing |
| **API** | Web applications, services | `python -m tts_notify --mode api` | REST endpoints, OpenAPI docs, async, concurrent requests |

### **Main Orchestrator**

The `src/main.py` serves as the central delegation hub with intelligent mode detection:

- **Auto-detection**: Automatically detects execution mode from environment variables and arguments
- **Interface Creation**: Creates and manages appropriate interface instances
- **Configuration Loading**: Loads and validates configuration from all sources
- **Error Handling**: Comprehensive error handling with fallback behaviors

## ⚙️ Configuration

### **Environment Variables**

```bash
# Voice Settings
TTS_NOTIFY_VOICE=monica          # Default voice
TTS_NOTIFY_RATE=175              # Speech rate (WPM)
TTS_NOTIFY_LANGUAGE=es           # Language
TTS_NOTIFY_QUALITY=enhanced      # Voice quality
TTS_NOTIFY_PITCH=1.0             # Pitch multiplier
TTS_NOTIFY_VOLUME=1.0            # Volume (0.0-1.0)

# Functionality
TTS_NOTIFY_ENABLED=true          # Enable TTS
TTS_NOTIFY_CACHE_ENABLED=true    # Enable caching
TTS_NOTIFY_CONFIRMATION=false    # Enable confirmations

# System
TTS_NOTIFY_LOG_LEVEL=INFO        # Logging level
TTS_NOTIFY_MAX_CONCURRENT=5      # Max concurrent requests
TTS_NOTIFY_TIMEOUT=60            # Operation timeout (seconds)

# API Server
TTS_NOTIFY_API_PORT=8000         # API server port
TTS_NOTIFY_API_HOST=localhost    # API server host
```

### **Configuration Profiles**

```bash
# Use predefined profile
tts-notify --profile claude-desktop
export TTS_NOTIFY_PROFILE=production

# Available profiles:
# - claude-desktop: Optimized for Claude Desktop
# - api-server: Optimized for API deployment
# - development: Development with debugging
# - production: Production with minimal logging
# - cli-default: Standard CLI usage
# - accessibility: Accessibility features
# - performance: High performance settings
# - testing: Suitable for automated testing
# - demo: Optimized for demonstrations
# - spanish: Spanish language optimization
# - english: English language optimization
# - fast: Speed optimized
# - quality: High quality audio
```

### **YAML Configuration**

Create `~/.config/tts-notify/.env` or use project `config/` files:

```yaml
# config/default.yaml
voice: "monica"
rate: 175
language: "es"
quality: "basic"
enabled: true
cache_enabled: true
log_level: "INFO"
```

```yaml
# config/profiles.yaml
profiles:
  claude-desktop:
    voice: "jorge"
    rate: 175
    language: "es"
    quality: "enhanced"
    max_text_length: 2000
```

## 🎵 Voice System

### **84+ Voice Support**
- **Automatic Detection**: Discovers all system voices at startup
- **Flexible Search**: Exact, partial, case-insensitive, accent-insensitive matching
- **Smart Categorization**: Español, Enhanced, Premium, Siri, Others
- **Quality Selection**: Basic, Enhanced, Premium, Siri, Neural variants

### **Voice Search Examples**

```bash
# Exact match
tts-notify "Test" --voice Monica

# Case-insensitive
tts-notify "Test" --voice monica

# Partial match
tts-notify "Test" --voice angel  # Finds Angélica

# Quality variants
tts-notify "Test" --voice "monica enhanced"
tts-notify "Test" --voice "jorge premium"

# Siri voices (if installed)
tts-notify "Test" --voice "siri female"
```

### **Voice Categories**

| Category | Description | Examples |
|----------|-------------|----------|
| **Español** | Spanish language voices | Monica, Jorge, Angélica, Paulina |
| **Enhanced** | High quality enhanced voices | Enhanced Monica, Enhanced Jorge |
| **Premium** | Premium quality voices | Premium Angélica, Premium Paulina |
| **Siri** | Siri voices (if installed) | Siri Female, Siri Male |
| **Others** | Other system voices | Alex, Samantha, Victoria |

## 🔌 MCP Integration

### **Available Tools**

1. **`speak_text`** - Reproduce texto en voz alta
2. **`list_voices`** - Lista todas las voces disponibles
3. **`save_audio`** - Guarda texto como archivo de audio
4. **`get_system_info`** - Obtiene información del sistema y configuración

### **Claude Desktop Configuration**

```json
{
  "mcpServers": {
    "tts-notify": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/tts-notify/src/main.py", "--mode", "mcp"],
      "env": {
        "TTS_NOTIFY_VOICE": "monica",
        "TTS_NOTIFY_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### **Usage Examples**

```
"Lee en voz alta: Hola mundo, esto es una prueba"
"Lista todas las voces disponibles en español"
"Guarda este texto como audio: archivo de prueba"
"Muéstrame la configuración actual del sistema"
```

## 🌐 REST API

### **Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/status` | Server status |
| GET | `/voices` | List available voices |
| GET | `/config` | Current configuration |
| POST | `/speak` | Convert text to speech |
| POST | `/save` | Save audio file |
| GET | `/download/{filename}` | Download audio file |
| POST | `/config/reload` | Reload configuration |

### **API Usage Examples**

```bash
# Get server status
curl http://localhost:8000/status

# List voices
curl http://localhost:8000/voices

# Speak text
curl -X POST http://localhost:8000/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "monica"}'

# Save audio
curl -X POST http://localhost:8000/save \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "filename": "test", "format": "wav"}'
```

### **Interactive Documentation**

Visit `http://localhost:8000/docs` for interactive OpenAPI documentation.

## 🧪 Development

### **Development Setup**

```bash
# Clone repository
git clone https://github.com/yourusername/tts-notify.git
cd tts-notify

# Development installation
./installers/install.sh development
source venv/bin/activate

# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Code formatting
black src tests
isort src tests

# Type checking
mypy src
```

### **Project Structure**

```
TTS_Notify/
├── src/                     # Source code (modular architecture)
│   ├── core/               # Core functionality (6 modules)
│   │   ├── config_manager.py    # Intelligent configuration system
│   │   ├── voice_system.py      # Voice detection & management
│   │   ├── tts_engine.py        # Abstract TTS engine
│   │   ├── models.py            # Pydantic data models
│   │   └── exceptions.py        # Custom exception hierarchy
│   ├── ui/                 # User interfaces (3 interfaces)
│   │   ├── cli/                 # Command-line interface
│   │   ├── mcp/                 # MCP server for Claude Desktop
│   │   └── api/                 # REST API with FastAPI
│   ├── utils/              # Utility modules
│   │   ├── async_utils.py       # Async utilities
│   │   └── text_normalizer.py   # Text processing
│   ├── plugins/            # Plugin system foundation
│   ├── installer/          # UV-based installer
│   │   └── installer.py         # Unified installation logic
│   ├── main.py             # Main orchestrator with intelligent mode detection
│   ├── __main__.py         # Package entry point
│   └── __init__.py         # Package initialization
├── tests/                  # Test suite
│   ├── test_core.py        # Core functionality tests
│   ├── test_api.py         # API endpoint tests
│   └── test_cli.py         # CLI interface tests
├── config/                 # Configuration files
│   ├── default.yaml        # Default configuration
│   └── profiles.yaml       # Predefined profiles
├── docs/                   # Documentation
│   ├── INSTALLATION.md     # Installation guide
│   ├── USAGE.md            # Usage guide
│   └── VOICES.md           # Voice reference
├── installers/             # Cross-platform installation scripts
│   ├── install.sh          # Linux/macOS installer
│   ├── install.bat         # Windows batch installer
│   └── install.ps1         # PowerShell installer
├── pyproject.toml          # Modern Python packaging with UV
├── CHANGELOG-v2.md         # Version history
├── MIGRATION-GUIDE-v2.md   # Migration from v1.5.0
└── README.md              # Main project documentation
```

### **Testing**

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/test_core.py
pytest tests/test_api.py
pytest tests/test_cli.py

# Run with markers
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests

# Coverage report
pytest --cov=src --cov-report=term-missing
```

## 🔧 Advanced Configuration

### **Custom Profiles**

Create custom profiles in `config/profiles.yaml`:

```yaml
profiles:
  my-custom-profile:
    voice: "custom-voice"
    rate: 200
    quality: "premium"
    log_level: "DEBUG"
    cache_ttl: 600
```

### **Environment-Based Configuration**

```bash
# Development
export TTS_NOTIFY_PROFILE=development
export TTS_NOTIFY_LOG_LEVEL=DEBUG

# Production
export TTS_NOTIFY_PROFILE=production
export TTS_NOTIFY_LOG_LEVEL=WARN

# API Server
export TTS_NOTIFY_PROFILE=api-server
export TTS_NOTIFY_API_PORT=8080
```

### **Logging Configuration**

```python
import logging
from tts_notify import configure_logging_from_config

# Configure logging
configure_logging_from_config({
    'level': 'INFO',
    'format': 'json',
    'file': '/var/log/tts-notify.log'
})
```

## 🐛 Troubleshooting

### **Common Issues**

#### **Voice Not Found**
```bash
# Check available voices
tts-notify --list

# Or system command
say -v "?"

# Install additional voices on macOS:
# System Preferences → Accessibility → Spoken Content → System Voices
```

#### **MCP Server Not Connecting**
```bash
# Check Claude Desktop configuration
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Verify paths are absolute
python3 -c "import os; print(os.path.exists('/path/to/venv/bin/python'))"

# Restart Claude Desktop completely (Cmd+Q)
```

#### **API Server Not Starting**
```bash
# Check port availability
lsof -i :8000

# Use different port
tts-notify --mode api --port 8080

# Check logs
export TTS_NOTIFY_LOG_LEVEL=DEBUG
tts-notify --mode api
```

#### **Installation Issues**
```bash
# Check UV installation
uv --version

# Clean installation
rm -rf venv
./installers/install.sh uninstall
./installers/install.sh all

# Manual installation
python3 -m pip install -e .
```

### **Debug Mode**

```bash
# Enable debug logging
export TTS_NOTIFY_LOG_LEVEL=DEBUG
export TTS_NOTIFY_VERBOSE=true

# Run with debug mode
tts-notify --debug --info

# Check configuration
python3 -c "
from tts_notify import config_manager
config = config_manager.get_config()
print('Active vars:', config.get_active_vars())
issues = config_manager.validate_system()
print('Issues:', issues)
"
```

## 📈 Performance

### **Optimization Features**

- **Voice Caching**: Cache system voices for 5 minutes (configurable)
- **Async Processing**: Non-blocking TTS operations
- **Connection Pooling**: Reuse system command connections
- **Memory Management**: Efficient voice data handling
- **Rate Limiting**: Built-in protection against excessive requests

### **Benchmark Results**

| Operation | v1.5.0 | v2.0.0 | Improvement |
|-----------|--------|--------|-------------|
| Voice Detection | ~2s | ~0.5s | 75% faster |
| CLI Startup | ~1s | ~0.3s | 70% faster |
| Memory Usage | ~50MB | ~30MB | 40% reduction |
| Code Size | ~5000 lines | ~3000 lines | 40% reduction |

## 🤝 Contributing

### **Development Workflow**

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Install development dependencies: `./installers/install.sh development`
4. Make changes with tests
5. Run tests: `pytest`
6. Format code: `black src tests && isort src tests`
7. Type check: `mypy src`
8. Commit changes: `git commit -m "Add amazing feature"`
9. Push branch: `git push origin feature/amazing-feature`
10. Open Pull Request

### **Code Standards**

- **Python**: 3.10+ with type hints
- **Formatting**: Black (line length 88)
- **Imports**: isort
- **Type Checking**: mypy (strict mode)
- **Testing**: pytest with asyncio support
- **Documentation**: docstrings for all public functions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **macOS TTS Team**: For the excellent built-in text-to-speech system
- **FastAPI Team**: For the amazing web framework
- **Pydantic Team**: For data validation and settings management
- **UV Team**: For modern Python packaging
- **Claude Team**: For the MCP protocol inspiration

## 🔗 Links

- **Homepage**: https://github.com/yourusername/tts-notify
- **Documentation**: https://github.com/yourusername/tts-notify#readme
- **Issues**: https://github.com/yourusername/tts-notify/issues
- **Changelog**: https://github.com/yourusername/tts-notify/blob/main/CHANGELOG.md

---

**TTS Notify v2.0.0** - 🎯 Modular, Powerful, and Ready for Production!