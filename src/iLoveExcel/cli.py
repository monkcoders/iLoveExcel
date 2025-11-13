"""
iLoveExcel - CLI module.

Command-line interface for CSV and Excel operations using Click.
"""

import logging
import sys
from pathlib import Path
from typing import List, Optional

import click

from . import __version__
from .excel_merge import merge_excel_files, merge_excel_sheets_by_name
from .io import csvs_to_excel
from .joins import join_csvs, join_excel_sheets_to_file
from .unions import union_csvs, union_multiple_csvs
from .utils import setup_logging, validate_join_type, parse_column_list

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__, prog_name="csvexcel")
@click.option('--log-level', default='INFO', help='Logging level (DEBUG, INFO, WARNING, ERROR)')
@click.option('--log-file', type=click.Path(), help='Optional log file path')
def main(log_level: str, log_file: Optional[str]):
    """
    iLoveExcel - Advanced CSV and Excel operations from the command line.
    
    Perform unions, joins, and merges on CSV and Excel files.
    """
    setup_logging(level=log_level, log_file=log_file)
    logger.info(f"iLoveExcel CLI v{__version__}")


@main.command()
@click.argument('csv_files', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('-o', '--output', required=True, type=click.Path(), help='Output Excel file path')
@click.option('-s', '--sheet-names', help='Comma-separated sheet names (optional)')
def csv_to_excel(csv_files: tuple, output: str, sheet_names: Optional[str]):
    """
    Convert multiple CSV files to a single Excel workbook with multiple sheets.
    
    Example:
        csvexcel csv-to-excel file1.csv file2.csv -o output.xlsx
        csvexcel csv-to-excel *.csv -o combined.xlsx -s "Sheet1,Sheet2"
    """
    try:
        csv_list = list(csv_files)
        sheet_list = parse_column_list(sheet_names) if sheet_names else None
        
        if sheet_list and len(sheet_list) != len(csv_list):
            raise click.BadParameter(f"Number of sheet names ({len(sheet_list)}) must match number of CSV files ({len(csv_list)})")
        
        click.echo(f"Converting {len(csv_list)} CSV files to Excel...")
        csvs_to_excel(csv_list, output, sheet_list)
        click.echo(f"✓ Created {output}")
    except Exception as e:
        logger.error(f"Error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('file_a', type=click.Path(exists=True))
@click.argument('file_b', type=click.Path(exists=True))
@click.option('-o', '--output', required=True, type=click.Path(), help='Output CSV file path')
@click.option('--dedupe/--no-dedupe', default=True, help='Remove duplicate rows (default: yes)')
@click.option('--dedupe-columns', help='Comma-separated columns for deduplication')
def union(file_a: str, file_b: str, output: str, dedupe: bool, dedupe_columns: Optional[str]):
    """
    Union (append) two CSV files.
    
    Example:
        csvexcel union file1.csv file2.csv -o combined.csv
        csvexcel union file1.csv file2.csv -o combined.csv --no-dedupe
        csvexcel union file1.csv file2.csv -o combined.csv --dedupe-columns "id,email"
    """
    try:
        dedupe_cols = parse_column_list(dedupe_columns) if dedupe_columns else None
        
        click.echo(f"Unioning {file_a} and {file_b}...")
        union_csvs(file_a, file_b, output, dedupe=dedupe, dedupe_columns=dedupe_cols)
        click.echo(f"✓ Created {output}")
    except Exception as e:
        logger.error(f"Error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('csv_files', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('-o', '--output', required=True, type=click.Path(), help='Output CSV file path')
@click.option('--dedupe/--no-dedupe', default=False, help='Remove duplicate rows')
@click.option('--dedupe-columns', help='Comma-separated columns for deduplication')
@click.option('--chunksize', type=int, help='Process in chunks (for large files)')
def union_multiple(csv_files: tuple, output: str, dedupe: bool, dedupe_columns: Optional[str], chunksize: Optional[int]):
    """
    Union multiple CSV files into one.
    
    Example:
        csvexcel union-multiple file1.csv file2.csv file3.csv -o combined.csv
        csvexcel union-multiple *.csv -o all_data.csv --dedupe
        csvexcel union-multiple *.csv -o large.csv --chunksize 10000
    """
    try:
        csv_list = list(csv_files)
        dedupe_cols = parse_column_list(dedupe_columns) if dedupe_columns else None
        
        click.echo(f"Unioning {len(csv_list)} CSV files...")
        union_multiple_csvs(
            csv_list,
            output,
            dedupe=dedupe,
            dedupe_columns=dedupe_cols,
            chunksize=chunksize,
            progress=True
        )
        click.echo(f"✓ Created {output}")
    except Exception as e:
        logger.error(f"Error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('file_left', type=click.Path(exists=True))
@click.argument('file_right', type=click.Path(exists=True))
@click.option('-o', '--output', required=True, type=click.Path(), help='Output CSV file path')
@click.option('--on', required=True, help='Comma-separated join key column(s)')
@click.option('--how', default='inner', help='Join type: inner, left, right, outer, cross')
def join(file_left: str, file_right: str, output: str, on: str, how: str):
    """
    Join two CSV files on specified key column(s).
    
    Example:
        csvexcel join left.csv right.csv -o joined.csv --on "id" --how inner
        csvexcel join orders.csv customers.csv -o result.csv --on "customer_id" --how left
        csvexcel join file1.csv file2.csv -o merged.csv --on "col1,col2" --how outer
    """
    try:
        how = validate_join_type(how)
        join_keys = parse_column_list(on)
        
        if not join_keys:
            raise click.BadParameter("--on parameter cannot be empty")
        
        # If only one key, use string instead of list
        join_on = join_keys[0] if len(join_keys) == 1 else join_keys
        
        click.echo(f"Joining {file_left} and {file_right} on {join_on} ({how} join)...")
        join_csvs(file_left, file_right, on=join_on, how=how, output_file=output)
        click.echo(f"✓ Created {output}")
    except Exception as e:
        logger.error(f"Error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', required=True, type=click.Path(), help='Output Excel file path')
@click.option('--sheet-left', required=True, help='Left sheet name or index')
@click.option('--sheet-right', required=True, help='Right sheet name or index')
@click.option('--on', required=True, help='Comma-separated join key column(s)')
@click.option('--how', default='inner', help='Join type: inner, left, right, outer, cross')
@click.option('--output-sheet', default='Joined', help='Output sheet name')
def join_excel_sheets(input_file: str, output: str, sheet_left: str, sheet_right: str, on: str, how: str, output_sheet: str):
    """
    Join two sheets from an Excel file.
    
    Example:
        csvexcel join-excel-sheets data.xlsx -o result.xlsx --sheet-left 0 --sheet-right 1 --on "id"
        csvexcel join-excel-sheets workbook.xlsx -o joined.xlsx --sheet-left "Sales" --sheet-right "Customers" --on "customer_id" --how left
    """
    try:
        how = validate_join_type(how)
        join_keys = parse_column_list(on)
        
        if not join_keys:
            raise click.BadParameter("--on parameter cannot be empty")
        
        join_on = join_keys[0] if len(join_keys) == 1 else join_keys
        
        # Try to convert sheet names to integers if they're numeric
        try:
            sheet_left = int(sheet_left)
        except ValueError:
            pass  # Keep as string
        
        try:
            sheet_right = int(sheet_right)
        except ValueError:
            pass  # Keep as string
        
        click.echo(f"Joining sheets '{sheet_left}' and '{sheet_right}' from {input_file}...")
        join_excel_sheets_to_file(
            input_file, output, sheet_left, sheet_right,
            on=join_on, how=how, output_sheet_name=output_sheet
        )
        click.echo(f"✓ Created {output}")
    except Exception as e:
        logger.error(f"Error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('excel_files', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('-o', '--output', required=True, type=click.Path(), help='Output Excel file path')
@click.option('--mode', type=click.Choice(['strict', 'lenient']), default='lenient', 
              help='strict: require identical columns, lenient: union columns (default)')
def merge_excel(excel_files: tuple, output: str, mode: str):
    """
    Merge multiple Excel files by combining sheets with the same name.
    
    Example:
        csvexcel merge-excel file1.xlsx file2.xlsx file3.xlsx -o merged.xlsx
        csvexcel merge-excel *.xlsx -o combined.xlsx --mode strict
    """
    try:
        excel_list = list(excel_files)
        
        click.echo(f"Merging {len(excel_list)} Excel files in '{mode}' mode...")
        merge_excel_files(excel_list, output, mode=mode, progress=True)
        click.echo(f"✓ Created {output}")
    except Exception as e:
        logger.error(f"Error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('excel_files', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('-o', '--output', required=True, type=click.Path(), help='Output Excel file path')
@click.option('--sheet', required=True, help='Sheet name to merge across files')
@click.option('--mode', type=click.Choice(['strict', 'lenient']), default='lenient')
def merge_sheet(excel_files: tuple, output: str, sheet: str, mode: str):
    """
    Merge a specific sheet from multiple Excel files.
    
    Example:
        csvexcel merge-sheet file1.xlsx file2.xlsx -o merged.xlsx --sheet "Sales"
    """
    try:
        excel_list = list(excel_files)
        
        click.echo(f"Merging sheet '{sheet}' from {len(excel_list)} Excel files...")
        merge_excel_sheets_by_name(excel_list, sheet, output, mode=mode)
        click.echo(f"✓ Created {output}")
    except Exception as e:
        logger.error(f"Error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
