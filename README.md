# iLoveExcel

**Advanced CSV and Excel operations with GUI and CLI**

iLoveExcel is a comprehensive Python toolkit for performing complex operations on CSV and Excel files, including unions, joins, and merges. It features both a user-friendly GUI and a powerful command-line interface.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## Features

### Core Operations

1. **CSV to Excel Conversion** - Convert multiple CSV files into a single Excel workbook with separate sheets
2. **CSV Union** - Combine multiple CSV files by appending rows, with optional deduplication
3. **CSV Join** - Join two or more CSV files on key columns (inner, left, right, outer, cross joins)
4. **Excel Sheet Join** - Join sheets within an Excel workbook
5. **Excel File Merge** - Merge multiple Excel files by combining sheets with the same name
6. **Chunked Processing** - Handle large files efficiently with streaming/chunked processing

### Key Features

- ✨ **Dual Interface**: Both GUI (PySimpleGUI) and CLI (Click)
- 🚀 **Performance**: Chunked processing for large files
- 🔄 **Flexible Joins**: Support for all SQL-style join types
- 🎯 **Smart Merging**: Strict and lenient modes for Excel merging
- 📊 **Deduplication**: Remove duplicate rows with configurable columns
- 🔍 **Type Hints**: Full type annotations for better IDE support
- 📝 **Logging**: Comprehensive logging with configurable levels
- 🌍 **Cross-Platform**: Works on Windows, Linux, and macOS

## System Requirements

- **Python**: 3.10 or higher
- **Operating Systems**: Windows 10+, Linux (any modern distro), macOS 10.15+
- **RAM**: 4GB minimum (8GB+ recommended for large files)
- **Disk Space**: 500MB for installation

See [PLATFORM_SUPPORT.md](PLATFORM_SUPPORT.md) for detailed platform compatibility information.

## Installation

### Quick Install

#### Windows
```cmd
git clone https://github.com/monkcoders/iLoveExcel.git
cd iLoveExcel
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

#### Linux
```bash
git clone https://github.com/monkcoders/iLoveExcel.git
cd iLoveExcel
sudo apt install python3-tk  # For GUI support
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

#### macOS
```bash
git clone https://github.com/monkcoders/iLoveExcel.git
cd iLoveExcel
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

### Install Dependencies Only

```bash
pip install -r requirements.txt
```

## Quick Start

### GUI Application

Start the graphical interface:

```bash
# Method 1: Using the installed command
iloveexcel-gui

# Method 2: Using Python module
python -m iLoveExcel
```

### Command Line Interface

```bash
# View available commands
csvexcel --help

# Convert CSVs to Excel
csvexcel csv-to-excel file1.csv file2.csv -o output.xlsx

# Union multiple CSVs
csvexcel union-multiple *.csv -o combined.csv --dedupe

# Join two CSVs
csvexcel join left.csv right.csv -o joined.csv --on "id" --how inner

# Merge Excel files
csvexcel merge-excel file1.xlsx file2.xlsx -o merged.xlsx
```

## Usage Examples

### Example 1: Convert CSVs to Excel

**Python API:**
```python
import iLoveExcel

iLoveExcel.csvs_to_excel(
    csv_files=['sales_q1.csv', 'sales_q2.csv', 'sales_q3.csv'],
    output_path='sales_2024.xlsx',
    sheet_names=['Q1', 'Q2', 'Q3']
)
```

**CLI:**
```bash
csvexcel csv-to-excel sales_q1.csv sales_q2.csv sales_q3.csv \
    -o sales_2024.xlsx \
    -s "Q1,Q2,Q3"
```

### Example 2: Union Multiple CSVs with Deduplication

**Python API:**
```python
import iLoveExcel

iLoveExcel.union_multiple_csvs(
    files=['data1.csv', 'data2.csv', 'data3.csv'],
    output_csv='all_data.csv',
    dedupe=True,
    dedupe_columns=['id', 'email']
)
```

**CLI:**
```bash
csvexcel union-multiple data1.csv data2.csv data3.csv \
    -o all_data.csv \
    --dedupe \
    --dedupe-columns "id,email"
```

### Example 3: Join CSVs (SQL-style)

**Python API:**
```python
import iLoveExcel

# Inner join
result_df = iLoveExcel.join_csvs(
    file_left='customers.csv',
    file_right='orders.csv',
    on='customer_id',
    how='inner',
    output_file='customer_orders.csv'
)

# Left join
result_df = iLoveExcel.join_csvs(
    file_left='employees.csv',
    file_right='departments.csv',
    on=['dept_id'],
    how='left',
    output_file='employee_dept.csv'
)
```

**CLI:**
```bash
# Inner join
csvexcel join customers.csv orders.csv \
    -o customer_orders.csv \
    --on "customer_id" \
    --how inner

# Left join
csvexcel join employees.csv departments.csv \
    -o employee_dept.csv \
    --on "dept_id" \
    --how left
```

### Example 4: Merge Excel Files

**Python API:**
```python
import iLoveExcel

# Lenient mode: union of all columns
iLoveExcel.merge_excel_files(
    excel_files=['report1.xlsx', 'report2.xlsx', 'report3.xlsx'],
    output_file='master_report.xlsx',
    mode='lenient'
)

# Strict mode: require identical columns
iLoveExcel.merge_excel_files(
    excel_files=['data1.xlsx', 'data2.xlsx'],
    output_file='combined.xlsx',
    mode='strict'
)
```

**CLI:**
```bash
# Lenient mode (default)
csvexcel merge-excel report1.xlsx report2.xlsx report3.xlsx \
    -o master_report.xlsx

# Strict mode
csvexcel merge-excel data1.xlsx data2.xlsx \
    -o combined.xlsx \
    --mode strict
```

## Project Structure

```
iLoveExcel/
├── src/
│   └── iLoveExcel/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # Entry point for python -m
│       ├── cli.py               # CLI interface (Click)
│       ├── gui.py               # GUI interface (PySimpleGUI)
│       ├── io.py                # I/O operations
│       ├── joins.py             # Join operations
│       ├── unions.py            # Union operations
│       ├── excel_merge.py       # Excel merging
│       └── utils.py             # Utilities
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_io.py
│   ├── test_joins.py
│   └── test_unions.py
├── examples/                    # Example files and demos
│   ├── sample1.csv
│   ├── sample2.csv
│   ├── employees.csv
│   ├── projects.csv
│   ├── demo.py
│   └── demo_run.sh
├── pyproject.toml              # Project configuration
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Troubleshooting

### Common Issues

#### Import Error: "No module named 'pandas'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

#### GUI doesn't start: "No module named 'PySimpleGUI'"
**Solution**: Install PySimpleGUI
```bash
pip install PySimpleGUI
```

#### Memory Error with large files
**Solution**: Use chunked processing
```python
union_multiple_csvs(files, output, chunksize=50000)
```

## License

This project is licensed under the MIT License.

## Contact

- **Repository**: [https://github.com/monkcoders/iLoveExcel](https://github.com/monkcoders/iLoveExcel)
- **Issues**: [https://github.com/monkcoders/iLoveExcel/issues](https://github.com/monkcoders/iLoveExcel/issues)

---

**Made with ❤️ by the iLoveExcel team**
