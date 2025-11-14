# iLoveExcel - Packaging Technical Notes

This document provides technical details about the wheel-based packaging system for iLoveExcel.

## Table of Contents

1. [Overview](#overview)
2. [Build System](#build-system)
3. [Dependency Management](#dependency-management)
4. [Extras System](#extras-system)
5. [Entry Points](#entry-points)
6. [Distribution Files](#distribution-files)
7. [Manylinux Wheels](#manylinux-wheels)
8. [Publishing to PyPI](#publishing-to-pypi)
9. [Tradeoffs](#tradeoffs)
10. [Troubleshooting](#troubleshooting)

---

## Overview

iLoveExcel uses a **modern Python packaging workflow** based on:
- **PEP 517/518**: Build system specification
- **Setuptools**: Build backend
- **src-layout**: Best practice package structure
- **Wheel format**: Binary distribution format
- **pyproject.toml**: Unified configuration

### Why Wheels?

Wheels are the **standard binary distribution format** for Python packages:
- ✅ Fast installation (no build step)
- ✅ Small size (~50KB for pure Python)
- ✅ Easy to publish (PyPI, internal repos)
- ✅ Dependencies managed by pip
- ✅ Integrates with existing Python tooling
- ✅ Cross-platform (pure Python wheels)

### Distribution Strategy

iLoveExcel provides **3 distribution methods** for different audiences:

| Method | Target Audience | Size | Python Required |
|--------|----------------|------|-----------------|
| **Wheel** | Python developers, CI/CD | ~50KB | Yes |
| **Zipapp** | Power users, quick sharing | ~2-5MB | Yes |
| **PyInstaller** | Non-technical users | ~50-150MB | No |

---

## Build System

### pyproject.toml

The build system is configured in `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"
```

**Key settings:**
- `setuptools>=65.0`: Modern setuptools with PEP 621 support
- `wheel`: Generates `.whl` files
- `setuptools.build_meta`: PEP 517 build backend

### Dynamic Versioning

Version is read from `src/iLoveExcel/__init__.py`:

```python
# src/iLoveExcel/__init__.py
__version__ = '0.1.0'
```

```toml
# pyproject.toml
[project]
dynamic = ["version"]

[tool.setuptools.dynamic]
version = {attr = "iLoveExcel.__version__"}
```

**Benefits:**
- ✅ Single source of truth
- ✅ No version drift
- ✅ Easy to update

**To update version:**
1. Edit `src/iLoveExcel/__init__.py`
2. Rebuild: `./scripts/build_wheel.sh`

### Build Scripts

**build_wheel.sh** (Linux/macOS):
- Creates isolated virtualenv (`build-venv/`)
- Installs build tools (`pip`, `build`, `setuptools`, `wheel`)
- Runs `python -m build --wheel`
- Produces `dist/iLoveExcel-<version>-py3-none-any.whl`

**build_wheel.bat** (Windows):
- Equivalent functionality for Windows
- Uses `call` and `cmd` commands

**Why isolated venv?**
- ✅ Clean build environment
- ✅ Reproducible builds
- ✅ No interference from development dependencies

---

## Dependency Management

### Core Dependencies

Pinned with **minimum version + upper bound** for stability:

```toml
dependencies = [
    "pandas>=2.0.0,<3.0.0",       # Data processing
    "openpyxl>=3.1.0,<4.0.0",     # Excel read/write
    "xlsxwriter>=3.1.0,<4.0.0",   # Excel formatting
    "click>=8.1.0,<9.0.0",        # CLI framework
    "tqdm>=4.65.0,<5.0.0",        # Progress bars
]
```

**Why pinning strategy?**
- ✅ `>=X.0.0`: Allow bug fixes and minor features
- ✅ `<(X+1).0.0`: Prevent breaking changes
- ✅ Balance stability vs updates

### requirements.txt

User-facing dependency list matching `pyproject.toml`:

```txt
pandas>=2.0.0,<3.0.0
openpyxl>=3.1.0,<4.0.0
xlsxwriter>=3.1.0,<4.0.0
click>=8.1.0,<9.0.0
tqdm>=4.65.0,<5.0.0
```

**Purpose:**
- Installation without wheel: `pip install -r requirements.txt`
- Lock files: `pip freeze > requirements.lock`
- Documentation: Shows users what's needed

### Tkinter Dependency

**Tkinter is NOT in requirements** because:
- ✅ Included with Python standard library
- ✅ No pip package needed
- ❌ Requires system package on Linux

**Linux installation:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

**Runtime check** in `__main__.py`:
```python
def check_tkinter_available():
    try:
        import tkinter
        return True
    except ImportError:
        print("Error: Tkinter is not available...")
        return False
```

---

## Extras System

### What are Extras?

Extras are **optional dependency groups** that users can install on demand:

```bash
pip install iLoveExcel[gui_pysimplegui]  # Install with PySimpleGUI
pip install iLoveExcel[all]              # Install everything
```

### Available Extras

```toml
[project.optional-dependencies]
gui_pysimplegui = ["PySimpleGUI>=4.60.0,<5.0.0"]
gui_streamlit = ["streamlit>=1.28.0,<2.0.0"]
gui_customtkinter = ["customtkinter>=5.0.0,<6.0.0"]
web = ["streamlit>=1.28.0,<2.0.0"]
packaging = ["build>=1.0.0", "twine>=4.0.0", "setuptools>=65.0", "wheel"]
dev = ["pytest>=7.4.0", "pytest-cov>=4.1.0", "black>=23.0.0", "mypy>=1.5.0", "ruff>=0.1.0"]
gui = ["PySimpleGUI>=4.60.0,<5.0.0", "streamlit>=1.28.0,<2.0.0", "customtkinter>=5.0.0,<6.0.0"]
all = ["PySimpleGUI>=4.60.0,<5.0.0", "streamlit>=1.28.0,<2.0.0", "customtkinter>=5.0.0,<6.0.0", "pytest>=7.4.0", "pytest-cov>=4.1.0", "black>=23.0.0", "mypy>=1.5.0", "ruff>=0.1.0", "build>=1.0.0", "twine>=4.0.0", "setuptools>=65.0", "wheel"]
```

### Why Extras?

**Advantages:**
- ✅ **Smaller base install**: Only Tkinter GUI (~50KB wheel + core deps)
- ✅ **User choice**: Install only what's needed
- ✅ **Backwards compatible**: PySimpleGUI users can still install it
- ✅ **Development tools**: Devs install `[dev]`, users don't need it

**Use cases:**
- Base install: CLI + Tkinter GUI (open-source, minimal)
- PySimpleGUI users: `[gui_pysimplegui]`
- Web hosting: `[gui_streamlit]`
- Developers: `[dev]` for testing/linting
- Package maintainers: `[packaging]` for build/publish
- Power users: `[all]` for everything

### Combined Extras

- **`[gui]`**: All GUI backends (PySimpleGUI + Streamlit + customtkinter)
- **`[all]`**: Everything (GUIs + dev tools + packaging tools)

---

## Entry Points

### Console Scripts

Defined in `pyproject.toml`:

```toml
[project.scripts]
iloveexcel = "iLoveExcel.__main__:launch_from_cli"
csvexcel = "iLoveExcel.cli:main"
```

**What happens when installed?**

pip creates executable scripts in `bin/` (Linux/macOS) or `Scripts/` (Windows):

```bash
# Linux/macOS
~/.venv/bin/iloveexcel     # Launches Tkinter GUI
~/.venv/bin/csvexcel       # Launches CLI

# Windows
.venv\Scripts\iloveexcel.exe
.venv\Scripts\csvexcel.exe
```

### Entry Point Functions

**iloveexcel → launch_from_cli():**
```python
def launch_from_cli():
    """Entry point for iloveexcel console script."""
    if not check_tkinter_available():
        sys.exit(1)
    launch_gui('tkinter')
```

**csvexcel → main():**
```python
@click.group()
def main():
    """iLoveExcel CLI - CSV and Excel operations"""
    pass
```

### Why Two Entry Points?

- **`iloveexcel`**: GUI launcher (Tkinter by default)
  - Simple: just type `iloveexcel`
  - Checks Tkinter availability
  - Can switch backends via environment variable

- **`csvexcel`**: CLI interface (Click commands)
  - Existing API (backwards compatible)
  - No GUI dependencies
  - Scriptable for automation

---

## Distribution Files

### What's in the Wheel?

```
iLoveExcel-0.1.0-py3-none-any.whl
├── iLoveExcel/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── gui.py
│   ├── gui_tk.py
│   ├── gui_common.py
│   ├── gui_launcher.py
│   ├── diffs.py
│   ├── io_helpers.py
│   ├── io.py
│   ├── joins.py
│   ├── unions.py
│   ├── excel_merge.py
│   └── utils.py
├── iLoveExcel-0.1.0.dist-info/
│   ├── METADATA            # Package metadata
│   ├── WHEEL               # Wheel metadata
│   ├── entry_points.txt    # Console scripts
│   ├── top_level.txt       # Top-level modules
│   └── RECORD              # File checksums
└── [no dependencies bundled]
```

**Key points:**
- ✅ Only Python code (`.py` files)
- ✅ Metadata in `.dist-info/`
- ✅ Entry points for `iloveexcel` and `csvexcel`
- ❌ No dependencies (installed separately by pip)
- ❌ No data files (unless in `MANIFEST.in`)

### MANIFEST.in

Controls **source distribution** (`.tar.gz`) contents:

```
include README.md LICENSE requirements.txt pyproject.toml
recursive-include src *.py *.pyi
exclude .git* .venv* dist/ build/
prune tests examples docs
```

**Why exclude tests/examples/docs?**
- ✅ Smaller source distribution
- ✅ Only runtime code included
- ✅ Tests run during development, not needed by users

### Wheel Filename

Format: `{distribution}-{version}-{python}-{abi}-{platform}.whl`

Example: `iLoveExcel-0.1.0-py3-none-any.whl`

**Breakdown:**
- `iLoveExcel`: Package name
- `0.1.0`: Version
- `py3`: Python 3.x compatible
- `none`: No C extensions (pure Python)
- `any`: Works on any platform

---

## Manylinux Wheels

### What is Manylinux?

**Manylinux** is a standard for building **binary wheels** that work across many Linux distributions.

**iLoveExcel is pure Python**, so we don't need manylinux wheels! Our wheel is `py3-none-any`.

### When would you need manylinux?

If your project has **binary dependencies** (C extensions):
- pandas (depends on NumPy with C code)
- Pillow (image processing)
- lxml (XML parser)

**But wait, pandas is a dependency!**

Yes, but pandas **ships its own manylinux wheels**:
- `pandas-2.0.0-cp310-cp310-manylinux_2_17_x86_64.whl`

When users `pip install iLoveExcel`, pip automatically:
1. Downloads iLoveExcel wheel
2. Sees pandas>=2.0.0 requirement
3. Downloads **pre-built pandas manylinux wheel**
4. No compilation needed!

### Platform-Specific Builds

Current wheel: `py3-none-any` (universal)

If you add **platform-specific code** (e.g., Windows registry access):
```bash
python -m build --wheel  # Creates platform-specific wheel
# Result: iLoveExcel-0.1.0-py3-none-win_amd64.whl
```

**Best practice**: Keep code cross-platform when possible.

---

## Publishing to PyPI

### Prerequisites

1. **Create PyPI account**: https://pypi.org/account/register/
2. **Install twine**: `pip install twine`
3. **Get API token**: https://pypi.org/manage/account/token/

### Publishing Steps

**1. Build wheel:**
```bash
./scripts/build_wheel.sh
```

**2. Test upload (TestPyPI first):**
```bash
twine upload --repository testpypi dist/iLoveExcel-*.whl
```

**3. Test install:**
```bash
pip install --index-url https://test.pypi.org/simple/ iLoveExcel
```

**4. Upload to production PyPI:**
```bash
twine upload dist/iLoveExcel-*.whl
```

**5. Users can now install:**
```bash
pip install iLoveExcel
```

### Versioning Strategy

Follow **Semantic Versioning** (SemVer):
- `MAJOR.MINOR.PATCH`
- Example: `0.1.0` → `0.2.0` → `1.0.0`

**Rules:**
- `MAJOR`: Breaking changes (incompatible API)
- `MINOR`: New features (backwards compatible)
- `PATCH`: Bug fixes (backwards compatible)

**Pre-releases:**
- `0.1.0a1` - Alpha
- `0.1.0b1` - Beta
- `0.1.0rc1` - Release candidate

### GitHub Releases

Automate with GitHub Actions:

```yaml
# .github/workflows/release.yml
name: Build and Publish

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install build twine
      - run: python -m build --wheel
      - run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

---

## Tradeoffs

### Wheel vs Zipapp vs PyInstaller

| Feature | Wheel | Zipapp | PyInstaller |
|---------|-------|--------|-------------|
| **File Size** | ~50KB | ~2-5MB | ~50-150MB |
| **Python Required** | Yes (3.10+) | Yes (3.10+) | No |
| **Install Steps** | 2-3 commands | 0 (just run) | 0 (just run) |
| **Dependencies** | Separate install | Bundled (most) | Bundled (all) |
| **Cross-Platform** | Yes (pure Python) | Yes | No (build per platform) |
| **Distribution** | PyPI, repos | Single file | Single executable |
| **Updates** | `pip install --upgrade` | Re-download | Re-download |
| **Build Time** | ~5 seconds | ~10 seconds | ~60 seconds |
| **Startup Time** | Fast | Fast | Slow (unpacks to temp) |
| **Antivirus Issues** | No | No | Yes (false positives) |
| **Best For** | Python developers | Power users | Non-technical users |

### Wheel Advantages

✅ **Small size**: Only Python code (~50KB)
✅ **Fast installation**: No build step
✅ **Standard format**: Works with all Python tools
✅ **Easy updates**: `pip install --upgrade`
✅ **Extras system**: Optional dependencies
✅ **PyPI publishing**: Reach millions of users
✅ **CI/CD friendly**: Automated builds/deploys

### Wheel Disadvantages

❌ **Requires Python**: Users need Python 3.10+
❌ **Dependency management**: Users must install deps
❌ **Not standalone**: Can't run without Python
❌ **Tkinter on Linux**: Requires system package

### When to Use Each Method

**Use Wheel when:**
- Target audience is Python developers
- Publishing to PyPI
- Integrating with CI/CD
- Want smallest file size
- Need optional extras

**Use Zipapp when:**
- Quick sharing with colleagues
- Portable demo/prototype
- Users have Python installed
- Want single file (but not full standalone)

**Use PyInstaller when:**
- Target audience is non-technical users
- No Python on target systems
- Want native desktop app feel
- File size not a concern

---

## Troubleshooting

### Build Failures

**Error: "No module named 'build'"**

Solution:
```bash
pip install build
```

**Error: "version not found in iLoveExcel.__init__"**

Solution: Ensure `__version__` is defined:
```python
# src/iLoveExcel/__init__.py
__version__ = '0.1.0'
```

**Error: "invalid pyproject.toml"**

Solution: Validate syntax:
```bash
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
```

### Installation Failures

**Error: "No matching distribution found for iLoveExcel"**

Solution: Check Python version:
```bash
python --version  # Must be 3.10+
```

**Error: "Tkinter is not available"**

Solution (Linux):
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter # Fedora/RHEL
sudo pacman -S tk                # Arch Linux
```

**Error: "pandas requires numpy"**

Solution: Let pip handle it:
```bash
pip install iLoveExcel  # pip installs numpy automatically
```

### Runtime Issues

**Error: "ModuleNotFoundError: No module named 'PySimpleGUI'"**

Solution: Install extras:
```bash
pip install iLoveExcel[gui_pysimplegui]
```

**Error: "No backend available"**

Solution: Check installed GUIs:
```bash
python -c "import tkinter; print('Tkinter OK')"
python -c "import PySimpleGUI; print('PySimpleGUI OK')"
```

### Publishing Issues

**Error: "403 Forbidden" on PyPI upload**

Solution: Check credentials:
```bash
# Use API token, not password
twine upload --username __token__ --password <your-token> dist/*
```

**Error: "File already exists"**

Solution: Increment version:
```python
# src/iLoveExcel/__init__.py
__version__ = '0.1.1'  # Increment
```

---

## Additional Resources

- **PEP 517**: Build system specification
- **PEP 518**: pyproject.toml specification
- **PEP 621**: Project metadata
- **PEP 427**: Wheel format
- **Setuptools docs**: https://setuptools.pypa.io/
- **Python Packaging Guide**: https://packaging.python.org/
- **PyPI publishing**: https://packaging.python.org/tutorials/packaging-projects/

---

**Document Version**: 1.0.0
**Last Updated**: 2024
**Maintainer**: @monkcoders
