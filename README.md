# iLoveExcel

**Advanced CSV and Excel operations with GUI and CLI**

A powerful Python tool for CSV/Excel file operations including merging, joining, unions, and conversions.

---

## ✨ Features

- 📊 **CSV ↔ Excel Conversion**: Seamless bidirectional conversion
- 🔀 **Data Merging**: Combine multiple CSV/Excel files
- 🔗 **Join Operations**: Inner, left, right, outer joins with key columns
- �� **Union Operations**: Combine files with same structure
- 📈 **Auto Column Width**: Automatic Excel column sizing
- 🎨 **GUI Interface**: User-friendly Tkinter GUI
- ⚡ **CLI Tool**: Command-line interface for automation
- 🌐 **Web Interface**: Optional Streamlit web app

---

## 🚀 Quick Start

### Installation

```bash
# Install from wheel (recommended)
pip install dist/iloveexcel-*.whl

# Or install from source
pip install -e .
```

### Usage

**GUI (Graphical Interface)**
```bash
iloveexcel
```

**CLI (Command Line)**
```bash
csvexcel --help
csvexcel convert input.csv output.xlsx
```

**Web Interface (Optional)**
```bash
pip install streamlit
streamlit run streamlit_app.py
```

---

## 📦 Distribution

### Building a Wheel Package

```bash
./scripts/build_wheel.sh
```

### Installing from Wheel

```bash
./scripts/install_from_wheel.sh
# Or: pip install dist/iloveexcel-*.whl
```

---

## 🛠️ Development

### Setup Development Environment

```bash
# Install with dev dependencies
pip install -e .[dev]

# Run tests
pytest

# Code formatting
black src/ tests/

# Type checking
mypy src/
```

### Running Tests

```bash
pytest tests/
pytest --cov=iLoveExcel tests/  # With coverage
```

---

## 📋 Requirements

- **Python**: 3.10+
- **Core Dependencies**: pandas, openpyxl, xlsxwriter, click
- **GUI**: Tkinter (included with Python)
- **Optional**: streamlit (for web interface)

---

## 📚 Documentation

For detailed documentation, see:
- `README.detailed.md` - Comprehensive guide
- `cleanup/removed_files/docs_redundant/` - Archived detailed docs
- Examples in `examples/` directory

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🔗 Links

- **Repository**: https://github.com/monkcoders/iLoveExcel
- **Issues**: https://github.com/monkcoders/iLoveExcel/issues

---

## ⚡ Quick Examples

**Convert CSV to Excel:**
```python
from iLoveExcel import csv_to_excel
csv_to_excel("data.csv", "data.xlsx")
```

**Join Two CSV Files:**
```python
from iLoveExcel import join_csvs
join_csvs("file1.csv", "file2.csv", "output.csv", 
          join_key="id", join_type="inner")
```

**Launch GUI:**
```python
from iLoveExcel import launch_gui
launch_gui()
```

---

**Version**: 0.1.0  
**Last Updated**: November 2025
