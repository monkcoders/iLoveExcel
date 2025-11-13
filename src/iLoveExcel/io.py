"""
iLoveExcel - I/O module for CSV and Excel file operations.

This module provides utility functions for reading and writing CSV and Excel files,
with support for chunked processing for large files.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd

logger = logging.getLogger(__name__)


def read_csv_chunked(
    file_path: Union[str, Path],
    chunksize: Optional[int] = None,
    **kwargs
) -> Union[pd.DataFrame, pd.io.parsers.TextFileReader]:
    """
    Read a CSV file with optional chunking for large files.
    
    Args:
        file_path: Path to the CSV file
        chunksize: Number of rows per chunk (None = read all at once)
        **kwargs: Additional arguments passed to pd.read_csv
    
    Returns:
        DataFrame if chunksize is None, otherwise TextFileReader iterator
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file is empty or invalid
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    
    logger.info(f"Reading CSV: {file_path} (chunksize={chunksize})")
    
    try:
        if chunksize is None:
            df = pd.read_csv(file_path, **kwargs)
            logger.info(f"Loaded {len(df)} rows from {file_path}")
            return df
        else:
            # Return iterator for chunked processing
            return pd.read_csv(file_path, chunksize=chunksize, **kwargs)
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV file is empty: {file_path}")
    except Exception as e:
        logger.error(f"Error reading CSV {file_path}: {e}")
        raise


def write_csv(
    df: pd.DataFrame,
    output_path: Union[str, Path],
    mode: str = 'w',
    **kwargs
) -> None:
    """
    Write a DataFrame to CSV file.
    
    Args:
        df: DataFrame to write
        output_path: Path to output CSV file
        mode: Write mode ('w' for write, 'a' for append)
        **kwargs: Additional arguments passed to df.to_csv
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Set defaults for to_csv
    kwargs.setdefault('index', False)
    kwargs.setdefault('header', mode == 'w')
    
    logger.info(f"Writing {len(df)} rows to CSV: {output_path} (mode={mode})")
    df.to_csv(output_path, mode=mode, **kwargs)


def read_excel_sheet(
    file_path: Union[str, Path],
    sheet_name: Union[str, int] = 0,
    **kwargs
) -> pd.DataFrame:
    """
    Read a specific sheet from an Excel file.
    
    Args:
        file_path: Path to the Excel file
        sheet_name: Sheet name or index (0-based)
        **kwargs: Additional arguments passed to pd.read_excel
    
    Returns:
        DataFrame containing the sheet data
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the sheet doesn't exist
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    
    logger.info(f"Reading Excel sheet '{sheet_name}' from {file_path}")
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
        logger.info(f"Loaded {len(df)} rows from sheet '{sheet_name}'")
        return df
    except Exception as e:
        logger.error(f"Error reading Excel sheet '{sheet_name}' from {file_path}: {e}")
        raise ValueError(f"Could not read sheet '{sheet_name}': {e}")


def get_excel_sheet_names(file_path: Union[str, Path]) -> List[str]:
    """
    Get list of sheet names from an Excel file.
    
    Args:
        file_path: Path to the Excel file
    
    Returns:
        List of sheet names
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    
    excel_file = pd.ExcelFile(file_path)
    return excel_file.sheet_names


def csvs_to_excel(
    csv_files: List[Union[str, Path]],
    output_path: Union[str, Path],
    sheet_names: Optional[List[str]] = None,
    **kwargs
) -> None:
    """
    Convert multiple CSV files into a single Excel workbook with multiple sheets.
    
    Args:
        csv_files: List of CSV file paths
        output_path: Path to output Excel file
        sheet_names: Optional list of sheet names (defaults to CSV filenames)
        **kwargs: Additional arguments passed to pd.read_csv
    
    Raises:
        ValueError: If csv_files is empty or sheet_names length doesn't match
    """
    if not csv_files:
        raise ValueError("csv_files list cannot be empty")
    
    if sheet_names and len(sheet_names) != len(csv_files):
        raise ValueError(f"sheet_names length ({len(sheet_names)}) must match csv_files length ({len(csv_files)})")
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate default sheet names if not provided
    if sheet_names is None:
        sheet_names = [Path(f).stem[:31] for f in csv_files]  # Excel sheet name limit is 31 chars
    
    logger.info(f"Converting {len(csv_files)} CSV files to Excel: {output_path}")
    
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for csv_file, sheet_name in zip(csv_files, sheet_names):
            try:
                df = read_csv_chunked(csv_file, chunksize=None, **kwargs)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                logger.info(f"  Added sheet '{sheet_name}' with {len(df)} rows")
            except Exception as e:
                logger.error(f"  Error processing {csv_file}: {e}")
                raise
    
    logger.info(f"Successfully created Excel file: {output_path}")


def write_dataframes_to_excel(
    dataframes: Dict[str, pd.DataFrame],
    output_path: Union[str, Path],
    engine: str = 'xlsxwriter'
) -> None:
    """
    Write multiple DataFrames to an Excel file with named sheets.
    
    Args:
        dataframes: Dictionary mapping sheet names to DataFrames
        output_path: Path to output Excel file
        engine: Excel writer engine ('xlsxwriter' or 'openpyxl')
    """
    if not dataframes:
        raise ValueError("dataframes dictionary cannot be empty")
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Writing {len(dataframes)} sheets to Excel: {output_path}")
    
    with pd.ExcelWriter(output_path, engine=engine) as writer:
        for sheet_name, df in dataframes.items():
            # Ensure sheet name is valid (max 31 chars, no special chars)
            safe_sheet_name = sheet_name[:31].replace('/', '_').replace('\\', '_')
            df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
            logger.info(f"  Wrote sheet '{safe_sheet_name}' with {len(df)} rows")
    
    logger.info(f"Successfully created Excel file: {output_path}")


def validate_file_exists(file_path: Union[str, Path]) -> Path:
    """
    Validate that a file exists.
    
    Args:
        file_path: Path to validate
    
    Returns:
        Path object if file exists
    
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return file_path
