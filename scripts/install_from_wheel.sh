#!/bin/bash
# iLoveExcel - Install from Wheel
# Helper script for end-users to install iLoveExcel from wheel package

set -e  # Exit on any error

echo "=========================================="
echo "iLoveExcel - Install from Wheel"
echo "=========================================="
echo ""

# Get the project root (parent of scripts/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Project root: $PROJECT_ROOT"
echo ""

# Check if wheel exists
if [ ! -f dist/iLoveExcel-*.whl ]; then
    echo "❌ ERROR: No wheel file found in dist/"
    echo ""
    echo "Please build the wheel first:"
    echo "  ./scripts/build_wheel.sh"
    echo ""
    exit 1
fi

WHEEL_FILE=$(ls dist/iLoveExcel-*.whl | head -n 1)
echo "Found wheel: $(basename "$WHEEL_FILE")"
echo ""

# Ask user about extras
echo "Installation options:"
echo "  1) Basic install (CLI + Tkinter GUI)"
echo "  2) With PySimpleGUI [gui_pysimplegui]"
echo "  3) With Streamlit web UI [gui_streamlit]"
echo "  4) All extras [all]"
echo ""
read -p "Select option (1-4) [default: 1]: " CHOICE
CHOICE=${CHOICE:-1}

EXTRAS=""
case $CHOICE in
    2) EXTRAS="[gui_pysimplegui]";;
    3) EXTRAS="[gui_streamlit]";;
    4) EXTRAS="[all]";;
    *) EXTRAS="";;
esac

echo ""
echo "Selected: Basic + $EXTRAS"
echo ""

# Create user virtualenv
VENV_DIR="$PROJECT_ROOT/.venv_iloveexcel"
if [ -d "$VENV_DIR" ]; then
    echo "→ Removing existing .venv_iloveexcel..."
    rm -rf "$VENV_DIR"
fi

echo "→ Creating virtual environment..."
python3 -m venv "$VENV_DIR"
echo "  ✓ Created .venv_iloveexcel/"
echo ""

# Activate virtualenv
echo "→ Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "  ✓ Activated"
echo ""

# Upgrade pip
echo "→ Upgrading pip..."
pip install --quiet --upgrade pip
echo "  ✓ Done"
echo ""

# Install wheel
echo "→ Installing iLoveExcel from wheel..."
if [ -z "$EXTRAS" ]; then
    pip install "$WHEEL_FILE"
else
    pip install "$WHEEL_FILE$EXTRAS"
fi
echo "  ✓ Installed"
echo ""

# Check for tkinter on Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "→ Checking Tkinter availability..."
    if ! python3 -c "import tkinter" 2>/dev/null; then
        echo "  ⚠️  WARNING: Tkinter not available"
        echo ""
        echo "To install Tkinter:"
        if command -v apt-get &> /dev/null; then
            echo "  sudo apt-get install python3-tk"
        elif command -v dnf &> /dev/null; then
            echo "  sudo dnf install python3-tkinter"
        elif command -v pacman &> /dev/null; then
            echo "  sudo pacman -S tk"
        else
            echo "  Install python3-tk package for your distribution"
        fi
        echo ""
    else
        echo "  ✓ Tkinter available"
        echo ""
    fi
fi

# Show completion message
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "✅ iLoveExcel is ready to use"
echo ""
echo "To run:"
echo "  1. Activate the environment:"
echo "     source .venv_iloveexcel/bin/activate"
echo ""
echo "  2. Launch GUI:"
echo "     iloveexcel"
echo ""
echo "  3. Or use CLI:"
echo "     csvexcel --help"
echo ""
echo "To deactivate when done:"
echo "  deactivate"
echo ""

# Keep environment activated for user
echo "Virtual environment is now activated for you."
echo "Type 'iloveexcel' to start!"
echo ""
