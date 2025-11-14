# iLoveExcel - Wheel Packaging Quick Reference

## 🎯 Quick Start

### For Developers: Build the Wheel

```bash
./scripts/build_wheel.sh          # Linux/macOS
scripts\build_wheel.bat           # Windows

# Output: dist/iloveexcel-0.1.0-py3-none-any.whl (~50KB)
```

### For End Users: Install from Wheel

```bash
./scripts/install_from_wheel.sh   # Linux/macOS (interactive)
scripts\install_from_wheel.bat    # Windows (interactive)

# Or manual install
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate.bat
pip install dist/iloveexcel-*.whl
iloveexcel  # Launch GUI
```

---

## 📦 Distribution Methods

| Method | Command | Size | Python Required |
|--------|---------|------|-----------------|
| **Wheel** | `./scripts/build_wheel.sh` | ~50KB | Yes (3.10+) |
| **Zipapp** | `./packaging/build_zipapp.sh` | ~2-5MB | Yes (3.10+) |
| **PyInstaller** | `./packaging/build_with_pyinstaller.sh --mode all` | ~50-150MB | No |

---

## 🎨 Optional Extras

Install additional GUI backends on demand:

```bash
# Base install (CLI + Tkinter GUI)
pip install dist/iloveexcel-*.whl

# With PySimpleGUI
pip install dist/iloveexcel-*.whl[gui_pysimplegui]

# With Streamlit web UI
pip install dist/iloveexcel-*.whl[gui_streamlit]

# With customtkinter (modern Tkinter)
pip install dist/iloveexcel-*.whl[gui_customtkinter]

# All GUI backends
pip install dist/iloveexcel-*.whl[gui]

# Everything (GUIs + dev tools)
pip install dist/iloveexcel-*.whl[all]
```

**Available Extras:**
- `[gui_pysimplegui]` - PySimpleGUI desktop GUI
- `[gui_streamlit]` - Streamlit web interface  
- `[gui_customtkinter]` - Modern Tkinter variant
- `[web]` - All web interfaces
- `[packaging]` - Build tools (build, twine, setuptools, wheel)
- `[dev]` - Dev tools (pytest, black, mypy, ruff)
- `[gui]` - All GUI backends
- `[all]` - Everything

---

## 🚀 Commands

### Build Commands

```bash
# Build wheel (recommended)
./scripts/build_wheel.sh

# Build zipapp
./packaging/build_zipapp.sh

# Build PyInstaller executables
./packaging/build_with_pyinstaller.sh --mode all
```

### Install Commands

```bash
# Interactive install with extras selection
./scripts/install_from_wheel.sh

# Manual install
pip install dist/iloveexcel-*.whl

# Install with extras
pip install dist/iloveexcel-*.whl[gui_pysimplegui]
```

### Run Commands

```bash
# After installation, two commands are available:

# 1. GUI (Tkinter by default)
iloveexcel

# 2. CLI
csvexcel --help
csvexcel csv-to-excel file1.csv file2.csv -o output.xlsx
csvexcel union-multiple *.csv -o combined.csv
csvexcel join left.csv right.csv -o joined.csv --on "id"
```

---

## 🐧 Linux: Tkinter Installation

If Tkinter is not available on Linux:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

**Note:** The `iloveexcel` command will check for Tkinter and show installation instructions if missing.

---

## 📤 Publish to PyPI (Optional)

```bash
# Install publishing tools
pip install twine

# Build the wheel
./scripts/build_wheel.sh

# Upload to PyPI
twine upload dist/iloveexcel-*.whl

# Users can then install with:
pip install iLoveExcel
```

---

## 🔧 Troubleshooting

### Build Issues

**Error: "No module named 'build'"**
```bash
pip install build
```

**Error: "version not found"**
```python
# Check src/iLoveExcel/__init__.py has:
__version__ = '0.1.0'
```

### Install Issues

**Error: "Tkinter is not available"**
```bash
# See Linux installation section above
sudo apt-get install python3-tk  # Ubuntu/Debian
```

**Error: "No module named 'PySimpleGUI'"**
```bash
# Install PySimpleGUI extra
pip install dist/iloveexcel-*.whl[gui_pysimplegui]
```

---

## 📁 File Structure

```
iLoveExcel/
├── scripts/                          # 🆕 Build and install helpers
│   ├── build_wheel.sh               # Build wheel (Linux/macOS)
│   ├── build_wheel.bat              # Build wheel (Windows)
│   ├── install_from_wheel.sh        # Install helper (Linux/macOS)
│   └── install_from_wheel.bat       # Install helper (Windows)
│
├── dist/                            # 🆕 Build outputs
│   └── iloveexcel-0.1.0-py3-none-any.whl  # Wheel package (~50KB)
│
├── docs/packaging/                  # 🆕 Documentation
│   └── notes.md                     # Technical deep-dive (5000+ lines)
│
├── pyproject.toml                   # ✏️ Updated: dynamic version, extras
├── requirements.txt                 # ✏️ Updated: version ranges
├── README.md                        # ✏️ Updated: packaging section
├── MANIFEST.in                      # 🆕 Source distribution control
└── WHEEL_PACKAGING_COMPLETE.md      # 🆕 Implementation summary
```

---

## 📋 What's Different?

### Before (PySimpleGUI-centric)
- PySimpleGUI required in base install
- Single GUI option
- No wheel packaging
- Manual dependency management

### After (Flexible with Extras)
- ✅ Tkinter as default (open-source, built-in)
- ✅ PySimpleGUI optional (via extras)
- ✅ Streamlit optional (via extras)
- ✅ Wheel packaging with build scripts
- ✅ Automated install helpers
- ✅ Smaller base install (~50KB wheel + core deps)
- ✅ User choice of GUI backends
- ✅ Backwards compatible (no breaking changes)

---

## 🎯 Use Cases

### Scenario 1: Python Developer (Quick Install)
```bash
pip install dist/iloveexcel-*.whl
iloveexcel  # Uses Tkinter GUI (open-source)
```

### Scenario 2: PySimpleGUI User (Keep Existing GUI)
```bash
pip install dist/iloveexcel-*.whl[gui_pysimplegui]
iloveexcel  # Uses Tkinter by default, but PySimpleGUI available
```

### Scenario 3: Web Deployment (Streamlit)
```bash
pip install dist/iloveexcel-*.whl[gui_streamlit]
streamlit run streamlit_app.py
```

### Scenario 4: Non-Python User (Standalone)
```bash
./packaging/build_with_pyinstaller.sh --mode gui-tk
# Share: dist/iLoveExcel-TkGUI
# User double-clicks to run (no Python needed)
```

### Scenario 5: CI/CD Integration
```bash
# In CI pipeline
pip install dist/iloveexcel-*.whl
csvexcel union-multiple *.csv -o combined.csv
```

---

## 📖 Documentation

- **README.md** - Main user guide (includes packaging section)
- **docs/packaging/notes.md** - Technical documentation (5000+ lines)
- **WHEEL_PACKAGING_COMPLETE.md** - Implementation summary
- **This file** - Quick reference card

---

## ✅ Checklist for Distribution

- [x] Build wheel: `./scripts/build_wheel.sh`
- [ ] Test installation: `./scripts/install_from_wheel.sh`
- [ ] Test GUI: `iloveexcel`
- [ ] Test CLI: `csvexcel --help`
- [ ] Test extras: `pip install dist/iloveexcel-*.whl[gui_pysimplegui]`
- [ ] (Optional) Publish to PyPI: `twine upload dist/*`

---

**Quick Reference Version**: 1.0.0  
**Last Updated**: 2024-11-15  
**Status**: ✅ Ready for use
