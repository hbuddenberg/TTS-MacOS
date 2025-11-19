#!/bin/bash

set -e

echo "TTS-MacOS v2 - ML-Compatible Python Installation"
echo "================================================="

# Find ML-compatible Python
PYTHON_CMD=""
for cmd in "python3.12" "python3.13" "python3.11" "python3.10"; do
    if command -v "$cmd" >/dev/null 2>&1; then
        VERSION=$($cmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if [[ "$VERSION" =~ ^3\.(1[0-3])$ ]]; then
            echo "Found compatible Python: $cmd ($VERSION)"
            PYTHON_CMD="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "ERROR: No ML-compatible Python found (3.10-3.13 required)"
    echo "Install with: brew install python@3.12"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
echo "Using Python: $PYTHON_VERSION"

# Clean up existing venv
if [ -d "venv-v2" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv-v2
fi

# Create virtual environment
echo "Creating virtual environment..."
$PYTHON_CMD -m venv venv-v2

# Activate
echo "Activating virtual environment..."
source venv-v2/bin/activate

# Verify
VENV_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
echo "Virtual environment Python: $VENV_VERSION"

if [ "$VENV_VERSION" != "$PYTHON_VERSION" ]; then
    echo "ERROR: Version mismatch!"
    exit 1
fi

# Install dependencies
echo "Upgrading pip..."
pip install --upgrade pip wheel

echo "Installing core dependencies..."
pip install fastapi mcp pydantic

echo "Installing audio processing..."
pip install numpy scipy soundfile

echo "Installing PyTorch..."
pip install "torch>=2.0.0,<2.5" "torchaudio>=2.0.0,<2.5"

echo "Installing Coqui TTS..."
pip install "coqui-tts>=0.24,<0.28"

echo "Installing additional dependencies..."
pip install librosa matplotlib tqdm

# Verify
echo "Verifying Coqui TTS..."
python -c "
import TTS
print(f'SUCCESS: Coqui TTS {TTS.__version__} installed!')
"

echo ""
echo "Installation completed successfully!"
echo "=================================="
echo "Python: $PYTHON_VERSION"
echo "Coqui TTS: Ready"
echo ""
echo "To use:"
echo "  source venv-v2/bin/activate"
echo "  python -c 'from TTS.api import TTS; print(\"Ready!\")'"