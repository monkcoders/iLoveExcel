#!/bin/bash
# iLoveExcel - Cleanup: Create Branch and Backup
# Creates a git branch and full repository backup before cleanup begins

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=========================================="
echo "iLoveExcel - Cleanup Phase 0"
echo "Create Branch and Backup"
echo -e "==========================================${NC}"
echo ""

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Project root: $PROJECT_ROOT"
echo ""

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BRANCH_NAME="cleanup/${TIMESTAMP}"
BACKUP_FILE="cleanup/backup_${TIMESTAMP}.zip"

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes${NC}"
    echo ""
    git status --short
    echo ""
    read -p "Commit these changes before proceeding? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        read -p "Enter commit message: " commit_msg
        git add -A
        git commit -m "$commit_msg"
        echo -e "${GREEN}✓ Changes committed${NC}"
    else
        echo -e "${YELLOW}Proceeding with uncommitted changes...${NC}"
    fi
    echo ""
fi

# Create cleanup branch
echo -e "${YELLOW}→ Creating cleanup branch: ${BRANCH_NAME}${NC}"
git checkout -b "$BRANCH_NAME"
echo -e "${GREEN}✓ Branch created and checked out${NC}"
echo ""

# Create backup
echo -e "${YELLOW}→ Creating full repository backup...${NC}"
cd ..
REPO_NAME=$(basename "$PROJECT_ROOT")

# Exclude some large/unnecessary files from backup
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
    exit 1
fi
echo ""

# Run baseline tests
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
CLEANUP_BRANCH=$BRANCH_NAME
CLEANUP_BACKUP=$BACKUP_FILE
BASELINE_TEST_RESULT=$TEST_RESULT
BASELINE_TEST_LOG=$TEST_LOG
PHASE_COMPLETED=0
CURRENT_PHASE=Phase 0: Preparation
EOF

echo -e "${GREEN}=========================================="
echo "✓ Phase 0 Complete"
echo "==========================================${NC}"
echo ""
echo "Branch: $BRANCH_NAME"
echo "Backup: $BACKUP_FILE ($BACKUP_SIZE)"
echo "Baseline tests: $TEST_RESULT"
echo ""
echo "Next steps:"
echo "  1. Run: ./scripts/cleanup_scan_candidates.sh"
echo "  2. Review: cleanup/cleanup_candidates.md"
echo "  3. Run: ./scripts/cleanup_present_and_confirm.sh"
echo ""
echo -e "${YELLOW}⚠️  All cleanup operations will be done on branch: ${BRANCH_NAME}${NC}"
echo ""
