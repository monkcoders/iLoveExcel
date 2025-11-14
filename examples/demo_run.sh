#!/bin/bash
# Demo script for iLoveExcel CLI operations

echo "=========================================="
echo "iLoveExcel CLI Demo"
echo "=========================================="
echo ""

# Create output directory
mkdir -p examples/output

echo "1. Converting CSVs to Excel..."
csvexcel csv-to-excel examples/sample1.csv examples/sample2.csv \
    -o examples/output/combined_cli.xlsx \
    -s "Sheet1,Sheet2"
echo "✓ Done"
echo ""

echo "2. Unioning multiple CSVs..."
csvexcel union-multiple examples/sample1.csv examples/sample2.csv \
    -o examples/output/union_cli.csv
echo "✓ Done"
echo ""

echo "3. Joining CSVs (inner join)..."
csvexcel join examples/employees.csv examples/projects.csv \
    -o examples/output/joined_cli.csv \
    --on "id" \
    --how inner
echo "✓ Done"
echo ""

echo "4. Joining CSVs (left join)..."
csvexcel join examples/employees.csv examples/projects.csv \
    -o examples/output/joined_left_cli.csv \
    --on "id" \
    --how left
echo "✓ Done"
echo ""

echo "=========================================="
echo "All CLI demos completed!"
echo "Output files are in: examples/output/"
echo "=========================================="
