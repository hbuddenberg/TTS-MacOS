@echo off
REM TTS Notify v2.0.0 - Windows Installer Script
REM Cross-platform installer for Windows systems

setlocal enabledelayedexpansion

REM Colors (Windows 10+ supports ANSI escape codes)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Project directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."

echo %BLUE%🔧 TTS Notify v2.0.0 - Windows Installer%NC%
echo %BLUE%📍 Project: %PROJECT_DIR%%NC%
echo.

REM Function to check if UV is installed
:check_uv
where uv >nul 2>nul
if %errorlevel% equ 0 (
    echo %GREEN%✅ UV package manager found%NC%
    exit /b 0
) else (
    echo %YELLOW%⚠️  UV not found, attempting to install...%NC%
    goto :install_uv
)

:install_uv
echo Installing UV package manager...
powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
if %errorlevel% equ 0 (
    echo %GREEN%✅ UV installed successfully%NC%
    exit /b 0
) else (
    echo %RED%❌ Failed to install UV%NC%
    exit /b 1
)

REM Function to check Python version
:check_python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo %RED%❌ Python not found%NC%
    exit /b 1
)

for /f "tokens=*" %%i in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PYTHON_VERSION=%%i
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"
if %errorlevel% equ 0 (
    echo %GREEN%✅ Python %PYTHON_VERSION% OK%NC%
    echo PYTHON_CMD=python > .env
    exit /b 0
) else (
    echo %RED%❌ Python 3.10+ required, found %PYTHON_VERSION%%NC%
    exit /b 1
)

REM Function to run installer
:run_installer
set MODE=%1
echo %BLUE%ℹ️  Starting %MODE% installation...%NC%

cd /d "%PROJECT_DIR%"

if exist "src\installer\installer.py" (
    python src\installer\installer.py %MODE%
    if %errorlevel% equ 0 (
        echo %GREEN%✅ Installation completed successfully%NC%
    ) else (
        echo %RED%❌ Installation failed%NC%
        exit /b 1
    )
) else (
    echo %RED%❌ Installer script not found%NC%
    exit /b 1
)
exit /b 0

REM Function to show usage
:show_usage
echo %BLUE%TTS Notify v2.0.0 Installation Options:%NC%
echo.
echo   1) Development - Install for development with virtual environment
echo   2) Production  - Install CLI globally for all users
echo   3) MCP Server  - Install for Claude Desktop integration
echo   4) Complete    - Install all components
echo   5) Uninstall   - Remove TTS Notify completely
echo   6) Exit
echo.

REM Main installation flow
:main
REM Check if we're in the right directory
if not exist "%PROJECT_DIR%\pyproject.toml" (
    echo %RED%❌ pyproject.toml not found. Please run from project directory.%NC%
    exit /b 1
)

REM Show system information
echo %BLUE%ℹ️  Detected OS: Windows%NC%

REM Check prerequisites
echo %BLUE%ℹ️  Checking prerequisites...%NC%

call :check_python
if %errorlevel% neq 0 exit /b 1

call :check_uv
if %errorlevel% neq 0 exit /b 1

REM Show installation menu
if "%~1"=="" (
    :menu_loop
    call :show_usage
    set /p choice="Select installation option (1-6): "

    if "!choice!"=="1" (
        call :run_installer development
        goto :end
    ) else if "!choice!"=="2" (
        call :run_installer production
        goto :end
    ) else if "!choice!"=="3" (
        call :run_installer mcp
        goto :end
    ) else if "!choice!"=="4" (
        call :run_installer all
        goto :end
    ) else if "!choice!"=="5" (
        call :run_installer uninstall
        goto :end
    ) else if "!choice!"=="6" (
        echo %BLUE%ℹ️  Installation cancelled%NC%
        exit /b 0
    ) else (
        echo %RED%❌ Invalid option. Please select 1-6.%NC%
        goto :menu_loop
    )
) else (
    REM Command line mode
    set MODE=%1
    if "%MODE%"=="development" goto :install_development
    if "%MODE%"=="production" goto :install_production
    if "%MODE%"=="mcp" goto :install_mcp
    if "%MODE%"=="all" goto :install_all
    if "%MODE%"=="uninstall" goto :install_uninstall

    echo %RED%❌ Invalid mode: %MODE%%NC%
    echo Valid modes: development, production, mcp, all, uninstall
    exit /b 1
)

:install_development
call :run_installer development
goto :end

:install_production
call :run_installer production
goto :end

:install_mcp
call :run_installer mcp
goto :end

:install_all
call :run_installer all
goto :end

:install_uninstall
call :run_installer uninstall
goto :end

:end
echo %GREEN%🎉 Installation process completed!%NC%
exit /b 0

REM Call main function
call :main %*