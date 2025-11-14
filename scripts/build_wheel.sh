#!/bin/bash
# iLoveExcel - Build Wheel Distribution
# Creates an isolated build environment and builds the Python wheel package

set -e  # Exit on any error

echo "=========================================="
echo "iLoveExcel Wheel Build Script"
echo "=========================================="
echo ""

# Get the project root (parent of scripts/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Project root: $PROJECT_ROOT"
echo ""

# Clean previous build artifacts
echo "→ Cleaning previous build artifacts..."
rm -rf dist/ build/ *.egg-info src/*.egg-info
echo "  ✓ Cleaned dist/, build/, *.egg-info"
echo ""

# Create isolated build environment
BUILD_VENV="$PROJECT_ROOT/build-venv"
if [ -d "$BUILD_VENV" ]; then
    echo "→ Removing existing build-venv..."
    rm -rf "$BUILD_VENV"
fi

echo "→ Creating isolated build environment..."
python3 -m venv "$BUILD_VENV"
echo "  ✓ Created build-venv/"
echo ""

# Activate build environment
echo "→ Activating build environment..."
source "$BUILD_VENV/bin/activate"
echo "  ✓ Activated"
echo ""

# Upgrade pip and install build tools
echo "→ Installing build tools..."
pip install --quiet --upgrade pip
pip install --quiet build wheel setuptools>=65.0
echo "  ✓ Installed: build, wheel, setuptools"
echo ""

# Build the wheel
echo "→ Building wheel package..."
python -m build --wheel
echo "  ✓ Wheel built successfully"
echo ""

# Deactivate build environment
deactivate

# Show results
echo "=========================================="
echo "Build Complete!"
echo "=========================================="
echo ""
echo "📦 Wheel package created:"
ls -lh dist/*.whl
echo ""
echo "Next steps:"
echo "  1. Test the wheel:"
echo "     ./scripts/install_from_wheel.sh"
echo ""
echo "  2. Or manually install in a new venv:"
echo "     python3 -m venv test-venv"
echo "     source test-venv/bin/activate"
echo "     pip install dist/iLoveExcel-*.whl"
echo "     iloveexcel  # Launch GUI"
echo ""
echo "  3. Install with optional extras:"
echo "     pip install dist/iLoveExcel-*.whl[gui_pysimplegui]"
echo "     pip install dist/iLoveExcel-*.whl[all]"
echo ""
echo "  4. Distribute:"
echo "     - Share dist/iLoveExcel-*.whl + requirements.txt"
echo "     - Or upload to PyPI: twine upload dist/*"
echo ""
