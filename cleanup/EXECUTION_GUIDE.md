# iLoveExcel - Repository Cleanup: Complete Guide

**Status**: 🟢 Ready for execution  
**Date**: 2024-11-15  
**Version**: 1.0

---

## 📋 Quick Start

### For the Human Reviewer

This cleanup will safely remove PySimpleGUI dependencies and simplify the repository to Tkinter-only GUI. All operations are **safe**, **reversible**, and **human-approved**.

**Time Required**: ~30-60 minutes  
**Risk Level**: 🟢 Low (full backup + revert script)  
**Breaking Changes**: Yes (PySimpleGUI users must switch to Tkinter)

---

## 🚀 Step-by-Step Execution

### Step 1: Create Branch and Backup (5 minutes)

```bash
cd /home/abhishek/projects/iLoveExcel/iLoveExcel
./scripts/cleanup_create_branch_and_backup.sh
```

**What this does**:
- Creates git branch `cleanup/<timestamp>`
- Creates full repo backup zip
- Runs baseline tests
- Creates `cleanup/cleanup_state.txt`

**Review before proceeding**:
- Backup file exists and has reasonable size
- Baseline test results recorded
- You're on the cleanup branch

---

### Step 2: Scan Repository (5 minutes)

```bash
./scripts/cleanup_scan_candidates.sh
```

**What this does**:
- Scans for PySimpleGUI files
- Finds alternate packaging scripts
- Lists redundant documentation
- Detects build artifacts
- Generates `cleanup/cleanup_candidates.md`

**Review before proceeding**:
```bash
cat cleanup/cleanup_candidates.md | less
```

**Check**:
- File lists are accurate
- No important files flagged for removal
- Understand impact of each category

---

### Step 3: Update Code (No Deletions Yet) (10 minutes)

**3a. Update gui_launcher.py**:
```bash
# Review the new version
cat cleanup/gui_launcher.py.new

# If approved, apply it
cp cleanup/gui_launcher.py.new src/iLoveExcel/gui_launcher.py
git add src/iLoveExcel/gui_launcher.py
git commit -m "refactor: simplify gui_launcher to Tkinter-only"
```

**3b. Test the change**:
```bash
./scripts/cleanup_run_tests.sh
```

**3c. Smoke test - Launch GUI**:
```bash
python3 -m iLoveExcel
# Verify Tkinter GUI launches without errors
# Then close the GUI
```

---

### Step 4: Remove PySimpleGUI Files (5 minutes)

**STOP**: Review list of files to remove:
```bash
grep -A 20 "Category 1: PySimpleGUI Files" cleanup/cleanup_candidates.md
```

**If approved**, execute:
```bash
# Create archive directory
mkdir -p cleanup/removed_files/gui_pysimplegui

# Move PySimpleGUI GUI file
git mv src/iLoveExcel/gui.py cleanup/removed_files/gui_pysimplegui/
git commit -m "remove: archive PySimpleGUI GUI backend"

# Run tests
./scripts/cleanup_run_tests.sh
```

---

### Step 5: Update pyproject.toml (5 minutes)

**STOP**: Review the patch:
```bash
cat cleanup/pyproject.toml.patch
```

**If approved**, apply manually:
```bash
# Edit pyproject.toml to remove extras
nano pyproject.toml

# Remove these sections:
# - gui_pysimplegui
# - gui_streamlit
# - gui (combined)
# - web
# - all
# - packaging
# - large-data

# Keep only:
# - dev

# Then commit
git add pyproject.toml
git commit -m "build: simplify optional-dependencies to dev only"

# Test wheel build
./scripts/build_wheel.sh
```

---

### Step 6: Remove Alternate Packaging Scripts (5 minutes)

**STOP**: Review list:
```bash
grep -A 20 "Category 2: Alternate Packaging Scripts" cleanup/cleanup_candidates.md
```

**If approved**, execute:
```bash
mkdir -p cleanup/removed_files/packaging_alternate

# Move PyInstaller scripts
git mv packaging/build_with_pyinstaller.sh cleanup/removed_files/packaging_alternate/
git mv packaging/build_with_pyinstaller.bat cleanup/removed_files/packaging_alternate/

# Move packaging README
git mv packaging/README.md cleanup/removed_files/packaging_alternate/

# Commit
git commit -m "remove: archive alternate packaging scripts"
```

---

### Step 7: Consolidate Documentation (10 minutes)

**STOP**: Review list:
```bash
grep -A 30 "Category 3: Redundant Documentation" cleanup/cleanup_candidates.md
```

**Recommended actions**:
1. Create simplified README.md (~200 lines, user-focused)
2. Move current verbose README.md to README.detailed.md
3. Archive implementation summaries and guides

**Execute** (after approval):
```bash
mkdir -p cleanup/removed_files/docs_redundant

# Move current README to detailed
git mv README.md README.detailed.md

# Create new simplified README (you'll need to write this)
nano README.md

# Archive redundant docs
git mv IMPLEMENTATION_SUMMARY.md cleanup/removed_files/docs_redundant/
git mv GUI_START_GUIDE.md cleanup/removed_files/docs_redundant/
git mv PROJECT_STRUCTURE.md cleanup/removed_files/docs_redundant/
git mv DEPLOYMENT_OPTIONS.md cleanup/removed_files/docs_redundant/
git mv INSTALL.md cleanup/removed_files/docs_redundant/

# Commit
git commit -m "docs: consolidate and simplify documentation"
```

---

### Step 8: Clean Build Artifacts (5 minutes)

**STOP**: Review list:
```bash
grep -A 30 "Category 4: Build Artifacts" cleanup/cleanup_candidates.md
```

**If approved**, execute:
```bash
# These are not in git, so just delete
rm -rf .venv/
rm -rf build-venv/
rm -rf build/
rm -rf dist/
rm -rf src/*.egg-info
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# Verify .gitignore includes these
echo "Verifying .gitignore..."
grep -E "venv|build|dist|__pycache__|\.pytest_cache|\.egg-info" .gitignore

# No git commit needed (not tracked)
```

---

### Step 9: Final Verification (10 minutes)

```bash
# Run full test suite
./scripts/cleanup_run_tests.sh

# Build wheel
./scripts/build_wheel.sh

# Test install
./scripts/install_from_wheel.sh

# Smoke test
python3 -m iLoveExcel
# Verify GUI launches

# CLI test
csvexcel --help
```

---

### Step 10: Generate Report and Review (5 minutes)

```bash
# Copy template
cp cleanup/CLEANUP_REPORT_TEMPLATE.md cleanup/CLEANUP_REPORT.md

# Fill in the details (automated or manual)
nano cleanup/CLEANUP_REPORT.md

# Commit
git add cleanup/CLEANUP_REPORT.md
git commit -m "docs: add cleanup execution report"
```

---

### Step 11: Push and Create PR

```bash
# Push cleanup branch
git push origin cleanup/<timestamp>

# Create PR on GitHub with cleanup report
```

---

## 🛡️ Safety Features

### Revert Anytime
```bash
./scripts/cleanup_revert.sh
```

### View Backup
```bash
ls -lh cleanup/backup_*.zip
```

### View Archived Files
```bash
ls -R cleanup/removed_files/
```

---

## ✅ Human Approval Checklist

### Before Starting
- [ ] Read complete cleanup plan
- [ ] Understand breaking changes
- [ ] Have 30-60 minutes available
- [ ] Working on correct repository

### Phase 3: PySimpleGUI Removal
- [ ] Reviewed list of files to archive
- [ ] Tested Tkinter GUI works
- [ ] Understood impact on users
- [ ] **APPROVED to proceed**

### Phase 4: Packaging Simplification
- [ ] Reviewed pyproject.toml.patch
- [ ] Tested wheel build
- [ ] Understood impact on distribution
- [ ] **APPROVED to proceed**

### Phase 5: Documentation Cleanup
- [ ] Reviewed list of docs to archive
- [ ] Created simplified README
- [ ] Verified no broken links
- [ ] **APPROVED to proceed**

### Phase 6: Build Artifacts
- [ ] Reviewed list of folders to delete
- [ ] Confirmed no important files
- [ ] Understood regeneration process
- [ ] **APPROVED to proceed**

### Final Sign-Off
- [ ] All tests passing
- [ ] Wheel builds successfully
- [ ] GUI launches correctly
- [ ] Documentation updated
- [ ] Cleanup report completed
- [ ] **APPROVED for merge to main**

---

## 📊 Expected Results

### Before
- **GUI Backends**: PySimpleGUI, Tkinter, Streamlit
- **Optional Extras**: 7 groups
- **Documentation**: 10+ MD files
- **Packaging**: Wheel, PyInstaller, Zipapp

### After
- **GUI Backends**: Tkinter (Streamlit optional)
- **Optional Extras**: 1 (dev only)
- **Documentation**: 3-5 core MD files
- **Packaging**: Wheel only

---

## 🆘 Troubleshooting

### Tests Fail After Update
```bash
# View test log
cat cleanup/test_results/test_*.log

# Revert last commit
git reset --hard HEAD~1

# Or revert entire cleanup
./scripts/cleanup_revert.sh
```

### GUI Doesn't Launch
```bash
# Check Tkinter
python3 -c "import tkinter; print('Tkinter OK')"

# Install if missing (Linux)
sudo apt-get install python3-tk
```

### Wheel Build Fails
```bash
# View build log
cat dist/*.log

# Check pyproject.toml syntax
python3 -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
```

---

## 📞 Support

If you encounter issues:
1. Check `cleanup/CLEANUP_REPORT.md` for status
2. Review test logs in `cleanup/test_results/`
3. Run `./scripts/cleanup_revert.sh` to rollback
4. Restore from backup if needed

---

**Ready to start?** Begin with Step 1! 🚀

**Estimated total time**: 30-60 minutes  
**Risk level**: 🟢 Low  
**Reversibility**: 🟢 Full (backup + revert script)
