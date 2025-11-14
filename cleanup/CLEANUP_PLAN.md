# iLoveExcel - Repository Cleanup Plan

**Date**: 2024-11-15  
**Branch**: `cleanup/<timestamp>` (to be created)  
**Goal**: Simplify repository to Tkinter-only GUI, remove PySimpleGUI, consolidate documentation

---

## 📋 Executive Summary

This plan outlines a **safe, reversible, human-approved** cleanup of the iLoveExcel repository to:

1. **Unify GUI to Tkinter** - Make Tkinter the only active GUI backend
2. **Remove PySimpleGUI** - Archive all PySimpleGUI-related files
3. **Keep Streamlit Optional** - Streamlit module stays but not installed by default
4. **Remove Packaging Extras** - Simplify to wheel build only (CLI + Tkinter GUI)
5. **Declutter Documentation** - Consolidate redundant MD files
6. **Clean Build Artifacts** - Remove venvs, dist/, build/ folders

---

## 🛡️ Safety Constraints

### Non-Breaking Rules
- ✅ **No API changes** - Public Python APIs remain unchanged
- ✅ **No runtime behavior changes** - Existing functionality preserved
- ✅ **Git branch isolation** - All work on `cleanup/<timestamp>` branch
- ✅ **Zip backup** - Full repo backup before any deletions
- ✅ **Archival, not deletion** - Files moved to `cleanup/removed_files/`
- ✅ **Human approval** - Explicit confirmation before each category
- ✅ **Test gates** - Unit tests + smoke tests after each step
- ✅ **Revert script** - One-command rollback if issues arise

### Files Never Touched (Without Explicit Approval)
- `LICENSE` - Legal requirement
- `CHANGELOG.md` - If exists, historical record
- `.gitignore`, `.git/` - Version control
- `tests/` - Unit test suite (may be updated, not removed)
- `src/iLoveExcel/__init__.py` - Public API

---

## 📂 File Categories for Cleanup

### Category 1: PySimpleGUI Files (REMOVE)
**Action**: Move to `cleanup/removed_files/gui_pysimplegui/`

```
src/iLoveExcel/gui.py                    # PySimpleGUI GUI implementation
```

**References to Update**:
- `src/iLoveExcel/gui_launcher.py` - Remove PySimpleGUI backend option
- `src/iLoveExcel/__main__.py` - Remove PySimpleGUI fallback logic
- `pyproject.toml` - Remove `gui_pysimplegui` extra
- Documentation - Remove PySimpleGUI mentions

**Impact**: PySimpleGUI GUI will no longer be available

### Category 2: Alternate Packaging Scripts (REMOVE)
**Action**: Move to `cleanup/removed_files/packaging_alternate/`

```
packaging/build_with_pyinstaller.sh      # PyInstaller build (Linux/macOS)
packaging/build_with_pyinstaller.bat     # PyInstaller build (Windows)
packaging/build_zipapp.sh                # Zipapp build (if exists)
packaging/build_zipapp.bat               # Zipapp build (if exists)
packaging/README.md                      # Packaging documentation
```

**Keep**:
```
scripts/build_wheel.sh                   # Primary wheel build
scripts/build_wheel.bat
scripts/install_from_wheel.sh
scripts/install_from_wheel.bat
```

**Impact**: Only wheel packaging will be supported going forward

### Category 3: Redundant Documentation (CONSOLIDATE)
**Action**: Move to `cleanup/removed_files/docs_redundant/`

```
IMPLEMENTATION_SUMMARY.md                # Redundant with README
GUI_START_GUIDE.md                       # Redundant with README
PROJECT_STRUCTURE.md                     # Redundant with README
DEPLOYMENT_OPTIONS.md                    # Redundant with README
INSTALL.md                               # Consolidate into README
WHEEL_PACKAGING_COMPLETE.md              # Implementation detail
docs/packaging/packaging_eval.md         # Historical comparison
docs/packaging/notes.md                  # Keep as technical reference
```

**Create**:
```
README.md                                # Concise user-facing README (simplified)
README.detailed.md                       # Move current verbose README here
docs/ARCHITECTURE.md                     # Technical architecture (if needed)
```

**Impact**: Simpler, more maintainable documentation

### Category 4: Build Artifacts & Virtual Environments (DELETE)
**Action**: Permanent deletion (not tracked in git anyway)

```
.venv/                                   # Virtual environment
build-venv/                              # Build virtual environment
build/                                   # Build artifacts
dist/                                    # Distribution files
src/iLoveExcel.egg-info/                 # Egg info
**/__pycache__/                          # Python cache
**/*.pyc, *.pyo                          # Compiled Python
.pytest_cache/                           # Pytest cache
```

**Impact**: Clean slate for builds (regenerated as needed)

### Category 5: Optional GUI Files (KEEP AS OPTIONAL)
**Action**: No changes, just mark as optional

```
streamlit_app.py                         # Keep for optional web UI
src/iLoveExcel/gui_tk.py                 # PRIMARY GUI (keep and enhance)
src/iLoveExcel/gui_common.py             # Shared GUI utilities (keep)
src/iLoveExcel/gui_launcher.py           # Update to Tkinter-only
```

**Impact**: Streamlit remains available but not installed by default

### Category 6: Packaging Extras in pyproject.toml (REMOVE)
**Action**: Update `pyproject.toml` to remove all extras except `dev`

**Remove**:
```toml
[project.optional-dependencies]
gui_pysimplegui = [...]                  # REMOVE
gui_streamlit = [...]                    # REMOVE
gui_customtkinter = [...]                # REMOVE
web = [...]                              # REMOVE
packaging = [...]                        # REMOVE
gui = [...]                              # REMOVE (combined)
all = [...]                              # REMOVE (combined)
```

**Keep**:
```toml
[project.optional-dependencies]
dev = [...]                              # Keep for developers
```

**Impact**: Simpler dependency management, smaller package

---

## 🔄 Execution Order (Step-by-Step)

### Phase 0: Preparation
1. ✅ Create `cleanup/<timestamp>` git branch
2. ✅ Create full repo zip backup to `cleanup/backup_<timestamp>.zip`
3. ✅ Run initial test suite to establish baseline
4. ✅ Generate `cleanup/cleanup_candidates.md` with file lists

### Phase 1: Code Updates (No Deletions Yet)
5. ✅ Update `src/iLoveExcel/gui_launcher.py` to default to Tkinter
6. ✅ Update `src/iLoveExcel/__main__.py` to remove PySimpleGUI fallback
7. ✅ Run unit tests + smoke test (Tkinter GUI launch)
8. ✅ Commit: "refactor: default to Tkinter GUI backend"

### Phase 2: Documentation Consolidation
9. ✅ Create simplified `README.md` (concise, user-focused)
10. ✅ Move current `README.md` to `README.detailed.md`
11. ✅ Update references in all files
12. ✅ Commit: "docs: simplify README and create detailed version"

### Phase 3: PySimpleGUI Removal (Human Approval Required)
13. 🛑 **STOP**: Present list of PySimpleGUI files for approval
14. ✅ Upon approval: `git mv src/iLoveExcel/gui.py cleanup/removed_files/gui_pysimplegui/`
15. ✅ Update imports/references (remove gui.py imports)
16. ✅ Run tests + smoke test
17. ✅ Commit: "remove: archive PySimpleGUI GUI backend"

### Phase 4: Packaging Simplification (Human Approval Required)
18. 🛑 **STOP**: Present list of packaging files for approval
19. ✅ Upon approval: Move PyInstaller/zipapp scripts to `cleanup/removed_files/packaging_alternate/`
20. ✅ Generate `pyproject.toml.patch` for extras removal
21. 🛑 **STOP**: Review patch for approval
22. ✅ Upon approval: Apply patch
23. ✅ Update `requirements.txt` (no PySimpleGUI references)
24. ✅ Run `scripts/build_wheel.sh` to test build
25. ✅ Commit: "build: simplify packaging to wheel-only"

### Phase 5: Documentation Cleanup (Human Approval Required)
26. 🛑 **STOP**: Present list of redundant docs for approval
27. ✅ Upon approval: Move redundant MDs to `cleanup/removed_files/docs_redundant/`
28. ✅ Update cross-references in remaining docs
29. ✅ Run documentation link checker
30. ✅ Commit: "docs: consolidate redundant documentation"

### Phase 6: Build Artifacts Cleanup (Human Approval Required)
31. 🛑 **STOP**: Present list of build artifacts/venvs for approval
32. ✅ Upon approval: Delete build/, dist/, .venv/, build-venv/, __pycache__/
33. ✅ Update `.gitignore` if needed
34. ✅ Commit: "chore: remove build artifacts and venvs"

### Phase 7: Final Verification
35. ✅ Run full test suite
36. ✅ Build wheel: `scripts/build_wheel.sh`
37. ✅ Test wheel install: `scripts/install_from_wheel.sh`
38. ✅ Smoke test: Launch Tkinter GUI
39. ✅ Generate `cleanup/cleanup_report.md`
40. ✅ Commit: "docs: add cleanup report"

### Phase 8: Review & Merge
41. ✅ Push `cleanup/<timestamp>` branch
42. 🛑 **STOP**: Human review of all changes
43. ✅ Create Pull Request with cleanup report
44. ✅ Merge to main (or keep on branch if reverting)

---

## 🧪 Testing Strategy

### Test Gates (Must Pass Before Proceeding)
After each phase, run:

1. **Unit Tests**
   ```bash
   pytest tests/ -v
   ```

2. **Smoke Test - CLI**
   ```bash
   csvexcel --help
   csvexcel --version
   ```

3. **Smoke Test - GUI**
   ```bash
   python3 -m iLoveExcel
   # Verify Tkinter GUI launches without errors
   ```

4. **Smoke Test - Wheel Build**
   ```bash
   ./scripts/build_wheel.sh
   # Verify wheel builds successfully
   ```

### Rollback Criteria
If any test fails:
1. Run `cleanup/revert.sh` to undo changes
2. Analyze failure
3. Fix issue
4. Re-run from failed phase

---

## 🔧 Scripts to Create

### 1. `scripts/cleanup_create_branch_and_backup.sh`
Creates branch, backup, and baseline tests

### 2. `scripts/cleanup_scan_candidates.sh`
Scans repo and generates `cleanup/cleanup_candidates.md`

### 3. `scripts/cleanup_present_and_confirm.sh`
Interactive confirmation for each category

### 4. `scripts/cleanup_move_removed_files.sh`
Moves approved files to `cleanup/removed_files/`

### 5. `scripts/cleanup_run_tests.sh`
Runs test suite and records results

### 6. `scripts/cleanup_revert.sh`
Reverts all changes and restores from backup

---

## 📊 Impact Analysis

### Before Cleanup
- **GUI Backends**: PySimpleGUI, Tkinter, Streamlit
- **Packaging Methods**: Wheel, PyInstaller, Zipapp
- **Documentation Files**: 10+ markdown files
- **Dependencies**: 15+ optional extras
- **Repo Size**: ~150 files, multiple build artifacts

### After Cleanup
- **GUI Backends**: Tkinter (primary), Streamlit (optional)
- **Packaging Methods**: Wheel only
- **Documentation Files**: 3-5 core markdown files
- **Dependencies**: 5 core + dev optional
- **Repo Size**: ~100 files, clean structure

### Benefits
✅ **Simpler maintenance** - One GUI backend to support  
✅ **Faster builds** - Single packaging method  
✅ **Clearer documentation** - Consolidated, focused  
✅ **Smaller footprint** - Fewer dependencies  
✅ **Better developer experience** - Less cognitive overhead  

### Risks
⚠️ **PySimpleGUI users** - Will need to switch to Tkinter  
⚠️ **PyInstaller users** - Will need to use wheel  
⚠️ **Documentation links** - External links may break  
⚠️ **Integration tests** - May need updates  

### Mitigation
- Keep archived files in `cleanup/removed_files/` for reference
- Add migration guide for PySimpleGUI users
- Update CHANGELOG with breaking changes
- Create tag before merge for easy rollback

---

## 📝 Human Approval Checklist

Before each phase, reviewer must approve:

### Phase 3: PySimpleGUI Removal
- [ ] Confirmed Tkinter GUI works correctly
- [ ] Reviewed list of files to be archived
- [ ] Understood impact on existing users
- [ ] **APPROVED / REJECTED**

### Phase 4: Packaging Simplification
- [ ] Reviewed `pyproject.toml` patch
- [ ] Confirmed wheel build works
- [ ] Understood impact on distribution
- [ ] **APPROVED / REJECTED**

### Phase 5: Documentation Cleanup
- [ ] Reviewed list of docs to be archived
- [ ] Confirmed remaining docs are sufficient
- [ ] Checked for broken links
- [ ] **APPROVED / REJECTED**

### Phase 6: Build Artifacts Cleanup
- [ ] Reviewed list of folders/files to delete
- [ ] Confirmed no important files in list
- [ ] Understood they will be regenerated
- [ ] **APPROVED / REJECTED**

---

## 🚨 Emergency Rollback

If anything goes wrong:

```bash
# Quick rollback
./scripts/cleanup_revert.sh

# Or manual rollback
git checkout main
git branch -D cleanup/<timestamp>
unzip cleanup/backup_<timestamp>.zip -d ../iLoveExcel_restored
```

---

## 📞 Next Steps

1. **Review this plan** - Ensure all concerns are addressed
2. **Run Phase 0** - Create branch and backup
3. **Review generated `cleanup_candidates.md`** - Verify file lists
4. **Approve or modify** - Give explicit go-ahead for each phase
5. **Execute phases** - Follow step-by-step with test gates
6. **Review final state** - Before merging to main

---

**Plan Version**: 1.0  
**Last Updated**: 2024-11-15  
**Status**: 🟡 Awaiting Approval
