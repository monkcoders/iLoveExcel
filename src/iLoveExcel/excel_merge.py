"""
iLoveExcel - Excel merge module for combining multiple Excel workbooks.

This module provides functions to merge multiple Excel files,
combining sheets with the same name across workbooks.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd
from tqdm import tqdm

from .io import get_excel_sheet_names, read_excel_sheet, write_dataframes_to_excel, validate_file_exists

logger = logging.getLogger(__name__)


def merge_excel_files(
    excel_files: List[Union[str, Path]],
    output_file: Union[str, Path],
    mode: str = 'lenient',
    progress: bool = True
) -> None:
    """
    Merge multiple Excel files by combining sheets with the same name.
    
    Args:
        excel_files: List of Excel file paths to merge
        output_file: Path to output merged Excel file
        mode: Merge mode - 'strict' (require identical columns) or 'lenient' (union of columns)
        progress: Whether to show progress bar
    
    Raises:
        ValueError: If excel_files is empty or mode is invalid
        FileNotFoundError: If any input file doesn't exist
    """
    if not excel_files:
        raise ValueError("excel_files list cannot be empty")
    
    if mode not in ['strict', 'lenient']:
        raise ValueError(f"mode must be 'strict' or 'lenient', got '{mode}'")
    
    # Validate all files exist
    for file_path in excel_files:
        validate_file_exists(file_path)
    
    logger.info(f"Merging {len(excel_files)} Excel files in '{mode}' mode -> {output_file}")
    
    # Step 1: Collect all unique sheet names across all workbooks
    all_sheet_names = set()
    file_sheets_map = {}
    
    for file_path in excel_files:
        sheet_names = get_excel_sheet_names(file_path)
        file_sheets_map[file_path] = sheet_names
        all_sheet_names.update(sheet_names)
    
    logger.info(f"Found {len(all_sheet_names)} unique sheet names: {sorted(all_sheet_names)}")
    
    # Step 2: For each sheet name, merge data from all files that have it
    merged_sheets = {}
    
    iterator = tqdm(sorted(all_sheet_names), desc="Merging sheets") if progress else sorted(all_sheet_names)
    
    for sheet_name in iterator:
        logger.info(f"Processing sheet: '{sheet_name}'")
        
        # Collect all DataFrames for this sheet across files
        sheet_dfs = []
        
        for file_path in excel_files:
            if sheet_name in file_sheets_map[file_path]:
                try:
                    df = read_excel_sheet(file_path, sheet_name)
                    sheet_dfs.append((file_path, df))
                    logger.debug(f"  {Path(file_path).name}: {len(df)} rows, {len(df.columns)} columns")
                except Exception as e:
                    logger.error(f"  Error reading sheet '{sheet_name}' from {file_path}: {e}")
                    raise
        
        if not sheet_dfs:
            logger.warning(f"  No data found for sheet '{sheet_name}' - skipping")
            continue
        
        # Merge the DataFrames for this sheet
        if mode == 'strict':
            merged_df = _merge_sheets_strict(sheet_dfs, sheet_name)
        else:  # lenient
            merged_df = _merge_sheets_lenient(sheet_dfs, sheet_name)
        
        merged_sheets[sheet_name] = merged_df
        logger.info(f"  Merged '{sheet_name}': {len(merged_df)} rows, {len(merged_df.columns)} columns")
    
    # Step 3: Write all merged sheets to output Excel file
    if not merged_sheets:
        raise ValueError("No sheets were successfully merged")
    
    write_dataframes_to_excel(merged_sheets, output_file)
    logger.info(f"Successfully merged {len(excel_files)} files into {output_file} ({len(merged_sheets)} sheets)")


def _merge_sheets_strict(
    sheet_dfs: List[tuple],
    sheet_name: str
) -> pd.DataFrame:
    """
    Merge sheets in strict mode - all must have identical columns in same order.
    
    Args:
        sheet_dfs: List of (file_path, DataFrame) tuples
        sheet_name: Name of the sheet being merged
    
    Returns:
        Merged DataFrame
    
    Raises:
        ValueError: If columns don't match
    """
    reference_file, reference_df = sheet_dfs[0]
    reference_columns = list(reference_df.columns)
    
    logger.debug(f"  Strict mode: reference columns from {Path(reference_file).name}: {reference_columns}")
    
    dfs_to_concat = [reference_df]
    
    for file_path, df in sheet_dfs[1:]:
        current_columns = list(df.columns)
        
        if current_columns != reference_columns:
            raise ValueError(
                f"Column mismatch in strict mode for sheet '{sheet_name}'.\n"
                f"  Reference ({Path(reference_file).name}): {reference_columns}\n"
                f"  Current ({Path(file_path).name}): {current_columns}"
            )
        
        dfs_to_concat.append(df)
    
    # Concatenate all DataFrames
    merged = pd.concat(dfs_to_concat, ignore_index=True)
    return merged


def _merge_sheets_lenient(
    sheet_dfs: List[tuple],
    sheet_name: str
) -> pd.DataFrame:
    """
    Merge sheets in lenient mode - union all columns, fill missing with NaN.
    
    Args:
        sheet_dfs: List of (file_path, DataFrame) tuples
        sheet_name: Name of the sheet being merged
    
    Returns:
        Merged DataFrame with union of all columns
    """
    # Collect all unique columns across all sheets
    all_columns = set()
    
    for file_path, df in sheet_dfs:
        all_columns.update(df.columns)
    
    # Sort for consistent ordering
    all_columns = sorted(all_columns)
    logger.debug(f"  Lenient mode: union of columns: {all_columns}")
    
    # Reindex each DataFrame to have all columns, filling missing with NaN
    dfs_to_concat = []
    
    for file_path, df in sheet_dfs:
        df_reindexed = df.reindex(columns=all_columns)
        dfs_to_concat.append(df_reindexed)
        
        missing_cols = set(all_columns) - set(df.columns)
        if missing_cols:
            logger.debug(f"    {Path(file_path).name}: added {len(missing_cols)} missing columns")
    
    # Concatenate all DataFrames
    merged = pd.concat(dfs_to_concat, ignore_index=True)
    return merged


def merge_excel_sheets_by_name(
    excel_files: List[Union[str, Path]],
    sheet_name: str,
    output_file: Union[str, Path],
    mode: str = 'lenient'
) -> None:
    """
    Merge a specific sheet (by name) from multiple Excel files.
    
    Args:
        excel_files: List of Excel file paths
        sheet_name: Name of the sheet to merge
        output_file: Path to output Excel file
        mode: Merge mode - 'strict' or 'lenient'
    
    Raises:
        ValueError: If sheet not found in any file
    """
    logger.info(f"Merging sheet '{sheet_name}' from {len(excel_files)} files")
    
    sheet_dfs = []
    
    for file_path in excel_files:
        validate_file_exists(file_path)
        
        sheet_names = get_excel_sheet_names(file_path)
        
        if sheet_name not in sheet_names:
            logger.warning(f"Sheet '{sheet_name}' not found in {file_path} - skipping")
            continue
        
        df = read_excel_sheet(file_path, sheet_name)
        sheet_dfs.append((file_path, df))
    
    if not sheet_dfs:
        raise ValueError(f"Sheet '{sheet_name}' not found in any of the provided files")
    
    # Merge
    if mode == 'strict':
        merged_df = _merge_sheets_strict(sheet_dfs, sheet_name)
    else:
        merged_df = _merge_sheets_lenient(sheet_dfs, sheet_name)
    
    # Write output
    write_dataframes_to_excel({sheet_name: merged_df}, output_file)
    logger.info(f"Merged sheet '{sheet_name}': {len(merged_df)} rows -> {output_file}")


def get_common_sheets(excel_files: List[Union[str, Path]]) -> List[str]:
    """
    Get list of sheet names that appear in ALL provided Excel files.
    
    Args:
        excel_files: List of Excel file paths
    
    Returns:
        List of common sheet names
    """
    if not excel_files:
        return []
    
    # Get sheets from first file
    common_sheets = set(get_excel_sheet_names(excel_files[0]))
    
    # Intersect with sheets from other files
    for file_path in excel_files[1:]:
        sheet_names = set(get_excel_sheet_names(file_path))
        common_sheets = common_sheets.intersection(sheet_names)
    
    return sorted(common_sheets)


def merge_excel_common_sheets_only(
    excel_files: List[Union[str, Path]],
    output_file: Union[str, Path],
    mode: str = 'lenient'
) -> None:
    """
    Merge only the sheets that are common to all Excel files.
    
    Args:
        excel_files: List of Excel file paths
        output_file: Path to output Excel file
        mode: Merge mode - 'strict' or 'lenient'
    """
    common_sheets = get_common_sheets(excel_files)
    
    if not common_sheets:
        raise ValueError("No common sheets found across all files")
    
    logger.info(f"Found {len(common_sheets)} common sheets: {common_sheets}")
    
    merged_sheets = {}
    
    for sheet_name in common_sheets:
        sheet_dfs = []
        
        for file_path in excel_files:
            df = read_excel_sheet(file_path, sheet_name)
            sheet_dfs.append((file_path, df))
        
        if mode == 'strict':
            merged_df = _merge_sheets_strict(sheet_dfs, sheet_name)
        else:
            merged_df = _merge_sheets_lenient(sheet_dfs, sheet_name)
        
        merged_sheets[sheet_name] = merged_df
        logger.info(f"Merged '{sheet_name}': {len(merged_df)} rows")
    
    write_dataframes_to_excel(merged_sheets, output_file)
    logger.info(f"Successfully merged common sheets to {output_file}")
