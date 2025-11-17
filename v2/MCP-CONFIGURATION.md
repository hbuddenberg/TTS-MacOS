# TTS-MacOS v2 - MCP JSON Configuration Guide

## 🔧 Claude Desktop Integration

TTS-MacOS v2 includes comprehensive MCP (Model Context Protocol) integration for Claude Desktop with automatic JSON configuration management.

### 📋 MCP Tools Available

#### Core Synthesis Tools

1. **`tts_speak`** - Primary TTS synthesis with intelligent engine selection
```json
{
  "text": "Hello world",
  "engine": "auto",
  "voice": "monica",
  "language": "en",
  "rate": 1.0,
  "volume": 1.0,
  "quality": "balanced",
  "speaker_wav": "/path/to/audio.wav"
}
```

2. **`tts_clone`** - Voice cloning from audio samples
```json
{
  "speaker_wav": "/path/to/audio.wav",
  "voice_name": "My Custom Voice",
  "description": "Voice cloned from sample audio"
}
```

3. **`tts_list_voices`** - Comprehensive voice discovery
```json
{
  "engine": "all",
  "language": "es",
  "include_clones": true
}
```

4. **`tts_save`** - Audio file generation
```json
{
  "text": "Save this audio",
  "filename": "output",
  "format": "wav",
  "engine": "auto"
}
```

5. **`tts_preview`** - Voice testing and preview
```json
{
  "voice": "monica",
  "language": "es",
  "sample_text": "Custom preview text"
}
```

6. **`tts_info`** - System information and status
```json
{}  // No parameters required
```

### ⚙️ Automatic Configuration

#### Installation with MCP Setup

```bash
# Complete installation with automatic Claude Desktop configuration
./install.sh

# The installer will:
# 1. Detect Claude Desktop installation
# 2. Ask if you want to install MCP server
# 3. Generate JSON configuration automatically
# 4. Create backup of existing configuration
# 5. Install both v2 and legacy servers (optional)
```

#### Manual Configuration

If you prefer manual setup or need to customize:

```bash
# Use the MCP configuration tool
./mcp-config install --v2

# Install both v2 and legacy servers
./mcp-config install --v2 --legacy

# Custom server name
./mcp-config install --v2 --name "my-tts-server"
```

### 📁 Generated JSON Configuration

The installer creates/modifies `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tts-macos-v2": {
      "command": "/path/to/tts-macos-v2/venv-v2/bin/python",
      "args": ["/path/to/tts-macos-v2/mcp_server_v2"],
      "env": {
        "PYTHONPATH": "/path/to/tts-macos-v2",
        "TTS_MACOS_V2": "1"
      }
    },
    "tts-macos-legacy": {
      "command": "/path/to/tts-macos-v2/venv-v2/bin/python", 
      "args": ["/path/to/tts-macos-v2/legacy/server.py", "--legacy"],
      "env": {
        "PYTHONPATH": "/path/to/tts-macos-v2/legacy",
        "TTS_MACOS_LEGACY": "1"
      }
    }
  }
}
```

### 🛠️ Configuration Management

#### MCP Configuration Tool Commands

```bash
# Detect Claude Desktop and installation status
./mcp-config detect

# Install MCP configuration
./mcp-config install --v2

# Test installation
./mcp-config test

# Show current status and configuration
./mcp-config status

# Uninstall specific server
./mcp-config uninstall --server tts-macos-v2

# Generate standalone installation script
./mcp-config generate-script --output install_mcp.sh
```

#### Environment Variables

The MCP servers use these environment variables:

- `PYTHONPATH`: Points to TTS-MacOS v2 directory
- `TTS_MACOS_V2`: Enables v2 features (v2 server)
- `TTS_MACOS_LEGACY`: Enables legacy mode (legacy server)

### 🔄 Backward Compatibility

#### Legacy Mode Support

The v2 MCP server includes full backward compatibility:

```python
# Legacy tools still work unchanged
tts_speak(text="Hello", voice="monica", rate=175)  # v1.x syntax
tts_list_voices()                                    # v1.x syntax
tts_save_audio(text="Save this", filename="output")   # v1.x syntax
```

#### Dual Server Installation

You can install both v2 and legacy servers simultaneously:

```json
{
  "mcpServers": {
    "tts-macos-v2": {
      // v2 server with full features
    },
    "tts-macos-legacy": {
      // v1.x server for compatibility
    }
  }
}
```

### 🎯 Usage Examples in Claude Desktop

#### Basic Text-to-Speech

```
User: Convert this to speech: "Hello world, this is a test of TTS-MacOS v2"
Claude: I'll convert that text to speech using the TTS-MacOS v2 system.

[Uses tts_speak tool with auto engine selection]
✅ TTS Synthesis Complete
🔊 Engine: AI (Coqui TTS)
🎤 Voice: default
🌍 Language: en
📊 Quality: balanced
⏱️ Time: 1.23s
```

#### Voice Cloning

```
User: I have this audio file /path/to/my_voice.wav. Can you create a custom voice?
Claude: I'll create a custom voice from your audio file using voice cloning.

[Uses tts_clone tool]
✅ Voice Clone Created Successfully
🎭 Voice Name: My Voice
📁 Original File: /path/to/my_voice.wav
🔧 Processed File: /path/to/processed_voice.wav
🤖 Model: xtts_v2
```

#### Multi-Language Support

```
User: Say "Bonjour le monde" in French
Claude: I'll synthesize that French text for you.

[Uses tts_speak with language="fr"]
✅ TTS Synthesis Complete
🔊 Engine: AI (Coqui TTS)
🎤 Voice: default french speaker
🌍 Language: fr
```

### 🔍 Troubleshooting MCP Configuration

#### Common Issues

1. **Claude Desktop not detecting tools**
   ```bash
   # Restart Claude Desktop completely
   # Check configuration
   ./mcp-config detect
   # Test installation
   ./mcp-config test
   ```

2. **Server not starting**
   ```bash
   # Check Python paths in configuration
   ./mcp-config status
   # Validate server files
   ./mcp-config test
   ```

3. **Voice cloning not working**
   ```bash
   # Check AI engine availability
   ./mcp-config status
   # Verify dependencies
   ./install.sh --non-interactive
   ```

#### Configuration Validation

```bash
# Complete diagnostic
./mcp-config detect    # Check Claude Desktop
./mcp-config test      # Test server functionality  
./mcp-config status    # Show current configuration
```

### 🎛️ Advanced Configuration

#### Custom Server Names

```bash
# Install with custom naming
./mcp-config install --v2 --name "production-tts"
./mcp-config install --legacy --name "fallback-tts"
```

#### Multiple Installations

You can install TTS-MacOS v2 in multiple locations:

```bash
# Development installation
./mcp-config install --v2 --python-path /opt/tts-dev/venv/bin/python

# Production installation  
./mcp-config install --v2 --name "tts-prod" --python-path /opt/tts-prod/venv/bin/python
```

#### Environment-Specific Configuration

```json
{
  "mcpServers": {
    "tts-macos-dev": {
      "command": "/opt/tts-dev/venv/bin/python",
      "args": ["/opt/tts-dev/mcp_server_v2"],
      "env": {
        "PYTHONPATH": "/opt/tts-dev",
        "TTS_MACOS_V2": "1",
        "TTS_MACOS_ENV": "development"
      }
    },
    "tts-macos-prod": {
      "command": "/opt/tts-prod/venv/bin/python", 
      "args": ["/opt/tts-prod/mcp_server_v2"],
      "env": {
        "PYTHONPATH": "/opt/tts-prod",
        "TTS_MACOS_V2": "1",
        "TTS_MACOS_ENV": "production"
      }
    }
  }
}
```

### 📚 API Reference

#### Tool Parameters

##### tts_speak
- `text` (string, required): Text to synthesize
- `engine` (string): "auto", "native", "ai"
- `voice` (string): Voice name or cloning path
- `language` (string): Language code (es, en, fr, de, etc.)
- `rate` (float): Speech rate multiplier (0.5-2.0)
- `volume` (float): Volume level (0.0-2.0)
- `quality` (string): "fast", "balanced", "premium"
- `speaker_wav` (string): Path for voice cloning

##### tts_clone
- `speaker_wav` (string, required): Path to WAV audio file
- `voice_name` (string, required): Name for cloned voice
- `description` (string): Optional description

##### tts_list_voices
- `engine` (string): "all", "native", "ai"
- `language` (string): Filter by language code
- `include_clones` (boolean): Include voice clones

### 🎉 Success Stories

The TTS-MacOS v2 MCP integration enables:

- **Real-time voice synthesis** directly in Claude conversations
- **Voice cloning** from audio samples for personalized content
- **Multi-language support** for global applications
- **Quality control** from fast to premium synthesis
- **Backward compatibility** with existing v1.x workflows

---

**TTS-MacOS v2** - Professional text-to-speech integrated seamlessly with Claude Desktop! 🎤✨