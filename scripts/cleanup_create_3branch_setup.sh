#!/bin/bash
# iLoveExcel - Cleanup: Create Backup Branch and Cleanup Branch
# Strategy: main → backup branch (commit all changes) → cleanup branch (do cleanup work)

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=========================================="
echo "iLoveExcel - 3-Branch Cleanup Strategy"
echo "==========================================${NC}"
echo ""
echo "This script will:"
echo "  1. Create backup branch from main"
echo "  2. Commit all current changes to backup"
echo "  3. Create cleanup branch from backup"
echo "  4. Create full repo backup zip"
echo "  5. Run baseline tests"
echo ""
echo -e "${BLUE}Branch Strategy:${NC}"
echo "  main branch           (unchanged, pristine)"
echo "      ↓"
echo "  backup branch         (current changes committed here)"
echo "      ↓"
echo "  cleanup branch        (cleanup work happens here)"
echo ""

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Project root: $PROJECT_ROOT"
echo ""

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_BRANCH="backup/pre-cleanup_${TIMESTAMP}"
CLEANUP_BRANCH="cleanup/${TIMESTAMP}"
BACKUP_FILE="cleanup/backup_${TIMESTAMP}.zip"

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Verify we're on main
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${YELLOW}⚠️  Warning: Not on main branch${NC}"
    read -p "Switch to main branch? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout main
        echo -e "${GREEN}✓ Switched to main${NC}"
    else
        echo "Cleanup cancelled. Please switch to main branch first."
        exit 1
    fi
    echo ""
fi

# Step 1: Create backup branch
echo -e "${BLUE}=========================================="
echo "Step 1: Create Backup Branch"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}→ Creating backup branch: ${BACKUP_BRANCH}${NC}"
git checkout -b "$BACKUP_BRANCH"
echo -e "${GREEN}✓ Backup branch created${NC}"
echo ""

# Step 2: Commit all changes to backup branch
echo -e "${BLUE}=========================================="
echo "Step 2: Commit All Changes to Backup"
echo "==========================================${NC}"
echo ""

# Check what we have
echo "Current status:"
git status --short
echo ""

# Stage all changes (modified, new, deleted)
echo -e "${YELLOW}→ Staging all changes...${NC}"
git add -A
echo -e "${GREEN}✓ All changes staged${NC}"
echo ""

# Show what will be committed
echo "Changes to be committed:"
git status --short
echo ""

read -p "Commit these changes to backup branch? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled. Restoring to main branch..."
    git checkout main
    git branch -D "$BACKUP_BRANCH"
    exit 1
fi

# Commit with descriptive message
COMMIT_MSG="backup: snapshot before cleanup on ${TIMESTAMP}

This backup branch contains all uncommitted changes from main branch
before the cleanup process begins. Includes:
- Wheel packaging implementation
- New Tkinter GUI
- CSV diff feature
- Documentation updates
- Cleanup infrastructure

Created as safety checkpoint before cleanup operations."

git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✓ All changes committed to backup branch${NC}"
echo ""

# Step 3: Create cleanup branch from backup
echo -e "${BLUE}=========================================="
echo "Step 3: Create Cleanup Branch from Backup"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}→ Creating cleanup branch: ${CLEANUP_BRANCH}${NC}"
git checkout -b "$CLEANUP_BRANCH"
echo -e "${GREEN}✓ Cleanup branch created from backup${NC}"
echo ""

# Step 4: Create full repository backup
echo -e "${BLUE}=========================================="
echo "Step 4: Create Repository Backup Zip"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}→ Creating full repository backup...${NC}"

# Ensure cleanup directory exists
mkdir -p cleanup

cd ..
REPO_NAME=$(basename "$PROJECT_ROOT")

# Create zip backup (excluding large/unnecessary files)
zip -r "${PROJECT_ROOT}/${BACKUP_FILE}" "$REPO_NAME" \
    -x "*.venv/*" \
    -x "*/build-venv/*" \
    -x "*/__pycache__/*" \
    -x "*.pyc" \
    -x "*.pyo" \
    -x "*/.pytest_cache/*" \
    -x "*.egg-info/*" \
    -x "*/dist/*" \
    -x "*/build/*" \
    -x "*/.git/objects/*" \
    2>&1 | grep -v "adding:" || true

cd "$PROJECT_ROOT"

if [ -f "$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo -e "${GREEN}✓ Backup created: ${BACKUP_FILE} (${BACKUP_SIZE})${NC}"
else
    echo -e "${RED}✗ Backup failed${NC}"
    echo "Cleanup cancelled. Restoring to main branch..."
    git checkout main
    git branch -D "$CLEANUP_BRANCH"
    git branch -D "$BACKUP_BRANCH"
    exit 1
fi
echo ""

# Step 5: Run baseline tests
echo -e "${BLUE}=========================================="
echo "Step 5: Run Baseline Tests"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}→ Running baseline test suite...${NC}"
echo ""

TEST_LOG="cleanup/test_results/baseline_${TIMESTAMP}.log"
mkdir -p cleanup/test_results

if command -v pytest &> /dev/null; then
    pytest tests/ -v > "$TEST_LOG" 2>&1 && TEST_RESULT="PASS" || TEST_RESULT="FAIL"
    
    if [ "$TEST_RESULT" = "PASS" ]; then
        echo -e "${GREEN}✓ All tests passed${NC}"
    else
        echo -e "${RED}✗ Some tests failed (see ${TEST_LOG})${NC}"
        echo ""
        echo "Last 20 lines of test output:"
        tail -n 20 "$TEST_LOG"
        echo ""
        echo -e "${YELLOW}Note: This is the baseline. Cleanup should not make it worse.${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  pytest not found, skipping baseline tests${NC}"
    TEST_RESULT="SKIPPED"
fi

echo ""
echo "Baseline test result: $TEST_RESULT" > "cleanup/test_results/baseline_status.txt"

# Create cleanup state file
cat > cleanup/cleanup_state.txt << EOF
CLEANUP_TIMESTAMP=$TIMESTAMP
BACKUP_BRANCH=$BACKUP_BRANCH
CLEANUP_BRANCH=$CLEANUP_BRANCH
CLEANUP_BACKUP=$BACKUP_FILE
BASELINE_TEST_RESULT=$TEST_RESULT
BASELINE_TEST_LOG=$TEST_LOG
PHASE_COMPLETED=0
CURRENT_PHASE=Phase 0: Preparation
STRATEGY=3-branch (main → backup → cleanup)
EOF

# Summary
echo -e "${GREEN}=========================================="
echo "✓ Phase 0 Complete - 3-Branch Setup"
echo "==========================================${NC}"
echo ""
echo "Branch Structure:"
echo "  ${GREEN}✓${NC} main branch:    $(git rev-parse --short main) (unchanged)"
echo "  ${GREEN}✓${NC} backup branch:  $BACKUP_BRANCH (all changes committed)"
echo "  ${GREEN}✓${NC} cleanup branch: $CLEANUP_BRANCH (current branch, ready for cleanup)"
echo ""
echo "Backup: $BACKUP_FILE ($BACKUP_SIZE)"
echo "Baseline tests: $TEST_RESULT"
echo ""
echo -e "${BLUE}Branch Strategy Diagram:${NC}"
echo "  main (pristine)"
echo "    └─→ $BACKUP_BRANCH (changes saved)"
echo "          └─→ $CLEANUP_BRANCH (cleanup work here) ← YOU ARE HERE"
echo ""
echo "Next steps:"
echo "  1. Run: ./scripts/cleanup_scan_candidates.sh"
echo "  2. Review: cleanup/cleanup_candidates.md"
echo "  3. Run: ./scripts/cleanup_present_and_confirm.sh"
echo ""
echo -e "${GREEN}Safety guarantees:${NC}"
echo "  ✓ main branch is untouched"
echo "  ✓ All changes saved in backup branch: $BACKUP_BRANCH"
echo "  ✓ Cleanup work isolated in: $CLEANUP_BRANCH"
echo "  ✓ Full repo backup: $BACKUP_FILE"
echo "  ✓ Can restore any branch at any time"
echo ""
echo -e "${YELLOW}To revert:${NC}"
echo "  git checkout main  # Go back to pristine main"
echo "  OR"
echo "  git checkout $BACKUP_BRANCH  # Go to backup with your changes"
echo "  OR"
echo "  ./scripts/cleanup_revert.sh  # Automated revert"
echo ""
