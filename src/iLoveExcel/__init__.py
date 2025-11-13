"""
iLoveExcel - Advanced CSV and Excel operations package.

A comprehensive toolkit for merging, joining, and transforming CSV and Excel files
with both GUI and CLI interfaces.
"""

__version__ = '0.1.0'
__author__ = 'iLoveExcel Contributors'
__license__ = 'MIT'

# Import main functionality for easy access
from .io import (
    read_csv_chunked,
    write_csv,
    read_excel_sheet,
    get_excel_sheet_names,
    csvs_to_excel,
    write_dataframes_to_excel,
)

from .unions import (
    union_csvs,
    union_multiple_csvs,
    union_csvs_with_validation,
)

from .joins import (
    join_csvs,
    join_excel_sheets,
    join_excel_sheets_to_file,
    join_multiple_csvs_sequential,
)

from .excel_merge import (
    merge_excel_files,
    merge_excel_sheets_by_name,
    merge_excel_common_sheets_only,
    get_common_sheets,
)

from .utils import (
    setup_logging,
    validate_join_type,
    safe_sheet_name,
)

__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__license__',
    
    # I/O functions
    'read_csv_chunked',
    'write_csv',
    'read_excel_sheet',
    'get_excel_sheet_names',
    'csvs_to_excel',
    'write_dataframes_to_excel',
    
    # Union functions
    'union_csvs',
    'union_multiple_csvs',
    'union_csvs_with_validation',
    
    # Join functions
    'join_csvs',
    'join_excel_sheets',
    'join_excel_sheets_to_file',
    'join_multiple_csvs_sequential',
    
    # Excel merge functions
    'merge_excel_files',
    'merge_excel_sheets_by_name',
    'merge_excel_common_sheets_only',
    'get_common_sheets',
    
    # Utilities
    'setup_logging',
    'validate_join_type',
    'safe_sheet_name',
]
