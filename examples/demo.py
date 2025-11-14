#!/usr/bin/env python3
"""
Demo script showing various iLoveExcel operations.

This script demonstrates:
1. Converting CSVs to Excel
2. Unioning multiple CSVs
3. Joining CSVs on a key
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import iLoveExcel
from iLoveExcel.utils import setup_logging

# Setup logging
setup_logging(level='INFO')

# Get example directory
EXAMPLE_DIR = Path(__file__).parent
OUTPUT_DIR = EXAMPLE_DIR / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("iLoveExcel Demo Script")
print("=" * 60)
print()

# ============================================================================
# Demo 1: Convert multiple CSVs to Excel workbook
# ============================================================================
print("Demo 1: Converting CSVs to Excel workbook...")
print("-" * 60)

csv_files = [
    EXAMPLE_DIR / 'sample1.csv',
    EXAMPLE_DIR / 'sample2.csv',
]

output_excel = OUTPUT_DIR / 'combined.xlsx'

iLoveExcel.csvs_to_excel(
    csv_files=csv_files,
    output_path=output_excel,
    sheet_names=['People_1', 'People_2']
)

print(f"✓ Created {output_excel}")
print()

# ============================================================================
# Demo 2: Union multiple CSVs
# ============================================================================
print("Demo 2: Unioning multiple CSVs...")
print("-" * 60)

union_output = OUTPUT_DIR / 'all_people.csv'

iLoveExcel.union_multiple_csvs(
    files=csv_files,
    output_csv=union_output,
    dedupe=False,  # Keep all rows including duplicates
    progress=True
)

print(f"✓ Created {union_output}")
print()

# ============================================================================
# Demo 3: Join two CSVs on a key
# ============================================================================
print("Demo 3: Joining CSVs (inner join on 'id')...")
print("-" * 60)

employees_file = EXAMPLE_DIR / 'employees.csv'
projects_file = EXAMPLE_DIR / 'projects.csv'
join_output = OUTPUT_DIR / 'employee_projects.csv'

result_df = iLoveExcel.join_csvs(
    file_left=employees_file,
    file_right=projects_file,
    on='id',
    how='inner',
    output_file=join_output
)

print(f"✓ Created {join_output}")
print(f"  Result has {len(result_df)} rows and {len(result_df.columns)} columns")
print(f"  Columns: {list(result_df.columns)}")
print()

# ============================================================================
# Demo 4: Join with 'left' join type
# ============================================================================
print("Demo 4: Left join (keep all employees)...")
print("-" * 60)

left_join_output = OUTPUT_DIR / 'employee_projects_left.csv'

result_df = iLoveExcel.join_csvs(
    file_left=employees_file,
    file_right=projects_file,
    on='id',
    how='left',
    output_file=left_join_output
)

print(f"✓ Created {left_join_output}")
print(f"  Result has {len(result_df)} rows")
print()

# ============================================================================
# Demo 5: Union with deduplication
# ============================================================================
print("Demo 5: Union with deduplication...")
print("-" * 60)

# Create a file with some duplicate rows
duplicate_file = OUTPUT_DIR / 'sample_with_dupes.csv'
with open(duplicate_file, 'w') as f:
    f.write("id,name,age,city\n")
    f.write("1,Alice,28,New York\n")  # Duplicate from sample1
    f.write("11,Kelly,30,Austin\n")
    f.write("12,Leo,36,Columbus\n")

union_dedupe_output = OUTPUT_DIR / 'all_people_dedupe.csv'

iLoveExcel.union_csvs(
    file_a=csv_files[0],
    file_b=duplicate_file,
    output_file=union_dedupe_output,
    dedupe=True  # Remove duplicates
)

print(f"✓ Created {union_dedupe_output} (with deduplication)")
print()

# ============================================================================
# Summary
# ============================================================================
print("=" * 60)
print("Demo completed successfully!")
print("=" * 60)
print(f"\nOutput files created in: {OUTPUT_DIR}")
print("\nTo run the GUI:")
print("  python -m iLoveExcel")
print("\nTo use the CLI:")
print("  csvexcel --help")
print()
