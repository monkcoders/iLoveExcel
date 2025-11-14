"""
iLoveExcel - Tkinter GUI module.

Modern Tkinter-based graphical interface for CSV and Excel operations.
Provides an alternative to PySimpleGUI with full open-source stack.
"""

import logging
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .excel_merge import merge_excel_files
from .io import csvs_to_excel
from .joins import join_csvs, join_excel_sheets_to_file
from .unions import union_csvs, union_multiple_csvs
from .utils import setup_logging
from .gui_common import WorkerThread, GUIState, validate_file_path, parse_file_list, format_bytes
from .diffs import diff_csv_side_by_side, export_diff_to_excel

logger = logging.getLogger(__name__)


class iLoveExcelGUI:
    """Main Tkinter GUI application for iLoveExcel."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("iLoveExcel - CSV & Excel Operations")
        self.root.geometry("1000x800")
        
        # State management
        self.state = GUIState()
        self.worker_thread = None
        self.log_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        # Operation mapping
        self.operation = None  # 'csv_to_excel', 'union', 'join', 'join_excel', 'merge_excel', 'csv_diff'
        
        # Create GUI components
        self._create_widgets()
        self._create_menu()
        
        # Start log polling
        self._poll_log_queue()
        
        logger.info("Tkinter GUI initialized")
    
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear Log", command=self._clear_log)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="CSV Side-by-Side Diff", command=self._open_diff_window)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help", command=self._show_help)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure root grid weight
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="iLoveExcel - CSV & Excel Operations",
            font=("TkDefaultFont", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Operation selection
        self._create_operation_section(main_frame, row=1)
        
        # File input section (multi-file or dual-file)
        self.input_frame = ttk.LabelFrame(main_frame, text="Input Files", padding="10")
        self.input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        self.input_frame.columnconfigure(1, weight=1)
        
        # Multi-file input widgets
        self.multi_file_label = ttk.Label(self.input_frame, text="Select Files:")
        self.multi_file_entry = ttk.Entry(self.input_frame, width=60)
        self.multi_file_button = ttk.Button(self.input_frame, text="Browse...", command=self._browse_multi_files)
        
        # Dual-file input widgets
        self.left_file_label = ttk.Label(self.input_frame, text="Left File:")
        self.left_file_entry = ttk.Entry(self.input_frame, width=60)
        self.left_file_button = ttk.Button(self.input_frame, text="Browse...", command=self._browse_left_file)
        
        self.right_file_label = ttk.Label(self.input_frame, text="Right File:")
        self.right_file_entry = ttk.Entry(self.input_frame, width=60)
        self.right_file_button = ttk.Button(self.input_frame, text="Browse...", command=self._browse_right_file)
        
        # Parameters section (dynamic based on operation)
        self.params_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="10")
        self.params_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        self.params_frame.columnconfigure(1, weight=1)
        
        # We'll create parameter widgets dynamically
        self.param_widgets = {}
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.output_entry = ttk.Entry(output_frame, width=60)
        self.output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.output_button = ttk.Button(output_frame, text="Browse...", command=self._browse_output)
        self.output_button.grid(row=0, column=2, padx=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, pady=10)
        
        self.start_button = ttk.Button(
            button_frame,
            text="▶ START OPERATION",
            command=self._start_operation,
            style="Accent.TButton"
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="⏹ STOP",
            command=self._stop_operation,
            state=tk.DISABLED
        )
        self.stop_button.grid(row=0, column=1, padx=5)
        
        ttk.Button(button_frame, text="Clear Log", command=self._clear_log).grid(row=0, column=2, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            mode='indeterminate',
            length=300
        )
        self.progress_bar.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Log output
        log_frame = ttk.LabelFrame(main_frame, text="Operation Log", padding="10")
        log_frame.grid(row=7, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            width=80,
            height=15,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main_frame row weights for resizing
        main_frame.rowconfigure(7, weight=1)
        
        # Set initial operation
        self._update_ui_for_operation('csv_to_excel')
    
    def _create_operation_section(self, parent, row):
        """Create operation selection radio buttons."""
        op_frame = ttk.LabelFrame(parent, text="Select Operation", padding="10")
        op_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.operation_var = tk.StringVar(value='csv_to_excel')
        
        operations = [
            ('csv_to_excel', 'Create Excel from CSVs'),
            ('union', 'Union CSVs'),
            ('join', 'Join CSVs'),
            ('join_excel', 'Join Excel Sheets'),
            ('merge_excel', 'Merge Excel Files'),
        ]
        
        for idx, (op_key, op_label) in enumerate(operations):
            rb = ttk.Radiobutton(
                op_frame,
                text=op_label,
                variable=self.operation_var,
                value=op_key,
                command=self._on_operation_changed
            )
            rb.grid(row=idx // 3, column=idx % 3, sticky=tk.W, padx=10, pady=2)
    
    def _on_operation_changed(self):
        """Handle operation radio button change."""
        operation = self.operation_var.get()
        self._update_ui_for_operation(operation)
    
    def _update_ui_for_operation(self, operation: str):
        """Update UI visibility based on selected operation."""
        self.operation = operation
        
        # Hide all input widgets first
        self._hide_all_input_widgets()
        
        # Clear parameter widgets
        for widget in self.param_widgets.values():
            if isinstance(widget, (list, tuple)):
                for w in widget:
                    w.grid_forget()
            else:
                widget.grid_forget()
        self.param_widgets.clear()
        
        # Show appropriate inputs and parameters
        if operation == 'csv_to_excel':
            self._show_multi_file_input("Select CSV Files:")
            self._create_csv2excel_params()
        
        elif operation == 'union':
            self._show_multi_file_input("Select CSV Files to Union:")
            self._create_union_params()
        
        elif operation == 'join':
            self._show_dual_file_input()
            self._create_join_params()
        
        elif operation == 'join_excel':
            self._show_multi_file_input("Select Excel File:")
            self._create_join_params()
            self._create_excel_sheet_params()
        
        elif operation == 'merge_excel':
            self._show_multi_file_input("Select Excel Files to Merge:")
            self._create_merge_params()
        
        self._log(f"Switched to operation: {operation}")
    
    def _hide_all_input_widgets(self):
        """Hide all input widgets."""
        self.multi_file_label.grid_forget()
        self.multi_file_entry.grid_forget()
        self.multi_file_button.grid_forget()
        self.left_file_label.grid_forget()
        self.left_file_entry.grid_forget()
        self.left_file_button.grid_forget()
        self.right_file_label.grid_forget()
        self.right_file_entry.grid_forget()
        self.right_file_button.grid_forget()
    
    def _show_multi_file_input(self, label_text: str):
        """Show multi-file input widgets."""
        self.multi_file_label.config(text=label_text)
        self.multi_file_label.grid(row=0, column=0, sticky=tk.W, padx=5)
        self.multi_file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        self.multi_file_button.grid(row=0, column=2, padx=5)
    
    def _show_dual_file_input(self):
        """Show dual-file input widgets."""
        self.left_file_label.grid(row=0, column=0, sticky=tk.W, padx=5)
        self.left_file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        self.left_file_button.grid(row=0, column=2, padx=5)
        
        self.right_file_label.grid(row=1, column=0, sticky=tk.W, padx=5)
        self.right_file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        self.right_file_button.grid(row=1, column=2, padx=5)
    
    def _create_csv2excel_params(self):
        """Create parameters for CSV to Excel operation."""
        row = 0
        
        # Sheet names
        label = ttk.Label(self.params_frame, text="Sheet Names:")
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        
        entry = ttk.Entry(self.params_frame, width=50)
        entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        help_label = ttk.Label(
            self.params_frame,
            text="(Optional: comma-separated sheet names)",
            font=("TkDefaultFont", 8)
        )
        help_label.grid(row=row, column=2, sticky=tk.W, padx=5)
        
        self.param_widgets['sheet_names'] = (label, entry, help_label)
    
    def _create_union_params(self):
        """Create parameters for Union operation."""
        row = 0
        
        # Deduplication checkbox
        dedupe_var = tk.BooleanVar(value=False)
        cb = ttk.Checkbutton(self.params_frame, text="Remove duplicate rows", variable=dedupe_var)
        cb.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)
        self.param_widgets['dedupe_var'] = dedupe_var
        self.param_widgets['dedupe_cb'] = cb
        row += 1
        
        # Dedupe columns
        label = ttk.Label(self.params_frame, text="Dedupe Columns:")
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        
        entry = ttk.Entry(self.params_frame, width=50)
        entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        help_label = ttk.Label(
            self.params_frame,
            text="(Optional: comma-separated column names)",
            font=("TkDefaultFont", 8)
        )
        help_label.grid(row=row, column=2, sticky=tk.W, padx=5)
        
        self.param_widgets['dedupe_cols'] = (label, entry, help_label)
        row += 1
        
        # Chunk size
        label = ttk.Label(self.params_frame, text="Chunk Size:")
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        
        entry = ttk.Entry(self.params_frame, width=20)
        entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=2)
        
        help_label = ttk.Label(
            self.params_frame,
            text="(Optional: for large files, e.g., 10000)",
            font=("TkDefaultFont", 8)
        )
        help_label.grid(row=row, column=2, sticky=tk.W, padx=5)
        
        self.param_widgets['chunksize'] = (label, entry, help_label)
    
    def _create_join_params(self):
        """Create parameters for Join operations."""
        row = 0
        
        # Join keys
        label = ttk.Label(self.params_frame, text="Join Keys:")
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        
        entry = ttk.Entry(self.params_frame, width=50)
        entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        help_label = ttk.Label(
            self.params_frame,
            text="(Comma-separated column names)",
            font=("TkDefaultFont", 8)
        )
        help_label.grid(row=row, column=2, sticky=tk.W, padx=5)
        
        self.param_widgets['join_keys'] = (label, entry, help_label)
        row += 1
        
        # Join type
        label = ttk.Label(self.params_frame, text="Join Type:")
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        
        join_type_var = tk.StringVar(value='inner')
        combo = ttk.Combobox(
            self.params_frame,
            textvariable=join_type_var,
            values=['inner', 'left', 'right', 'outer', 'cross'],
            state='readonly',
            width=15
        )
        combo.grid(row=row, column=1, sticky=tk.W, padx=5, pady=2)
        
        self.param_widgets['join_type_var'] = join_type_var
        self.param_widgets['join_type'] = (label, combo)
    
    def _create_excel_sheet_params(self):
        """Create parameters for Excel sheet selection."""
        # Get current row count
        row = len([w for w in self.param_widgets.values() if isinstance(w, tuple)]) + 1
        
        # Left sheet
        label = ttk.Label(self.params_frame, text="Left Sheet:")
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        
        entry = ttk.Entry(self.params_frame, width=30)
        entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=2)
        
        help_label = ttk.Label(
            self.params_frame,
            text="(Sheet name or 0-based index)",
            font=("TkDefaultFont", 8)
        )
        help_label.grid(row=row, column=2, sticky=tk.W, padx=5)
        
        self.param_widgets['left_sheet'] = (label, entry, help_label)
        row += 1
        
        # Right sheet
        label = ttk.Label(self.params_frame, text="Right Sheet:")
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        
        entry = ttk.Entry(self.params_frame, width=30)
        entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=2)
        
        help_label = ttk.Label(
            self.params_frame,
            text="(Sheet name or 0-based index)",
            font=("TkDefaultFont", 8)
        )
        help_label.grid(row=row, column=2, sticky=tk.W, padx=5)
        
        self.param_widgets['right_sheet'] = (label, entry, help_label)
    
    def _create_merge_params(self):
        """Create parameters for Merge Excel operation."""
        row = 0
        
        # Mode selection
        label = ttk.Label(self.params_frame, text="Merge Mode:")
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        
        mode_var = tk.StringVar(value='lenient')
        
        frame = ttk.Frame(self.params_frame)
        frame.grid(row=row, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Radiobutton(frame, text="Lenient (unions all columns)", variable=mode_var, value='lenient').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame, text="Strict (requires identical columns)", variable=mode_var, value='strict').pack(side=tk.LEFT, padx=5)
        
        self.param_widgets['mode_var'] = mode_var
        self.param_widgets['mode'] = (label, frame)
    
    # File browsing methods
    
    def _browse_multi_files(self):
        """Browse for multiple files."""
        filetypes = [
            ("CSV and Excel files", "*.csv *.xlsx *.xls"),
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx *.xls"),
            ("All files", "*.*")
        ]
        files = filedialog.askopenfilenames(title="Select Files", filetypes=filetypes)
        if files:
            self.multi_file_entry.delete(0, tk.END)
            self.multi_file_entry.insert(0, ";".join(files))
    
    def _browse_left_file(self):
        """Browse for left file."""
        filetypes = [
            ("CSV and Excel files", "*.csv *.xlsx *.xls"),
            ("All files", "*.*")
        ]
        file = filedialog.askopenfilename(title="Select Left File", filetypes=filetypes)
        if file:
            self.left_file_entry.delete(0, tk.END)
            self.left_file_entry.insert(0, file)
    
    def _browse_right_file(self):
        """Browse for right file."""
        filetypes = [
            ("CSV and Excel files", "*.csv *.xlsx *.xls"),
            ("All files", "*.*")
        ]
        file = filedialog.askopenfilename(title="Select Right File", filetypes=filetypes)
        if file:
            self.right_file_entry.delete(0, tk.END)
            self.right_file_entry.insert(0, file)
    
    def _browse_output(self):
        """Browse for output file."""
        if self.operation in ['csv_to_excel', 'join_excel', 'merge_excel']:
            filetypes = [("Excel files", "*.xlsx"), ("All files", "*.*")]
            defaultextension = ".xlsx"
        else:
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
            defaultextension = ".csv"
        
        file = filedialog.asksaveasfilename(
            title="Select Output File",
            filetypes=filetypes,
            defaultextension=defaultextension
        )
        if file:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file)
    
    # Operation execution
    
    def _start_operation(self):
        """Start the selected operation in a background thread."""
        if self.state.is_running:
            messagebox.showwarning("Operation Running", "An operation is already running!")
            return
        
        try:
            # Validate and prepare operation
            operation_func, args, kwargs = self._prepare_operation()
            
            # Clear queues
            while not self.log_queue.empty():
                self.log_queue.get()
            while not self.result_queue.empty():
                self.result_queue.get()
            
            # Start worker thread
            self.worker_thread = WorkerThread(
                operation_func,
                args,
                kwargs,
                self.result_queue,
                self.log_queue
            )
            self.worker_thread.start()
            
            # Update UI state
            self.state.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.progress_bar.start()
            
            # Start result polling
            self._poll_result_queue()
            
        except Exception as e:
            logger.error(f"Failed to start operation: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to start operation:\n{e}")
    
    def _prepare_operation(self) -> Tuple:
        """Prepare operation function and arguments based on current settings."""
        operation = self.operation
        
        if operation == 'csv_to_excel':
            files_str = self.multi_file_entry.get()
            files = parse_file_list(files_str, separator=';')
            if not files:
                raise ValueError("No input CSV files selected")
            
            output = self.output_entry.get().strip()
            if not output:
                raise ValueError("No output Excel file specified")
            
            sheet_names_str = self.param_widgets['sheet_names'][1].get().strip()
            sheet_names = [s.strip() for s in sheet_names_str.split(',') if s.strip()] if sheet_names_str else None
            
            return csvs_to_excel, (files, output), {'sheet_names': sheet_names}
        
        elif operation == 'union':
            files_str = self.multi_file_entry.get()
            files = parse_file_list(files_str, separator=';')
            if len(files) < 2:
                raise ValueError("Need at least 2 CSV files for union")
            
            output = self.output_entry.get().strip()
            if not output:
                raise ValueError("No output CSV file specified")
            
            dedupe = self.param_widgets['dedupe_var'].get()
            
            dedupe_cols_str = self.param_widgets['dedupe_cols'][1].get().strip()
            dedupe_cols = [c.strip() for c in dedupe_cols_str.split(',') if c.strip()] if dedupe_cols_str else None
            
            chunksize_str = self.param_widgets['chunksize'][1].get().strip()
            chunksize = int(chunksize_str) if chunksize_str else None
            
            return (
                union_multiple_csvs,
                (files, output),
                {'dedupe': dedupe, 'dedupe_columns': dedupe_cols, 'chunksize': chunksize, 'progress': False}
            )
        
        elif operation == 'join':
            left_file = self.left_file_entry.get().strip()
            right_file = self.right_file_entry.get().strip()
            
            if not left_file or not right_file:
                raise ValueError("Both left and right files must be specified")
            
            output = self.output_entry.get().strip()
            if not output:
                raise ValueError("No output CSV file specified")
            
            join_keys_str = self.param_widgets['join_keys'][1].get().strip()
            if not join_keys_str:
                raise ValueError("Join keys must be specified")
            join_keys = [k.strip() for k in join_keys_str.split(',')]
            
            join_type = self.param_widgets['join_type_var'].get()
            
            return (
                join_csvs,
                (left_file, right_file, join_keys, output),
                {'how': join_type}
            )
        
        elif operation == 'join_excel':
            excel_file = self.multi_file_entry.get().strip()
            if not excel_file or ';' in excel_file:
                raise ValueError("Please select exactly one Excel file")
            
            output = self.output_entry.get().strip()
            if not output:
                raise ValueError("No output Excel file specified")
            
            left_sheet = self.param_widgets['left_sheet'][1].get().strip()
            right_sheet = self.param_widgets['right_sheet'][1].get().strip()
            
            if not left_sheet or not right_sheet:
                raise ValueError("Both left and right sheet must be specified")
            
            # Try to convert to int if possible (for index-based selection)
            try:
                left_sheet = int(left_sheet)
            except ValueError:
                pass  # Use as string (sheet name)
            
            try:
                right_sheet = int(right_sheet)
            except ValueError:
                pass
            
            join_keys_str = self.param_widgets['join_keys'][1].get().strip()
            if not join_keys_str:
                raise ValueError("Join keys must be specified")
            join_keys = [k.strip() for k in join_keys_str.split(',')]
            
            join_type = self.param_widgets['join_type_var'].get()
            
            return (
                join_excel_sheets_to_file,
                (excel_file, left_sheet, right_sheet, join_keys, output),
                {'how': join_type}
            )
        
        elif operation == 'merge_excel':
            files_str = self.multi_file_entry.get()
            files = parse_file_list(files_str, separator=';')
            if len(files) < 2:
                raise ValueError("Need at least 2 Excel files for merge")
            
            output = self.output_entry.get().strip()
            if not output:
                raise ValueError("No output Excel file specified")
            
            mode = self.param_widgets['mode_var'].get()
            strict_mode = (mode == 'strict')
            
            return (
                merge_excel_files,
                (files, output),
                {'strict_mode': strict_mode}
            )
        
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    def _stop_operation(self):
        """Stop the running operation (if possible)."""
        if self.worker_thread and self.worker_thread.is_alive():
            # Note: Python threads can't be forcefully stopped, but we can mark it
            self._log("⚠ Operation stop requested (thread will finish current task)...")
            messagebox.showinfo("Stop", "Stop requested. The operation will finish its current task.")
    
    def _poll_result_queue(self):
        """Poll the result queue for operation completion."""
        try:
            status, result = self.result_queue.get_nowait()
            
            # Operation completed
            self.state.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.progress_bar.stop()
            
            if status == 'success':
                self._log(f"✓ Operation completed successfully!")
                messagebox.showinfo("Success", "Operation completed successfully!")
            else:  # error
                self._log(f"✗ Error: {result}")
                messagebox.showerror("Error", f"Operation failed:\n{result}")
        
        except queue.Empty:
            # Keep polling if operation still running
            if self.state.is_running:
                self.root.after(100, self._poll_result_queue)
    
    def _poll_log_queue(self):
        """Poll the log queue for messages."""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self._log(message.rstrip())
        except queue.Empty:
            pass
        
        # Continue polling
        self.root.after(100, self._poll_log_queue)
    
    def _log(self, message: str):
        """Add message to log output."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _clear_log(self):
        """Clear the log output."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    # Diff window
    
    def _open_diff_window(self):
        """Open the CSV diff comparison window."""
        DiffWindow(self.root)
    
    # Help dialogs
    
    def _show_help(self):
        """Show help dialog."""
        help_text = """iLoveExcel - Help

HOW TO USE:
1. Select an operation from the radio buttons
2. The interface will show only relevant options for that operation
3. Fill in the required fields
4. Click the green "▶ START OPERATION" button to execute
5. Monitor progress in the log pane

OPERATIONS:

1. Create Excel from CSVs
   - Select multiple CSV files
   - Each CSV becomes a sheet in a single Excel workbook
   - Optional: Provide custom sheet names (comma-separated)

2. Union CSVs
   - Select 2+ CSV files to combine
   - All rows are appended into a single CSV
   - Enable deduplication to remove duplicate rows

3. Join CSVs
   - Select left and right CSV files
   - Specify join keys (comma-separated column names)
   - Choose join type (inner, left, right, outer, cross)

4. Join Excel Sheets
   - Select an Excel file
   - Specify left and right sheet (name or 0-based index)
   - Specify join keys and join type

5. Merge Excel Files
   - Select 2+ Excel files to merge
   - Merges sheets with the same name across workbooks
   - Lenient mode: unions all columns (default)
   - Strict mode: requires identical columns

TOOLS:
- CSV Side-by-Side Diff: Compare two CSV files row-by-row

TIPS:
- Use chunk size for very large CSV files
- All operations run in background, GUI stays responsive
        """
        
        top = tk.Toplevel(self.root)
        top.title("Help - iLoveExcel")
        top.geometry("700x600")
        
        text = scrolledtext.ScrolledText(top, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert('1.0', help_text)
        text.config(state=tk.DISABLED)
        
        ttk.Button(top, text="Close", command=top.destroy).pack(pady=10)
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """iLoveExcel

A powerful tool for CSV and Excel file operations.

Features:
• CSV to Excel conversion
• CSV unions and joins
• Excel sheet merging
• Side-by-side CSV comparison
• Cross-platform support

GUI Backend: Tkinter (Open Source)

© 2025 iLoveExcel Project
        """
        messagebox.showinfo("About iLoveExcel", about_text)


class DiffWindow:
    """CSV Side-by-Side Diff window."""
    
    def __init__(self, parent):
        """Initialize diff window."""
        self.window = tk.Toplevel(parent)
        self.window.title("CSV Side-by-Side Diff Comparison")
        self.window.geometry("1100x700")
        
        self.worker_thread = None
        self.log_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        self._create_widgets()
        self._poll_log_queue()
    
    def _create_widgets(self):
        """Create diff window widgets."""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input files
        input_frame = ttk.LabelFrame(main_frame, text="Input Files", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Left File (A):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.file_a_entry = ttk.Entry(input_frame, width=60)
        self.file_a_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        ttk.Button(input_frame, text="Browse...", command=self._browse_file_a).grid(row=0, column=2, padx=5)
        
        ttk.Label(input_frame, text="Right File (B):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.file_b_entry = ttk.Entry(input_frame, width=60)
        self.file_b_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        ttk.Button(input_frame, text="Browse...", command=self._browse_file_b).grid(row=1, column=2, padx=5)
        
        # Settings
        settings_frame = ttk.LabelFrame(main_frame, text="Comparison Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=5)
        
        # Compare mode
        mode_frame = ttk.Frame(settings_frame)
        mode_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(mode_frame, text="Compare Mode:").pack(side=tk.LEFT, padx=5)
        self.compare_mode_var = tk.StringVar(value='by_index')
        ttk.Radiobutton(mode_frame, text="By Row Index", variable=self.compare_mode_var, value='by_index').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="By Key Column(s)", variable=self.compare_mode_var, value='by_key').pack(side=tk.LEFT, padx=5)
        
        # Key columns
        key_frame = ttk.Frame(settings_frame)
        key_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(key_frame, text="Key Column(s):").pack(side=tk.LEFT, padx=5)
        self.key_cols_entry = ttk.Entry(key_frame, width=40)
        self.key_cols_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(key_frame, text="(comma-separated)", font=("TkDefaultFont", 8)).pack(side=tk.LEFT)
        
        # Options
        options_frame = ttk.Frame(settings_frame)
        options_frame.pack(fill=tk.X, pady=2)
        
        self.show_only_diffs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Show Only Differences", variable=self.show_only_diffs_var).pack(side=tk.LEFT, padx=5)
        
        self.ignore_whitespace_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Ignore Whitespace", variable=self.ignore_whitespace_var).pack(side=tk.LEFT, padx=5)
        
        self.case_insensitive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Case Insensitive", variable=self.case_insensitive_var).pack(side=tk.LEFT, padx=5)
        
        # Max rows
        max_rows_frame = ttk.Frame(settings_frame)
        max_rows_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(max_rows_frame, text="Max Rows to Display:").pack(side=tk.LEFT, padx=5)
        self.max_rows_entry = ttk.Entry(max_rows_frame, width=10)
        self.max_rows_entry.insert(0, "1000")
        self.max_rows_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(max_rows_frame, text="(0 = unlimited)", font=("TkDefaultFont", 8)).pack(side=tk.LEFT)
        
        # Export
        export_frame = ttk.Frame(settings_frame)
        export_frame.pack(fill=tk.X, pady=2)
        
        self.highlight_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(export_frame, text="Highlight differences in Excel export", variable=self.highlight_var).pack(side=tk.LEFT, padx=5)
        
        output_export_frame = ttk.Frame(settings_frame)
        output_export_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(output_export_frame, text="Output File:").pack(side=tk.LEFT, padx=5)
        self.output_entry = ttk.Entry(output_export_frame, width=50)
        self.output_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(output_export_frame, text="Browse...", command=self._browse_output).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Compare", command=self._compare).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to Excel", command=self._export).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self._clear).pack(side=tk.LEFT, padx=5)
        
        # Results (summary)
        self.summary_label = ttk.Label(main_frame, text="", font=("TkDefaultFont", 10))
        self.summary_label.pack(pady=5)
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Store diff results
        self.diff_df = None
        self.stats = None
    
    def _browse_file_a(self):
        """Browse for file A."""
        file = filedialog.askopenfilename(
            title="Select File A",
            filetypes=[("CSV and Excel files", "*.csv *.xlsx *.xls"), ("All files", "*.*")]
        )
        if file:
            self.file_a_entry.delete(0, tk.END)
            self.file_a_entry.insert(0, file)
    
    def _browse_file_b(self):
        """Browse for file B."""
        file = filedialog.askopenfilename(
            title="Select File B",
            filetypes=[("CSV and Excel files", "*.csv *.xlsx *.xls"), ("All files", "*.*")]
        )
        if file:
            self.file_b_entry.delete(0, tk.END)
            self.file_b_entry.insert(0, file)
    
    def _browse_output(self):
        """Browse for output file."""
        file = filedialog.asksaveasfilename(
            title="Select Output File",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            defaultextension=".xlsx"
        )
        if file:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file)
    
    def _compare(self):
        """Run comparison."""
        try:
            file_a = self.file_a_entry.get().strip()
            file_b = self.file_b_entry.get().strip()
            
            if not file_a or not file_b:
                messagebox.showerror("Error", "Both files must be specified")
                return
            
            compare_by_index = (self.compare_mode_var.get() == 'by_index')
            
            key_columns = None
            if not compare_by_index:
                key_cols_str = self.key_cols_entry.get().strip()
                if not key_cols_str:
                    messagebox.showerror("Error", "Key column(s) must be specified for key-based comparison")
                    return
                key_columns = [k.strip() for k in key_cols_str.split(',')]
            
            max_rows_str = self.max_rows_entry.get().strip()
            max_rows = int(max_rows_str) if max_rows_str and max_rows_str != '0' else None
            
            # Run comparison
            self._log("Starting comparison...")
            
            self.diff_df, self.stats = diff_csv_side_by_side(
                file_a,
                file_b,
                key_columns=key_columns,
                compare_by_index=compare_by_index,
                ignore_whitespace=self.ignore_whitespace_var.get(),
                case_insensitive=self.case_insensitive_var.get(),
                ignore_column_order=False,
                show_only_diffs=self.show_only_diffs_var.get(),
                max_rows=max_rows
            )
            
            # Update summary
            summary = (
                f"Summary: {self.stats['total']} total rows compared • "
                f"{self.stats['different']} differences found • "
                f"{self.stats['matching']} matching • "
                f"{self.stats['only_a']} only in A • "
                f"{self.stats['only_b']} only in B"
            )
            self.summary_label.config(text=summary)
            
            self._log(f"✓ Comparison complete: {self.stats}")
            self._log(f"  Total rows: {self.stats['total']}")
            self._log(f"  Differences: {self.stats['different']}")
            self._log(f"  Matches: {self.stats['matching']}")
            self._log(f"  Only in A: {self.stats['only_a']}")
            self._log(f"  Only in B: {self.stats['only_b']}")
            
            messagebox.showinfo("Success", "Comparison completed! See log for details.\nUse 'Export to Excel' to save results.")
        
        except Exception as e:
            logger.error(f"Diff comparison error: {e}", exc_info=True)
            self._log(f"✗ Error: {e}")
            messagebox.showerror("Error", f"Comparison failed:\n{e}")
    
    def _export(self):
        """Export diff results to Excel."""
        if self.diff_df is None or self.stats is None:
            messagebox.showwarning("Warning", "Please run comparison first!")
            return
        
        try:
            output = self.output_entry.get().strip()
            if not output:
                messagebox.showerror("Error", "Output file must be specified")
                return
            
            file_a_name = Path(self.file_a_entry.get().strip()).stem
            file_b_name = Path(self.file_b_entry.get().strip()).stem
            
            self._log(f"Exporting to {output}...")
            
            export_diff_to_excel(
                self.diff_df,
                self.stats,
                output,
                file_a_name=file_a_name,
                file_b_name=file_b_name,
                highlight=self.highlight_var.get()
            )
            
            self._log(f"✓ Exported to {output}")
            messagebox.showinfo("Success", f"Results exported to:\n{output}")
        
        except Exception as e:
            logger.error(f"Export error: {e}", exc_info=True)
            self._log(f"✗ Export error: {e}")
            messagebox.showerror("Error", f"Export failed:\n{e}")
    
    def _clear(self):
        """Clear all fields."""
        self.file_a_entry.delete(0, tk.END)
        self.file_b_entry.delete(0, tk.END)
        self.key_cols_entry.delete(0, tk.END)
        self.output_entry.delete(0, tk.END)
        self.summary_label.config(text="")
        self.diff_df = None
        self.stats = None
        self._clear_log()
    
    def _log(self, message: str):
        """Add message to log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _clear_log(self):
        """Clear log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _poll_log_queue(self):
        """Poll log queue."""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self._log(message.rstrip())
        except queue.Empty:
            pass
        
        self.window.after(100, self._poll_log_queue)


def main_gui():
    """Launch the Tkinter GUI."""
    # Set up logging
    setup_logging()
    
    # Create root window
    root = tk.Tk()
    
    # Create app
    app = iLoveExcelGUI(root)
    
    # Start main loop
    logger.info("Starting Tkinter GUI main loop")
    root.mainloop()


if __name__ == '__main__':
    main_gui()
