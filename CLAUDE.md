# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TTS-macOS is a Text-to-Speech tool for macOS that operates in three modes:
1. **MCP Server** - Integrates with Claude Desktop as an MCP server
2. **CLI Tool** - Standalone command-line tool (installed globally or via uvx)
3. **UVX Mode** - Direct execution without installation (like npx)

The project uses macOS's native TTS engine (`say` command), requiring zero external dependencies for speech synthesis.

## Project Structure

```
mcp-tts-macos/           # Main project directory
├── server.py            # MCP server implementation
├── src/tts_macos/       # CLI tool implementation
│   ├── cli.py           # CLI logic with voice detection
│   ├── __main__.py      # Entry point for CLI
│   └── __init__.py
├── setup.py             # Package configuration for pip install
├── install.sh           # MCP server installer
├── install-cli.sh       # CLI global installer
├── requirements.txt     # Python dependencies (mcp>=1.0.0)
└── examples.sh          # Usage examples
```

## Architecture

### MCP Server Mode (server.py)

- Uses `mcp.server` library to expose three tools:
  - `speak_text` - Reproduces text with configurable voice and rate
  - `list_voices` - Lists available Spanish voices
  - `save_audio` - Saves text as AIFF audio file on Desktop
- Runs asynchronously using `asyncio` and `stdio_server`
- Executes macOS `say` command via subprocess
- Configured in Claude Desktop via `claude_desktop_config.json`

### CLI Tool Mode (src/tts_macos/cli.py)

- **Key Feature**: Auto-detects available Spanish voices from system using `say -v ?`
- Provides fallback voices if detection fails (monica, paulina, jorge, juan, diego, angelica)
- Uses `argparse` for command-line interface
- Supports:
  - Text-to-speech reproduction with customizable voice and rate (100-300 WPM)
  - Audio file saving (AIFF format)
  - Voice listing with system detection

### Voice System

The CLI implements dynamic voice detection (`obtener_voces_sistema()` in cli.py:13-43):
- Parses `say -v ?` output to find Spanish voices
- Creates lowercase aliases automatically
- Falls back to hardcoded voices if detection fails
- This makes the tool resilient across different macOS voice configurations

## Available Voices

Default Spanish voices (may vary by system):
- `monica` - Español México (Mujer)
- `paulina` - Español México (Mujer)
- `jorge` - Español España (Hombre)
- `juan` - Español España (Hombre)
- `diego` - Español Argentina (Hombre)
- `angelica` - Español México (Mujer)

Voice names are case-insensitive in CLI but must be capitalized for the `say` command.

## Development Commands

### Testing the MCP Server

```bash
cd mcp-tts-macos
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py  # Will wait for MCP connections
```

### Testing the CLI Tool

```bash
# Direct execution
cd mcp-tts-macos
python3 src/tts_macos/cli.py "Test message"

# With uvx (no installation)
cd mcp-tts-macos
uvx --from . tts-macos "Test message"
uvx --from . tts-macos --list
uvx --from . tts-macos "Test" --voice jorge --rate 200

# After installation
tts-macos "Test message"
tts-macos --help
```

### Installation

```bash
# Install MCP server
cd mcp-tts-macos
./install.sh  # Creates venv, installs deps, configures Claude Desktop

# Install CLI globally
cd mcp-tts-macos
./install-cli.sh  # Interactive installer with 3 options

# Use with uvx (recommended for development)
brew install uv
uvx --from . tts-macos "text"
```

## Key Implementation Details

### Async Execution Pattern (server.py)

The MCP server uses `asyncio.create_subprocess_exec()` for non-blocking execution:
```python
process = await asyncio.create_subprocess_exec(
    *cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
)
stdout, stderr = await process.communicate()
```

### Voice Detection (cli.py)

Auto-detects voices by parsing `say -v ?` output:
- Searches for lines containing 'spanish' or 'español'
- Extracts voice name (first word in line)
- Creates lowercase alias mapping
- Critical for compatibility across macOS versions with different voice installations

### File Saving

Audio files are saved to Desktop by default:
```python
output_path = f"/Users/{subprocess.getoutput('whoami')}/Desktop/{filename}"
```

## Configuration Files

### Claude Desktop Config

Located at: `~/Library/Application Support/Claude/claude_desktop_config.json`

Format:
```json
{
  "mcpServers": {
    "tts-macos": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

The `install.sh` script auto-generates this with absolute paths.

## Troubleshooting

### Voice Not Found

If a voice isn't available, the CLI falls back to "Monica". Users can:
1. Check available voices: `say -v ? | grep -i spanish`
2. Install voices via: System Preferences → Accessibility → Spoken Content → System Voices

### MCP Server Not Connecting

1. Verify paths in `claude_desktop_config.json` are absolute
2. Ensure venv is activated and dependencies installed
3. Restart Claude Desktop completely (Cmd+Q)
4. Check Claude logs in `~/Library/Logs/Claude/`

### CLI Command Not Found After Installation

Add to PATH (handled by install-cli.sh):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Version History

- v1.2.1 - Added dynamic voice detection in CLI
- v1.1.0 - Added CLI mode and uvx support
- v1.0.0 - Initial MCP server implementation

## Dependencies

- Python 3.10+ (required)
- `mcp>=1.0.0` (for server mode only)
- macOS native `say` command (built-in)
- `uv` (optional, for uvx mode)

## Testing

No formal test suite. Manual testing:
```bash
# Test voice availability
say -v Monica "test"

# Test CLI
tts-macos "test" --voice monica
tts-macos --list

# Test MCP server (through Claude Desktop)
"Lee en voz alta: Hola mundo"
```

## Hooks for Claude Code

The `.claude/hooks/` directory contains shell scripts that integrate TTS-macOS with Claude Code:

### Available Hooks

1. **post-response** - Reads Claude's responses aloud after generation
   - Filters out code blocks and markdown
   - Truncates long responses based on `TTS_MAX_LENGTH`
   - Runs in background to avoid blocking

2. **user-prompt-submit** - Confirms when user submits a prompt
   - Announces "Procesando tu solicitud" with configurable voice
   - Useful for accessibility and confirmation

### Hook Configuration

Hooks are controlled via environment variables:

```bash
# Enable response reading
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=175
export TTS_MAX_LENGTH=500

# Enable prompt confirmation (optional)
export TTS_PROMPT_ENABLED=true
export TTS_PROMPT_VOICE=jorge
export TTS_PROMPT_RATE=200
```

### Hook Files

- `post-response` - Main hook for reading responses
- `user-prompt-submit` - Hook for prompt confirmation
- `enable-tts.sh` - Interactive configuration script
- `demo.sh` - Demonstration of all features
- `README.md` - Complete documentation
- `EJEMPLOS.md` - Usage examples in Spanish
- `INICIO-RAPIDO.md` - Quick start guide

### Testing Hooks

```bash
# Interactive configuration
source .claude/hooks/enable-tts.sh

# Run demo
./.claude/hooks/demo.sh

# Test manually
echo "Test response" | ./.claude/hooks/post-response
```

## Notes for AI Assistants

- Always use absolute paths when modifying `claude_desktop_config.json`
- The CLI's voice detection is a critical feature - preserve it when making changes
- Audio rate must be between 100-300 WPM (validated in cli.py:200)
- All audio output is AIFF format (macOS native)
- The project has extensive Spanish documentation alongside English code
- Hooks are controlled via environment variables and run in background (non-blocking)
- Text is filtered before TTS to remove code blocks and markdown
