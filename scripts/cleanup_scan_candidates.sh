#!/bin/bash
# iLoveExcel - Cleanup: Scan Candidates
# Scans repository and generates lists of files to review for cleanup

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${YELLOW}=========================================="
echo "iLoveExcel - Cleanup: Scan Candidates"
echo "==========================================${NC}"
echo ""

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

OUTPUT_FILE="cleanup/cleanup_candidates.md"

echo "Scanning repository for cleanup candidates..."
echo "Output: $OUTPUT_FILE"
echo ""

# Start generating the report
cat > "$OUTPUT_FILE" << 'EOF'
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

EOF

# Category 1: PySimpleGUI Files
echo -e "${BLUE}→ Scanning for PySimpleGUI files...${NC}"
cat >> "$OUTPUT_FILE" << 'EOF'
## Category 1: PySimpleGUI Files

**Action**: 🗑️ Move to `cleanup/removed_files/gui_pysimplegui/`

### Source Files
EOF

# Find files importing PySimpleGUI
echo "Checking for PySimpleGUI imports..."
if grep -r "import PySimpleGUI" src/ --include="*.py" 2>/dev/null | cut -d':' -f1 | sort -u >> /tmp/pysimplegui_files.txt 2>/dev/null; then
    while IFS= read -r file; do
        echo "- \`$file\` - $(head -n 3 "$file" | tail -n 1)" >> "$OUTPUT_FILE"
    done < /tmp/pysimplegui_files.txt
    rm /tmp/pysimplegui_files.txt
else
    echo "- None found" >> "$OUTPUT_FILE"
fi

cat >> "$OUTPUT_FILE" << 'EOF'

### References to Update
EOF

# Find files referencing PySimpleGUI
echo "Checking for PySimpleGUI references..."
if grep -r "pysimplegui\|PySimpleGUI" --include="*.py" --include="*.md" --include="*.toml" src/ docs/ *.md pyproject.toml requirements.txt 2>/dev/null | grep -v "cleanup/" | cut -d':' -f1 | sort -u >> /tmp/pysimplegui_refs.txt 2>/dev/null; then
    while IFS= read -r file; do
        count=$(grep -c "pysimplegui\|PySimpleGUI" "$file" 2>/dev/null || echo "0")
        echo "- \`$file\` - $count references" >> "$OUTPUT_FILE"
    done < /tmp/pysimplegui_refs.txt
    rm /tmp/pysimplegui_refs.txt
else
    echo "- None found" >> "$OUTPUT_FILE"
fi

# Category 2: Alternate Packaging Scripts
echo -e "${BLUE}→ Scanning for alternate packaging scripts...${NC}"
cat >> "$OUTPUT_FILE" << 'EOF'

---

## Category 2: Alternate Packaging Scripts

**Action**: 📦 Move to `cleanup/removed_files/packaging_alternate/`

### PyInstaller Scripts
EOF

find packaging/ -type f \( -name "*pyinstaller*" -o -name "*zipapp*" \) 2>/dev/null | while read -r file; do
    echo "- \`$file\` - $(wc -l < "$file") lines" >> "$OUTPUT_FILE"
done || echo "- None found" >> "$OUTPUT_FILE"

cat >> "$OUTPUT_FILE" << 'EOF'

### Packaging Documentation
EOF

find packaging/ docs/ -type f -name "*.md" 2>/dev/null | while read -r file; do
    echo "- \`$file\` - $(wc -l < "$file") lines" >> "$OUTPUT_FILE"
done || echo "- None found" >> "$OUTPUT_FILE"

cat >> "$OUTPUT_FILE" << 'EOF'

### Keep (Primary Wheel Build)
- ✅ `scripts/build_wheel.sh`
- ✅ `scripts/build_wheel.bat`
- ✅ `scripts/install_from_wheel.sh`
- ✅ `scripts/install_from_wheel.bat`
EOF

# Category 3: Redundant Documentation
echo -e "${BLUE}→ Scanning for redundant documentation...${NC}"
cat >> "$OUTPUT_FILE" << 'EOF'

---

## Category 3: Redundant Documentation

**Action**: 📦 Move to `cleanup/removed_files/docs_redundant/`

### Potentially Redundant Files
EOF

# List markdown files at root
find . -maxdepth 1 -type f -name "*.md" ! -name "README.md" ! -name "LICENSE*" ! -name "CHANGELOG*" 2>/dev/null | while read -r file; do
    lines=$(wc -l < "$file")
    echo "- \`$file\` - $lines lines" >> "$OUTPUT_FILE"
done

cat >> "$OUTPUT_FILE" << 'EOF'

### Documentation in docs/
EOF

find docs/ -type f -name "*.md" 2>/dev/null | while read -r file; do
    lines=$(wc -l < "$file")
    echo "- \`$file\` - $lines lines" >> "$OUTPUT_FILE"
done || echo "- None found" >> "$OUTPUT_FILE"

cat >> "$OUTPUT_FILE" << 'EOF'

### Recommended Actions
- **CREATE**: `README.md` (simplified, ~200 lines, user-focused)
- **CREATE**: `README.detailed.md` (move current verbose README here)
- **KEEP**: `LICENSE`, `CHANGELOG.md` (if exists)
- **ARCHIVE**: Implementation summaries, installation guides (consolidate into README)
EOF

# Category 4: Build Artifacts
echo -e "${BLUE}→ Scanning for build artifacts...${NC}"
cat >> "$OUTPUT_FILE" << 'EOF'

---

## Category 4: Build Artifacts & Virtual Environments

**Action**: ❌ Permanent deletion (not tracked in git)

### Virtual Environments
EOF

find . -maxdepth 2 -type d \( -name ".venv" -o -name "venv" -o -name "env" -o -name "build-venv" \) 2>/dev/null | while read -r dir; do
    if [ -d "$dir" ]; then
        size=$(du -sh "$dir" 2>/dev/null | cut -f1)
        echo "- \`$dir/\` - $size" >> "$OUTPUT_FILE"
    fi
done

cat >> "$OUTPUT_FILE" << 'EOF'

### Build Directories
EOF

find . -maxdepth 2 -type d \( -name "build" -o -name "dist" -o -name "*.egg-info" \) 2>/dev/null | grep -v "/cleanup/" | while read -r dir; do
    if [ -d "$dir" ]; then
        size=$(du -sh "$dir" 2>/dev/null | cut -f1)
        echo "- \`$dir/\` - $size" >> "$OUTPUT_FILE"
    fi
done

cat >> "$OUTPUT_FILE" << 'EOF'

### Python Cache
EOF

find . -type d -name "__pycache__" 2>/dev/null | head -n 10 | while read -r dir; do
    size=$(du -sh "$dir" 2>/dev/null | cut -f1)
    echo "- \`$dir/\` - $size" >> "$OUTPUT_FILE"
done
echo "- _(and more...)_" >> "$OUTPUT_FILE"

cat >> "$OUTPUT_FILE" << 'EOF'

### Pytest Cache
EOF

find . -type d -name ".pytest_cache" 2>/dev/null | while read -r dir; do
    if [ -d "$dir" ]; then
        size=$(du -sh "$dir" 2>/dev/null | cut -f1)
        echo "- \`$dir/\` - $size" >> "$OUTPUT_FILE"
    fi
done || echo "- None found" >> "$OUTPUT_FILE"

# Category 5: pyproject.toml Extras
echo -e "${BLUE}→ Scanning pyproject.toml for extras...${NC}"
cat >> "$OUTPUT_FILE" << 'EOF'

---

## Category 5: pyproject.toml Extras

**Action**: 🔧 Update `pyproject.toml` to remove extras

### Current Extras (from pyproject.toml)
EOF

if [ -f "pyproject.toml" ]; then
    if grep -A 100 "\[project.optional-dependencies\]" pyproject.toml 2>/dev/null | grep "^[a-z_]" | cut -d'=' -f1 | while read -r extra; do
        extra=$(echo "$extra" | tr -d ' ')
        if [ -n "$extra" ]; then
            echo "- \`$extra\`" >> "$OUTPUT_FILE"
        fi
    done; then
        :
    else
        echo "- None found" >> "$OUTPUT_FILE"
    fi
fi

cat >> "$OUTPUT_FILE" << 'EOF'

### Recommended Changes
- **REMOVE**: `gui_pysimplegui` - PySimpleGUI no longer supported
- **REMOVE**: `gui_streamlit` - Streamlit optional, not as extra
- **REMOVE**: `gui_customtkinter` - Not implemented
- **REMOVE**: `web` - Combined extra, not needed
- **REMOVE**: `packaging` - Dev tools, not user-facing
- **REMOVE**: `gui` - Combined extra, not needed
- **REMOVE**: `all` - Combined extra, not needed
- **KEEP**: `dev` - Developer tools (pytest, black, mypy, ruff)
EOF

# Category 6: Dead Code Candidates
echo -e "${BLUE}→ Scanning for potential dead code...${NC}"
cat >> "$OUTPUT_FILE" << 'EOF'

---

## Category 6: Dead Code Candidates

**Action**: 🔍 Review for potential removal (needs human verification)

### Files Not Imported Anywhere
EOF

# This is a heuristic - find Python files not referenced elsewhere
find src/iLoveExcel/ -name "*.py" ! -name "__init__.py" ! -name "__main__.py" 2>/dev/null | while read -r file; do
    basename=$(basename "$file" .py)
    # Check if this module is imported anywhere
    if ! grep -r "from.*import.*$basename\|import.*$basename" src/ tests/ examples/ --include="*.py" 2>/dev/null | grep -v "$file" > /dev/null; then
        echo "- \`$file\` - No imports found (verify manually)" >> "$OUTPUT_FILE"
    fi
done

cat >> "$OUTPUT_FILE" << 'EOF'

**Note**: These files may still be used indirectly. Manual verification required.
EOF

# Summary
cat >> "$OUTPUT_FILE" << 'EOF'

---

## Summary Statistics

EOF

echo "### File Counts" >> "$OUTPUT_FILE"
echo "- Python files: $(find src/ -name "*.py" | wc -l)" >> "$OUTPUT_FILE"
echo "- Test files: $(find tests/ -name "*.py" 2>/dev/null | wc -l)" >> "$OUTPUT_FILE"
echo "- Markdown files: $(find . -name "*.md" | grep -v cleanup/ | wc -l)" >> "$OUTPUT_FILE"
echo "- Shell scripts: $(find scripts/ packaging/ -name "*.sh" 2>/dev/null | wc -l)" >> "$OUTPUT_FILE"

cat >> "$OUTPUT_FILE" << 'EOF'

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
EOF

echo -e "${GREEN}✓ Scan complete${NC}"
echo ""
echo "Report generated: $OUTPUT_FILE"
echo ""
echo -e "${YELLOW}⚠️  Please review the report before proceeding${NC}"
echo ""
echo "Next step:"
echo "  cat cleanup/cleanup_candidates.md | less"
echo "  # Or open in your editor"
echo ""
