#!/bin/bash

# TTS-MacOS v2 - Installation Script for Dependencies
# This script sets up the virtual environment and installs required packages

set -e

echo "🚀 TTS-MacOS v2 - Installing Dependencies..."

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Please run this script from the v2 directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv-v2" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv-v2
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv-v2/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip

# Install basic requirements first
echo "📚 Installing basic requirements..."
pip install wheel setuptools

# Install platform-specific dependencies
echo "🍎 Detecting platform..."
PLATFORM=$(uname)

if [ "$PLATFORM" = "Darwin" ]; then
    echo "🍎 macOS detected - installing libsndfile..."
    # Check if libsndfile is installed
    if ! brew list libsndfile &>/dev/null; then
        echo "Installing libsndfile via Homebrew..."
        brew install libsndfile
    else
        echo "libsndfile already installed"
    fi
elif [ "$PLATFORM" = "Linux" ]; then
    echo "🐧 Linux detected - checking for espeak-ng..."
    # Check if espeak-ng is available
    if ! command -v espeak-ng &>/dev/null; then
        echo "⚠️  Warning: espeak-ng not found. Install with: sudo apt-get install espeak-ng"
    fi
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Test imports
echo "🧪 Testing imports..."
python -c "
try:
    import mcp
    print('✅ mcp imported successfully')
except ImportError as e:
    print(f'❌ mcp import failed: {e}')

try:
    import pydantic
    print('✅ pydantic imported successfully')
except ImportError as e:
    print(f'❌ pydantic import failed: {e}')

try:
    import torch
    print('✅ torch imported successfully')
    print(f'🔥 CUDA available: {torch.cuda.is_available()}')
except ImportError as e:
    print(f'❌ torch import failed: {e}')

try:
    import TTS
    print('✅ TTS imported successfully')
except ImportError as e:
    print(f'❌ TTS import failed: {e}')
"

# Create activation script for convenience
cat > activate-v2.sh << 'EOF'
#!/bin/bash
# TTS-MacOS v2 Environment Activation Script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "$SCRIPT_DIR/venv-v2/bin/activate"
echo "🎯 TTS-MacOS v2 environment activated!"
echo "📦 Python: $(python --version)"
echo "📂 Working directory: $(pwd)"
EOF

chmod +x activate-v2.sh

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎯 To activate the TTS-MacOS v2 environment:"
echo "   source activate-v2.sh"
echo ""
echo "🚀 To test the system:"
echo "   python -c \"from v2.engines import EngineSelector; print('Engine selector works!')\""
echo ""
echo "📚 For GPU support (if available):"
echo "   pip install torch-audio"
echo ""
