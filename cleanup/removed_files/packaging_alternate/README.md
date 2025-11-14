# Alternate Packaging Scripts - Archived

**Date Archived**: 2025-11-15
**Reason**: Consolidating to wheel packaging as primary distribution method

## Files Archived

- `build_with_pyinstaller.sh` - PyInstaller build script (Linux/macOS)
- `build_with_pyinstaller.bat` - PyInstaller build script (Windows)
- `README.md` - Original packaging documentation
- `packaging_eval.md` - Packaging method evaluation
- `notes.md` - Packaging development notes
- `csv_diff_mockup.md` - UI mockup documentation

## Why Removed

Wheel packaging (via setuptools/build) is now the primary distribution method:
- Standard Python packaging format
- Easier to maintain and update
- Better dependency management
- Smaller package size
- Cross-platform compatibility built-in

PyInstaller and other standalone packaging methods are archived but available if needed.

## How to Restore (if needed)

If you need PyInstaller packaging:

1. Restore the scripts:
   ```bash
   mkdir -p packaging
   cp cleanup/removed_files/packaging_alternate/build_with_pyinstaller.* packaging/
   ```

2. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

3. Run the build:
   ```bash
   ./packaging/build_with_pyinstaller.sh
   ```

## Current Packaging Method

Use the wheel build scripts in `scripts/`:
- `scripts/build_wheel.sh` - Build wheel package
- `scripts/install_from_wheel.sh` - Install from wheel

See main README.md for packaging documentation.
