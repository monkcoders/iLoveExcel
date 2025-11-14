"""
iLoveExcel - GUI Common Utilities

Shared utilities for GUI implementations (PySimpleGUI, Tkinter, etc.)
Provides worker thread management, progress queue handling, and common widgets.
"""

import logging
import queue
import threading
from typing import Any, Callable, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class WorkerThread(threading.Thread):
    """
    Background worker thread for long-running operations.
    
    Executes a task function in the background and communicates results
    and progress messages through queues, preventing GUI blocking.
    """
    
    def __init__(
        self,
        task_func: Callable,
        args: Tuple = (),
        kwargs: Optional[Dict] = None,
        result_queue: Optional[queue.Queue] = None,
        log_queue: Optional[queue.Queue] = None,
        progress_queue: Optional[queue.Queue] = None
    ):
        """
        Initialize worker thread.
        
        Args:
            task_func: Function to execute in background
            args: Positional arguments for task_func
            kwargs: Keyword arguments for task_func
            result_queue: Queue for final result ('success'/'error', value)
            log_queue: Queue for log messages (str)
            progress_queue: Queue for progress updates (0-100)
        """
        super().__init__(daemon=True)
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs or {}
        self.result_queue = result_queue or queue.Queue()
        self.log_queue = log_queue or queue.Queue()
        self.progress_queue = progress_queue or queue.Queue()
        self._stop_event = threading.Event()
    
    def run(self):
        """Execute the task and put result in queue."""
        try:
            self.log_queue.put("Starting operation...\n")
            self.progress_queue.put(10)
            
            result = self.task_func(*self.args, **self.kwargs)
            
            if not self._stop_event.is_set():
                self.progress_queue.put(100)
                self.result_queue.put(('success', result))
                self.log_queue.put("✓ Operation completed successfully!\n")
        except Exception as e:
            logger.error(f"Worker thread error: {e}", exc_info=True)
            if not self._stop_event.is_set():
                self.result_queue.put(('error', str(e)))
                self.log_queue.put(f"✗ Error: {e}\n")
    
    def stop(self):
        """Signal the worker to stop (best effort)."""
        self._stop_event.set()


class ProgressReporter:
    """
    Helper class for reporting progress from worker functions.
    
    Usage in worker functions:
        def my_task(progress_queue):
            reporter = ProgressReporter(progress_queue)
            for i in range(100):
                # do work
                reporter.report(i)
    """
    
    def __init__(self, progress_queue: queue.Queue, log_queue: Optional[queue.Queue] = None):
        """
        Initialize progress reporter.
        
        Args:
            progress_queue: Queue to send progress updates (0-100)
            log_queue: Optional queue for log messages
        """
        self.progress_queue = progress_queue
        self.log_queue = log_queue
    
    def report(self, percent: int, message: Optional[str] = None):
        """
        Report progress percentage.
        
        Args:
            percent: Progress percentage (0-100)
            message: Optional log message
        """
        self.progress_queue.put(max(0, min(100, percent)))
        if message and self.log_queue:
            self.log_queue.put(message)
    
    def log(self, message: str):
        """Send a log message."""
        if self.log_queue:
            self.log_queue.put(message)


def column_number_to_letter(n: int) -> str:
    """
    Convert column number (0-indexed) to Excel column letter.
    
    Args:
        n: Column index (0 = A, 1 = B, 25 = Z, 26 = AA, etc.)
    
    Returns:
        Column letter string (A, B, ..., Z, AA, AB, ...)
    
    Examples:
        >>> column_number_to_letter(0)
        'A'
        >>> column_number_to_letter(25)
        'Z'
        >>> column_number_to_letter(26)
        'AA'
    """
    result = ""
    n += 1  # Excel columns are 1-indexed
    while n > 0:
        n -= 1
        result = chr(65 + (n % 26)) + result
        n //= 26
    return result


def validate_file_path(path: str, must_exist: bool = True) -> Tuple[bool, str]:
    """
    Validate a file path.
    
    Args:
        path: File path to validate
        must_exist: If True, file must exist
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    from pathlib import Path
    
    if not path or not path.strip():
        return False, "File path cannot be empty"
    
    path_obj = Path(path)
    
    if must_exist and not path_obj.exists():
        return False, f"File does not exist: {path}"
    
    if must_exist and not path_obj.is_file():
        return False, f"Path is not a file: {path}"
    
    return True, ""


def parse_file_list(file_string: str, separator: str = ';') -> list:
    """
    Parse semicolon or pipe-separated file paths.
    
    Args:
        file_string: String with multiple file paths
        separator: Separator character (default ';')
    
    Returns:
        List of file paths
    """
    if not file_string or not file_string.strip():
        return []
    
    files = [f.strip() for f in file_string.split(separator) if f.strip()]
    return files


def format_bytes(bytes_val: int) -> str:
    """
    Format bytes to human-readable string.
    
    Args:
        bytes_val: Number of bytes
    
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} PB"


def safe_get_from_queue(q: queue.Queue, timeout: float = 0.01) -> Optional[Any]:
    """
    Safely get item from queue without blocking.
    
    Args:
        q: Queue to read from
        timeout: Timeout in seconds
    
    Returns:
        Item from queue or None if empty/timeout
    """
    try:
        return q.get_nowait()
    except queue.Empty:
        return None


class GUIState:
    """
    Simple state manager for GUI applications.
    
    Stores current operation, files, and settings to maintain state
    across GUI updates.
    """
    
    def __init__(self):
        """Initialize empty state."""
        self.operation = None
        self.input_files = []
        self.output_file = None
        self.settings = {}
        self.worker_thread = None
        self.is_running = False
    
    def reset(self):
        """Reset state to initial values."""
        self.operation = None
        self.input_files = []
        self.output_file = None
        self.settings = {}
        self.is_running = False
    
    def update(self, **kwargs):
        """Update multiple state values."""
        for key, value in kwargs.items():
            setattr(self, key, value)


# Default GUI configuration
DEFAULT_GUI_CONFIG = {
    'window_title': 'iLoveExcel',
    'window_size': (1000, 800),
    'font_family': 'Arial',
    'font_size': 10,
    'button_width': 15,
    'entry_width': 50,
    'text_area_height': 10,
    'padding': 5,
    'log_max_lines': 1000,
}


def get_gui_config(overrides: Optional[Dict] = None) -> Dict:
    """
    Get GUI configuration with optional overrides.
    
    Args:
        overrides: Dictionary of config values to override
    
    Returns:
        Complete configuration dictionary
    """
    config = DEFAULT_GUI_CONFIG.copy()
    if overrides:
        config.update(overrides)
    return config
