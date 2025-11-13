"""
Unit tests for iLoveExcel I/O module.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import shutil

from iLoveExcel.io import (
    read_csv_chunked,
    write_csv,
    read_excel_sheet,
    csvs_to_excel,
    get_excel_sheet_names,
    validate_file_exists,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_csv(temp_dir):
    """Create a sample CSV file."""
    csv_path = temp_dir / "sample.csv"
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35]
    })
    df.to_csv(csv_path, index=False)
    return csv_path


class TestReadCSV:
    """Tests for CSV reading functions."""
    
    def test_read_csv_basic(self, sample_csv):
        """Test basic CSV reading."""
        df = read_csv_chunked(sample_csv)
        assert len(df) == 3
        assert list(df.columns) == ['id', 'name', 'age']
    
    def test_read_csv_nonexistent(self, temp_dir):
        """Test reading nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            read_csv_chunked(temp_dir / "nonexistent.csv")
    
    def test_read_csv_chunked(self, sample_csv):
        """Test chunked reading returns iterator."""
        chunks = read_csv_chunked(sample_csv, chunksize=2)
        chunk_list = list(chunks)
        assert len(chunk_list) == 2  # 3 rows with chunksize 2 = 2 chunks


class TestWriteCSV:
    """Tests for CSV writing functions."""
    
    def test_write_csv_basic(self, temp_dir):
        """Test basic CSV writing."""
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        output_path = temp_dir / "output.csv"
        
        write_csv(df, output_path)
        
        assert output_path.exists()
        df_read = pd.read_csv(output_path)
        assert len(df_read) == 3
    
    def test_write_csv_creates_directory(self, temp_dir):
        """Test that write_csv creates parent directories."""
        output_path = temp_dir / "subdir" / "output.csv"
        df = pd.DataFrame({'a': [1, 2]})
        
        write_csv(df, output_path)
        
        assert output_path.exists()


class TestExcelOperations:
    """Tests for Excel operations."""
    
    def test_csvs_to_excel(self, temp_dir):
        """Test converting CSVs to Excel."""
        # Create two CSV files
        csv1 = temp_dir / "file1.csv"
        csv2 = temp_dir / "file2.csv"
        
        pd.DataFrame({'a': [1, 2]}).to_csv(csv1, index=False)
        pd.DataFrame({'b': [3, 4]}).to_csv(csv2, index=False)
        
        output_excel = temp_dir / "output.xlsx"
        csvs_to_excel([csv1, csv2], output_excel, sheet_names=['Sheet1', 'Sheet2'])
        
        assert output_excel.exists()
        
        # Verify sheets
        sheet_names = get_excel_sheet_names(output_excel)
        assert 'Sheet1' in sheet_names
        assert 'Sheet2' in sheet_names


class TestValidation:
    """Tests for validation functions."""
    
    def test_validate_file_exists_valid(self, sample_csv):
        """Test validation with existing file."""
        result = validate_file_exists(sample_csv)
        assert result == Path(sample_csv)
    
    def test_validate_file_exists_invalid(self, temp_dir):
        """Test validation with nonexistent file."""
        with pytest.raises(FileNotFoundError):
            validate_file_exists(temp_dir / "nonexistent.csv")


# Additional test stubs for future implementation
def test_read_excel_sheet_stub():
    """Stub for read_excel_sheet tests."""
    pass


def test_write_dataframes_to_excel_stub():
    """Stub for write_dataframes_to_excel tests."""
    pass
