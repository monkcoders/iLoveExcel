#!/bin/bash
# iLoveExcel - Cleanup: Run Tests
# Runs test suite and records results

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}=========================================="
echo "iLoveExcel - Cleanup: Run Tests"
echo "==========================================${NC}"
echo ""

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
TEST_LOG="cleanup/test_results/test_${TIMESTAMP}.log"

mkdir -p cleanup/test_results

echo "Running test suite..."
echo "Log file: $TEST_LOG"
echo ""

# Run pytest if available
if command -v pytest &> /dev/null; then
    echo "→ Running pytest..."
    echo ""
    
    pytest tests/ -v 2>&1 | tee "$TEST_LOG"
    TEST_EXIT_CODE=${PIPESTATUS[0]}
    
    echo ""
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed${NC}"
        TEST_RESULT="PASS"
    else
        echo -e "${RED}✗ Some tests failed${NC}"
        TEST_RESULT="FAIL"
    fi
else
    echo -e "${YELLOW}⚠️  pytest not found${NC}"
    echo "Install with: pip install pytest"
    TEST_RESULT="SKIPPED"
fi

echo ""
echo "Test result: $TEST_RESULT" > "cleanup/test_results/test_status_${TIMESTAMP}.txt"

# Run smoke tests
echo ""
echo -e "${YELLOW}→ Running smoke tests...${NC}"
echo ""

# Test 1: CLI help
echo "1. Testing CLI (csvexcel --help)..."
if python3 -m iLoveExcel.cli --help > /dev/null 2>&1; then
    echo -e "   ${GREEN}✓ CLI works${NC}"
else
    echo -e "   ${RED}✗ CLI failed${NC}"
fi

# Test 2: Check Tkinter availability
echo "2. Testing Tkinter availability..."
if python3 -c "import tkinter" 2>/dev/null; then
    echo -e "   ${GREEN}✓ Tkinter available${NC}"
else
    echo -e "   ${YELLOW}⚠️  Tkinter not available${NC}"
fi

# Test 3: Import main package
echo "3. Testing package import..."
if python3 -c "import iLoveExcel; print(f'Version: {iLoveExcel.__version__}')" 2>/dev/null; then
    echo -e "   ${GREEN}✓ Package imports successfully${NC}"
else
    echo -e "   ${RED}✗ Package import failed${NC}"
fi

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Exit code: $TEST_EXIT_CODE"
echo "Result: $TEST_RESULT"
echo "Log: $TEST_LOG"
echo ""

if [ "$TEST_RESULT" = "PASS" ]; then
    echo -e "${GREEN}✓ Tests passed - safe to proceed with cleanup${NC}"
    exit 0
elif [ "$TEST_RESULT" = "FAIL" ]; then
    echo -e "${RED}✗ Tests failed - review failures before proceeding${NC}"
    exit 1
else
    echo -e "${YELLOW}⚠️  Tests skipped - manual verification recommended${NC}"
    exit 0
fi
