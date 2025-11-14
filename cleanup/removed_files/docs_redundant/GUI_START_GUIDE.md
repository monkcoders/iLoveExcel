# iLoveExcel GUI - Quick Start Guide

## ✅ SUCCESS! The GUI is now running!

## How to Start the GUI

### Method 1: Using the Start Script (Easiest)
```bash
./start_gui.sh
```

### Method 2: Manual Start
```bash
cd /home/abhishek/projects/iLoveExcel/iLoveExcel
source .venv/bin/activate
python -m iLoveExcel
```

### Method 3: Using the installed command
```bash
cd /home/abhishek/projects/iLoveExcel/iLoveExcel
source .venv/bin/activate
iloveexcel-gui
```

## Important Notes

### Dependencies Installed
- ✅ pandas
- ✅ PySimpleGUI 5.0.10 (from private server)
- ✅ openpyxl
- ✅ xlsxwriter
- ✅ click
- ✅ tqdm
- ✅ python3-tk (system package)

### GUI Features Available

1. **Create Excel from CSVs**
   - Select multiple CSV files
   - Each becomes a sheet in the workbook

2. **Union CSVs**
   - Combine multiple CSVs
   - Optional deduplication

3. **Join CSVs**
   - SQL-style joins (inner, left, right, outer, cross)
   - Specify join keys

4. **Join Excel Sheets**
   - Join sheets within a workbook
   - By name or index

5. **Merge Excel Files**
   - Combine multiple Excel files
   - Strict or lenient mode

### Using the GUI

1. Select an operation (radio button)
2. Choose input files (Browse buttons)
3. Configure parameters (join keys, modes, etc.)
4. Set output file location
5. Click "Run"
6. Monitor progress in the log pane

### Troubleshooting

If the GUI doesn't start:
1. Make sure you're in the project directory
2. Activate the virtual environment: `source .venv/bin/activate`
3. Check tkinter is installed: `python -c "import tkinter"`
4. Re-install PySimpleGUI: `pip install --extra-index-url https://PySimpleGUI.net/install PySimpleGUI`

### Stopping the GUI

- Click the "Exit" button in the GUI window
- Or press Ctrl+C in the terminal

## CLI Alternative

If you prefer command-line:
```bash
source .venv/bin/activate
csvexcel --help
csvexcel csv-to-excel file1.csv file2.csv -o output.xlsx
```

## Examples

Try the demo scripts:
```bash
source .venv/bin/activate
python examples/demo.py
./examples/demo_run.sh
```

## Support

- Full documentation: `README.md`
- Installation guide: `INSTALL.md`
- Project structure: `PROJECT_STRUCTURE.md`
