# Packaging iLoveExcel with PyInstaller

This directory contains scripts and configuration for building standalone executables of iLoveExcel.

## Quick Start

### Linux/macOS

```bash
# Make script executable
chmod +x packaging/build_with_pyinstaller.sh

# Build both CLI and GUI (default)
./packaging/build_with_pyinstaller.sh

# Build specific components
./packaging/build_with_pyinstaller.sh --mode cli      # CLI only
./packaging/build_with_pyinstaller.sh --mode gui      # PySimpleGUI GUI only
./packaging/build_with_pyinstaller.sh --mode gui-tk   # Tkinter GUI only
./packaging/build_with_pyinstaller.sh --mode all      # CLI + both GUIs

# Build as folder instead of single file (faster startup)
./packaging/build_with_pyinstaller.sh --type onedir

# Clean build first
./packaging/build_with_pyinstaller.sh --clean
```

### Windows

```cmd
REM Build both CLI and GUI (default)
packaging\build_with_pyinstaller.bat

REM Build specific components
packaging\build_with_pyinstaller.bat --mode cli      # CLI only
packaging\build_with_pyinstaller.bat --mode gui      # PySimpleGUI GUI only
packaging\build_with_pyinstaller.bat --mode gui-tk   # Tkinter GUI only
packaging\build_with_pyinstaller.bat --mode all      # CLI + both GUIs

REM Build as folder instead of single file (faster startup)
packaging\build_with_pyinstaller.bat --type onedir

REM Clean build first
packaging\build_with_pyinstaller.bat --clean
```

## Build Options

### Build Modes

- **`cli`**: Build CLI executable only (`iLoveExcel-CLI`)
- **`gui`**: Build PySimpleGUI GUI executable only (`iLoveExcel-GUI`)
- **`gui-tk`**: Build Tkinter GUI executable only (`iLoveExcel-TkGUI`)
- **`both`**: Build CLI + PySimpleGUI GUI *(default)*
- **`all`**: Build all three executables

### Build Types

- **`onefile`**: Single executable file *(default)*
  - Pros: Easy to distribute (one file)
  - Cons: Slower startup (extracts to temp), larger file size
  - Typical size: 80-120 MB

- **`onedir`**: Folder with executable and dependencies
  - Pros: Faster startup, slightly smaller total size
  - Cons: Must distribute entire folder
  - Typical size: 100-150 MB

### Options

- **`--clean`**: Remove previous build artifacts before building

## Output

After building, executables will be in the `dist/` directory:

```
dist/
├── iLoveExcel-CLI          # or .exe on Windows
├── iLoveExcel-GUI          # or .exe on Windows
└── iLoveExcel-TkGUI        # or .exe on Windows
```

For `--type onedir` builds:

```
dist/
├── iLoveExcel-CLI/
│   ├── iLoveExcel-CLI      # Main executable
│   └── _internal/          # Dependencies
├── iLoveExcel-GUI/
│   ├── iLoveExcel-GUI
│   └── _internal/
└── iLoveExcel-TkGUI/
    ├── iLoveExcel-TkGUI
    └── _internal/
```

## Prerequisites

### Install PyInstaller

```bash
pip install pyinstaller
```

### Install Project Dependencies

```bash
pip install -r requirements.txt
```

## Testing Executables

### CLI
```bash
# Linux/macOS
./dist/iLoveExcel-CLI --help
./dist/iLoveExcel-CLI csv-to-excel input1.csv input2.csv -o output.xlsx

# Windows
dist\iLoveExcel-CLI.exe --help
dist\iLoveExcel-CLI.exe csv-to-excel input1.csv input2.csv -o output.xlsx
```

### GUI (PySimpleGUI)
```bash
# Linux/macOS
./dist/iLoveExcel-GUI

# Windows
dist\iLoveExcel-GUI.exe
```

### GUI (Tkinter)
```bash
# Linux/macOS
./dist/iLoveExcel-TkGUI

# Windows
dist\iLoveExcel-TkGUI.exe
```

## Troubleshooting

### Antivirus False Positives

PyInstaller executables are sometimes flagged by antivirus software. This is a known issue:

- **Windows Defender**: May quarantine the executable
  - Solution: Add exception in Windows Security settings
  - Or: Code sign the executable (requires certificate)

- **Other AV Software**: Similar behavior
  - Submit to VirusTotal for whitelisting
  - Consider code signing

### Import Errors

If the executable fails with import errors:

1. Check that all dependencies are in `requirements.txt`
2. Try cleaning and rebuilding: `--clean`
3. Check PyInstaller warnings during build
4. Add hidden imports to spec file (see Advanced section)

### Large File Size

To reduce executable size:

1. Use `--type onedir` instead of `onefile`
2. Exclude unnecessary modules (see Advanced section)
3. Use UPX compression (install `upx` separately)

### Slow Startup (onefile mode)

`--onefile` executables extract to temp on startup:

- **Solution 1**: Use `--type onedir` for faster startup
- **Solution 2**: Accept slower startup for easier distribution

## Advanced Configuration

### Custom PyInstaller Spec File

For more control, create a custom `.spec` file:

```bash
# Generate spec file
pyinstaller --onefile --windowed --name iLoveExcel-GUI src/iLoveExcel/gui.py --specpath packaging/

# Edit packaging/iLoveExcel-GUI.spec to customize

# Build from spec
pyinstaller packaging/iLoveExcel-GUI.spec
```

### Adding Hidden Imports

If modules are not auto-detected, add to spec file:

```python
# In .spec file
a = Analysis(
    ['src/iLoveExcel/gui.py'],
    hiddenimports=['openpyxl', 'pandas', 'xlsxwriter'],
    ...
)
```

### Excluding Modules

To reduce size, exclude unnecessary modules:

```bash
pyinstaller --onefile \
    --exclude-module matplotlib \
    --exclude-module IPython \
    --exclude-module notebook \
    src/iLoveExcel/gui.py
```

### Adding Data Files

To include non-Python files (icons, data):

```bash
pyinstaller --onefile \
    --add-data "icons/:icons/" \
    src/iLoveExcel/gui.py
```

### Custom Icon

```bash
# Windows
pyinstaller --onefile --windowed --icon=icons/iLoveExcel.ico src/iLoveExcel/gui.py

# macOS
pyinstaller --onefile --windowed --icon=icons/iLoveExcel.icns src/iLoveExcel/gui.py
```

## Platform-Specific Notes

### Windows

- Executables are `.exe` files
- May need Visual C++ Redistributable
- Consider using installer (NSIS, Inno Setup)

### macOS

- Build on oldest supported macOS version
- May need to approve in System Preferences > Security
- Consider creating `.dmg` installer
- Code signing recommended for distribution

### Linux

- Build on oldest supported distro (e.g., Ubuntu 20.04)
- Resulting binary is distro-specific
- Consider AppImage for better portability
- Users may need to `chmod +x`

## Distribution

### Checksums

Generate SHA256 checksums for verification:

```bash
# Linux/macOS
shasum -a 256 dist/iLoveExcel-* > dist/SHA256SUMS

# Windows (PowerShell)
Get-FileHash dist\*.exe -Algorithm SHA256 > dist\SHA256SUMS.txt
```

### Packaging for Release

```bash
# Linux/macOS
cd dist/
tar -czf iLoveExcel-linux-x64.tar.gz iLoveExcel-*
zip -r iLoveExcel-linux-x64.zip iLoveExcel-*

# Windows
# Use 7-Zip or Windows built-in Compress
```

### GitHub Releases

Upload to GitHub Releases:

1. Create release tag (e.g., `v1.0.0`)
2. Upload executables as release assets
3. Include SHA256SUMS file
4. Add release notes

## CI/CD Integration

See `docs/packaging/packaging_eval.md` for GitHub Actions workflow examples.

## Further Reading

- [PyInstaller Documentation](https://pyinstaller.org/)
- [Packaging Evaluation](../docs/packaging/packaging_eval.md) - Comparison of packaging tools
- [Common Issues](https://pyinstaller.org/en/stable/when-things-go-wrong.html)

## Support

If you encounter issues:

1. Check PyInstaller warnings during build
2. Review [troubleshooting section](#troubleshooting)
3. Search [PyInstaller issues](https://github.com/pyinstaller/pyinstaller/issues)
4. Open issue in iLoveExcel repository
