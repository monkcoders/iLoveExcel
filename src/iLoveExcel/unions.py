"""
iLoveExcel - Unions module for combining CSV files.

This module provides functions to union/append multiple CSV files,
with optional deduplication and chunked processing for large files.
"""

import logging
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd
from tqdm import tqdm

from .io import read_csv_chunked, write_csv, validate_file_exists

logger = logging.getLogger(__name__)


def union_csvs(
    file_a: Union[str, Path],
    file_b: Union[str, Path],
    output_file: Union[str, Path],
    dedupe: bool = True,
    dedupe_columns: Optional[List[str]] = None
) -> None:
    """
    Union/append two CSV files with optional deduplication.
    
    Args:
        file_a: Path to first CSV file
        file_b: Path to second CSV file
        output_file: Path to output CSV file
        dedupe: Whether to remove duplicate rows
        dedupe_columns: Columns to use for deduplication (None = all columns)
    
    Raises:
        FileNotFoundError: If input files don't exist
        ValueError: If files have incompatible structures
    """
    validate_file_exists(file_a)
    validate_file_exists(file_b)
    
    logger.info(f"Unioning {file_a} and {file_b} -> {output_file}")
    
    # Read both files
    df_a = read_csv_chunked(file_a)
    df_b = read_csv_chunked(file_b)
    
    # Check column compatibility
    if set(df_a.columns) != set(df_b.columns):
        logger.warning(f"Column mismatch between files. A: {list(df_a.columns)}, B: {list(df_b.columns)}")
        # Reindex to ensure same columns
        all_columns = list(df_a.columns.union(df_b.columns))
        df_a = df_a.reindex(columns=all_columns)
        df_b = df_b.reindex(columns=all_columns)
    
    # Concatenate
    df_union = pd.concat([df_a, df_b], ignore_index=True)
    logger.info(f"Combined: {len(df_a)} + {len(df_b)} = {len(df_union)} rows")
    
    # Deduplicate if requested
    if dedupe:
        original_count = len(df_union)
        if dedupe_columns:
            df_union = df_union.drop_duplicates(subset=dedupe_columns, keep='first')
        else:
            df_union = df_union.drop_duplicates(keep='first')
        removed = original_count - len(df_union)
        logger.info(f"Removed {removed} duplicate rows (keeping first occurrence)")
    
    # Write output
    write_csv(df_union, output_file)
    logger.info(f"Successfully wrote {len(df_union)} rows to {output_file}")


def union_multiple_csvs(
    files: List[Union[str, Path]],
    output_csv: Union[str, Path],
    dedupe: bool = False,
    dedupe_columns: Optional[List[str]] = None,
    chunksize: Optional[int] = None,
    progress: bool = True
) -> None:
    """
    Union multiple CSV files into a single output file with optional chunked processing.
    
    Args:
        files: List of CSV file paths to union
        output_csv: Path to output CSV file
        dedupe: Whether to remove duplicate rows (applied at the end if chunksize is used)
        dedupe_columns: Columns to use for deduplication (None = all columns)
        chunksize: Number of rows per chunk for memory-efficient processing (None = load all)
        progress: Whether to show progress bar
    
    Raises:
        ValueError: If files list is empty
        FileNotFoundError: If any input file doesn't exist
    """
    if not files:
        raise ValueError("files list cannot be empty")
    
    # Validate all files exist
    for file_path in files:
        validate_file_exists(file_path)
    
    logger.info(f"Unioning {len(files)} CSV files -> {output_csv}")
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if chunksize is None:
        # Load all files into memory and concatenate
        dfs = []
        iterator = tqdm(files, desc="Reading CSV files") if progress else files
        
        for file_path in iterator:
            try:
                df = read_csv_chunked(file_path)
                dfs.append(df)
            except Exception as e:
                logger.error(f"Error reading {file_path}: {e}")
                raise
        
        # Concatenate all DataFrames
        df_union = pd.concat(dfs, ignore_index=True)
        logger.info(f"Combined {len(files)} files: {len(df_union)} total rows")
        
        # Deduplicate if requested
        if dedupe:
            original_count = len(df_union)
            if dedupe_columns:
                df_union = df_union.drop_duplicates(subset=dedupe_columns, keep='first')
            else:
                df_union = df_union.drop_duplicates(keep='first')
            removed = original_count - len(df_union)
            logger.info(f"Removed {removed} duplicate rows")
        
        # Write output
        write_csv(df_union, output_csv)
        logger.info(f"Successfully wrote {len(df_union)} rows to {output_csv}")
    
    else:
        # Chunked processing - write progressively
        logger.info(f"Using chunked processing with chunksize={chunksize}")
        first_file = True
        total_rows = 0
        
        for file_idx, file_path in enumerate(files):
            logger.info(f"Processing file {file_idx + 1}/{len(files)}: {file_path}")
            
            # Read file in chunks
            chunk_iterator = read_csv_chunked(file_path, chunksize=chunksize)
            
            for chunk_idx, chunk in enumerate(chunk_iterator):
                mode = 'w' if first_file and chunk_idx == 0 else 'a'
                write_csv(chunk, output_csv, mode=mode)
                total_rows += len(chunk)
                first_file = False
                
                if progress:
                    print(f"  Processed chunk {chunk_idx + 1} from {Path(file_path).name}: {len(chunk)} rows")
        
        logger.info(f"Wrote {total_rows} total rows (before deduplication)")
        
        # If deduplication is requested, need to reload and dedupe
        # (This is unavoidable - deduplication requires seeing all rows)
        if dedupe:
            logger.info("Performing deduplication (requires reloading data)...")
            df = read_csv_chunked(output_csv)
            original_count = len(df)
            
            if dedupe_columns:
                df = df.drop_duplicates(subset=dedupe_columns, keep='first')
            else:
                df = df.drop_duplicates(keep='first')
            
            removed = original_count - len(df)
            logger.info(f"Removed {removed} duplicate rows")
            write_csv(df, output_csv)
        
        logger.info(f"Successfully created union file: {output_csv}")


def union_csvs_with_validation(
    files: List[Union[str, Path]],
    output_csv: Union[str, Path],
    strict_columns: bool = False,
    dedupe: bool = False,
    dedupe_columns: Optional[List[str]] = None,
    chunksize: Optional[int] = None
) -> None:
    """
    Union CSV files with column validation.
    
    Args:
        files: List of CSV file paths to union
        output_csv: Path to output CSV file
        strict_columns: If True, require all files to have identical columns in same order
        dedupe: Whether to remove duplicate rows
        dedupe_columns: Columns to use for deduplication
        chunksize: Number of rows per chunk for processing
    
    Raises:
        ValueError: If strict_columns=True and columns don't match
    """
    if not files:
        raise ValueError("files list cannot be empty")
    
    # Read headers from all files
    logger.info("Validating column structure across files...")
    reference_columns = None
    
    for file_path in files:
        validate_file_exists(file_path)
        # Read just the first row to get columns
        df_sample = pd.read_csv(file_path, nrows=0)
        
        if reference_columns is None:
            reference_columns = list(df_sample.columns)
            logger.info(f"Reference columns from {file_path}: {reference_columns}")
        else:
            current_columns = list(df_sample.columns)
            
            if strict_columns:
                if current_columns != reference_columns:
                    raise ValueError(
                        f"Column mismatch in strict mode.\n"
                        f"  Expected: {reference_columns}\n"
                        f"  Got in {file_path}: {current_columns}"
                    )
            else:
                # Just log differences
                if set(current_columns) != set(reference_columns):
                    logger.warning(f"Different columns in {file_path}: {current_columns}")
    
    # Proceed with union
    union_multiple_csvs(
        files=files,
        output_csv=output_csv,
        dedupe=dedupe,
        dedupe_columns=dedupe_columns,
        chunksize=chunksize
    )
