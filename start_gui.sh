#!/bin/bash
# Quick start script for iLoveExcel GUI

cd "$(dirname "$0")"

echo "Starting iLoveExcel GUI..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import PySimpleGUI" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    pip install --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
    pip install -e .
fi

# Launch GUI
echo "Launching iLoveExcel GUI..."
python -m iLoveExcel
