#!/bin/bash
# build_with_pyinstaller.sh
# Build iLoveExcel executables using PyInstaller on Linux/macOS

set -e  # Exit on error

echo "=========================================="
echo " iLoveExcel - PyInstaller Build Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo -e "${RED}Error: PyInstaller is not installed.${NC}"
    echo "Install with: pip install pyinstaller"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "Project root: $PROJECT_ROOT"
echo ""

# Parse command-line arguments
MODE="both"  # Options: cli, gui, gui-tk, both, all
BUILD_TYPE="onefile"  # Options: onefile, onedir
CLEAN="no"

while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --type)
            BUILD_TYPE="$2"
            shift 2
            ;;
        --clean)
            CLEAN="yes"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --mode {cli|gui|gui-tk|both|all}  What to build (default: both)"
            echo "                                      cli:    CLI only"
            echo "                                      gui:    PySimpleGUI GUI only"
            echo "                                      gui-tk: Tkinter GUI only"
            echo "                                      both:   CLI + PySimpleGUI GUI"
            echo "                                      all:    CLI + both GUIs"
            echo "  --type {onefile|onedir}            Build type (default: onefile)"
            echo "  --clean                            Clean build directories first"
            echo "  --help                             Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "Build configuration:"
echo "  Mode: $MODE"
echo "  Type: $BUILD_TYPE"
echo "  Clean: $CLEAN"
echo ""

# Clean build directories if requested
if [ "$CLEAN" = "yes" ]; then
    echo -e "${YELLOW}Cleaning build directories...${NC}"
    rm -rf build/ dist/ *.spec
    echo -e "${GREEN}✓ Cleaned${NC}"
    echo ""
fi

# Determine PyInstaller flags
if [ "$BUILD_TYPE" = "onefile" ]; then
    TYPE_FLAG="--onefile"
else
    TYPE_FLAG=""
fi

# Function to build CLI
build_cli() {
    echo -e "${YELLOW}Building CLI executable...${NC}"
    pyinstaller $TYPE_FLAG \
        --name iLoveExcel-CLI \
        --clean \
        --noconfirm \
        src/iLoveExcel/cli.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ CLI build successful${NC}"
    else
        echo -e "${RED}✗ CLI build failed${NC}"
        exit 1
    fi
    echo ""
}

# Function to build PySimpleGUI GUI
build_gui() {
    echo -e "${YELLOW}Building PySimpleGUI GUI executable...${NC}"
    pyinstaller $TYPE_FLAG \
        --windowed \
        --name iLoveExcel-GUI \
        --clean \
        --noconfirm \
        src/iLoveExcel/gui.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ PySimpleGUI GUI build successful${NC}"
    else
        echo -e "${RED}✗ PySimpleGUI GUI build failed${NC}"
        exit 1
    fi
    echo ""
}

# Function to build Tkinter GUI
build_gui_tk() {
    echo -e "${YELLOW}Building Tkinter GUI executable...${NC}"
    pyinstaller $TYPE_FLAG \
        --windowed \
        --name iLoveExcel-TkGUI \
        --clean \
        --noconfirm \
        src/iLoveExcel/gui_tk.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Tkinter GUI build successful${NC}"
    else
        echo -e "${RED}✗ Tkinter GUI build failed${NC}"
        exit 1
    fi
    echo ""
}

# Build based on mode
case $MODE in
    cli)
        build_cli
        ;;
    gui)
        build_gui
        ;;
    gui-tk)
        build_gui_tk
        ;;
    both)
        build_cli
        build_gui
        ;;
    all)
        build_cli
        build_gui
        build_gui_tk
        ;;
    *)
        echo -e "${RED}Invalid mode: $MODE${NC}"
        exit 1
        ;;
esac

# Summary
echo "=========================================="
echo -e "${GREEN} Build Complete! ${NC}"
echo "=========================================="
echo ""
echo "Executables are in: dist/"
ls -lh dist/

if [ "$BUILD_TYPE" = "onefile" ]; then
    echo ""
    echo "Single-file executables created."
    echo "You can distribute the files in dist/ directly."
else
    echo ""
    echo "Folder-based executables created."
    echo "Distribute the entire folder for each executable."
fi

echo ""
echo "To test:"
if [ "$MODE" = "cli" ] || [ "$MODE" = "both" ] || [ "$MODE" = "all" ]; then
    echo "  ./dist/iLoveExcel-CLI --help"
fi
if [ "$MODE" = "gui" ] || [ "$MODE" = "both" ] || [ "$MODE" = "all" ]; then
    echo "  ./dist/iLoveExcel-GUI"
fi
if [ "$MODE" = "gui-tk" ] || [ "$MODE" = "all" ]; then
    echo "  ./dist/iLoveExcel-TkGUI"
fi
echo ""
