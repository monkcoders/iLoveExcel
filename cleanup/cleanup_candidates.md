# iLoveExcel - Cleanup Candidates

**Generated**: $(date)  
**Purpose**: List files identified for removal, archival, or cleanup

**Legend**:
- 🗑️ **REMOVE** - Move to `cleanup/removed_files/`
- 📦 **ARCHIVE** - Move to `cleanup/removed_files/` but keep reference
- 🔧 **UPDATE** - Modify file content
- ✅ **KEEP** - No changes needed
- ❌ **DELETE** - Permanent deletion (build artifacts only)

---

## Category 1: PySimpleGUI Files

**Action**: 🗑️ Move to `cleanup/removed_files/gui_pysimplegui/`

### Source Files
- `src/iLoveExcel/gui_launcher.py` - 
- `src/iLoveExcel/gui.py` - 

### References to Update
- `DEPLOYMENT_OPTIONS.md` - 3 references
- `docs/packaging/notes.md` - 10 references
- `GUI_START_GUIDE.md` - 2 references
- `IMPLEMENTATION_SUMMARY.md` - 3 references
- `INSTALL.md` - 6 references
- `PROJECT_STRUCTURE.md` - 4 references
- `pyproject.toml` - 4 references
- `QUICK_REFERENCE.md` - 14 references
- `README.md` - 12 references
- `src/iLoveExcel/gui_common.py` - 1 references
- `src/iLoveExcel/gui_launcher.py` - 20 references
- `src/iLoveExcel/gui.py` - 6 references
- `src/iLoveExcel/gui_tk.py` - 1 references
- `src/iLoveExcel/__main__.py` - 16 references

---

## Category 2: Alternate Packaging Scripts

**Action**: 📦 Move to `cleanup/removed_files/packaging_alternate/`

### PyInstaller Scripts
- `packaging/build_with_pyinstaller.bat` - 188 lines
- `packaging/build_with_pyinstaller.sh` - 207 lines

### Packaging Documentation
- `packaging/README.md` - 318 lines
- `docs/ui_mockups/csv_diff_mockup.md` - 313 lines
- `docs/packaging/packaging_eval.md` - 0 lines
- `docs/packaging/notes.md` - 640 lines

### Keep (Primary Wheel Build)
- ✅ `scripts/build_wheel.sh`
- ✅ `scripts/build_wheel.bat`
- ✅ `scripts/install_from_wheel.sh`
- ✅ `scripts/install_from_wheel.bat`

---

## Category 3: Redundant Documentation

**Action**: 📦 Move to `cleanup/removed_files/docs_redundant/`

### Potentially Redundant Files
- `./IMPLEMENTATION_SUMMARY.md` - 493 lines
- `./QUICK_REFERENCE.md` - 291 lines
- `./DEPLOYMENT_OPTIONS.md` - 357 lines
- `./PROJECT_STRUCTURE.md` - 309 lines
- `./INSTALL.md` - 283 lines
- `./GUI_START_GUIDE.md` - 103 lines

### Documentation in docs/
- `docs/ui_mockups/csv_diff_mockup.md` - 313 lines
- `docs/packaging/packaging_eval.md` - 0 lines
- `docs/packaging/notes.md` - 640 lines

### Recommended Actions
- **CREATE**: `README.md` (simplified, ~200 lines, user-focused)
- **CREATE**: `README.detailed.md` (move current verbose README here)
- **KEEP**: `LICENSE`, `CHANGELOG.md` (if exists)
- **ARCHIVE**: Implementation summaries, installation guides (consolidate into README)

---

## Category 4: Build Artifacts & Virtual Environments

**Action**: ❌ Permanent deletion (not tracked in git)

### Virtual Environments
- `./build-venv/` - 18M
- `./.venv/` - 501M

### Build Directories
- `./build/` - 200K
- `./dist/` - 56K
- `./src/iLoveExcel.egg-info/` - 48K

### Python Cache
- `./build-venv/lib/python3.10/site-packages/build/_compat/__pycache__/` - 20K
- `./build-venv/lib/python3.10/site-packages/build/__pycache__/` - 72K
- `./build-venv/lib/python3.10/site-packages/wheel/vendored/packaging/__pycache__/` - 132K
- `./build-venv/lib/python3.10/site-packages/wheel/vendored/__pycache__/` - 8.0K
- `./build-venv/lib/python3.10/site-packages/wheel/cli/__pycache__/` - 36K
- `./build-venv/lib/python3.10/site-packages/wheel/__pycache__/` - 68K
- `./build-venv/lib/python3.10/site-packages/packaging/licenses/__pycache__/` - 52K
- `./build-venv/lib/python3.10/site-packages/packaging/__pycache__/` - 160K
- `./build-venv/lib/python3.10/site-packages/setuptools/_distutils/__pycache__/` - 336K
- `./build-venv/lib/python3.10/site-packages/setuptools/_distutils/command/__pycache__/` - 212K
- _(and more...)_

### Pytest Cache

---

## Category 5: pyproject.toml Extras

**Action**: 🔧 Update `pyproject.toml` to remove extras

### Current Extras (from pyproject.toml)
- `gui_pysimplegui`
- `gui_streamlit`
- `gui`
- `web`
- `all`
- `dev`
- `packaging`
- `large-data`
- `csvexcel`
- `iloveexcel`
- `dynamic`
- `where`
- `iLoveExcel`
- `testpaths`
- `python_files`
- `python_classes`
- `python_functions`
- `python_version`
- `warn_return_any`
- `warn_unused_configs`
- `disallow_untyped_defs`
- `disallow_incomplete_defs`
- `line-length`
- `target-version`

### Recommended Changes
- **REMOVE**: `gui_pysimplegui` - PySimpleGUI no longer supported
- **REMOVE**: `gui_streamlit` - Streamlit optional, not as extra
- **REMOVE**: `gui_customtkinter` - Not implemented
- **REMOVE**: `web` - Combined extra, not needed
- **REMOVE**: `packaging` - Dev tools, not user-facing
- **REMOVE**: `gui` - Combined extra, not needed
- **REMOVE**: `all` - Combined extra, not needed
- **KEEP**: `dev` - Developer tools (pytest, black, mypy, ruff)

---

## Category 6: Dead Code Candidates

**Action**: ✅ **SKIP - ALL FILES ARE IMPORTANT**

### Decision: Keep All Source Files
All files in this category are confirmed as important and functional:
- ✅ `src/iLoveExcel/unions.py` - KEEP (important functionality)
- ✅ `src/iLoveExcel/gui_common.py` - KEEP (shared GUI utilities)
- ✅ `src/iLoveExcel/io_helpers.py` - KEEP (I/O operations)
- ✅ `src/iLoveExcel/joins.py` - KEEP (join operations)
- ✅ `src/iLoveExcel/diffs.py` - KEEP (CSV diff feature)
- ✅ `src/iLoveExcel/utils.py` - KEEP (utility functions)
- ✅ `src/iLoveExcel/gui_launcher.py` - KEEP (GUI entry point)
- ✅ `src/iLoveExcel/excel_merge.py` - KEEP (merge functionality)
- ✅ `src/iLoveExcel/gui_tk.py` - KEEP (Tkinter GUI)
- ✅ `src/iLoveExcel/cli.py` - KEEP (CLI interface)

**Note**: No dead code removal will be performed. All source files preserved.

---

## Summary Statistics

### File Counts
- Python files: 14
- Test files: 6
- Markdown files: 20
- Shell scripts: 8

### Estimated Impact
- **Files to archive**: ~15-20 files
- **Files to delete**: Build artifacts (regenerated as needed)
- **Files to update**: 5-10 files (remove PySimpleGUI references)
- **Disk space saved**: ~50-100 MB (after removing venvs/build artifacts)

---

## Next Steps

1. **Review this document carefully**
2. **Approve or modify each category**
3. **Run**: `./scripts/cleanup_present_and_confirm.sh`
4. **Execute approved cleanup operations**

---

**Generated by**: `scripts/cleanup_scan_candidates.sh`  
**Review required**: YES ✋  
**Auto-execution**: NO ❌
