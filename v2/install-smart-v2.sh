#!/bin/bash

# TTS-MacOS v2 - Smart Installation Script (v2.0)
# Reads Python compatibility from pyproject.toml and ensures correct version

set -e

echo "TTS-MacOS v2 - Smart Installation (pyproject.toml aware)"
echo "=========================================================="

# Function to extract Python version requirements from pyproject.toml
get_python_requirements() {
    if [ -f "pyproject.toml" ]; then
        # Extract requires-python line
        local python_req=$(grep -o 'requires-python = "[^"]*"' pyproject.toml | cut -d'"' -f2)
        echo "$python_req"
    else
        echo ">=3.10, <3.14"  # Fallback
    fi
}

# Function to parse version requirement and extract min/max
parse_python_requirement() {
    local requirement="$1"

    # Extract minimum version (>=X.Y)
    local min_version=$(echo "$requirement" | grep -o '>=[0-9]\+\.[0-9]\+' | grep -o '[0-9]\+\.[0-9]\+')

    # Extract maximum version (<X.Y)
    local max_version=$(echo "$requirement" | grep -o '<[0-9]\+\.[0-9]\+' | grep -o '[0-9]\+\.[0-9]\+')

    echo "$min_version,$max_version"
}

# Function to check if Python version satisfies requirement
check_version_requirement() {
    local version="$1"
    local min_version="$2"
    local max_version="$3"

    if [ -n "$min_version" ]; then
        if ! python3 -c "import sys; exit(0 if tuple(map(int, sys.version.split('.')[:2])) >= tuple(map(int, '$min_version'.split('.'))) else 1)"; then
            return 1
        fi
    fi

    if [ -n "$max_version" ]; then
        if ! python3 -c "import sys; exit(0 if tuple(map(int, sys.version.split('.')[:2])) < tuple(map(int, '$max_version'.split('.'))) else 1)"; then
            return 1
        fi
    fi

    return 0
}

# Function to check if Python command is compatible
is_python_compatible() {
    local python_cmd="$1"
    local min_version="$2"
    local max_version="$3"

    if ! command -v "$python_cmd" >/dev/null 2>&1; then
        return 1
    fi

    # Get version in format X.Y
    local version=$($python_cmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

    # Check against requirements
    if [ -n "$min_version" ]; then
        if ! python3 -c "import sys; exit(0 if tuple(map(int, '$version'.split('.'))) >= tuple(map(int, '$min_version'.split('.'))) else 1)"; then
            return 1
        fi
    fi

    if [ -n "$max_version" ]; then
        if ! python3 -c "import sys; exit(0 if tuple(map(int, '$version'.split('.'))) < tuple(map(int, '$max_version'.split('.'))) else 1)"; then
            return 1
        fi
    fi

    return 0
}

# Read Python requirements from project configuration
echo "Reading Python requirements from pyproject.toml..."
PYTHON_REQUIREMENTS=$(get_python_requirements)
echo "Project requires Python: $PYTHON_REQUIREMENTS"

# Parse requirements
IFS=',' read -r MIN_VERSION MAX_VERSION <<< "$(parse_python_requirement "$PYTHON_REQUIREMENTS")"
echo "Minimum: ${MIN_VERSION:-not specified}, Maximum: ${MAX_VERSION:-not specified}"

# Find compatible Python version
echo ""
echo "Searching for compatible Python version..."

PYTHON_CMD=""

# Try preferred versions in order
for version in "3.13" "3.12" "3.11" "3.10"; do
    for cmd in "python$version" "/opt/homebrew/bin/python$version" "/usr/local/bin/python$version"; do
        if is_python_compatible "$cmd" "$MIN_VERSION" "$MAX_VERSION"; then
            full_version=$($cmd --version 2>&1)
            echo "✓ Found compatible Python: $cmd ($full_version)"
            PYTHON_CMD="$cmd"
            break 2
        fi
    done
done

# Fallback to python3 if compatible
if [ -z "$PYTHON_CMD" ]; then
    if is_python_compatible "python3" "$MIN_VERSION" "$MAX_VERSION"; then
        full_version=$(python3 --version 2>&1)
        echo "✓ Using system python3: ($full_version)"
        PYTHON_CMD="python3"
    fi
fi

# If no compatible Python found, show error and suggestions
if [ -z "$PYTHON_CMD" ]; then
    echo ""
    echo "❌ ERROR: No compatible Python version found!"
    echo "Project requirements: $PYTHON_REQUIREMENTS"
    echo ""
    echo "💡 Solutions:"
    if [ "$MIN_VERSION" != "" ] && [ "$MAX_VERSION" != "" ]; then
        echo "Install Python between $MIN_VERSION and $MAX_VERSION:"
    elif [ "$MIN_VERSION" != "" ]; then
        echo "Install Python $MIN_VERSION or higher:"
    else
        echo "Install a compatible Python version:"
    fi
    echo ""
    echo "  # With Homebrew (recommended):"
    if [ "$MAX_VERSION" != "" ]; then
        echo "  brew install python@3.12"
        echo "  brew install python@3.13"
    else
        echo "  brew install python@3.12"
    fi
    echo ""
    echo "  # With pyenv:"
    echo "  pyenv install 3.12.8"
    echo "  pyenv global 3.12.8"
    exit 1
fi

# Get and display selected Python version
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
echo ""
echo "🚀 Selected Python: $PYTHON_VERSION"

# Validate version compatibility one more time
if ! check_version_requirement "$PYTHON_VERSION" "$MIN_VERSION" "$MAX_VERSION"; then
    echo "❌ ERROR: Selected Python version doesn't meet project requirements"
    exit 1
fi

# Clean up existing venv if present
if [ -d "venv-v2" ]; then
    echo "🧹 Removing existing virtual environment..."
    rm -rf venv-v2
fi

# Create virtual environment
echo "📦 Creating virtual environment with compatible Python..."
$PYTHON_CMD -m venv venv-v2

# Activate and verify
echo "🔌 Activating virtual environment..."
source venv-v2/bin/activate

VENV_PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
echo "✓ Virtual environment Python: $VENV_PYTHON_VERSION"

if [ "$VENV_PYTHON_VERSION" != "$PYTHON_VERSION" ]; then
    echo "❌ ERROR: Version mismatch in virtual environment!"
    exit 1
fi

# Install project dependencies using pyproject.toml
echo ""
echo "📚 Installing project dependencies from pyproject.toml..."

# Upgrade pip first
echo "⬆️  Upgrading pip..."
pip install --upgrade pip wheel

# Install project in editable mode
echo "🔧 Installing TTS-MacOS v2.0..."
if [ -f "pyproject.toml" ]; then
    pip install -e .
else
    echo "⚠️  pyproject.toml not found, installing core dependencies manually..."
    pip install fastapi mcp pydantic numpy scipy soundfile torch torchaudio "TTS>=0.22.0"
fi

# Verify critical installation
echo ""
echo "🔍 Verifying installation..."
python -c "
try:
    import sys
    print(f'✓ Python {sys.version.split()[0]}')
except ImportError as e:
    print(f'❌ Python verification failed: {e}')
    exit(1)
"

# Test TTS components
python -c "
try:
    import mcp
    print('✓ MCP installed')
except ImportError as e:
    print(f'❌ MCP not found: {e}')

try:
    import TTS
    print(f'✓ Coqui TTS {TTS.__version__} installed successfully!')
except ImportError as e:
    print(f'❌ Coqui TTS not found: {e}')
    exit(1)

try:
    import torch
    print(f'✓ PyTorch {torch.__version__} installed successfully!')
except ImportError as e:
    print(f'❌ PyTorch not found: {e}')
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation completed successfully!"
    echo "=================================="
    echo "✓ TTS-MacOS v2.0 installed"
    echo "✓ Python: $PYTHON_VERSION (meets project requirements: $PYTHON_REQUIREMENTS)"
    echo "✓ Coqui TTS: Ready to use"
    echo "✓ Virtual Environment: venv-v2"
    echo ""
    echo "🚀 Usage:"
    echo "  source venv-v2/bin/activate"
    echo "  tts-macos-v2 --help"
    echo "  tts-macos-v2 'Hello from TTS-MacOS v2!'"
    echo ""
    echo "📖 Or test Coqui TTS directly:"
    echo "  python -c 'from TTS.api import TTS; print(\"Coqui TTS ready!\")'"
else
    echo ""
    echo "❌ Installation verification failed"
    echo "Check the error messages above for details"
    exit 1
fi