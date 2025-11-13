@echo off
REM Quick start script for iLoveExcel GUI (Windows)

cd /d "%~dp0"

echo Starting iLoveExcel GUI...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import PySimpleGUI" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    pip install --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
    pip install -e .
)

REM Launch GUI
echo Launching iLoveExcel GUI...
python -m iLoveExcel

pause
