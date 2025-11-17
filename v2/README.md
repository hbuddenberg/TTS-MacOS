# TTS-MacOS v2 - Dual-Engine Text-to-Speech System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/tts-macos/tts-macos-v2)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)

## 🎯 Overview

TTS-MacOS v2 is a revolutionary text-to-speech system that combines the speed of native OS TTS with the quality of AI-powered voice synthesis. Featuring dual-engine architecture, voice cloning capabilities, and cross-platform support.

### ✨ Key Features

- **🔧 Dual-Engine Architecture**: Native OS TTS + AI Coqui TTS
- **🎭 Voice Cloning**: Create custom voices from 6-second audio samples  
- **🌍 Multi-Language**: 16+ languages with native quality
- **💻 Cross-Platform**: macOS and Linux support
- **🤖 Intelligent Selection**: Automatic engine and voice optimization
- **⚡ High Performance**: Smart caching and GPU acceleration
- **🔄 Backward Compatible**: 100% compatible with TTS-MacOS v1.x

## 🚀 Quick Start

### Installation

```bash
# Clone or download TTS-MacOS v2
cd tts-macos-v2

# Run the installation script
./install.sh

# Activate the environment
source activate-tts-v2.sh

# Test the system
python -c "from v2.engines import EngineSelector; print('TTS-MacOS v2 ready!')"
```

### Basic Usage

#### MCP Server (Claude Desktop)

```bash
# Start the MCP server
./mcp-server-v2

# Or with legacy compatibility
./mcp-server-v2 --legacy
```

#### Command Line Interface

```bash
# Basic synthesis
./tts-macos-v2 "Hello world" --engine auto

# Voice cloning
./tts-macos-v2 clone-voice my_voice.wav --name "My Voice"

# List available voices
./tts-macos-v2 list-voices --engine all

# Preview a voice
./tts-macos-v2 preview-voice monica --language es

# Save to file
./tts-macos-v2 "Save this text" --output speech.wav

# Batch processing
./tts-macos-v2 batch *.txt --output-dir ./audio/
```

## 🏗️ Architecture

### Dual-Engine System

TTS-MacOS v2 features a sophisticated dual-engine architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    TTS-MacOS v2                           │
├─────────────────────────────────────────────────────────────┤
│  EngineSelector (Intelligent Engine Selection)             │
├─────────────────┬───────────────────────────────────────────┤
│  Native Engine  │              AI Engine                    │
│  (OS TTS)       │         (Coqui TTS)                      │
│  • Fast         │  • High Quality Voices                   │
│  • Low Latency  │  • Voice Cloning                         │
│  • System Integration │ • Multi-Language Support        │
│  • macOS say    │  • XTTS-v2 Model                         │
│  • Linux espeak │  • GPU Acceleration                      │
└─────────────────┴───────────────────────────────────────────┘
```

### Component Structure

```
v2/
├── engines/           # TTS engine implementations
│   ├── native.py      # OS-native TTS (macOS say, Linux espeak)
│   ├── ai_engine.py   # Coqui TTS with XTTS-v2
│   └── selector.py    # Intelligent engine selection
├── core/              # Core functionality
│   ├── config.py      # Configuration management
│   └── smart_features.py  # AI-powered features
├── cli/               # Command-line interface
│   └── main.py        # Enhanced CLI with dual-engine support
├── legacy/            # v1.x compatibility layer
│   ├── server.py      # Legacy MCP server
│   ├── cli.py         # Legacy CLI
│   └── voice_detector.py  # v1.x voice detection
└── mcp_server_v2.py   # Unified MCP server
```

## 🎤 Voice Systems

### Native Engine Voices

- **Spanish Voices**: Monica, Jorge, Ángelica, Francisca, Paulina, etc.
- **Enhanced Voices**: High-quality system voices
- **Premium Voices**: Best quality native voices
- **Dynamic Detection**: Automatic voice discovery

### AI Engine Voices

- **XTTS-v2**: Multilingual voice cloning (16+ languages)
- **Custom Voices**: User-created voice clones
- **Language Support**: Cross-language voice synthesis
- **High Quality**: Production-grade AI voices

### Voice Cloning

Create custom voices from just 6 seconds of audio:

```bash
# Clone a voice
./tts-macos-v2 clone-voice sample.wav --name "Custom Voice" --description "My custom voice"

# Use the cloned voice
./tts-macos-v2 "This is my custom voice speaking" --voice "Custom Voice" --engine ai
```

## 🔧 MCP Tools

### Core MCP Tools

#### `tts_speak` - Primary Synthesis
```json
{
  "text": "Hello world",
  "engine": "auto",
  "voice": "monica", 
  "language": "en",
  "rate": 1.0,
  "volume": 1.0,
  "quality": "balanced",
  "speaker_wav": "/path/to/audio.wav"  // For voice cloning
}
```

#### `tts_clone` - Voice Cloning
```json
{
  "speaker_wav": "/path/to/audio.wav",
  "voice_name": "My Custom Voice",
  "description": "Voice cloned from sample"
}
```

#### `tts_list_voices` - Voice Discovery
```json
{
  "engine": "all",
  "language": "es",
  "include_clones": true
}
```

#### `tts_save` - Audio File Generation
```json
{
  "text": "Save this audio",
  "filename": "output",
  "format": "wav",
  "engine": "auto"
}
```

#### `tts_preview` - Voice Testing
```json
{
  "voice": "monica",
  "language": "es",
  "sample_text": "Custom preview text"
}
```

#### `tts_info` - System Information
Returns detailed system and engine information.

## 🎛️ Configuration

### Configuration File

Location: `~/.config/tts-macos-v2/config.json`

```json
{
  "version": "2.0.0",
  "default_engine": "auto",
  "default_language": "en", 
  "default_quality": "balanced",
  "cache_size_mb": 2048,
  "auto_download_models": true,
  "prefer_gpu": true,
  "native_engine": {
    "enabled": true,
    "preferred_voices": {
      "es": "monica",
      "en": "samantha"
    }
  },
  "ai_engine": {
    "enabled": true,
    "default_model": "xtts_v2",
    "cache_models": true
  }
}
```

### CLI Configuration

```bash
# Show current configuration
./tts-macos-v2 config --show

# Set configuration values
./tts-macos-v2 config --set default_engine=ai
./tts-macos-v2 config --set cache_size_mb=4096

# Reset to defaults
./tts-macos-v2 config --reset

# Clear model cache
./tts-macos-v2 config --clear-cache
```

## 🌍 Language Support

### Supported Languages

| Language | Code | Native Voices | AI Voices | Voice Cloning |
|----------|------|---------------|-----------|---------------|
| English  | en   | ✅            | ✅        | ✅           |
| Spanish  | es   | ✅            | ✅        | ✅           |
| French   | fr   | ✅            | ✅        | ✅           |
| German   | de   | ✅            | ✅        | ✅           |
| Italian  | it   | ✅            | ✅        | ✅           |
| Portuguese| pt  | ✅            | ✅        | ✅           |
| Polish   | pl   | ✅            | ✅        | ✅           |
| Turkish  | tr   | ✅            | ✅        | ✅           |
| Russian  | ru   | ✅            | ✅        | ✅           |
| Dutch    | nl   | ✅            | ✅        | ✅           |
| Czech    | cs   | ✅            | ✅        | ✅           |
| Arabic   | ar   | ✅            | ✅        | ✅           |
| Chinese  | zh-cn| ❌            | ✅        | ✅           |
| Japanese | ja   | ❌            | ✅        | ✅           |
| Hungarian| hu   | ❌            | ✅        | ✅           |
| Korean   | ko   | ❌            | ✅        | ✅           |

## ⚡ Performance

### Engine Selection Logic

The system automatically selects the best engine based on:

- **Voice Cloning**: AI engine required
- **Quality**: Premium → AI, Fast → Native
- **Language**: Non-native languages → AI
- **Speed**: Real-time needs → Native

### Performance Benchmarks

| Operation | Native Engine | AI Engine |
|-----------|---------------|-----------|
| Latency   | <100ms        | 200-500ms |
| Quality   | Good          | Excellent |
| Cloning   | Not supported | ✅        |
| Languages | OS-specific   | 16+       |

### GPU Acceleration

On Linux with NVIDIA GPUs:

```bash
# Enable GPU support
pip install torch-audio

# Check GPU availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

## 🔄 Migration from v1.x

### Automatic Migration

TTS-MacOS v2 maintains 100% backward compatibility:

```bash
# Use legacy mode
./tts-macos-v2 legacy "Hello world" --voice monica

# Legacy MCP server
./mcp-server-v2 --legacy
```

### Manual Migration

#### CLI Commands

| v1.x Command | v2 Equivalent |
|--------------|---------------|
| `tts-macos "text"` | `./tts-macos-v2 "text" --engine native` |
| `tts-macos --list` | `./tts-macos-v2 list-voices --engine native` |
| `tts-macos "text" -o file.aiff` | `./tts-macos-v2 "text" -o file.wav` |

#### MCP Configuration

Update `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tts-macos-v2": {
      "command": "/path/to/tts-macos-v2/mcp-server-v2",
      "args": []
    }
  }
}
```

### New Features Adoption

Gradually adopt v2 features:

1. **Start with auto engine**: `--engine auto`
2. **Try AI voices**: `--engine ai --language es`
3. **Voice cloning**: `clone-voice` command
4. **Smart features**: Let the system optimize parameters

## 🛠️ Development

### Project Structure

```
tts-macos-v2/
├── v2/                    # Main package
│   ├── engines/          # TTS engines
│   ├── core/             # Core functionality  
│   ├── cli/              # Command-line interface
│   ├── legacy/           # v1.x compatibility
│   └── __init__.py       # Package initialization
├── mcp_server_v2.py      # Unified MCP server
├── install.sh            # Installation script
├── requirements.txt      # Dependencies
├── pyproject.toml        # Package configuration
└── README.md            # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Testing

```bash
# Run tests
python -m pytest tests/

# Test specific components
python -c "from v2.engines import EngineSelector; print('✅ Engines')"
python -c "from v2.core.config import TTSConfig; print('✅ Config')"
python -c "from v2.cli.main import EnhancedCLI; print('✅ CLI')"
```

## 🔧 Troubleshooting

### Common Issues

#### Installation Problems

**Problem**: `externally-managed-environment` error
```bash
# Solution: Use the provided installation script
./install.sh
```

**Problem**: TTS library not found
```bash
# Solution: Activate environment and reinstall
source activate-tts-v2.sh
pip install TTS>=0.22.0
```

#### Voice Cloning Issues

**Problem**: Poor voice cloning quality
- Use 6+ seconds of clear audio
- Ensure WAV format, 16-24kHz sample rate
- Minimize background noise
- Use consistent speaking style

#### Performance Issues

**Problem**: Slow synthesis
- Use `--engine native` for faster synthesis
- Enable GPU acceleration on Linux
- Clear cache: `./tts-macos-v2 config --clear-cache`

#### MCP Server Issues

**Problem**: Server not connecting
1. Check paths in `claude_desktop_config.json`
2. Verify Python environment is activated
3. Restart Claude Desktop completely
4. Check Claude logs in `~/Library/Logs/Claude/`

### Debug Mode

Enable debug logging:

```bash
export TTS_MACOS_DEBUG=1
./tts-macos-v2 "test" --engine auto
```

## 📚 Advanced Features

### Smart Voice Selection

The system includes AI-powered voice recommendation:

```python
from v2.core.smart_features import VoiceRecommender

recommender = VoiceRecommender()
recommendation = recommender.recommend_voice(
    text="Your content here",
    language="en",
    voice_type="expressive"
)
print(f"Recommended voice: {recommendation['voice']}")
```

### Automatic Language Detection

```python
from v2.core.smart_features import AutoLanguageDetector

detector = AutoLanguageDetector()
result = detector.detect_language("Hola mundo")
print(f"Detected: {result['detected_language']} ({result['confidence']:.2f})")
```

### Performance Optimization

```python
from v2.core.smart_features import PerformanceOptimizer

optimizer = PerformanceOptimizer()
params = optimizer.optimize_parameters(
    text="Your text",
    engine_type="ai",
    quality_preference="premium"
)
```

## 📖 API Reference

### EngineSelector

```python
from v2.engines import EngineSelector, EngineType

selector = EngineSelector()

# Select best engine
engine = selector.select_engine(
    engine=EngineType.AUTO,
    voice_cloning=True,
    language="es",
    quality="premium"
)

# List all voices
voices = selector.list_all_voices()

# Get engine information
info = selector.get_engine_info()
```

### TTSConfig

```python
from v2.core.config import TTSConfig, TTSRequest

config = TTSConfig()

# Create synthesis request
request = TTSRequest(
    text="Hello world",
    engine="auto",
    voice="monica",
    language="es"
)

# Configuration management
config.update_config({"default_engine": "ai"})
cache_size = config.get_cache_size()
```

## 📄 License

TTS-MacOS v2 is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🤝 Support

- **Documentation**: [Full documentation](https://docs.tts-macos.com)
- **Issues**: [GitHub Issues](https://github.com/tts-macos/tts-macos-v2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tts-macos/tts-macos-v2/discussions)

## 🎉 Acknowledgments

- [Coqui TTS](https://github.com/coqui-ai/TTS) for the amazing AI TTS engine
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP framework
- The TTS-MacOS community for feedback and contributions

---

**TTS-MacOS v2** - The future of text-to-speech is here! 🎤✨