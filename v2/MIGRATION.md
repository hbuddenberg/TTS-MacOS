# Migration Guide: TTS-MacOS v1.x to v2.0

This guide helps you migrate from TTS-MacOS v1.x to v2.0 with minimal disruption while taking advantage of new features.

## 🎯 Overview

TTS-MacOS v2.0 introduces revolutionary features while maintaining 100% backward compatibility with v1.x:

- ✅ **100% Backward Compatible** - All existing v1.x functionality preserved
- 🚀 **Dual-Engine Architecture** - Native + AI TTS engines
- 🎭 **Voice Cloning** - Create custom voices from audio samples
- 🌍 **Multi-Platform** - macOS + Linux support
- 🤖 **Smart Features** - AI-powered optimization

## 📋 Migration Checklist

- [ ] Install TTS-MacOS v2.0
- [ ] Test backward compatibility
- [ ] Update Claude Desktop configuration (optional)
- [ ] Explore new AI features
- [ ] Gradually adopt new functionality

## 🔄 Backward Compatibility

### Legacy Mode

TTS-MacOS v2.0 includes complete v1.x compatibility:

```bash
# Use v1.x commands unchanged
./tts-macos-v2 legacy "Hello world" --voice monica

# Legacy MCP server
./mcp-server-v2 --legacy
```

### Automatic Fallback

All v1.x commands work without changes:

| v1.x Command | v2.0 Behavior |
|--------------|---------------|
| `tts-macos "text"` | Uses native engine automatically |
| `tts-macos --list` | Shows native voices only |
| `tts-macos "text" -o file.aiff` | Saves as AIFF format |
| `say -v Monica "text"` | Unchanged system command |

### Configuration Migration

Your existing v1.x configuration is preserved:

```bash
# v1.x hooks and environment variables still work
export TTS_VOICE=monica
export TTS_RATE=175
export TTS_ENABLED=true
```

## 🚀 Step-by-Step Migration

### Step 1: Install v2.0 Alongside v1.x

```bash
# Download and install v2.0 (doesn't affect v1.x)
cd /path/to/tts-macos-v2
./install.sh

# Verify installation
source activate-tts-v2.sh
./tts-macos-v2 --help
```

### Step 2: Test Backward Compatibility

```bash
# Test legacy CLI functionality
./tts-macos-v2 legacy "Testing migration" --voice monica

# Test legacy MCP server
./mcp-server-v2 --legacy &

# Your existing Claude Desktop v1.x config still works
```

### Step 3: Explore New Features (Optional)

```bash
# Test AI engine
./tts-macos-v2 "Testing AI voices" --engine ai

# List all available voices
./tts-macos-v2 list-voices --engine all

# Try voice cloning (if you have audio samples)
./tts-macos-v2 clone-voice sample.wav --name "My Voice"
```

### Step 4: Update Configuration (Optional)

#### Claude Desktop Configuration

**Option A: Keep v1.x Configuration**
```json
{
  "mcpServers": {
    "tts-macos": {
      "command": "/path/to/mcp-tts-macos/server.py"
    }
  }
}
```

**Option B: Upgrade to v2.0**
```json
{
  "mcpServers": {
    "tts-macos-v2": {
      "command": "/path/to/tts-macos-v2/mcp-server-v2"
    }
  }
}
```

#### CLI Usage

**Gradual adoption:**

```bash
# Phase 1: Continue using v1.x commands
./tts-macos-v2 legacy "text" --voice monica

# Phase 2: Try auto engine selection
./tts-macos-v2 "text" --engine auto

# Phase 3: Use AI features
./tts-macos-v2 "text" --engine ai --language es
```

## 🎤 Voice System Migration

### Native Voices (Unchanged)

All your existing native voices work exactly as before:

```bash
# These commands work unchanged
./tts-macos-v2 "Hola mundo" --voice monica
./tts-macos-v2 "Hello world" --voice samantha
./tts-macos-v2 "Bonjour le monde" --voice aurelie
```

### New AI Voices

In addition to native voices, you now have access to AI voices:

```bash
# AI voices (new in v2.0)
./tts-macos-v2 "AI voice test" --engine ai
./tts-macos-v2 "Multilingual test" --engine ai --language ja
```

### Voice Cloning (New Feature)

Create custom voices from audio samples:

```bash
# New v2.0 feature
./tts-macos-v2 clone-voice my_sample.wav --name "My Custom Voice"

# Use the cloned voice
./tts-macos-v2 "This is my cloned voice" --voice "My Custom Voice" --engine ai
```

## 🔧 MCP Tools Migration

### v1.x MCP Tools (Still Available)

```python
# These work unchanged in legacy mode
tts_speak(text="Hello", voice="monica", rate=175)
tts_list_voices()
tts_save_audio(text="Save this", filename="output")
```

### v2.0 Enhanced MCP Tools

```python
# Enhanced v2.0 tools with more features
tts_speak(
    text="Hello world",
    engine="auto",           # NEW: Engine selection
    voice="monica",
    language="es",           # NEW: Language specification
    quality="premium",       # NEW: Quality control
    speaker_wav="/path/to/audio.wav"  # NEW: Voice cloning
)

tts_clone(
    speaker_wav="/path/to/audio.wav",
    voice_name="My Voice"
)

tts_list_voices(
    engine="all",           # NEW: Filter by engine
    language="es",          # NEW: Filter by language
    include_clones=True     # NEW: Include voice clones
)
```

## 📁 File Structure Changes

### v1.x Structure (Preserved)

```
mcp-tts-macos/           # Your v1.x installation (unchanged)
├── server.py
├── src/tts_macos/
├── install.sh
└── ... (other v1.x files)
```

### v2.0 Structure (New Installation)

```
tts-macos-v2/            # New v2.0 installation
├── v2/
│   ├── engines/         # NEW: Dual-engine architecture
│   ├── core/           # NEW: Core functionality
│   ├── cli/            # NEW: Enhanced CLI
│   ├── legacy/         # NEW: v1.x compatibility layer
│   └── __init__.py
├── mcp_server_v2.py    # NEW: Unified MCP server
├── install.sh          # NEW: Cross-platform installer
└── ... (v2.0 files)
```

## 🔄 Gradual Migration Path

### Phase 1: Parallel Installation (Week 1)

- Install v2.0 alongside v1.x
- Test legacy mode functionality
- Verify existing workflows still work

### Phase 2: Feature Exploration (Week 2-3)

- Try auto engine selection
- Experiment with AI voices
- Test voice cloning capabilities

### Phase 3: Gradual Adoption (Week 4+)

- Update Claude Desktop to use v2.0
- Migrate scripts to use new CLI
- Adopt AI features for appropriate use cases

### Phase 4: Full Migration (Optional)

- Decommission v1.x if desired
- Migrate all workflows to v2.0
- Take advantage of all new features

## 🛠️ Troubleshooting Migration Issues

### Common Migration Problems

#### Problem: Legacy commands not found

```bash
# ✅ Use legacy mode
./tts-macos-v2 legacy "text" --voice monica

# ✅ Or update to v2.0 syntax
./tts-macos-v2 "text" --engine native --voice monica
```

#### Problem: MCP server not connecting

```bash
# ✅ Check v2.0 server path
./mcp-server-v2

# ✅ Or use legacy mode
./mcp-server-v2 --legacy
```

#### Problem: Voice not found

```bash
# ✅ List all available voices
./tts-macos-v2 list-voices --engine all

# ✅ Try auto engine selection
./tts-macos-v2 "text" --engine auto
```

#### Problem: Configuration not working

```bash
# ✅ Use v2.0 configuration
./tts-macos-v2 config --show

# ✅ Or continue using v1.x environment variables
export TTS_VOICE=monica
```

### Performance Considerations

#### AI Engine Slower Than Expected

```bash
# ✅ Use native engine for speed
./tts-macos-v2 "text" --engine native

# ✅ Or enable GPU acceleration (Linux)
pip install torch-audio
```

#### High Memory Usage

```bash
# ✅ Clear AI model cache
./tts-macos-v2 config --clear-cache

# ✅ Use native engine for memory efficiency
./tts-macos-v2 "text" --engine native
```

## 🎯 Best Practices for Migration

### 1. Test Thoroughly

```bash
# Test your most common use cases
./tts-macos-v2 legacy "Your frequent text" --voice your-voice

# Verify MCP functionality
./tts-macos-v2 list-voices --engine native
```

### 2. Gradual Adoption

```bash
# Start with auto engine selection
./tts-macos-v2 "text" --engine auto

# Progress to specific features as needed
./tts-macos-v2 "text" --engine ai --language es
```

### 3. Monitor Performance

```bash
# Check system information
./tts-macos-v2 info

# Monitor cache usage
./tts-macos-v2 config --show | grep cache
```

### 4. Backup Configuration

```bash
# Backup v1.x configuration before migration
cp -r ~/.config/tts-macos ~/.config/tts-macos-backup

# Export Claude Desktop config
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json ~/Desktop/backup.json
```

## 📚 New Feature Adoption Guide

### Voice Cloning Workflow

```bash
# 1. Prepare audio sample (6+ seconds, clear voice)
# Format: WAV, 16-24kHz, minimal background noise

# 2. Clone the voice
./tts-macos-v2 clone-voice sample.wav --name "Custom Voice" --description "My voice"

# 3. Test the cloned voice
./tts-macos-v2 preview-voice "Custom Voice" --text "Testing my cloned voice"

# 4. Use in production
./tts-macos-v2 "This is my custom voice" --voice "Custom Voice" --engine ai
```

### Multi-Language Content

```bash
# Spanish content
./tts-macos-v2 "Hola mundo" --engine ai --language es

# Japanese content (AI only)
./tts-macos-v2 "こんにちは世界" --engine ai --language ja

# Auto-detect language (if NLP libraries installed)
./tts-macos-v2 "Text in unknown language" --engine ai
```

### Quality Optimization

```bash
# Fast synthesis (native engine)
./tts-macos-v2 "Quick text" --engine native --quality fast

# Balanced quality (auto selection)
./tts-macos-v2 "Regular text" --engine auto --quality balanced

# Premium quality (AI engine)
./tts-macos-v2 "Important content" --engine ai --quality premium
```

## 🎉 Migration Success Metrics

Your migration is successful when:

- ✅ All existing v1.x functionality works in legacy mode
- ✅ You can use auto engine selection
- ✅ AI voices work for your use cases
- ✅ Voice cloning works (if applicable)
- ✅ Performance meets your needs
- ✅ Configuration is updated as desired

## 🆘 Support and Resources

### Getting Help

- **Documentation**: [TTS-MacOS v2.0 Documentation](README.md)
- **Issues**: [GitHub Issues](https://github.com/tts-macos/tts-macos-v2/issues)
- **Migration Issues**: [Tag with 'migration'](https://github.com/tts-macos/tts-macos-v2/issues?q=label%3Amigration)

### Community

- **Discussions**: [GitHub Discussions](https://github.com/tts-macos/tts-macos-v2/discussions)
- **Examples**: Share your migration experience
- **Voice Clones**: Share successful voice cloning setups

---

**Congratulations!** 🎉 You're ready to migrate to TTS-MacOS v2.0 and enjoy all the new features while maintaining your existing workflows.