# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TTS Notify v2.0.0 is a modular Text-to-Speech notification system for macOS with three interfaces: CLI, MCP (Model Context Protocol) for Claude Desktop, and REST API. The architecture underwent a complete rewrite from v1.5.0, transitioning from monolithic to modular design while maintaining 100% backward compatibility.

## Key Architecture Concepts

### Main Orchestrator Pattern
The `TTSNotifyOrchestrator` in `src/main.py` serves as the central delegation hub. It automatically detects execution mode (CLI/MCP/API) based on environment variables and arguments, then creates and manages the appropriate interface instance. All entry points flow through this orchestrator.

### Modular Core System
The core functionality is split across `src/core/`:
- **config_manager.py**: Pydantic-based configuration with 30+ environment variables and 10+ predefined profiles
- **voice_system.py**: Dynamic voice detection from macOS `say -v ?` command with 84+ voice support and caching
- **tts_engine.py**: Abstract TTS engine with concrete macOS implementation using async subprocess execution
- **models.py**: Complete type system with Pydantic models for voices, requests, and responses

### Interface Layer
All user interfaces (`src/ui/`) use the same core backend:
- **cli/**: Command-line interface maintaining v1.5.0 feature parity
- **mcp/**: FastMCP server for Claude Desktop integration with 4 tools
- **api/**: FastAPI-based REST service with OpenAPI documentation

### Configuration Hierarchy
Configuration follows strict precedence: Environment variables → YAML files → Pydantic defaults → Profile definitions. Key profiles include `claude-desktop`, `api-server`, `development`, and `production`.

## Development Commands

### Installation and Setup
```bash
# Complete installation (recommended)
./installers/install.sh all

# Development mode with virtual environment
./installers/install.sh development
source venv/bin/activate

# Alternative: UV-based installation
uv pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/test_core.py
pytest tests/test_api.py
pytest tests/test_cli.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run tests by markers
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests
```

### Code Quality
```bash
# Format code
black src tests

# Sort imports
isort src tests

# Type checking
mypy src

# Linting
flake8 src
```

### Running the Application
```bash
# Main orchestrator (auto-detects mode)
python src/main.py "Hello world"

# Force specific mode
python src/main.py --mode cli --list
python src/main.py --mode mcp
python src/main.py --mode api

# Direct interface execution
python -m ui.cli.main "Test"
python -m ui.mcp.server
python -m ui.api.server
```

## Development Workflow

### Adding New Features
1. Core functionality goes in `src/core/`
2. New interfaces follow the pattern in `src/ui/`
3. Configuration variables in `src/core/config_manager.py`
4. Add corresponding tests in `tests/`

### Environment Variables for Development
Key variables to understand:
- `TTS_NOTIFY_MODE`: Force specific execution mode
- `TTS_NOTIFY_PROFILE`: Use predefined configuration profile
- `TTS_NOTIFY_DEBUG_MODE`: Enable debug logging
- `TTS_NOTIFY_LOG_LEVEL`: Set logging level (DEBUG/INFO/WARN/ERROR)

### Voice System Understanding
The voice system parses macOS `say -v ?` output and categorizes voices into Español, Enhanced, Premium, Siri, and Others. It implements a 3-tier search algorithm (exact → prefix → partial → fallback) and caches results for 5 minutes to improve performance from ~2s to ~0.5s detection time.

### Interface Integration Points
All interfaces use the same core components:
- `VoiceManager` for voice operations
- `MacOSTTSEngine` for audio synthesis
- `TTSConfig` for configuration
- Voice detection and caching is shared across interfaces

## Testing Strategy

The project uses manual testing for TTS functionality and automated testing for configuration and models. Voice detection varies across macOS versions and voice installations, making automated voice testing challenging.

### Test Categories
- **Unit tests**: Core models, configuration validation
- **Integration tests**: CLI interface, API endpoints
- **Manual tests**: Voice operations, TTS synthesis, MCP integration

### Running Single Tests
```bash
# Test specific functionality
pytest tests/test_core.py::TestModels::test_voice_creation

# Test with verbose output
pytest -v tests/test_api.py

# Test specific marker
pytest -m "integration and not slow"
```

## Important Implementation Details

### Async Architecture
All TTS operations are async using `asyncio.create_subprocess_exec()`. The MCP server and API are fully async, while the CLI uses `asyncio.run()` to bridge sync/async boundaries.

### Error Handling
Custom exception hierarchy in `src/core/exceptions.py` with detailed error context. All interfaces implement comprehensive error handling with fallback behaviors.

### Cross-Platform Considerations
While designed for macOS TTS, the architecture supports Linux and Windows with appropriate TTS engines. The installer handles platform detection and dependency management.

### Performance Optimizations
- Voice caching with 5-minute TTL
- Connection pooling for subprocess operations
- Memory-efficient voice data handling
- Rate limiting built into request processing

## Entry Points Summary

- **`src/main.py`**: Main orchestrator with intelligent mode detection
- **`src/__main__.py`**: Package entry point calling orchestrator
- **`src/ui/cli/main.py`**: CLI interface
- **`src/ui/mcp/server.py`**: MCP server for Claude Desktop
- **`src/ui/api/server.py`**: REST API with FastAPI
- **`src/installer/installer.py`**: UV-based unified installer
- **`installers/*.sh/.bat/.ps1`**: Platform-specific installation scripts