#!/bin/bash
# iLoveExcel - Cleanup: Revert
# Reverts all cleanup changes and restores from backup

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${RED}=========================================="
echo "iLoveExcel - Cleanup: REVERT"
echo "==========================================${NC}"
echo ""
echo -e "${RED}⚠️  WARNING: This will undo all cleanup changes!${NC}"
echo ""

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if cleanup state exists
if [ ! -f "cleanup/cleanup_state.txt" ]; then
    echo -e "${RED}Error: No cleanup state found${NC}"
    echo "Nothing to revert."
    exit 1
fi

# Read cleanup state
source cleanup/cleanup_state.txt

echo "Current branch: $(git branch --show-current)"
if [ -n "$BACKUP_BRANCH" ]; then
    echo "Backup branch: $BACKUP_BRANCH (with committed changes)"
fi
echo "Cleanup branch: $CLEANUP_BRANCH"
echo "Backup file: $CLEANUP_BACKUP"
echo ""
echo "Revert options:"
echo "  1) Go back to main (pristine, no changes)"
echo "  2) Go back to backup branch (with your committed changes)"
echo "  3) Delete cleanup branch but stay where you are"
echo "  4) Cancel"
echo ""
read -p "Select option (1-4): " -n 1 -r
echo ""
REVERT_OPTION=$REPLY

if [ "$REVERT_OPTION" = "4" ]; then
    echo "Revert cancelled."
    exit 0
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# Handle based on option selected
if [ "$REVERT_OPTION" = "1" ]; then
    # Option 1: Go back to main
    echo -e "${YELLOW}→ Switching to main branch...${NC}"
    
    # Discard uncommitted changes if any
    if ! git diff-index --quiet HEAD --; then
        echo -e "${YELLOW}Discarding uncommitted changes...${NC}"
        git reset --hard HEAD
    fi
    
    git checkout main || {
        echo -e "${RED}Error: Could not switch to main branch${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ On main branch (pristine)${NC}"
    echo ""
    
    # Delete cleanup branch
    echo -e "${YELLOW}→ Deleting cleanup branch...${NC}"
    git branch -D "$CLEANUP_BRANCH" 2>/dev/null || echo "Cleanup branch already deleted"
    echo -e "${GREEN}✓ Cleanup branch deleted${NC}"
    echo ""
    
    # Optionally delete backup branch
    if [ -n "$BACKUP_BRANCH" ]; then
        read -p "Delete backup branch too? (y/n): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git branch -D "$BACKUP_BRANCH" 2>/dev/null || echo "Backup branch already deleted"
            echo -e "${GREEN}✓ Backup branch deleted${NC}"
        else
            echo -e "${YELLOW}Backup branch preserved: $BACKUP_BRANCH${NC}"
        fi
    fi

elif [ "$REVERT_OPTION" = "2" ]; then
    # Option 2: Go back to backup branch
    if [ -z "$BACKUP_BRANCH" ]; then
        echo -e "${RED}Error: No backup branch found in cleanup state${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}→ Switching to backup branch...${NC}"
    
    # Discard uncommitted changes if any
    if ! git diff-index --quiet HEAD --; then
        echo -e "${YELLOW}Discarding uncommitted changes...${NC}"
        git reset --hard HEAD
    fi
    
    git checkout "$BACKUP_BRANCH" || {
        echo -e "${RED}Error: Could not switch to backup branch${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ On backup branch (with your committed changes)${NC}"
    echo ""
    
    # Delete cleanup branch
    echo -e "${YELLOW}→ Deleting cleanup branch...${NC}"
    git branch -D "$CLEANUP_BRANCH" 2>/dev/null || echo "Cleanup branch already deleted"
    echo -e "${GREEN}✓ Cleanup branch deleted${NC}"
    echo ""

elif [ "$REVERT_OPTION" = "3" ]; then
    # Option 3: Just delete cleanup branch
    if [ "$CURRENT_BRANCH" = "$CLEANUP_BRANCH" ]; then
        echo -e "${YELLOW}→ Cannot delete current branch. Switching to main first...${NC}"
        git checkout main || git checkout "$BACKUP_BRANCH" || {
            echo -e "${RED}Error: Could not switch branches${NC}"
            exit 1
        }
    fi
    
    echo -e "${YELLOW}→ Deleting cleanup branch...${NC}"
    git branch -D "$CLEANUP_BRANCH" 2>/dev/null || echo "Cleanup branch already deleted"
    echo -e "${GREEN}✓ Cleanup branch deleted${NC}"
    echo ""
fi

# Optionally restore from backup
echo -e "${YELLOW}Do you want to restore from backup?${NC}"
echo "This will extract the backup to a separate directory for reference."
echo ""
read -p "Restore backup to ../iLoveExcel_restored? (y/n): " -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "$CLEANUP_BACKUP" ]; then
        cd ..
        RESTORE_DIR="iLoveExcel_restored_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$RESTORE_DIR"
        unzip -q "$PROJECT_ROOT/$CLEANUP_BACKUP" -d "$RESTORE_DIR"
        echo -e "${GREEN}✓ Backup restored to: ../$RESTORE_DIR${NC}"
        cd "$PROJECT_ROOT"
    else
        echo -e "${RED}Error: Backup file not found: $CLEANUP_BACKUP${NC}"
    fi
fi
echo ""

# Clean up cleanup directory (optional)
read -p "Remove cleanup directory? (y/n): " -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Keep backup file, remove other cleanup files
    find cleanup/ -type f ! -name "backup_*.zip" -delete 2>/dev/null || true
    find cleanup/ -type d -empty -delete 2>/dev/null || true
    echo -e "${GREEN}✓ Cleanup directory cleared (backups preserved)${NC}"
fi
echo ""

echo -e "${GREEN}=========================================="
echo "✓ Revert Complete"
echo "==========================================${NC}"
echo ""

if [ "$REVERT_OPTION" = "1" ]; then
    echo "You are now on the main branch (pristine, no changes)."
    echo "All cleanup changes have been reverted."
elif [ "$REVERT_OPTION" = "2" ]; then
    echo "You are now on the backup branch (with your committed changes)."
    echo "Cleanup branch has been deleted."
    echo "Your work before cleanup is preserved here."
elif [ "$REVERT_OPTION" = "3" ]; then
    echo "Cleanup branch has been deleted."
    echo "You are on: $(git branch --show-current)"
fi

echo ""
if [ -f "$CLEANUP_BACKUP" ]; then
    echo "Backup file preserved: $CLEANUP_BACKUP"
fi

if [ -n "$BACKUP_BRANCH" ] && git branch | grep -q "$BACKUP_BRANCH"; then
    echo "Backup branch preserved: $BACKUP_BRANCH"
fi
echo ""
