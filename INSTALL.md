# iLoveExcel - Quick Installation & Usage Guide

## Installation

### Step 1: Install Python
Ensure you have Python 3.10 or higher installed:
```bash
python --version
```

### Step 2: Navigate to Project Directory
```bash
cd /home/abhishek/projects/iLoveExcel/iLoveExcel
```

### Step 3: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# On Windows: venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Install Package in Development Mode
```bash
pip install -e .
```

## Quick Start

### Launch GUI
```bash
# Method 1: Using installed command
iloveexcel-gui

# Method 2: Using Python module
python -m iLoveExcel
```

### Use CLI
```bash
# View help
csvexcel --help

# Convert CSVs to Excel
csvexcel csv-to-excel examples/sample1.csv examples/sample2.csv -o output.xlsx

# Union CSVs
csvexcel union-multiple examples/sample*.csv -o combined.csv

# Join CSVs
csvexcel join examples/employees.csv examples/projects.csv -o joined.csv --on "id" --how inner

# Merge Excel files
csvexcel merge-excel file1.xlsx file2.xlsx -o merged.xlsx
```

### Run Demo
```bash
# Python API demo
python examples/demo.py

# CLI demo (after making it executable)
chmod +x examples/demo_run.sh
./examples/demo_run.sh
```

### Use Python API
```python
import iLoveExcel

# Convert CSVs to Excel
iLoveExcel.csvs_to_excel(
    csv_files=['file1.csv', 'file2.csv'],
    output_path='output.xlsx',
    sheet_names=['Sheet1', 'Sheet2']
)

# Union multiple CSVs
iLoveExcel.union_multiple_csvs(
    files=['a.csv', 'b.csv', 'c.csv'],
    output_csv='combined.csv',
    dedupe=True
)

# Join CSVs
result_df = iLoveExcel.join_csvs(
    file_left='customers.csv',
    file_right='orders.csv',
    on='customer_id',
    how='inner',
    output_file='result.csv'
)

# Merge Excel files
iLoveExcel.merge_excel_files(
    excel_files=['report1.xlsx', 'report2.xlsx'],
    output_file='merged.xlsx',
    mode='lenient'
)
```

## Troubleshooting

### Dependencies Not Found
```bash
pip install -r requirements.txt
```

### Command Not Found (csvexcel, iloveexcel-gui)
```bash
pip install -e .
```

### Import Error
Make sure you're in the correct directory and have installed the package:
```bash
cd /home/abhishek/projects/iLoveExcel/iLoveExcel
pip install -e .
```

### Permission Error
Make demo script executable:
```bash
chmod +x examples/demo_run.sh
```

## Next Steps

1. Read the full README.md for detailed documentation
2. Explore examples/ directory for sample data
3. Run examples/demo.py to see API usage
4. Check PROJECT_STRUCTURE.md for architecture details
5. View tests/ directory for usage examples

## Support

- Documentation: README.md
- Project Structure: PROJECT_STRUCTURE.md
- Examples: examples/ directory
- Tests: tests/ directory
