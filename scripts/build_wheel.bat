@echo off
REM iLoveExcel - Build Wheel Distribution
REM Creates an isolated build environment and builds the Python wheel package

echo ==========================================
echo iLoveExcel Wheel Build Script
echo ==========================================
echo.

REM Get the project root (parent of scripts/)
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
cd /d "%PROJECT_ROOT%"

echo Project root: %PROJECT_ROOT%
echo.

REM Clean previous build artifacts
echo ^> Cleaning previous build artifacts...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.egg-info rmdir /s /q *.egg-info
if exist src\*.egg-info rmdir /s /q src\*.egg-info
echo   [OK] Cleaned dist/, build/, *.egg-info
echo.

REM Create isolated build environment
set BUILD_VENV=%PROJECT_ROOT%\build-venv
if exist "%BUILD_VENV%" (
    echo ^> Removing existing build-venv...
    rmdir /s /q "%BUILD_VENV%"
)

echo ^> Creating isolated build environment...
python -m venv "%BUILD_VENV%"
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    exit /b 1
)
echo   [OK] Created build-venv\
echo.

REM Activate build environment
echo ^> Activating build environment...
call "%BUILD_VENV%\Scripts\activate.bat"
echo   [OK] Activated
echo.

REM Upgrade pip and install build tools
echo ^> Installing build tools...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet build wheel setuptools>=65.0
echo   [OK] Installed: build, wheel, setuptools
echo.

REM Build the wheel
echo ^> Building wheel package...
python -m build --wheel
if errorlevel 1 (
    echo [ERROR] Build failed
    deactivate
    exit /b 1
)
echo   [OK] Wheel built successfully
echo.

REM Deactivate build environment
call deactivate

REM Show results
echo ==========================================
echo Build Complete!
echo ==========================================
echo.
echo [Package] Wheel package created:
dir /b dist\*.whl
echo.
echo Next steps:
echo   1. Test the wheel:
echo      scripts\install_from_wheel.bat
echo.
echo   2. Or manually install in a new venv:
echo      python -m venv test-venv
echo      test-venv\Scripts\activate.bat
echo      pip install dist\iLoveExcel-*.whl
echo      iloveexcel  :: Launch GUI
echo.
echo   3. Install with optional extras:
echo      pip install dist\iLoveExcel-*.whl[gui_pysimplegui]
echo      pip install dist\iLoveExcel-*.whl[all]
echo.
echo   4. Distribute:
echo      - Share dist\iLoveExcel-*.whl + requirements.txt
echo      - Or upload to PyPI: twine upload dist\*
echo.

pause
