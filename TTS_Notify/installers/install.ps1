# TTS Notify v2.0.0 - PowerShell Installer
# Cross-platform installer for Windows systems using PowerShell

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("development", "production", "mcp", "all", "uninstall")]
    [string]$Mode = ""
)

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    White = "White"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✅ $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠️  $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "❌ $Message" "Red"
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ️  $Message" "Blue"
}

# Project directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

Write-ColorOutput "🔧 TTS Notify v2.0.0 - PowerShell Installer" "Blue"
Write-ColorOutput "📍 Project: $ProjectDir" "Blue"
Write-Host ""

# Function to check if UV is installed
function Test-UVInstalled {
    try {
        $null = Get-Command uv -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Function to install UV
function Install-UV {
    Write-Info "Installing UV package manager..."
    try {
        Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -UseBasicParsing | Invoke-Expression
        Write-Success "UV installed successfully"
        return $true
    } catch {
        Write-Error "Failed to install UV: $($_.Exception.Message)"
        return $false
    }
}

# Function to check Python version
function Test-PythonVersion {
    try {
        $pythonCmd = Get-Command python -ErrorAction Stop
        $version = & python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        $isValid = & python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"

        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python $version OK"
            "PYTHON_CMD=python" | Out-File -FilePath ".env" -Encoding UTF8
            return $true
        } else {
            Write-Error "Python 3.10+ required, found $version"
            return $false
        }
    } catch {
        Write-Error "Python not found or not working: $($_.Exception.Message)"
        return $false
    }
}

# Function to run installer
function Invoke-TTSNotifyInstaller {
    param([string]$InstallMode)

    Write-Info "Starting $InstallMode installation..."

    Set-Location $ProjectDir

    $installerPath = Join-Path $ProjectDir "src\installer\installer.py"
    if (Test-Path $installerPath) {
        try {
            & python $installerPath $InstallMode
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Installation completed successfully"
                return $true
            } else {
                Write-Error "Installation failed with exit code $LASTEXITCODE"
                return $false
            }
        } catch {
            Write-Error "Failed to run installer: $($_.Exception.Message)"
            return $false
        }
    } else {
        Write-Error "Installer script not found at $installerPath"
        return $false
    }
}

# Function to show usage
function Show-Usage {
    Write-ColorOutput "TTS Notify v2.0.0 Installation Options:" "Blue"
    Write-Host ""
    Write-Host "  1) Development - Install for development with virtual environment"
    Write-Host "  2) Production  - Install CLI globally for all users"
    Write-Host "  3) MCP Server  - Install for Claude Desktop integration"
    Write-Host "  4) Complete    - Install all components"
    Write-Host "  5) Uninstall   - Remove TTS Notify completely"
    Write-Host "  6) Exit"
    Write-Host ""
}

# Function to show interactive menu
function Show-InteractiveMenu {
    while ($true) {
        Show-Usage
        $choice = Read-Host "Select installation option (1-6)"

        switch ($choice) {
            "1" {
                Invoke-TTSNotifyInstaller "development"
                break
            }
            "2" {
                Invoke-TTSNotifyInstaller "production"
                break
            }
            "3" {
                Invoke-TTSNotifyInstaller "mcp"
                break
            }
            "4" {
                Invoke-TTSNotifyInstaller "all"
                break
            }
            "5" {
                Invoke-TTSNotifyInstaller "uninstall"
                break
            }
            "6" {
                Write-Info "Installation cancelled"
                exit 0
            }
            default {
                Write-Error "Invalid option. Please select 1-6."
            }
        }

        if ($choice -in "1","2","3","4","5") {
            break
        }
    }
}

# Main installation flow
try {
    # Check if we're in the right directory
    $pyprojectPath = Join-Path $ProjectDir "pyproject.toml"
    if (-not (Test-Path $pyprojectPath)) {
        Write-Error "pyproject.toml not found. Please run from project directory."
        exit 1
    }

    # Show system information
    Write-Info "Detected OS: Windows"

    # Check prerequisites
    Write-Info "Checking prerequisites..."

    if (-not (Test-PythonVersion)) {
        exit 1
    }

    if (-not (Test-UVInstalled)) {
        if (-not (Install-UV)) {
            Write-Error "UV is required for installation"
            exit 1
        }
    }

    # Run installation
    if ([string]::IsNullOrEmpty($Mode)) {
        Show-InteractiveMenu
    } else {
        switch ($Mode.ToLower()) {
            "development" { Invoke-TTSNotifyInstaller "development" }
            "production" { Invoke-TTSNotifyInstaller "production" }
            "mcp" { Invoke-TTSNotifyInstaller "mcp" }
            "all" { Invoke-TTSNotifyInstaller "all" }
            "uninstall" { Invoke-TTSNotifyInstaller "uninstall" }
            default {
                Write-Error "Invalid mode: $Mode"
                Write-Host "Valid modes: development, production, mcp, all, uninstall"
                exit 1
            }
        }
    }

    Write-Success "Installation process completed!"

} catch {
    Write-Error "Installation failed: $($_.Exception.Message)"
    exit 1
}