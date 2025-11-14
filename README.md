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
6. **CSV Side-by-Side Diff** - 🆕 Compare two CSV files row-by-row with highlighting
7. **Chunked Processing** - Handle large files efficiently with streaming/chunked processing

### Key Features

- ✨ **Multiple GUI Backends**: PySimpleGUI or Tkinter (fully open-source option)
- 🔍 **CSV Diff Tool**: 🆕 Side-by-side comparison with Excel export and highlighting
- 📏 **Auto-Column-Width**: 🆕 Automatic Excel column sizing based on content
- 📦 **Standalone Executables**: 🆕 Build with PyInstaller for distribution
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
# Method 1: Using the installed command (default: PySimpleGUI)
iloveexcel-gui

# Method 2: Using Python module
python -m iLoveExcel

# Method 3: Choose GUI backend explicitly
iloveexcel-gui --gui-backend tkinter    # Use Tkinter (fully open-source)
iloveexcel-gui --gui-backend pysimplegui  # Use PySimpleGUI (default)

# Method 4: Set environment variable
export ILOVEEXCEL_GUI=tkinter  # Linux/macOS
set ILOVEEXCEL_GUI=tkinter     # Windows
iloveexcel-gui
```

**Available GUI Backends:**
- **PySimpleGUI** (default) - Feature-rich with polished UI
- **Tkinter** (new!) - Fully open-source, included with Python

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


# CSV side-by-side diff (CLI)
csvexcel diff file_a.csv file_b.csv -o comparison.xlsx --key-columns "id,email"

# Use CSV diff from GUI
# Tools menu → CSV Side-by-Side Diff
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

### Example 5: CSV Side-by-Side Diff (NEW!)

**Python API:**
```python
from iLoveExcel import diff_csv_side_by_side, export_diff_to_excel

# Compare two CSV files
diff_df, stats = diff_csv_side_by_side(
    file_a='version_a.csv',
    file_b='version_b.csv',
    key_columns=['id'],  # Align by key column
    compare_by_index=False,
    ignore_whitespace=True,
    show_only_diffs=True
)

# Export to Excel with highlighting
export_diff_to_excel(
    diff_df,
    stats,
    'comparison_report.xlsx',
    file_a_name='Version A',
    file_b_name='Version B',
    highlight=True  # Color-code differences
)

print(f"Found {stats['different']} differences")
```

**GUI:**
- Open **Tools** → **CSV Side-by-Side Diff**
- Select files A and B
- Choose comparison mode (by index or by key)
- Configure options (ignore whitespace, case sensitivity, etc.)
- Click **Compare** to see results
- Click **Export to Excel** to save with highlighting

**CLI:**
```bash
csvexcel diff version_a.csv version_b.csv \
    -o comparison_report.xlsx \
    --key-columns "id" \
    --ignore-whitespace \
    --show-only-diffs
```

### Example 6: Auto-Column-Width for Excel (NEW!)

**Python API:**
```python
from iLoveExcel import apply_auto_column_width
import pandas as pd

# Create Excel file
df = pd.DataFrame({
    'Short': ['A', 'B'],
    'Very Long Column Name': ['Value 1', 'Value 2']
})
df.to_excel('output.xlsx', index=False)

# Apply auto-width
apply_auto_column_width(
    'output.xlsx',
    min_width=10,
    max_width=50,
    padding=2
)
```

**With ExcelWriter:**
```python
from iLoveExcel import apply_auto_width_to_writer
import pandas as pd

with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Data', index=False)
    apply_auto_width_to_writer(writer, 'Data')
```

## Building and Distribution

iLoveExcel supports **three distribution methods**, each suited for different use cases:

### Method 1: Wheel Package (Recommended for Python Users)

Build a Python wheel for easy installation via pip. This is the **recommended method** for Python developers.

**For Developers:**

```bash
# Build the wheel
./scripts/build_wheel.sh           # Linux/macOS
scripts\build_wheel.bat            # Windows

# Output: dist/iLoveExcel-0.1.0-py3-none-any.whl
```

**For End Users:**

```bash
# Easy install with helper script
./scripts/install_from_wheel.sh    # Linux/macOS
scripts\install_from_wheel.bat     # Windows

# Or manual install
python3 -m venv .venv
source .venv/bin/activate           # Linux/macOS: source .venv/bin/activate
pip install dist/iLoveExcel-*.whl
iloveexcel  # Launch GUI
```

**Install with Optional GUI Backends:**

```bash
# Install with PySimpleGUI
pip install dist/iLoveExcel-*.whl[gui_pysimplegui]

# Install with Streamlit web UI
pip install dist/iLoveExcel-*.whl[gui_streamlit]

# Install all extras (all GUIs + dev tools)
pip install dist/iLoveExcel-*.whl[all]
```

**Available Extras:**
- `[gui_pysimplegui]` - PySimpleGUI desktop GUI
- `[gui_streamlit]` - Streamlit web interface
- `[gui_customtkinter]` - Modern Tkinter (customtkinter)
- `[web]` - All web interfaces (Streamlit)
- `[packaging]` - Build tools (setuptools, wheel, build, twine)
- `[dev]` - Development tools (pytest, black, mypy, ruff)
- `[gui]` - All GUI backends
- `[all]` - Everything (all GUIs + dev + packaging tools)

**What's Included in the Base Install?**
- ✅ Command-line interface (`csvexcel`)
- ✅ Tkinter GUI (`iloveexcel`) - open-source, included with Python
- ✅ All core operations (CSV/Excel processing, diffs, joins, unions)
- ✅ Dependencies: pandas, openpyxl, xlsxwriter, click, tqdm

**System Requirements:**
- **Linux users**: Install `python3-tk` if Tkinter GUI is not available:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk
  
  # Fedora/RHEL
  sudo dnf install python3-tkinter
  
  # Arch Linux
  sudo pacman -S tk
  ```
- **Windows/macOS**: Tkinter is included with Python by default

**Advantages:**
- ✅ Small size (~50KB wheel + dependencies downloaded separately)
- ✅ Easy to share (wheel + requirements.txt)
- ✅ Integrates with existing Python environments
- ✅ Optional extras for different GUI backends
- ✅ Fast installation
- ❌ Requires Python 3.10+ on user's system
- ❌ Dependencies installed separately

See [docs/packaging/notes.md](docs/packaging/notes.md) for technical details on wheel packaging.

### Method 2: Zipapp (Portable Python Archive)

Create a single-file Python archive (`.pyz`) for easy distribution. Requires Python on the target system.

```bash
# Build zipapp
./packaging/build_zipapp.sh          # Linux/macOS
packaging\build_zipapp.bat           # Windows

# Run the zipapp
python3 dist/iLoveExcel.pyz          # No installation needed!
```

**Advantages:**
- ✅ Single file distribution
- ✅ No installation required (just run with Python)
- ✅ Dependencies bundled (except pandas/numpy - too large)
- ❌ Requires Python 3.10+ on user's system
- ❌ Larger than wheel (~2-5MB)

### Method 3: Standalone Executables (PyInstaller)

Build native executables for distribution **without requiring Python** on the target system.

```bash
# Install PyInstaller
pip install pyinstaller

# Build all executables (CLI + both GUIs)
./packaging/build_with_pyinstaller.sh --mode all

# Build specific component
./packaging/build_with_pyinstaller.sh --mode gui-tk   # Tkinter GUI only
./packaging/build_with_pyinstaller.sh --mode cli      # CLI only

# Create folder distribution (faster startup)
./packaging/build_with_pyinstaller.sh --type onedir

# Windows
packaging\build_with_pyinstaller.bat --mode all
```

Executables will be in `dist/`:
- `iLoveExcel-CLI` - Command-line interface
- `iLoveExcel-GUI` - PySimpleGUI interface
- `iLoveExcel-TkGUI` - Tkinter interface

**Advantages:**
- ✅ No Python required on target system
- ✅ Easy for non-technical users
- ✅ Native look and feel
- ❌ Large file size (~50-150MB per executable)
- ❌ Separate builds for each platform
- ❌ May trigger antivirus warnings (false positives)

See [packaging/README.md](packaging/README.md) and [docs/packaging/packaging_eval.md](docs/packaging/packaging_eval.md) for detailed information.

### Distribution Comparison

| Method | File Size | Python Required | Install Steps | Best For |
|--------|-----------|-----------------|---------------|----------|
| **Wheel** | ~50KB | ✅ Yes (3.10+) | 2-3 commands | Python developers, CI/CD |
| **Zipapp** | ~2-5MB | ✅ Yes (3.10+) | 0 (just run) | Quick sharing, portable |
| **PyInstaller** | ~50-150MB | ❌ No | 0 (just run) | Non-Python users, desktop apps |

### Publishing to PyPI (Optional)

To publish your wheel to PyPI for `pip install iLoveExcel`:

```bash
# Install twine
pip install twine

# Build wheel
./scripts/build_wheel.sh

# Upload to PyPI
twine upload dist/iLoveExcel-*.whl

# Users can now install with:
pip install iLoveExcel
```

See [docs/packaging/notes.md](docs/packaging/notes.md) for PyPI publishing details.

## Project Structure

```
iLoveExcel/
├── src/
│   └── iLoveExcel/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # Entry point for python -m
│       ├── cli.py               # CLI interface (Click)
│       ├── gui.py               # GUI interface (PySimpleGUI)
│       ├── gui_tk.py            # 🆕 GUI interface (Tkinter)
│       ├── gui_common.py        # 🆕 Shared GUI utilities
│       ├── gui_launcher.py      # 🆕 GUI backend selection
│       ├── io.py                # I/O operations
│       ├── io_helpers.py        # 🆕 Auto-column-width utilities
│       ├── diffs.py             # 🆕 CSV diff functionality
│       ├── joins.py             # Join operations
│       ├── unions.py            # Union operations
│       ├── excel_merge.py       # Excel merging
│       └── utils.py             # Utilities
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_io.py
│   ├── test_joins.py
│   ├── test_unions.py
│   ├── test_diffs.py            # 🆕 Diff tests
│   └── test_auto_width.py       # 🆕 Auto-width tests
├── examples/                    # Example files and demos
│   ├── sample1.csv
│   ├── sample2.csv
│   ├── employees.csv
│   ├── projects.csv
│   ├── demo.py
│   ├── demo_run.sh
│   └── demo_run.bat             # 🆕 Windows demo script
├── packaging/                   # 🆕 Build scripts
│   ├── build_with_pyinstaller.sh
│   ├── build_with_pyinstaller.bat
│   └── README.md
├── docs/                        # 🆕 Documentation
│   ├── ui_mockups/
│   │   └── csv_diff_mockup.md
│   └── packaging/
│       └── packaging_eval.md
├── pyproject.toml              # Project configuration
├── requirements.txt            # Dependencies
├── INSTALL.md                  # Installation guide
├── PLATFORM_SUPPORT.md         # Platform compatibility
├── DEPLOYMENT_OPTIONS.md       # Deployment guide
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
**Solution 1**: Install PySimpleGUI
```bash
pip install PySimpleGUI
```

**Solution 2**: Use Tkinter backend instead (open-source, included with Python)
```bash
iloveexcel-gui --gui-backend tkinter
# or
export ILOVEEXCEL_GUI=tkinter
iloveexcel-gui
```

#### Memory Error with large files
**Solution**: Use chunked processing
```python
union_multiple_csvs(files, output, chunksize=50000)
```

#### Executable flagged by antivirus
**Solution**: This is a false positive common with PyInstaller executables
- Add exception in your antivirus software
- Download from trusted source (GitHub Releases)
- Verify SHA256 checksum
- Consider code signing for production distribution

See [packaging/README.md](packaging/README.md) for more troubleshooting.

## Documentation

- **[Installation Guide](INSTALL.md)** - Detailed installation instructions
- **[Platform Support](PLATFORM_SUPPORT.md)** - Platform compatibility matrix
- **[Deployment Options](DEPLOYMENT_OPTIONS.md)** - Web and standalone deployment
- **[Streamlit Deployment](STREAMLIT_DEPLOYMENT.md)** - Deploy as web application
- **[Packaging Guide](packaging/README.md)** - Create standalone executables
- **[Packaging Evaluation](docs/packaging/packaging_eval.md)** - Compare packaging tools
- **[CSV Diff UI Mockup](docs/ui_mockups/csv_diff_mockup.md)** - Diff feature design

## Web Application

iLoveExcel can also run as a web application using Streamlit:

```bash
# Install Streamlit
pip install streamlit

# Run web interface
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

See [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) for deploying to Streamlit Cloud (free hosting).

## License

This project is licensed under the MIT License.

## Contact

- **Repository**: [https://github.com/monkcoders/iLoveExcel](https://github.com/monkcoders/iLoveExcel)
- **Issues**: [https://github.com/monkcoders/iLoveExcel/issues](https://github.com/monkcoders/iLoveExcel/issues)

---

**Made with ❤️ by the @monkcoders**
