# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TTS-macOS is a Text-to-Speech tool for macOS that operates in three modes:
1. **MCP Server** - Integrates with Claude Desktop as an MCP server
2. **CLI Tool** - Standalone command-line tool (installed globally)
3. **UVX Mode** - Direct execution without installation (like npx)

The project uses macOS's native TTS engine (`say` command), requiring zero external dependencies for speech synthesis.

## Project Structure

```
mcp-tts-macos/
├── server.py              # MCP server - async execution with mcp.server
├── src/tts_macos/
│   ├── cli.py            # CLI implementation with dynamic voice detection
│   ├── __main__.py       # Entry point for `python -m tts_macos`
│   └── __init__.py
├── pyproject.toml        # Modern Python packaging (hatchling)
├── setup.py              # Legacy setup for compatibility
├── install.sh            # MCP server installer (creates venv, config)
├── install-cli.sh        # CLI global installer
└── requirements.txt      # Python dependencies (mcp>=1.0.0)
```

## Core Architecture

### Voice Detection System

Both `server.py` and `src/tts_macos/cli.py` implement **dynamic voice detection** by parsing `say -v ?` output at runtime. This is critical for cross-version compatibility.

**Key functions:**
- `get_system_voices()` / `obtener_voces_sistema()` - Parses `say -v ?` to build voice mapping
- `find_voice_in_system()` / `buscar_voz_en_sistema()` - Flexible voice search with 3 strategies:
  1. Exact match (accent-insensitive via `normalize_text()`)
  2. Prefix match (e.g., "siri" finds "Siri Female")
  3. Partial substring match
- `normalize_text()` - Uses `unicodedata.normalize('NFD')` to strip accents for comparison

**Fallback chain:** User query → Exact match → Prefix match → Substring match → First Spanish voice → "Monica"

### MCP Server (server.py)

- **Framework:** Uses `mcp.server.stdio` for async stdio communication
- **Tools exposed:**
  - `speak_text` - TTS playback with voice/rate params
  - `list_voices` - Categorized voice listing (Español, Siri, Enhanced/Premium)
  - `save_audio` - Save to Desktop as AIFF
- **Async pattern:** `asyncio.create_subprocess_exec()` for non-blocking `say` command execution
- **Voice categories:** Detects Spanish, Siri, Enhanced, Premium voices via keyword matching in `say -v ?` output

### CLI Tool (src/tts_macos/cli.py)

- **Entry points:**
  - `tts-macos` command (via pyproject.toml `project.scripts`)
  - `python -m tts_macos` (via `__main__.py`)
  - `uvx --from . tts-macos` (uvx mode)
- **Key design:** No hardcoded voice `choices` in argparse - accepts any string and performs flexible search
- **Version:** Stored in `__version__` variable (currently "1.2.1")

## Development Commands

### Testing MCP Server

```bash
cd mcp-tts-macos
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py  # Waits for MCP stdio connections
```

Test by configuring in `~/Library/Application Support/Claude/claude_desktop_config.json` and using Claude Desktop.

### Testing CLI

```bash
# Direct module execution
python3 src/tts_macos/cli.py "Test message"
python3 -m tts_macos "Test message"

# With uvx (recommended for dev - no installation)
uvx --from . tts-macos "Test message"
uvx --from . tts-macos --list
uvx --from . tts-macos "Test" --voice jorge --rate 200

# After global install
tts-macos "Test message"
tts-macos --help
```

### Installing

```bash
# MCP server - creates venv and configures Claude Desktop
./install.sh

# CLI globally - offers 3 installation methods
./install-cli.sh

# Test voice detection
say -v ? | head -10
python3 -c "from src.tts_macos.cli import obtener_voces_sistema; print(obtener_voces_sistema())"
```

## Key Implementation Details

### Accent-Insensitive Text Normalization

```python
def normalize_text(text: str) -> str:
    """Removes accents using NFD decomposition"""
    nfd = unicodedata.normalize('NFD', text)
    without_accents = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
    return without_accents.lower()
```

This enables queries like "angelica" to match "Angélica".

### Voice Categorization

Both CLI and server categorize voices by scanning `say -v ?` output for keywords:
- **Spanish:** `'spanish'` or `'español'` in line
- **Siri:** `'siri'` in line
- **Enhanced:** `'enhanced'` in line
- **Premium:** `'premium'` in line

### File Output Path

Audio files save to Desktop:
```python
output_path = f"/Users/{subprocess.getoutput('whoami')}/Desktop/{filename}"
```

Always appends `.aiff` extension if missing.

### Rate Validation

CLI validates speech rate in `main()`:
```python
if not 100 <= args.rate <= 300:
    print("⚠️  Velocidad debe estar entre 100 y 300 palabras por minuto")
```

Server schema enforces via JSON schema `minimum`/`maximum`.

## Package Configuration

The project uses **pyproject.toml** (PEP 621) with hatchling as build backend:
- **Entry points:** `tts-macos` and `tts` commands both point to `tts_macos.cli:main`
- **Optional dependencies:** `[project.optional-dependencies.mcp]` for server mode
- **Build targets:** `hatch.build.targets.wheel` specifies `packages = ["src/tts_macos"]`

Legacy `setup.py` exists for compatibility but pyproject.toml is authoritative.

## Claude Desktop Integration

MCP server requires absolute paths in config:
```json
{
  "mcpServers": {
    "tts-macos": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

`install.sh` auto-generates this config using `$PROJECT_DIR` variable.

## Troubleshooting

**Voice not found:** Check `say -v ? | grep -i spanish` to verify voice installation. Install missing voices via System Preferences → Accessibility → Spoken Content → System Voices.

**MCP server not connecting:**
1. Verify absolute paths in `claude_desktop_config.json`
2. Check venv activation: `which python` should show `venv/bin/python`
3. Restart Claude Desktop (Cmd+Q)
4. Check logs: `~/Library/Logs/Claude/`

**CLI command not found:** Ensure `~/.local/bin` or installation directory is in `$PATH`.

## Critical Code Locations

- **Voice detection logic:** `server.py:32-161`, `cli.py:14-173`
- **Flexible search:** `server.py:117-161` (`find_voice_in_system`), `cli.py:128-173` (`buscar_voz_en_sistema`)
- **MCP tool handlers:** `server.py:254-391`
- **CLI argument parsing:** `cli.py:295-355`
- **Rate validation:** `cli.py:368-370`
- **File save path:** `server.py:368`, `cli.py:219`

## Development Notes

- **Preserve voice detection:** The dynamic `say -v ?` parsing is essential - never hardcode voice lists
- **Accent handling:** Always use `normalize_text()` when comparing voice names
- **No test suite:** Manual testing only (see examples in README.md)
- **Bilingual docs:** Spanish documentation alongside English code comments
- **AIFF format:** macOS native format, no conversion needed
- **Python 3.10+:** Required for type hints and modern syntax
