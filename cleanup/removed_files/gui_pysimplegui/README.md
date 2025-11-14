# PySimpleGUI Implementation - Archived

**Date Archived**: $(date +%Y-%m-%d)
**Reason**: Migrating to Tkinter-only GUI backend

## Files Archived

- `gui.py` - Original PySimpleGUI implementation of the GUI

## Why Removed

PySimpleGUI support has been removed in favor of a unified Tkinter-only GUI backend:
- Tkinter is included with Python by default (no extra dependencies)
- Simplifies the codebase and maintenance
- Streamlit remains available as separate web interface option

## How to Restore (if needed)

If you need to restore PySimpleGUI support:

1. Copy gui.py back to src/iLoveExcel/
   ```bash
   cp cleanup/removed_files/gui_pysimplegui/gui.py src/iLoveExcel/
   ```

2. Update gui_launcher.py to re-add PySimpleGUI backend

3. Install PySimpleGUI:
   ```bash
   pip install PySimpleGUI
   ```

## Original Functionality

The archived gui.py provided:
- CSV to Excel conversion GUI
- Excel to CSV conversion GUI
- File selection dialogs
- Progress indicators
- Error handling

All this functionality is now available via the Tkinter GUI (gui_tk.py).
