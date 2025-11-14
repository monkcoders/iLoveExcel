# iLoveExcel - Complete Project Structure

## Project Overview

iLoveExcel is a comprehensive Python package for advanced CSV and Excel operations, featuring:
- **GUI Interface** (PySimpleGUI) for non-technical users
- **CLI Interface** (Click) for command-line operations
- **Python API** for programmatic use
- Support for large file processing with chunking
- Full type hints and comprehensive logging

## File Tree

```
iLoveExcel/
├── src/
│   └── iLoveExcel/
│       ├── __init__.py          # Package initialization with exports
│       ├── __main__.py          # Entry point for `python -m iLoveExcel`
│       ├── cli.py               # Click-based CLI with 8 commands
│       ├── gui.py               # PySimpleGUI interface with threading
│       ├── io.py                # I/O operations (CSV/Excel read/write)
│       ├── joins.py             # Join operations (CSV + Excel)
│       ├── unions.py            # Union/append operations
│       ├── excel_merge.py       # Excel file merging (strict/lenient)
│       └── utils.py             # Utilities (logging, validation)
│
├── tests/
│   ├── __init__.py
│   ├── test_io.py               # Tests for I/O module
│   ├── test_joins.py            # Tests for joins module
│   └── test_unions.py           # Tests for unions module
│
├── examples/
│   ├── sample1.csv              # Sample data: 5 people
│   ├── sample2.csv              # Sample data: 5 more people
│   ├── employees.csv            # Sample data: employee info
│   ├── projects.csv             # Sample data: project assignments
│   ├── demo.py                  # Python API demo script
│   └── demo_run.sh              # CLI demo script
│
├── pyproject.toml               # Project configuration (setuptools)
├── requirements.txt             # Production dependencies
├── README.md                    # Comprehensive documentation
└── cli.py                       # Legacy CLI (kept for compatibility)
```

## Module Descriptions

### Core Modules

#### `io.py` - I/O Operations (233 lines)
- `read_csv_chunked()` - Read CSV with optional chunking
- `write_csv()` - Write DataFrame to CSV
- `read_excel_sheet()` - Read specific Excel sheet
- `get_excel_sheet_names()` - List sheets in Excel file
- `csvs_to_excel()` - Convert multiple CSVs to Excel workbook
- `write_dataframes_to_excel()` - Write multiple sheets to Excel
- `validate_file_exists()` - File existence validation

#### `unions.py` - Union Operations (216 lines)
- `union_csvs()` - Union two CSVs with optional deduplication
- `union_multiple_csvs()` - Union many CSVs with chunked support
- `union_csvs_with_validation()` - Union with column validation

#### `joins.py` - Join Operations (232 lines)
- `join_csvs()` - Join two CSVs on key columns (inner/left/right/outer/cross)
- `join_excel_sheets()` - Join sheets within Excel file
- `join_excel_sheets_to_file()` - Join sheets and save to new file
- `join_multiple_csvs_sequential()` - Sequential joins of multiple files
- `validate_join_keys()` - Validate join keys exist

#### `excel_merge.py` - Excel Merging (258 lines)
- `merge_excel_files()` - Merge multiple Excel files by sheet name
- `merge_excel_sheets_by_name()` - Merge specific sheet across files
- `merge_excel_common_sheets_only()` - Merge only common sheets
- `get_common_sheets()` - Find sheets common to all files
- `_merge_sheets_strict()` - Strict mode (identical columns required)
- `_merge_sheets_lenient()` - Lenient mode (union of columns)

#### `utils.py` - Utilities (227 lines)
- `setup_logging()` - Configure logging system
- `confirm_overwrite()` - Interactive file overwrite confirmation
- `validate_positive_int()` - Integer validation
- `format_size()` - Human-readable file sizes
- `safe_sheet_name()` - Convert to valid Excel sheet name
- `parse_column_list()` - Parse comma-separated columns
- `validate_join_type()` - Validate join type parameter
- `ProgressTracker` - Progress tracking class

### Interface Modules

#### `cli.py` - Command-Line Interface (274 lines)
8 commands using Click:
1. `csv-to-excel` - Convert CSVs to Excel workbook
2. `union` - Union two CSV files
3. `union-multiple` - Union many CSV files
4. `join` - Join two CSVs on key
5. `join-excel-sheets` - Join Excel sheets
6. `merge-excel` - Merge Excel files
7. `merge-sheet` - Merge specific sheet across files

Global options: `--log-level`, `--log-file`, `--version`

#### `gui.py` - Graphical Interface (422 lines)
- PySimpleGUI-based windowed application
- 5 operation modes (radio buttons)
- File selection dialogs
- Parameter configuration (join keys, types, modes)
- Progress bar and log output
- Background threading for non-blocking operations
- `WorkerThread` class for async processing
- `main_gui()` - Main event loop

### Package Structure

#### `__init__.py` - Package Exports (84 lines)
Exports all public APIs:
- Version info: `__version__`, `__author__`, `__license__`
- I/O functions (6 functions)
- Union functions (3 functions)
- Join functions (4 functions)
- Excel merge functions (4 functions)
- Utilities (3 functions)

#### `__main__.py` - Entry Point (30 lines)
- Starts GUI when running `python -m iLoveExcel`
- Error handling and graceful shutdown

## Features Implemented

### 1. CSV to Excel Conversion ✓
- Multiple CSVs → Single Excel workbook
- Custom sheet names
- Automatic sheet name sanitization

### 2. CSV Union ✓
- Two-file union with `union_csvs()`
- Multi-file union with `union_multiple_csvs()`
- Optional deduplication (all columns or subset)
- Chunked processing for large files
- Column validation (strict/lenient)

### 3. CSV Join ✓
- All SQL join types: inner, left, right, outer, cross
- Single or multiple join keys
- Chunked processing support
- Sequential joins for 3+ files

### 4. Excel Sheet Join ✓
- Join sheets within same workbook
- Join by sheet name or index
- Save to new workbook

### 5. Excel File Merge ✓
- Merge by sheet name across files
- Strict mode (identical columns required)
- Lenient mode (union of columns, fill NaN)
- Progress tracking

### 6. Performance Features ✓
- Chunked CSV reading/writing
- Progressive disk writing for large unions
- Streaming support
- Memory-efficient operations

### 7. Robustness ✓
- Comprehensive error messages
- File validation
- Column validation
- Join key validation
- Type hints throughout
- Logging at INFO/DEBUG levels

### 8. Developer Features ✓
- Full type annotations
- Comprehensive docstrings
- Modular architecture
- Test stubs
- Example files and demos

## Installation & Usage

### Install
```bash
pip install -e .
```

### GUI
```bash
python -m iLoveExcel
# or
iloveexcel-gui
```

### CLI
```bash
csvexcel --help
csvexcel csv-to-excel file1.csv file2.csv -o output.xlsx
csvexcel join left.csv right.csv -o joined.csv --on "id" --how inner
csvexcel merge-excel file1.xlsx file2.xlsx -o merged.xlsx
```

### Python API
```python
import iLoveExcel

# Convert CSVs to Excel
iLoveExcel.csvs_to_excel(['file1.csv', 'file2.csv'], 'output.xlsx')

# Union with deduplication
iLoveExcel.union_multiple_csvs(['a.csv', 'b.csv'], 'out.csv', dedupe=True)

# Inner join
df = iLoveExcel.join_csvs('left.csv', 'right.csv', on='id', how='inner')

# Merge Excel files
iLoveExcel.merge_excel_files(['f1.xlsx', 'f2.xlsx'], 'merged.xlsx')
```

## Examples Provided

### Sample Data Files
- `sample1.csv` - 5 people (id, name, age, city)
- `sample2.csv` - 5 more people
- `employees.csv` - Employee info (id, department, salary)
- `projects.csv` - Project assignments (id, project, hours)

### Demo Scripts
- `demo.py` - Python API examples (5 demos)
- `demo_run.sh` - CLI examples (4 commands)

## Testing

Test stubs provided for:
- `test_io.py` - I/O operations testing
- `test_unions.py` - Union operations testing
- `test_joins.py` - Join operations testing

Run tests:
```bash
pytest
pytest --cov=iLoveExcel
```

## Dependencies

### Production
- pandas>=2.0.0
- PySimpleGUI>=4.60.0
- openpyxl>=3.1.0
- xlsxwriter>=3.1.0
- click>=8.1.0
- tqdm>=4.65.0

### Development
- pytest>=7.4.0
- pytest-cov>=4.1.0
- mypy>=1.5.0
- black>=23.7.0
- flake8>=6.1.0

### Optional
- dask[dataframe]>=2023.1.0 (for very large files)

## Key Design Decisions

1. **Dual Interface**: GUI for ease of use, CLI for automation
2. **Chunked Processing**: Support files larger than memory
3. **Modular Architecture**: Separate modules for each operation type
4. **Type Safety**: Full type hints for IDE support
5. **Flexible Merging**: Both strict and lenient modes
6. **Progressive Writing**: Write to disk during processing
7. **Background Threading**: Non-blocking GUI operations
8. **Comprehensive Logging**: DEBUG and INFO levels

## Entry Points

Configured in `pyproject.toml`:
- `csvexcel` → `iLoveExcel.cli:main` (CLI)
- `iloveexcel-gui` → `iLoveExcel.__main__:main` (GUI)

## Total Lines of Code

- Core modules: ~1,400 lines
- Interface modules: ~700 lines
- Tests: ~250 lines
- Examples: ~150 lines
- Config/docs: ~600 lines
- **Total: ~3,100 lines** of production code

## Next Steps for Production

1. Add comprehensive test coverage (currently stubs)
2. Add input sanitization for GUI
3. Implement progress callbacks for tqdm
4. Add Excel formula preservation
5. Add data type inference options
6. Create standalone executable (PyInstaller)
7. Add configuration file support
8. Implement undo/history for GUI
9. Add preview panes for data
10. Create detailed API documentation

---

**Project Status**: Alpha (v0.1.0)  
**License**: MIT  
**Python**: 3.10+
