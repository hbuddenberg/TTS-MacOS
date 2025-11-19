# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TTS Notify is a Text-to-Speech notification system for macOS that operates in three modes:
1. **MCP Server** - Integrates with Claude Desktop as an MCP server
2. **CLI Tool** - Standalone command-line tool (installed globally or via uvx)
3. **UVX Mode** - Direct execution without installation (like npx)

The project uses macOS's native TTS engine (`say` command), requiring zero external dependencies for speech synthesis.

## Project Structure

```
TTS_Notify/              # Main project directory
├── src/
│   ├── mcp_server.py     # MCP server implementation
│   ├── cli.py           # CLI logic with voice detection
│   ├── __main__.py      # Entry point for CLI
│   └── __init__.py      # Package initialization
├── documentation/
│   ├── README.md        # Main documentation
│   ├── INSTALLATION.md  # Detailed installation guide
│   ├── USAGE.md         # Usage examples and advanced features
│   └── VOICES.md        # Complete voice reference
├── installers/
│   ├── install-mcp.sh   # MCP server installer
│   └── install-cli.sh   # CLI global installer
├── pyproject.toml       # Modern Python packaging
├── requirements.txt     # Python dependencies (mcp>=1.0.0)
└── LICENSE             # MIT License
```

## Architecture

### MCP Server Mode (src/mcp_server.py)

- Uses `mcp.server.fastmcp` library to expose three tools:
  - `speak_text` - Reproduces text with configurable voice and rate, **ALL system voices supported**
  - `list_voices` - Lists **ALL** available voices categorized (Español, Enhanced, Siri, etc.)
  - `save_audio` - Saves text as AIFF audio file on Desktop with any voice
- **Auto-detection**: Detects ALL system voices at startup (~84+ voices)
- **Flexible search**: Supports exact, partial, case-insensitive voice matching
- Runs asynchronously using `asyncio` and FastMCP
- Executes macOS `say` command via subprocess
- Configured in Claude Desktop via `claude_desktop_config.json`

### CLI Tool Mode (src/cli.py)

- **Key Feature**: Auto-detects **ALL** voices from system using `say -v ?` (~84+ voices)
- **Categorizes voices**: Español, Siri, Enhanced, Premium, Others
- **Flexible search**: Exact, partial, case-insensitive matching
- Provides fallback voices if detection fails
- Uses `argparse` for command-line interface (no `choices` restriction)
- Supports:
  - Text-to-speech with ANY voice in the system
  - Audio file saving (AIFF format)
  - Voice listing with categorization (--list)
  - Flexible voice search

## Voice System

The CLI implements dynamic voice detection (`obtener_voces_sistema()` in cli.py:31-80):
- Parses `say -v ?` output to find Spanish voices
- Creates lowercase aliases automatically
- Falls back to hardcoded voices if detection fails
- This makes the tool resilient across different macOS voice configurations

### Voice Categories

**Español (16 voces):**
- Eddy, Flo, Grandma, Grandpa, Reed, Rocko, Sandy, Shelley (España y México)

**Enhanced/Premium (12 voces):**
- Angélica (México), Francisca (Chile), Jorge (España), Paulina (México)
- Mónica (España), Juan (México), Diego (Argentina), Carlos (Colombia)
- Isabela (Argentina), Marisol (España), Soledad (Colombia), Jimena (Colombia)

**Siri (cuando se instalen):**
- Siri Female, Siri Male (auto-detectadas)

### Voice Search

Voice names support **flexible search**:
- **Exact**: `Monica`, `Angélica`, `Jorge`
- **Case-insensitive**: `angelica`, `MONICA`, `jorge`
- **Partial**: `angel` → Angélica, `franc` → Francisca
- **Fallback**: If not found → first Spanish voice → Monica

## Development Commands

### Testing the MCP Server

```bash
cd TTS_Notify
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/mcp_server.py  # Will wait for MCP connections
```

### Testing the CLI Tool

```bash
# Direct execution
cd TTS_Notify
python src/cli.py "Test message"

# With uvx (no installation)
cd TTS_Notify
uvx --from . tts-notify "Test message"
uvx --from . tts-notify --list
uvx --from . tts-notify "Test" --voice jorge --rate 200

# After installation
tts-notify "Test message"
tts-notify --help
```

### Installation

```bash
# Install MCP server
cd TTS_Notify
./installers/install-mcp.sh  # Creates venv, installs deps, configures Claude Desktop

# Install CLI globally
cd TTS_Notify
./installers/install-cli.sh  # Interactive installer with 3 options

# Use with uvx (recommended for development)
brew install uv
uvx --from TTS_Notify tts-notify "text"
```

## Key Implementation Details

### Async Execution Pattern (mcp_server.py)

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
    "tts-notify": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/TTS_Notify/src/mcp_server.py"]
    }
  }
}
```

The `installers/install-mcp.sh` script auto-generates this with absolute paths.

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

- v1.5.0 - Complete restructure as TTS Notify, clean codebase
- v1.4.4 - Last stable version as TTS-macOS
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
tts-notify "test" --voice monica
tts-notify --list

# Test MCP server (through Claude Desktop)
"Lee en voz alta: Hola mundo"
```

## Hooks for Claude Code

The `.claude/hooks/` directory contains shell scripts that integrate TTS Notify with Claude Code:

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
- Audio rate must be between 100-300 WPM (validated in cli.py:398-400)
- All audio output is AIFF format (macOS native)
- The project has extensive Spanish documentation alongside English code
- Hooks are controlled via environment variables and run in background (non-blocking)
- Text is filtered before TTS to remove code blocks and markdown
- Version 1.5.0 represents a complete restructure and cleanup of the codebase

## Key Differences from Previous Versions

- **Clean structure**: Organized under TTS_Notify/ with proper separation
- **Updated naming**: Changed from tts-macos to tts-notify
- **Simplified dependencies**: Removed heavy ML/AI dependencies from v2
- **Enhanced documentation**: Complete guides in documentation/
- **Improved installers**: Updated for new structure and paths
- **Better voice management**: Same robust voice detection system
- **Modern packaging**: Updated pyproject.toml for TTS Notify