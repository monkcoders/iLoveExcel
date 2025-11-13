"""
Unit tests for iLoveExcel joins module.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import shutil

from iLoveExcel.joins import (
    join_csvs,
    join_excel_sheets,
    validate_join_keys,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def join_csv_files(temp_dir):
    """Create sample CSV files for join testing."""
    left_file = temp_dir / "left.csv"
    right_file = temp_dir / "right.csv"
    
    df_left = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana']
    })
    
    df_right = pd.DataFrame({
        'id': [2, 3, 4, 5],
        'dept': ['Sales', 'Engineering', 'Marketing', 'HR']
    })
    
    df_left.to_csv(left_file, index=False)
    df_right.to_csv(right_file, index=False)
    
    return left_file, right_file


class TestJoinCSVs:
    """Tests for join_csvs function."""
    
    def test_inner_join(self, join_csv_files, temp_dir):
        """Test inner join of two CSV files."""
        left, right = join_csv_files
        output = temp_dir / "joined.csv"
        
        result = join_csvs(left, right, on='id', how='inner', output_file=output)
        
        assert output.exists()
        assert len(result) == 3  # IDs 2, 3, 4 are common
        assert 'name' in result.columns
        assert 'dept' in result.columns
    
    def test_left_join(self, join_csv_files, temp_dir):
        """Test left join of two CSV files."""
        left, right = join_csv_files
        output = temp_dir / "left_joined.csv"
        
        result = join_csvs(left, right, on='id', how='left', output_file=output)
        
        assert len(result) == 4  # All rows from left
    
    def test_invalid_join_type(self, join_csv_files, temp_dir):
        """Test that invalid join type raises error."""
        left, right = join_csv_files
        output = temp_dir / "output.csv"
        
        with pytest.raises(ValueError):
            join_csvs(left, right, on='id', how='invalid', output_file=output)
    
    def test_missing_join_key(self, temp_dir):
        """Test that missing join key raises error."""
        # Create files with different columns
        left = temp_dir / "left.csv"
        right = temp_dir / "right.csv"
        
        pd.DataFrame({'id': [1, 2], 'name': ['A', 'B']}).to_csv(left, index=False)
        pd.DataFrame({'key': [1, 2], 'value': ['X', 'Y']}).to_csv(right, index=False)
        
        with pytest.raises(ValueError):
            join_csvs(left, right, on='missing_key', how='inner')


class TestValidateJoinKeys:
    """Tests for validate_join_keys function."""
    
    def test_validate_existing_key(self):
        """Test validation with existing key."""
        df = pd.DataFrame({'id': [1, 2], 'name': ['A', 'B']})
        # Should not raise error
        validate_join_keys(df, 'id')
    
    def test_validate_missing_key(self):
        """Test validation with missing key."""
        df = pd.DataFrame({'id': [1, 2], 'name': ['A', 'B']})
        with pytest.raises(ValueError):
            validate_join_keys(df, 'missing_key')


# Test stubs for future implementation
def test_join_excel_sheets_stub():
    """Stub for join_excel_sheets tests."""
    pass


def test_join_multiple_csvs_stub():
    """Stub for sequential join tests."""
    pass
