@echo off
REM iLoveExcel - Install from Wheel
REM Helper script for end-users to install iLoveExcel from wheel package

echo ==========================================
echo iLoveExcel - Install from Wheel
echo ==========================================
echo.

REM Get the project root (parent of scripts/)
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
cd /d "%PROJECT_ROOT%"

echo Project root: %PROJECT_ROOT%
echo.

REM Check if wheel exists
if not exist dist\iLoveExcel-*.whl (
    echo [ERROR] No wheel file found in dist\
    echo.
    echo Please build the wheel first:
    echo   scripts\build_wheel.bat
    echo.
    pause
    exit /b 1
)

for %%f in (dist\iLoveExcel-*.whl) do set WHEEL_FILE=%%f
echo Found wheel: %WHEEL_FILE%
echo.

REM Ask user about extras
echo Installation options:
echo   1^) Basic install ^(CLI + Tkinter GUI^)
echo   2^) With PySimpleGUI [gui_pysimplegui]
echo   3^) With Streamlit web UI [gui_streamlit]
echo   4^) All extras [all]
echo.
set /p CHOICE="Select option (1-4) [default: 1]: "
if "%CHOICE%"=="" set CHOICE=1

set EXTRAS=
if "%CHOICE%"=="2" set EXTRAS=[gui_pysimplegui]
if "%CHOICE%"=="3" set EXTRAS=[gui_streamlit]
if "%CHOICE%"=="4" set EXTRAS=[all]

echo.
echo Selected: Basic + %EXTRAS%
echo.

REM Create user virtualenv
set VENV_DIR=%PROJECT_ROOT%\.venv_iloveexcel
if exist "%VENV_DIR%" (
    echo ^> Removing existing .venv_iloveexcel...
    rmdir /s /q "%VENV_DIR%"
)

echo ^> Creating virtual environment...
python -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo   [OK] Created .venv_iloveexcel\
echo.

REM Activate virtualenv
echo ^> Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
echo   [OK] Activated
echo.

REM Upgrade pip
echo ^> Upgrading pip...
python -m pip install --quiet --upgrade pip
echo   [OK] Done
echo.

REM Install wheel
echo ^> Installing iLoveExcel from wheel...
if "%EXTRAS%"=="" (
    pip install "%WHEEL_FILE%"
) else (
    pip install "%WHEEL_FILE%%EXTRAS%"
)
if errorlevel 1 (
    echo [ERROR] Installation failed
    call deactivate
    pause
    exit /b 1
)
echo   [OK] Installed
echo.

REM Show completion message
echo ==========================================
echo Installation Complete!
echo ==========================================
echo.
echo [OK] iLoveExcel is ready to use
echo.
echo To run:
echo   1. Activate the environment:
echo      .venv_iloveexcel\Scripts\activate.bat
echo.
echo   2. Launch GUI:
echo      iloveexcel
echo.
echo   3. Or use CLI:
echo      csvexcel --help
echo.
echo To deactivate when done:
echo   deactivate
echo.

REM Keep environment activated for user
echo Virtual environment is now activated for you.
echo Type 'iloveexcel' to start!
echo.

REM Don't auto-close so user can try commands
cmd /k
