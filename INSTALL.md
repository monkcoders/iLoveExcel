# iLoveExcel - Installation & Usage Guide

## System Requirements
- **Python**: 3.10 or higher
- **Operating Systems**: Windows, Linux, macOS
- **RAM**: Minimum 4GB (8GB+ recommended for large files)
- **Disk Space**: 500MB for installation

## Installation

### Step 1: Install Python

#### Windows
Download Python from [python.org](https://www.python.org/downloads/) and install.  
Verify installation:
```cmd
python --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv python3-tk
python3 --version
```

#### macOS
```bash
# Using Homebrew
brew install python@3.10
python3 --version
```

### Step 2: Navigate to Project Directory

#### Windows
```cmd
cd C:\path\to\iLoveExcel
```

#### Linux/macOS
```bash
cd /path/to/iLoveExcel
```

### Step 3: Create Virtual Environment (Recommended)

#### Windows
```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4: Install Dependencies

#### All Platforms
```bash
pip install -r requirements.txt
```

**Note for PySimpleGUI 5.x users:**
```bash
pip install --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
```

### Step 5: Install Package in Development Mode

#### All Platforms
```bash
pip install -e .
```

## Quick Start

### Launch GUI

#### Windows
```cmd
REM Method 1: Using batch script (easiest)
start_gui.bat

REM Method 2: Using installed command
iloveexcel-gui

REM Method 3: Using Python module
python -m iLoveExcel
```

#### Linux/macOS
```bash
# Method 1: Using shell script (easiest)
./start_gui.sh

# Method 2: Using installed command
iloveexcel-gui

# Method 3: Using Python module
python -m iLoveExcel
```

### Use CLI

#### All Platforms
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

**Note for Windows:** Use backslashes for paths if needed:
```cmd
csvexcel csv-to-excel examples\sample1.csv examples\sample2.csv -o output.xlsx
```

### Run Demo

#### Windows
```cmd
REM Python API demo
python examples\demo.py

REM CLI demo
examples\demo_run.bat
```

#### Linux/macOS
```bash
# Python API demo
python examples/demo.py

# CLI demo (make executable first)
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

### Python Not Found (Windows)
Make sure Python is added to PATH during installation.  
Or use full path:
```cmd
C:\Python310\python.exe --version
```

### Python Not Found (Linux)
Install Python:
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv
```

### tkinter Not Found (Linux Only)
GUI requires tkinter:
```bash
sudo apt install python3-tk
```

### Dependencies Not Found
```bash
pip install -r requirements.txt
```

### Command Not Found (csvexcel, iloveexcel-gui)

#### Windows
```cmd
REM Reinstall package
pip install -e .

REM Add Scripts to PATH or use full path
.venv\Scripts\csvexcel.exe --help
```

#### Linux/macOS
```bash
# Reinstall package
pip install -e .

# Or use full path
.venv/bin/csvexcel --help
```

### Import Error
Make sure you're in the correct directory and have installed the package:
```bash
# Windows
cd C:\path\to\iLoveExcel
pip install -e .

# Linux/macOS
cd /path/to/iLoveExcel
pip install -e .
```

### Permission Error (Linux/macOS)
Make shell scripts executable:
```bash
chmod +x start_gui.sh
chmod +x examples/demo_run.sh
```

### PySimpleGUI Version Issues
If you encounter theme errors or API issues:
```bash
# Install PySimpleGUI 5.x from private server
pip install --extra-index-url https://PySimpleGUI.net/install PySimpleGUI

# Or use open-source version (4.x)
pip install PySimpleGUI==4.60.5
```

### Path Separator Issues
The project uses `pathlib.Path` which handles platform differences automatically.  
However, in shell commands:
- **Windows**: Use `\` or `/` (both work)
- **Linux/macOS**: Use `/`

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
