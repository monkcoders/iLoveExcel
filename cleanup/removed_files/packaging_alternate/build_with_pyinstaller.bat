@echo off
REM build_with_pyinstaller.bat
REM Build iLoveExcel executables using PyInstaller on Windows

setlocal enabledelayedexpansion

echo ==========================================
echo  iLoveExcel - PyInstaller Build Script
echo ==========================================
echo.

REM Check if PyInstaller is installed
where pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PyInstaller is not installed.
    echo Install with: pip install pyinstaller
    exit /b 1
)

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
cd /d "%PROJECT_ROOT%"

echo Project root: %PROJECT_ROOT%
echo.

REM Default parameters
set "MODE=both"
set "BUILD_TYPE=onefile"
set "CLEAN=no"

REM Parse command-line arguments
:parse_args
if "%~1"=="" goto end_parse_args
if "%~1"=="--mode" (
    set "MODE=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--type" (
    set "BUILD_TYPE=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--clean" (
    set "CLEAN=yes"
    shift
    goto parse_args
)
if "%~1"=="--help" (
    echo Usage: %~nx0 [OPTIONS]
    echo.
    echo Options:
    echo   --mode {cli^|gui^|gui-tk^|both^|all}  What to build ^(default: both^)
    echo                                       cli:    CLI only
    echo                                       gui:    PySimpleGUI GUI only
    echo                                       gui-tk: Tkinter GUI only
    echo                                       both:   CLI + PySimpleGUI GUI
    echo                                       all:    CLI + both GUIs
    echo   --type {onefile^|onedir}            Build type ^(default: onefile^)
    echo   --clean                            Clean build directories first
    echo   --help                             Show this help message
    exit /b 0
)
echo [ERROR] Unknown option: %~1
echo Use --help for usage information
exit /b 1
:end_parse_args

echo Build configuration:
echo   Mode: %MODE%
echo   Type: %BUILD_TYPE%
echo   Clean: %CLEAN%
echo.

REM Clean build directories if requested
if "%CLEAN%"=="yes" (
    echo Cleaning build directories...
    if exist build rmdir /s /q build
    if exist dist rmdir /s /q dist
    del /q *.spec 2>nul
    echo [OK] Cleaned
    echo.
)

REM Determine PyInstaller flags
set "TYPE_FLAG="
if "%BUILD_TYPE%"=="onefile" (
    set "TYPE_FLAG=--onefile"
)

REM Build CLI
if "%MODE%"=="cli" goto build_cli
if "%MODE%"=="both" goto build_cli
if "%MODE%"=="all" goto build_cli
goto skip_cli

:build_cli
echo Building CLI executable...
pyinstaller %TYPE_FLAG% --name iLoveExcel-CLI --clean --noconfirm src\iLoveExcel\cli.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] CLI build failed
    exit /b 1
)
echo [OK] CLI build successful
echo.

:skip_cli

REM Build PySimpleGUI GUI
if "%MODE%"=="gui" goto build_gui
if "%MODE%"=="both" goto build_gui
if "%MODE%"=="all" goto build_gui
goto skip_gui

:build_gui
echo Building PySimpleGUI GUI executable...
pyinstaller %TYPE_FLAG% --windowed --name iLoveExcel-GUI --clean --noconfirm src\iLoveExcel\gui.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PySimpleGUI GUI build failed
    exit /b 1
)
echo [OK] PySimpleGUI GUI build successful
echo.

:skip_gui

REM Build Tkinter GUI
if "%MODE%"=="gui-tk" goto build_gui_tk
if "%MODE%"=="all" goto build_gui_tk
goto skip_gui_tk

:build_gui_tk
echo Building Tkinter GUI executable...
pyinstaller %TYPE_FLAG% --windowed --name iLoveExcel-TkGUI --clean --noconfirm src\iLoveExcel\gui_tk.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Tkinter GUI build failed
    exit /b 1
)
echo [OK] Tkinter GUI build successful
echo.

:skip_gui_tk

REM Summary
echo ==========================================
echo  Build Complete!
echo ==========================================
echo.
echo Executables are in: dist\
dir /b dist\

if "%BUILD_TYPE%"=="onefile" (
    echo.
    echo Single-file executables created.
    echo You can distribute the files in dist\ directly.
) else (
    echo.
    echo Folder-based executables created.
    echo Distribute the entire folder for each executable.
)

echo.
echo To test:
if "%MODE%"=="cli" (
    echo   dist\iLoveExcel-CLI.exe --help
)
if "%MODE%"=="gui" (
    echo   dist\iLoveExcel-GUI.exe
)
if "%MODE%"=="gui-tk" (
    echo   dist\iLoveExcel-TkGUI.exe
)
if "%MODE%"=="both" (
    echo   dist\iLoveExcel-CLI.exe --help
    echo   dist\iLoveExcel-GUI.exe
)
if "%MODE%"=="all" (
    echo   dist\iLoveExcel-CLI.exe --help
    echo   dist\iLoveExcel-GUI.exe
    echo   dist\iLoveExcel-TkGUI.exe
)
echo.

endlocal
