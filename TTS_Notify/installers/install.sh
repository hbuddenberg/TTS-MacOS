#!/bin/bash
# TTS Notify v2.0.0 - Cross-platform Installer Script
# Supports macOS and Linux systems

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🔧 TTS Notify v2.0.0 - Cross-platform Installer${NC}"
echo -e "${BLUE}📍 Project: $PROJECT_DIR${NC}"
echo

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Function to detect OS
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos";;
        Linux*)     echo "linux";;
        CYGWIN*|MINGW*|MSYS*) echo "windows";;
        *)          echo "unknown";;
    esac
}

# Function to check if UV is installed
check_uv() {
    if command -v uv &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to install UV
install_uv() {
    print_info "Installing UV package manager..."
    if curl -LsSf https://astral.sh/uv/install.sh | sh; then
        # Add UV to PATH for current session
        export PATH="$HOME/.cargo/bin:$PATH"
        print_status "UV installed successfully"
        return 0
    else
        print_error "Failed to install UV"
        return 1
    fi
}

# Function to check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
            print_status "Python $PYTHON_VERSION OK"
            echo "PYTHON_CMD=python3" >> .env
            return 0
        else
            print_error "Python 3.10+ required, found $PYTHON_VERSION"
            return 1
        fi
    else
        print_error "Python 3 not found"
        return 1
    fi
}

# Function to check macOS TTS
check_macos_tts() {
    if [ "$(detect_os)" = "macos" ]; then
        if command -v say &> /dev/null; then
            if say -v "?" &> /dev/null; then
                print_status "macOS TTS (say command) OK"
                return 0
            else
                print_error "macOS TTS not working"
                return 1
            fi
        else
            print_error "macOS TTS not available"
            return 1
        fi
    else
        print_warning "Not macOS - TTS support may be limited"
        return 0
    fi
}

# Function to run installer
run_installer() {
    local mode="$1"
    print_info "Starting $mode installation..."

    cd "$PROJECT_DIR"

    if [ -f "src/installer/installer.py" ]; then
        python3 src/installer/installer.py "$mode"
    else
        print_error "Installer script not found"
        return 1
    fi
}

# Function to show usage
show_usage() {
    echo -e "${BLUE}TTS Notify v2.0.0 Installation Options:${NC}"
    echo
    echo "  1) Development - Install for development with virtual environment"
    echo "  2) Production  - Install CLI globally for all users"
    echo "  3) MCP Server  - Install for Claude Desktop integration"
    echo "  4) Complete    - Install all components"
    echo "  5) Uninstall   - Remove TTS Notify completely"
    echo "  6) Exit"
    echo
}

# Main installation flow
main() {
    # Check if we're in the right directory
    if [ ! -f "$PROJECT_DIR/pyproject.toml" ]; then
        print_error "pyproject.toml not found. Please run from project directory."
        exit 1
    fi

    # Show system information
    OS=$(detect_os)
    print_info "Detected OS: $OS"

    # Check prerequisites
    print_info "Checking prerequisites..."

    if ! check_python; then
        exit 1
    fi

    if ! check_macos_tts; then
        exit 1
    fi

    if ! check_uv; then
        if ! install_uv; then
            print_error "UV is required for installation"
            exit 1
        fi
    fi

    # Show installation menu
    if [ $# -eq 0 ]; then
        while true; do
            show_usage
            read -p "Select installation option (1-6): " choice
            case $choice in
                1)
                    run_installer "development"
                    break
                    ;;
                2)
                    run_installer "production"
                    break
                    ;;
                3)
                    run_installer "mcp"
                    break
                    ;;
                4)
                    run_installer "all"
                    break
                    ;;
                5)
                    run_installer "uninstall"
                    break
                    ;;
                6)
                    print_info "Installation cancelled"
                    exit 0
                    ;;
                *)
                    print_error "Invalid option. Please select 1-6."
                    ;;
            esac
        done
    else
        # Command line mode
        mode="$1"
        case $mode in
            development|production|mcp|all|uninstall)
                run_installer "$mode"
                ;;
            *)
                print_error "Invalid mode: $mode"
                echo "Valid modes: development, production, mcp, all, uninstall"
                exit 1
                ;;
        esac
    fi

    print_status "Installation process completed!"
}

# Quick install functions for convenience
install_dev() {
    main "development"
}

install_prod() {
    main "production"
}

install_mcp() {
    main "mcp"
}

install_all() {
    main "all"
}

uninstall() {
    main "uninstall"
}

# Run main function
main "$@"