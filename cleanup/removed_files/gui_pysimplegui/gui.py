"""
iLoveExcel - GUI module.

PySimpleGUI-based graphical interface for CSV and Excel operations.
"""

import logging
import queue
import threading
from pathlib import Path
from typing import Dict, List, Optional

import PySimpleGUI as sg

from .excel_merge import merge_excel_files
from .io import csvs_to_excel
from .joins import join_csvs, join_excel_sheets_to_file
from .unions import union_csvs, union_multiple_csvs
from .utils import setup_logging, safe_sheet_name

logger = logging.getLogger(__name__)

# Set PySimpleGUI theme (compatible with both 4.x and 5.x)
try:
    sg.theme('LightBlue2')
except AttributeError:
    # PySimpleGUI 5.x uses different method
    try:
        sg.set_options(theme='LightBlue2')
    except:
        pass  # Continue without theme if not available


class WorkerThread(threading.Thread):
    """
    Background worker thread for long-running operations.
    """
    
    def __init__(self, task_func, args, kwargs, result_queue, log_queue):
        """
        Initialize worker thread.
        
        Args:
            task_func: Function to execute
            args: Positional arguments for task_func
            kwargs: Keyword arguments for task_func
            result_queue: Queue for result/error
            log_queue: Queue for log messages
        """
        super().__init__(daemon=True)
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs
        self.result_queue = result_queue
        self.log_queue = log_queue
    
    def run(self):
        """Execute the task and put result in queue."""
        try:
            self.log_queue.put(f"Starting operation...\n")
            result = self.task_func(*self.args, **self.kwargs)
            self.result_queue.put(('success', result))
            self.log_queue.put(f"✓ Operation completed successfully!\n")
        except Exception as e:
            logger.error(f"Worker thread error: {e}", exc_info=True)
            self.result_queue.put(('error', str(e)))
            self.log_queue.put(f"✗ Error: {e}\n")


def create_main_window():
    """Create and return the main GUI window layout with fixed structure and scrollable content."""
    
    # Operation selection
    operations_frame = [
        [sg.Text('Select Operation:', font=('Any', 11, 'bold'))],
        [sg.Radio('Create Excel from CSVs', 'OPERATION', key='-OP_CSV_TO_EXCEL-', 
                  default=True, enable_events=True)],
        [sg.Radio('Union CSVs', 'OPERATION', key='-OP_UNION-', enable_events=True)],
        [sg.Radio('Join CSVs', 'OPERATION', key='-OP_JOIN-', enable_events=True)],
        [sg.Radio('Join Excel Sheets', 'OPERATION', key='-OP_JOIN_EXCEL-', enable_events=True)],
        [sg.Radio('Merge Excel Files', 'OPERATION', key='-OP_MERGE_EXCEL-', enable_events=True)],
    ]
    
    # File selection - Multi-file input (for CSV to Excel, Union, Merge)
    multi_file_input = [
        [sg.Text('Select Files:', key='-LABEL_MULTI_FILES-', size=(15, 1)), 
         sg.Input(key='-FILES-', size=(50, 1)), 
         sg.FilesBrowse(key='-BROWSE_FILES-', file_types=(("CSV/Excel Files", "*.csv *.xlsx *.xls"), ("All Files", "*.*")))],
    ]
    
    # File selection - Two file inputs (for Join operations)
    dual_file_input = [
        [sg.Text('Left File:', key='-LABEL_LEFT-', size=(15, 1)), 
         sg.Input(key='-FILE_LEFT-', size=(50, 1)), 
         sg.FileBrowse(key='-BROWSE_LEFT-',
                       file_types=(("CSV/Excel Files", "*.csv *.xlsx *.xls"), ("All Files", "*.*")))],
        [sg.Text('Right File:', key='-LABEL_RIGHT-', size=(15, 1)), 
         sg.Input(key='-FILE_RIGHT-', size=(50, 1)), 
         sg.FileBrowse(key='-BROWSE_RIGHT-',
                       file_types=(("CSV/Excel Files", "*.csv *.xlsx *.xls"), ("All Files", "*.*")))],
    ]
    
    # CSV to Excel Parameters (fixed size)
    csv2excel_params = [
        [sg.Text('Sheet Names (comma-separated, optional):', size=(40, 1))],
        [sg.Input(key='-SHEET_NAMES-', size=(60, 1))],
        [sg.Text('Leave empty to use CSV filenames as sheet names', font=('Any', 9, 'italic'))],
    ]
    
    # Union Parameters (fixed size)
    union_params = [
        [sg.Checkbox('Deduplicate rows', key='-DEDUPE-', default=True)],
        [sg.Text('Dedupe Columns (comma-separated, optional):', size=(40, 1))],
        [sg.Input(key='-DEDUPE_COLS-', size=(60, 1))],
    ]
    
    # Join Parameters (fixed size)
    join_params = [
        [sg.Text('Join Keys (comma-separated):', size=(40, 1))],
        [sg.Input(key='-JOIN_KEYS-', size=(60, 1))],
        [sg.Text('Join Type:', size=(15, 1)), 
         sg.Combo(['inner', 'left', 'right', 'outer', 'cross'], 
                  default_value='inner', key='-JOIN_TYPE-', size=(15, 1))],
    ]
    
    # Excel Sheet Parameters (fixed size)
    excel_sheet_params = [
        [sg.Text('Left Sheet (name or index):', size=(40, 1))],
        [sg.Input(key='-SHEET_LEFT-', size=(30, 1))],
        [sg.Text('Right Sheet (name or index):', size=(40, 1))],
        [sg.Input(key='-SHEET_RIGHT-', size=(30, 1))],
    ]
    
    # Merge Parameters (fixed size)
    merge_params = [
        [sg.Radio('Lenient mode (union of columns)', 'MERGE_MODE', key='-LENIENT_MODE-', default=True)],
        [sg.Radio('Strict mode (identical columns required)', 'MERGE_MODE', key='-STRICT_MODE-')],
        [sg.Text(' ')],  # Spacer for consistent height
    ]
    
    # Operation-specific parameters in a FIXED SIZE container using pin to prevent reflow
    # All parameter sections are placed in the same position and visibility is toggled
    params_section = [
        [sg.pin(sg.Column(csv2excel_params, key='-FRAME_CSV2EXCEL-', visible=True, 
                         size=(700, 100), pad=(0, 0)))],
        [sg.pin(sg.Column(union_params, key='-FRAME_UNION-', visible=False, 
                         size=(700, 100), pad=(0, 0)))],
        [sg.pin(sg.Column(join_params, key='-FRAME_JOIN-', visible=False, 
                         size=(700, 100), pad=(0, 0)))],
        [sg.pin(sg.Column(excel_sheet_params, key='-FRAME_EXCEL_SHEET-', visible=False, 
                         size=(700, 100), pad=(0, 0)))],
        [sg.pin(sg.Column(merge_params, key='-FRAME_MERGE-', visible=False, 
                         size=(700, 100), pad=(0, 0)))],
    ]
    
    # Output settings
    output_section = [
        [sg.Text('Output File:', size=(15, 1)), 
         sg.Input(key='-OUTPUT-', size=(50, 1)), 
         sg.FileSaveAs(key='-BROWSE_OUTPUT-', 
                       file_types=(("Excel Files", "*.xlsx"), ("CSV Files", "*.csv"), ("All Files", "*.*")))],
    ]
    
    # Advanced options
    advanced_section = [
        [sg.Text('Chunk Size (optional):', size=(20, 1)), 
         sg.Input(key='-CHUNKSIZE-', size=(15, 1)),
         sg.Text('Log Level:', size=(10, 1)), 
         sg.Combo(['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                  default_value='INFO', key='-LOG_LEVEL-', size=(12, 1))],
    ]
    
    # Control buttons - ALWAYS visible at the same position
    button_section = [
        [sg.Button('▶ START OPERATION', size=(20, 2), button_color=('white', '#2E7D32'), 
                  font=('Any', 12, 'bold'), key='-RUN-'),
         sg.Button('Clear Log', size=(12, 1), key='-CLEAR-'),
         sg.Button('Help', size=(12, 1)),
         sg.Button('Exit', size=(12, 1), button_color=('white', '#C62828'))],
        [sg.ProgressBar(100, orientation='h', size=(80, 20), key='-PROGRESS-', visible=False)],
    ]
    
    # Output log
    log_section = [
        [sg.Multiline(size=(95, 10), key='-LOG-', autoscroll=True, disabled=True, 
                      background_color='#F0F0F0', text_color='#000000')],
    ]
    
    # Main scrollable content layout
    scrollable_content = [
        [sg.Frame('Operations', operations_frame, expand_x=True)],
        [sg.Frame('Input Files', 
                  [[sg.pin(sg.Column(multi_file_input, key='-INPUT_MULTI-', visible=True))],
                   [sg.pin(sg.Column(dual_file_input, key='-INPUT_DUAL-', visible=False))]], 
                  expand_x=True)],
        [sg.Frame('Parameters', params_section, expand_x=True)],
        [sg.Frame('Output', output_section, expand_x=True)],
        [sg.Frame('Advanced Options', advanced_section, expand_x=True)],
        [sg.HorizontalSeparator()],
        [sg.Column(button_section, justification='center', expand_x=True)],
        [sg.HorizontalSeparator()],
        [sg.Frame('Operation Log', log_section, expand_x=True)],
    ]
    
    # Main layout with scrollable column
    layout = [
        [sg.Text('iLoveExcel - CSV & Excel Operations', font=('Any', 16, 'bold'), 
                 justification='center', expand_x=True, pad=(0, 10))],
        [sg.HorizontalSeparator()],
        [sg.Column(scrollable_content, scrollable=True, vertical_scroll_only=True, 
                   size=(950, 700), expand_x=True, expand_y=True, pad=(5, 5))],
    ]
    
    window = sg.Window('iLoveExcel', layout, size=(980, 780), resizable=True, finalize=True)
    return window


def parse_files(files_str: str) -> List[str]:
    """Parse semicolon-separated file paths."""
    if not files_str or not files_str.strip():
        return []
    # PySimpleGUI FilesBrowse returns semicolon-separated paths
    files = [f.strip() for f in files_str.split(';') if f.strip()]
    return files


def parse_sheet_names(sheet_names_str: str) -> Optional[List[str]]:
    """Parse comma-separated sheet names."""
    if not sheet_names_str or not sheet_names_str.strip():
        return None
    return [s.strip() for s in sheet_names_str.split(',') if s.strip()]


def parse_join_keys(keys_str: str) -> List[str]:
    """Parse comma-separated join keys."""
    if not keys_str or not keys_str.strip():
        return []
    return [k.strip() for k in keys_str.split(',') if k.strip()]


def update_ui_for_operation(window, operation: str):
    """
    Update UI visibility based on selected operation using fixed layout.
    Only one parameter frame and one input type is visible at a time.
    
    Args:
        window: PySimpleGUI window object
        operation: Selected operation type
    """
    # Hide all parameter frames
    window['-FRAME_CSV2EXCEL-'].update(visible=False)
    window['-FRAME_UNION-'].update(visible=False)
    window['-FRAME_JOIN-'].update(visible=False)
    window['-FRAME_EXCEL_SHEET-'].update(visible=False)
    window['-FRAME_MERGE-'].update(visible=False)
    
    # Hide both input types initially
    window['-INPUT_MULTI-'].update(visible=False)
    window['-INPUT_DUAL-'].update(visible=False)
    
    # Show relevant components based on operation
    if operation == 'csv_to_excel':
        # CSV to Excel: show multi-file input and CSV2Excel params
        window['-INPUT_MULTI-'].update(visible=True)
        window['-LABEL_MULTI_FILES-'].update('Select CSV Files:')
        window['-FRAME_CSV2EXCEL-'].update(visible=True)
    
    elif operation == 'union':
        # Union: show multi-file input and union params
        window['-INPUT_MULTI-'].update(visible=True)
        window['-LABEL_MULTI_FILES-'].update('Select CSV Files to Union:')
        window['-FRAME_UNION-'].update(visible=True)
    
    elif operation == 'join':
        # Join CSVs: show dual file inputs and join params
        window['-INPUT_DUAL-'].update(visible=True)
        window['-FRAME_JOIN-'].update(visible=True)
    
    elif operation == 'join_excel':
        # Join Excel sheets: show multi-file input (single file), join + excel sheet params
        window['-INPUT_MULTI-'].update(visible=True)
        window['-LABEL_MULTI_FILES-'].update('Select Excel File:')
        window['-FRAME_JOIN-'].update(visible=True)
        window['-FRAME_EXCEL_SHEET-'].update(visible=True)
    
    elif operation == 'merge_excel':
        # Merge Excel: show multi-file input and merge params
        window['-INPUT_MULTI-'].update(visible=True)
        window['-LABEL_MULTI_FILES-'].update('Select Excel Files to Merge:')
        window['-FRAME_MERGE-'].update(visible=True)


def show_help():
    """Display help window with usage instructions."""
    help_text = """
iLoveExcel - Help

HOW TO USE:
1. Select an operation from the radio buttons
2. The interface will show only relevant options for that operation
3. Fill in the required fields
4. Click the green "▶ START OPERATION" button to execute
5. Monitor progress in the log pane

OPERATIONS:

1. Create Excel from CSVs
   - Select multiple CSV files using the Browse button
   - Each CSV becomes a sheet in a single Excel workbook
   - Optional: Provide custom sheet names (comma-separated)
   - Specify output Excel file location

2. Union CSVs
   - Select 2+ CSV files to combine
   - All rows are appended into a single CSV
   - Enable deduplication to remove duplicate rows
   - Optionally specify columns to check for duplicates
   - Specify output CSV file location

3. Join CSVs
   - Select left CSV file
   - Select right CSV file
   - Specify join keys (comma-separated column names)
   - Choose join type (inner, left, right, outer, cross)
   - Specify output CSV file location

4. Join Excel Sheets
   - Select an Excel file
   - Specify left sheet (name or 0-based index)
   - Specify right sheet (name or 0-based index)
   - Specify join keys and join type
   - Specify output Excel file location

5. Merge Excel Files
   - Select 2+ Excel files to merge
   - Merges sheets with the same name across workbooks
   - Lenient mode: unions all columns (default, safer)
   - Strict mode: requires identical columns in all files
   - Specify output Excel file location

TIPS:
- Use chunk size for very large CSV files (e.g., 10000, 50000)
- Deduplication requires loading all data into memory
- Set log level to DEBUG for detailed operation information
- Click "Clear Log" to clear the output pane
- All operations run in background, GUI stays responsive
    """
    
    sg.popup_scrolled(help_text, title='Help - iLoveExcel', size=(70, 30))


def run_operation_thread(operation: str, values: Dict, log_queue: queue.Queue) -> threading.Thread:
    """
    Start a background thread to run the selected operation.
    
    Returns the thread and a result queue.
    """
    result_queue = queue.Queue()
    
    try:
        if operation == 'csv_to_excel':
            files = parse_files(values['-FILES-'])
            if not files:
                raise ValueError("No input CSV files selected")
            
            output = values['-OUTPUT-']
            if not output:
                raise ValueError("No output Excel file specified")
            
            sheet_names = parse_sheet_names(values['-SHEET_NAMES-'])
            
            worker = WorkerThread(
                csvs_to_excel,
                (files, output),
                {'sheet_names': sheet_names},
                result_queue,
                log_queue
            )
        
        elif operation == 'union':
            files = parse_files(values['-FILES-'])
            if len(files) < 2:
                raise ValueError("Need at least 2 CSV files for union")
            
            output = values['-OUTPUT-']
            if not output:
                raise ValueError("No output CSV file specified")
            
            dedupe = values['-DEDUPE-']
            dedupe_cols_str = values['-DEDUPE_COLS-']
            dedupe_cols = parse_join_keys(dedupe_cols_str) if dedupe_cols_str else None
            
            chunksize_str = values['-CHUNKSIZE-']
            chunksize = int(chunksize_str) if chunksize_str else None
            
            worker = WorkerThread(
                union_multiple_csvs,
                (files, output),
                {'dedupe': dedupe, 'dedupe_columns': dedupe_cols, 'chunksize': chunksize, 'progress': False},
                result_queue,
                log_queue
            )
        
        elif operation == 'join':
            file_left = values['-FILE_LEFT-']
            file_right = values['-FILE_RIGHT-']
            
            if not file_left:
                raise ValueError("Left CSV file not selected")
            if not file_right:
                raise ValueError("Right CSV file not selected")
            
            output = values['-OUTPUT-']
            if not output:
                raise ValueError("No output CSV file specified")
            
            join_keys = parse_join_keys(values['-JOIN_KEYS-'])
            if not join_keys:
                raise ValueError("Join keys cannot be empty")
            
            join_type = values['-JOIN_TYPE-']
            join_on = join_keys[0] if len(join_keys) == 1 else join_keys
            
            worker = WorkerThread(
                join_csvs,
                (file_left, file_right, join_on),
                {'how': join_type, 'output_file': output},
                result_queue,
                log_queue
            )
        
        elif operation == 'join_excel':
            files = parse_files(values['-FILES-'])
            if not files or len(files) != 1:
                raise ValueError("Select exactly 1 Excel file")
            
            output = values['-OUTPUT-']
            if not output:
                raise ValueError("No output Excel file specified")
            
            sheet_left = values['-SHEET_LEFT-']
            sheet_right = values['-SHEET_RIGHT-']
            if not sheet_left or not sheet_right:
                raise ValueError("Both sheet names/indices must be specified")
            
            # Try to convert to int if numeric
            try:
                sheet_left = int(sheet_left)
            except ValueError:
                pass
            try:
                sheet_right = int(sheet_right)
            except ValueError:
                pass
            
            join_keys = parse_join_keys(values['-JOIN_KEYS-'])
            if not join_keys:
                raise ValueError("Join keys cannot be empty")
            
            join_type = values['-JOIN_TYPE-']
            join_on = join_keys[0] if len(join_keys) == 1 else join_keys
            
            worker = WorkerThread(
                join_excel_sheets_to_file,
                (files[0], output, sheet_left, sheet_right, join_on),
                {'how': join_type},
                result_queue,
                log_queue
            )
        
        elif operation == 'merge_excel':
            files = parse_files(values['-FILES-'])
            if len(files) < 2:
                raise ValueError("Need at least 2 Excel files for merging")
            
            output = values['-OUTPUT-']
            if not output:
                raise ValueError("No output Excel file specified")
            
            mode = 'strict' if values['-STRICT_MODE-'] else 'lenient'
            
            worker = WorkerThread(
                merge_excel_files,
                (files, output),
                {'mode': mode, 'progress': False},
                result_queue,
                log_queue
            )
        
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        worker.start()
        return worker, result_queue
    
    except Exception as e:
        log_queue.put(f"✗ Error: {e}\n")
        result_queue.put(('error', str(e)))
        return None, result_queue


def main_gui():
    """Main GUI application loop."""
    # Setup logging
    setup_logging(level='INFO')
    
    window = create_main_window()
    log_queue = queue.Queue()
    result_queue = None
    worker_thread = None
    
    # Initialize UI for default operation
    update_ui_for_operation(window, 'csv_to_excel')
    
    # Main event loop
    while True:
        event, values = window.read(timeout=100)  # 100ms timeout for checking queues
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        # Handle operation selection changes
        if event in ['-OP_CSV_TO_EXCEL-', '-OP_UNION-', '-OP_JOIN-', '-OP_JOIN_EXCEL-', '-OP_MERGE_EXCEL-']:
            # Determine which operation is selected
            if values['-OP_CSV_TO_EXCEL-']:
                update_ui_for_operation(window, 'csv_to_excel')
            elif values['-OP_UNION-']:
                update_ui_for_operation(window, 'union')
            elif values['-OP_JOIN-']:
                update_ui_for_operation(window, 'join')
            elif values['-OP_JOIN_EXCEL-']:
                update_ui_for_operation(window, 'join_excel')
            elif values['-OP_MERGE_EXCEL-']:
                update_ui_for_operation(window, 'merge_excel')
        
        if event == '-CLEAR-':
            window['-LOG-'].update('')
            window['-PROGRESS-'].update(visible=False)
        
        if event == 'Help':
            show_help()
        
        if event == '-RUN-':
            # Determine which operation is selected
            if values['-OP_CSV_TO_EXCEL-']:
                operation = 'csv_to_excel'
            elif values['-OP_UNION-']:
                operation = 'union'
            elif values['-OP_JOIN-']:
                operation = 'join'
            elif values['-OP_JOIN_EXCEL-']:
                operation = 'join_excel'
            elif values['-OP_MERGE_EXCEL-']:
                operation = 'merge_excel'
            else:
                sg.popup_error('Please select an operation')
                continue
            
            # Clear log and show progress
            window['-LOG-'].update('')
            window['-PROGRESS-'].update(visible=True, current_count=0)
            window['-LOG-'].print(f"═══════════════════════════════════════════════════\n", end='')
            window['-LOG-'].print(f"Starting: {operation.replace('_', ' ').title()}\n", end='')
            window['-LOG-'].print(f"═══════════════════════════════════════════════════\n", end='')
            
            # Start worker thread
            worker_thread, result_queue = run_operation_thread(operation, values, log_queue)
        
        # Check log queue for messages
        try:
            while True:
                message = log_queue.get_nowait()
                window['-LOG-'].print(message, end='')
        except queue.Empty:
            pass
        
        # Check result queue
        if result_queue:
            try:
                status, result = result_queue.get_nowait()
                window['-PROGRESS-'].update(visible=False)
                
                if status == 'success':
                    window['-LOG-'].print(f"\n{'═'*51}\n", end='')
                    window['-LOG-'].print(f"✓ OPERATION COMPLETED SUCCESSFULLY!\n", end='')
                    window['-LOG-'].print(f"{'═'*51}\n", end='')
                    sg.popup('✓ Success!', 
                            'Operation completed successfully!', 
                            keep_on_top=True,
                            button_color=('white', '#2E7D32'))
                else:
                    window['-LOG-'].print(f"\n{'═'*51}\n", end='')
                    window['-LOG-'].print(f"✗ OPERATION FAILED\n", end='')
                    window['-LOG-'].print(f"{'═'*51}\n", end='')
                    sg.popup_error('✗ Error', 
                                  f'Operation failed:\n\n{result}', 
                                  keep_on_top=True)
                
                result_queue = None
                worker_thread = None
            except queue.Empty:
                pass
    
    window.close()


if __name__ == '__main__':
    main_gui()
