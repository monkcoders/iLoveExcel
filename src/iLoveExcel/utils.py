"""
iLoveExcel - Utilities module.

Provides logging setup, validation helpers, and other utility functions.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional, Union


def setup_logging(
    level: str = 'INFO',
    log_file: Optional[Union[str, Path]] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Configure logging for the application.
    
    Args:
        level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        log_file: Optional path to log file
        format_string: Optional custom format string
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Convert level string to logging constant
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')
    
    # Configure root logger
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter(format_string))
    handlers.append(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(logging.Formatter(format_string))
        handlers.append(file_handler)
    
    # Configure logging
    logging.basicConfig(
        level=numeric_level,
        format=format_string,
        handlers=handlers,
        force=True  # Override any existing configuration
    )
    
    logging.info(f"Logging initialized at {level} level")


def confirm_overwrite(file_path: Union[str, Path]) -> bool:
    """
    Ask user to confirm overwriting an existing file.
    
    Args:
        file_path: Path to check
    
    Returns:
        True if user confirms or file doesn't exist, False otherwise
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return True
    
    response = input(f"File {file_path} already exists. Overwrite? (y/N): ").strip().lower()
    return response in ['y', 'yes']


def validate_positive_int(value: int, name: str = "value") -> int:
    """
    Validate that a value is a positive integer.
    
    Args:
        value: Value to validate
        name: Name for error messages
    
    Returns:
        The value if valid
    
    Raises:
        ValueError: If value is not positive
    """
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer, got {value}")
    return value


def format_size(size_bytes: int) -> str:
    """
    Format byte size as human-readable string.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    Get size of a file in bytes.
    
    Args:
        file_path: Path to file
    
    Returns:
        File size in bytes
    """
    return Path(file_path).stat().st_size


def ensure_extension(file_path: Union[str, Path], extension: str) -> Path:
    """
    Ensure a file path has the specified extension.
    
    Args:
        file_path: Original file path
        extension: Desired extension (with or without leading dot)
    
    Returns:
        Path with correct extension
    """
    file_path = Path(file_path)
    
    if not extension.startswith('.'):
        extension = f'.{extension}'
    
    if file_path.suffix.lower() != extension.lower():
        file_path = file_path.with_suffix(extension)
    
    return file_path


def truncate_string(s: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate a string to maximum length.
    
    Args:
        s: String to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncating
    
    Returns:
        Truncated string
    """
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix


def safe_sheet_name(name: str, max_length: int = 31) -> str:
    """
    Convert a string to a valid Excel sheet name.
    
    Excel sheet names have restrictions:
    - Max 31 characters
    - Cannot contain: / \\ ? * [ ]
    - Cannot be empty
    
    Args:
        name: Proposed sheet name
        max_length: Maximum length (default 31 for Excel)
    
    Returns:
        Valid sheet name
    """
    if not name:
        return "Sheet1"
    
    # Replace invalid characters
    invalid_chars = ['/', '\\', '?', '*', '[', ']']
    for char in invalid_chars:
        name = name.replace(char, '_')
    
    # Truncate to max length
    name = name[:max_length]
    
    # Ensure not empty after processing
    if not name.strip():
        return "Sheet1"
    
    return name


class ProgressTracker:
    """
    Simple progress tracker for long-running operations.
    """
    
    def __init__(self, total: int, description: str = "Processing"):
        """
        Initialize progress tracker.
        
        Args:
            total: Total number of items to process
            description: Description of the operation
        """
        self.total = total
        self.current = 0
        self.description = description
        self.logger = logging.getLogger(__name__)
    
    def update(self, amount: int = 1) -> None:
        """
        Update progress by the specified amount.
        
        Args:
            amount: Amount to increment
        """
        self.current += amount
        percentage = (self.current / self.total * 100) if self.total > 0 else 0
        self.logger.info(f"{self.description}: {self.current}/{self.total} ({percentage:.1f}%)")
    
    def finish(self) -> None:
        """Mark progress as complete."""
        self.current = self.total
        self.logger.info(f"{self.description}: Complete!")


def parse_column_list(column_str: str) -> list:
    """
    Parse a comma-separated string of column names into a list.
    
    Args:
        column_str: String like "col1,col2,col3" or "col1, col2, col3"
    
    Returns:
        List of column names with whitespace stripped
    """
    if not column_str or not column_str.strip():
        return []
    
    columns = [col.strip() for col in column_str.split(',')]
    return [col for col in columns if col]  # Remove empty strings


def validate_join_type(join_type: str) -> str:
    """
    Validate and normalize join type.
    
    Args:
        join_type: Join type string
    
    Returns:
        Normalized join type
    
    Raises:
        ValueError: If join type is invalid
    """
    valid_types = ['inner', 'left', 'right', 'outer', 'cross']
    join_type = join_type.lower().strip()
    
    if join_type not in valid_types:
        raise ValueError(f"Invalid join type '{join_type}'. Must be one of: {', '.join(valid_types)}")
    
    return join_type


def get_env_var(var_name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get environment variable with optional default.
    
    Args:
        var_name: Name of environment variable
        default: Default value if not found
    
    Returns:
        Environment variable value or default
    """
    return os.environ.get(var_name, default)
