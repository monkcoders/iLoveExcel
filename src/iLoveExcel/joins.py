"""
iLoveExcel - Joins module for joining CSV and Excel files.

This module provides functions to join CSV files on key columns,
similar to SQL joins (inner, left, right, outer, cross).
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd

from .io import (
    read_csv_chunked,
    read_excel_sheet,
    write_csv,
    write_dataframes_to_excel,
    validate_file_exists,
    get_excel_sheet_names,
)

logger = logging.getLogger(__name__)


def join_csvs(
    file_left: Union[str, Path],
    file_right: Union[str, Path],
    on: Union[str, List[str]],
    how: str = 'inner',
    output_file: Union[str, Path] = None,
    chunksize: Optional[int] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Join two CSV files on specified key column(s).
    
    Args:
        file_left: Path to left CSV file
        file_right: Path to right CSV file
        on: Column name(s) to join on (can be string or list of strings)
        how: Join type - 'inner', 'left', 'right', 'outer', or 'cross'
        output_file: Optional path to save result as CSV
        chunksize: Chunk size for reading (None = read all at once)
        **kwargs: Additional arguments passed to pd.merge
    
    Returns:
        Joined DataFrame
    
    Raises:
        ValueError: If 'how' parameter is invalid or join keys don't exist
        FileNotFoundError: If input files don't exist
    """
    # Validate inputs
    validate_file_exists(file_left)
    validate_file_exists(file_right)
    
    valid_how = ['inner', 'left', 'right', 'outer', 'cross']
    if how not in valid_how:
        raise ValueError(f"'how' must be one of {valid_how}, got '{how}'")
    
    logger.info(f"Joining {file_left} and {file_right} on {on} (how={how})")
    
    # For now, chunked join is complex - we'll read fully
    # (In production, you'd implement iterative join for very large files)
    if chunksize:
        logger.warning("chunksize parameter not fully implemented for joins - reading fully")
    
    # Read both files
    df_left = read_csv_chunked(file_left, chunksize=None)
    df_right = read_csv_chunked(file_right, chunksize=None)
    
    # Validate join keys exist
    on_list = [on] if isinstance(on, str) else on
    
    for key in on_list:
        if key not in df_left.columns:
            raise ValueError(f"Join key '{key}' not found in left file columns: {list(df_left.columns)}")
        if key not in df_right.columns:
            raise ValueError(f"Join key '{key}' not found in right file columns: {list(df_right.columns)}")
    
    # Perform the join
    logger.info(f"Left: {len(df_left)} rows, Right: {len(df_right)} rows")
    
    if how == 'cross':
        # Cross join doesn't use 'on'
        df_result = df_left.merge(df_right, how='cross', **kwargs)
    else:
        df_result = df_left.merge(df_right, on=on, how=how, **kwargs)
    
    logger.info(f"Join result: {len(df_result)} rows")
    
    # Write to file if requested
    if output_file:
        write_csv(df_result, output_file)
        logger.info(f"Saved join result to {output_file}")
    
    return df_result


def join_excel_sheets(
    file_path: Union[str, Path],
    sheet_left: Union[str, int],
    sheet_right: Union[str, int],
    on: Union[str, List[str]],
    how: str = 'inner',
    output_sheet_name: str = 'Joined',
    **kwargs
) -> pd.DataFrame:
    """
    Join two sheets from the same Excel file.
    
    Args:
        file_path: Path to Excel file
        sheet_left: Left sheet name or index
        sheet_right: Right sheet name or index
        on: Column name(s) to join on
        how: Join type - 'inner', 'left', 'right', 'outer', or 'cross'
        output_sheet_name: Name for the result sheet
        **kwargs: Additional arguments passed to pd.merge
    
    Returns:
        Joined DataFrame
    """
    validate_file_exists(file_path)
    
    logger.info(f"Joining sheets '{sheet_left}' and '{sheet_right}' from {file_path}")
    
    # Read both sheets
    df_left = read_excel_sheet(file_path, sheet_left)
    df_right = read_excel_sheet(file_path, sheet_right)
    
    # Validate join keys
    on_list = [on] if isinstance(on, str) else on
    
    for key in on_list:
        if key not in df_left.columns:
            raise ValueError(f"Join key '{key}' not found in sheet '{sheet_left}'")
        if key not in df_right.columns:
            raise ValueError(f"Join key '{key}' not found in sheet '{sheet_right}'")
    
    # Perform join
    logger.info(f"Left sheet: {len(df_left)} rows, Right sheet: {len(df_right)} rows")
    
    if how == 'cross':
        df_result = df_left.merge(df_right, how='cross', **kwargs)
    else:
        df_result = df_left.merge(df_right, on=on, how=how, **kwargs)
    
    logger.info(f"Join result: {len(df_result)} rows")
    
    return df_result


def join_excel_sheets_to_file(
    input_file: Union[str, Path],
    output_file: Union[str, Path],
    sheet_left: Union[str, int],
    sheet_right: Union[str, int],
    on: Union[str, List[str]],
    how: str = 'inner',
    output_sheet_name: str = 'Joined',
    **kwargs
) -> None:
    """
    Join two sheets from an Excel file and save result to a new Excel file.
    
    Args:
        input_file: Path to input Excel file
        output_file: Path to output Excel file
        sheet_left: Left sheet name or index
        sheet_right: Right sheet name or index
        on: Column name(s) to join on
        how: Join type
        output_sheet_name: Name for the output sheet
        **kwargs: Additional merge arguments
    """
    df_result = join_excel_sheets(
        input_file, sheet_left, sheet_right, on, how, output_sheet_name, **kwargs
    )
    
    # Write to Excel
    write_dataframes_to_excel({output_sheet_name: df_result}, output_file)
    logger.info(f"Saved joined result to {output_file}")


def join_multiple_csvs_sequential(
    files: List[Union[str, Path]],
    on: Union[str, List[str]],
    how: str = 'inner',
    output_file: Optional[Union[str, Path]] = None
) -> pd.DataFrame:
    """
    Join multiple CSV files sequentially on a common key.
    
    Performs left joins: file1 JOIN file2 JOIN file3 ...
    
    Args:
        files: List of CSV file paths (at least 2)
        on: Column name(s) to join on (must exist in all files)
        how: Join type for all joins
        output_file: Optional path to save result
    
    Returns:
        Final joined DataFrame
    
    Raises:
        ValueError: If less than 2 files provided
    """
    if len(files) < 2:
        raise ValueError(f"Need at least 2 files to join, got {len(files)}")
    
    logger.info(f"Sequential join of {len(files)} files on {on} (how={how})")
    
    # Start with first file
    result_df = read_csv_chunked(files[0], chunksize=None)
    logger.info(f"Starting with {files[0]}: {len(result_df)} rows")
    
    # Join each subsequent file
    for i, file_path in enumerate(files[1:], start=2):
        df_next = read_csv_chunked(file_path, chunksize=None)
        logger.info(f"Joining file {i}/{len(files)}: {file_path} ({len(df_next)} rows)")
        
        # Validate join key exists
        on_list = [on] if isinstance(on, str) else on
        for key in on_list:
            if key not in df_next.columns:
                raise ValueError(f"Join key '{key}' not found in {file_path}")
        
        # Perform join
        if how == 'cross':
            result_df = result_df.merge(df_next, how='cross')
        else:
            result_df = result_df.merge(df_next, on=on, how=how)
        
        logger.info(f"  Result after join {i-1}: {len(result_df)} rows")
    
    logger.info(f"Final result: {len(result_df)} rows")
    
    # Save if requested
    if output_file:
        write_csv(result_df, output_file)
        logger.info(f"Saved result to {output_file}")
    
    return result_df


def validate_join_keys(
    df: pd.DataFrame,
    keys: Union[str, List[str]],
    file_name: str = "DataFrame"
) -> None:
    """
    Validate that join keys exist in a DataFrame.
    
    Args:
        df: DataFrame to check
        keys: Key column(s) to validate
        file_name: Name for error messages
    
    Raises:
        ValueError: If any key is missing
    """
    key_list = [keys] if isinstance(keys, str) else keys
    
    for key in key_list:
        if key not in df.columns:
            raise ValueError(
                f"Join key '{key}' not found in {file_name}. "
                f"Available columns: {list(df.columns)}"
            )
