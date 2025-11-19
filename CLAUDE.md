# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TTS Notify is a Text-to-Speech notification system for macOS that operates in three modes:
1. **MCP Server** - Integrates with Claude Desktop as an MCP server
2. **CLI Tool** - Standalone command-line tool (installed globally or via uvx)
3. **UVX Mode** - Direct execution without installation (like npx)

The project uses macOS's native TTS engine (`say` command), requiring zero external dependencies for speech synthesis.

## Key Architecture Components

### Voice Detection System
The core innovation is the **dynamic voice detection system** (`obtener_voces_sistema()` in cli.py:31-80 and `get_system_voices()` in mcp_server.py:41-65):
- **Auto-detection**: Parses `say -v ?` output to discover ALL system voices (~84+ voices)
- **Flexible search**: Supports exact, partial, case-insensitive, accent-insensitive matching
- **Categorization**: Groups voices by type (Español, Enhanced, Premium, Siri, Others)
- **Fallback system**: Hardcoded voices if system detection fails
- **Cross-platform resilience**: Works across different macOS versions with different voice installations

### MCP Server Implementation
- **FastMCP integration**: Uses `mcp.server.fastmcp` for async server implementation
- **Three tools**: `speak_text`, `list_voices`, `save_audio` - all with flexible voice search
- **Async execution**: Non-blocking subprocess calls using `asyncio.create_subprocess_exec()`
- **Voice type forcing**: Can force specific voice variants (normal/enhanced/premium/siri)
- **Error handling**: Comprehensive error handling with fallback to Monica

### CLI Implementation
- **argparse interface**: Full CLI with comprehensive help system
- **Voice listing**: Both detailed and compact formats with filtering capabilities
- **Flexible filters**: Filter by gender, language, voice type
- **Smart project detection**: 3-strategy approach to find project paths for help examples
- **Rate validation**: Enforces 100-300 WPM limits (cli.py:887-892)

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

### Environment Setup

```bash
# Create virtual environment for development
cd TTS_Notify
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install development dependencies
pip install --upgrade pip
```

### Testing the MCP Server

```bash
# Start MCP server (will wait for connections)
cd TTS_Notify
python src/mcp_server.py

# Test MCP server tools (requires Claude Desktop running)
# Tools: speak_text, list_voices, save_audio
```

### Testing the CLI Tool

```bash
# Direct execution (development)
cd TTS_Notify
python src/cli.py "Test message"

# With uvx (no installation required)
cd TTS_Notify
uvx --from . tts-notify "Test message"
uvx --from . tts-notify --list
uvx --from . tts-notify --list --compact
uvx --from . tts-notify --list --gen female
uvx --from . tts-notify --list --lang es_ES
uvx --from . tts-notify "Test" --voice jorge --rate 200

# Test voice search flexibility
uvx --from . tts-notify "Test" --voice angelica  # finds Angélica
uvx --from . tts-notify "Test" --voice "jorge enhanced"  # Enhanced variant
```

### Installation Scripts

```bash
# Install MCP server (creates venv, configures Claude Desktop)
cd TTS_Notify
./installers/install-mcp.sh

# Install CLI globally (interactive with 3 options)
cd TTS_Notify
./installers/install-cli.sh

# Development with uvx (recommended)
brew install uv
uvx --from TTS_Notify tts-notify "text"
```

### Building and Packaging

```bash
# Build package (uses hatchling build system)
cd TTS_Notify
pip install build
python -m build

# Install locally in development mode
pip install -e .
```

## Key Implementation Details

### Voice Search Algorithm

The project implements a **3-tier voice search system**:
1. **Exact match**: Case-insensitive, accent-insensitive comparison
2. **Prefix match**: Search by voice name start (prioritized)
3. **Partial match**: Search anywhere in voice description
4. **Fallback**: First Spanish voice, then "Monica"

Located in `buscar_voz_en_sistema()` (cli.py:128-169) and `find_voice_in_system()` (mcp_server.py:124-165).

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

### Voice Detection and Categorization

Both CLI and MCP server share voice detection logic:
- Parses `say -v ?` output to discover all system voices
- Categorizes by type: Español, Enhanced, Premium, Siri, Others
- Creates lowercase alias mapping for flexible search
- Critical for compatibility across macOS versions

### Smart Project Path Detection

CLI implements 3-strategy project detection (cli.py:683-726):
1. **Script path analysis**: Extract project path from script location
2. **Parent directory search**: Look for mcp_server.py in current/parent directories
3. **CWD pattern matching**: Check if CWD contains "TTS_Notify"

### File Paths and Output

- **Audio files**: Saved to Desktop by default using dynamic user detection
- **Configuration**: Uses absolute paths for Claude Desktop config
- **Python packaging**: Hatchling build system with src/ layout

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

### Manual Testing Strategy

The project uses manual testing rather than automated tests:

```bash
# Test voice availability (macOS native)
say -v Monica "test"
say -v ?  # List all system voices

# Test CLI functionality
tts-notify "test" --voice monica
tts-notify --list
tts-notify --list --compact
tts-notify --list --gen female
tts-notify "test" --save output_file

# Test voice search flexibility
tts-notify "test" --voice angelica    # Should find Angélica
tts-notify "test" --voice siri        # Should find Siri if installed
tts-notify "test" --voice "monica enhanced"  # Should find Enhanced variant

# Test MCP server (through Claude Desktop)
"Lee en voz alta: Hola mundo"
"Lista todas las voces disponibles"
"Guarda este texto como audio: archivo de prueba"

# Test edge cases
tts-notify "test" --rate 100  # Minimum rate
tts-notify "test" --rate 300  # Maximum rate
tts-notify "test" --voice nonexistent_voice  # Should fallback to Monica
```

### Key Test Scenarios

1. **Voice Detection**: Verify system voices are detected correctly
2. **Search Flexibility**: Test accent-insensitive, case-insensitive, partial matching
3. **Rate Validation**: Test 100-300 WPM limits
4. **File Saving**: Verify audio files are saved to Desktop
5. **MCP Integration**: Test all three MCP tools through Claude Desktop
6. **Fallback Behavior**: Verify graceful fallback when voices are missing

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

## Critical Development Notes

### Code Architecture Preservation
- **Voice detection system**: The core `obtener_voces_sistema()`/`get_system_voices()` functions are critical - maintain their logic when making changes
- **Search algorithm**: The 3-tier voice search system must be preserved for compatibility
- **Rate validation**: Always enforce 100-300 WPM limits (cli.py:887-892)
- **Fallback behavior**: Maintain "Monica" as the final fallback voice

### Path Management
- **Absolute paths required**: Claude Desktop config requires absolute paths - use the smart project detection
- **Dynamic user detection**: Use `subprocess.getoutput('whoami')` for user-specific paths
- **Desktop output**: Audio files default to Desktop using dynamic user detection

### Dependencies and Build System
- **Zero ML dependencies**: The project intentionally uses only macOS native `say` command
- **Hatchling build**: Uses modern Python packaging with src/ layout
- **Optional MCP dependency**: `mcp>=1.0.0` only required for server mode

### Internationalization
- **Spanish documentation**: Extensive Spanish docs alongside English code
- **Accent handling**: Unicode normalization removes accents for voice matching
- **Multi-language voices**: Supports voices from multiple Spanish-speaking regions

### Hook System Integration
- **Environment-controlled**: Hooks use environment variables for configuration
- **Background execution**: All hooks run non-blocking to avoid workflow interruption
- **Content filtering**: Text is filtered to remove code blocks and markdown before TTS

### Version History Context
- **v1.5.0**: Complete restructure from TTS-macOS to TTS Notify
- **Clean architecture**: Organized under TTS_Notify/ with proper separation
- **Simplified stack**: Removed heavy ML/AI dependencies from previous versions
- **Enhanced docs**: Complete documentation suite in documentation/