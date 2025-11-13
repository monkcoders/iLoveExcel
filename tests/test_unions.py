"""
Unit tests for iLoveExcel unions module.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import shutil

from iLoveExcel.unions import (
    union_csvs,
    union_multiple_csvs,
    union_csvs_with_validation,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_csv_files(temp_dir):
    """Create sample CSV files for testing."""
    csv1 = temp_dir / "file1.csv"
    csv2 = temp_dir / "file2.csv"
    
    df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['A', 'B', 'C']})
    df2 = pd.DataFrame({'id': [4, 5, 6], 'name': ['D', 'E', 'F']})
    
    df1.to_csv(csv1, index=False)
    df2.to_csv(csv2, index=False)
    
    return [csv1, csv2]


class TestUnionCSVs:
    """Tests for union_csvs function."""
    
    def test_union_two_files(self, sample_csv_files, temp_dir):
        """Test basic union of two CSV files."""
        output = temp_dir / "union.csv"
        
        union_csvs(sample_csv_files[0], sample_csv_files[1], output, dedupe=False)
        
        assert output.exists()
        df = pd.read_csv(output)
        assert len(df) == 6  # 3 + 3 rows
    
    def test_union_with_deduplication(self, temp_dir):
        """Test union with deduplication."""
        csv1 = temp_dir / "file1.csv"
        csv2 = temp_dir / "file2.csv"
        
        # Create files with duplicate rows
        df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['A', 'B', 'C']})
        df2 = pd.DataFrame({'id': [2, 3, 4], 'name': ['B', 'C', 'D']})
        
        df1.to_csv(csv1, index=False)
        df2.to_csv(csv2, index=False)
        
        output = temp_dir / "union_deduped.csv"
        union_csvs(csv1, csv2, output, dedupe=True)
        
        df = pd.read_csv(output)
        assert len(df) == 4  # Unique rows: 1,2,3,4


class TestUnionMultipleCSVs:
    """Tests for union_multiple_csvs function."""
    
    def test_union_multiple_files(self, sample_csv_files, temp_dir):
        """Test union of multiple CSV files."""
        output = temp_dir / "multi_union.csv"
        
        union_multiple_csvs(sample_csv_files, output, dedupe=False)
        
        assert output.exists()
        df = pd.read_csv(output)
        assert len(df) == 6
    
    def test_union_empty_list_raises_error(self, temp_dir):
        """Test that empty file list raises error."""
        with pytest.raises(ValueError):
            union_multiple_csvs([], temp_dir / "output.csv")


# Test stubs for future implementation
def test_union_csvs_with_validation_stub():
    """Stub for union_csvs_with_validation tests."""
    pass


def test_union_chunked_processing_stub():
    """Stub for chunked processing tests."""
    pass
