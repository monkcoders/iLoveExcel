"""
Unit tests for diffs module.

Tests CSV side-by-side diff comparison functionality.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile

from iLoveExcel.diffs import (
    diff_csv_side_by_side,
    export_diff_to_excel,
)


# Sample data for testing
SAMPLE_A_DATA = """id,name,email,age,city
1,John Smith,john@email.com,30,New York
2,Jane Doe,jane@email.com,25,Los Angeles
3,Bob Wilson,bob@email.com,35,Chicago
4,Alice Brown,alice@email.com,28,Houston
5,Charlie Davis,charlie@email.com,32,Phoenix
"""

SAMPLE_B_DATA = """id,name,email,age,city
1,John Smith,john@email.com,30,New York
2,Jane Doe,jane@email.com,26,Los Angeles
3,Bob Wilson,bob@email.com,35,Miami
6,Eve Martinez,eve@email.com,29,Seattle
7,Frank Lopez,frank@email.com,31,Boston
"""


@pytest.fixture
def sample_files(tmp_path):
    """Create sample CSV files for testing."""
    file_a = tmp_path / "sample_a.csv"
    file_b = tmp_path / "sample_b.csv"
    
    file_a.write_text(SAMPLE_A_DATA)
    file_b.write_text(SAMPLE_B_DATA)
    
    return file_a, file_b


def test_diff_by_index(sample_files):
    """Test diff comparison by row index."""
    file_a, file_b = sample_files
    
    diff_df, stats = diff_csv_side_by_side(
        file_a,
        file_b,
        compare_by_index=True,
        show_only_diffs=False
    )
    
    # Should have rows for all indices (0-6)
    assert len(diff_df) > 0
    assert stats['total'] > 0
    
    # Check that we have various status types
    statuses = set(diff_df['Status'].unique())
    assert 'MATCH' in statuses or 'DIFF' in statuses or 'ONLY_A' in statuses or 'ONLY_B' in statuses


def test_diff_by_key(sample_files):
    """Test diff comparison by key column."""
    file_a, file_b = sample_files
    
    diff_df, stats = diff_csv_side_by_side(
        file_a,
        file_b,
        key_columns=['id'],
        compare_by_index=False,
        show_only_diffs=False
    )
    
    assert len(diff_df) > 0
    assert stats['total'] > 0
    
    # Should have matches and differences
    assert stats['matching'] > 0 or stats['different'] > 0


def test_show_only_diffs(sample_files):
    """Test filtering to show only differences."""
    file_a, file_b = sample_files
    
    diff_df_all, stats_all = diff_csv_side_by_side(
        file_a,
        file_b,
        compare_by_index=True,
        show_only_diffs=False
    )
    
    diff_df_diffs, stats_diffs = diff_csv_side_by_side(
        file_a,
        file_b,
        compare_by_index=True,
        show_only_diffs=True
    )
    
    # Diff-only should have fewer or equal rows
    assert len(diff_df_diffs) <= len(diff_df_all)
    
    # Diff-only should not contain MATCH status
    if len(diff_df_diffs) > 0:
        assert 'MATCH' not in diff_df_diffs['Status'].values


def test_ignore_whitespace(tmp_path):
    """Test whitespace ignoring."""
    file_a = tmp_path / "a.csv"
    file_b = tmp_path / "b.csv"
    
    file_a.write_text("name,value\nAlice,100\n")
    file_b.write_text("name,value\n Alice ,100\n")  # Extra spaces
    
    # Without ignoring whitespace - should differ
    diff_df, stats = diff_csv_side_by_side(
        file_a,
        file_b,
        compare_by_index=True,
        ignore_whitespace=False
    )
    assert stats['different'] > 0
    
    # With ignoring whitespace - should match
    diff_df, stats = diff_csv_side_by_side(
        file_a,
        file_b,
        compare_by_index=True,
        ignore_whitespace=True
    )
    assert stats['matching'] > 0


def test_case_insensitive(tmp_path):
    """Test case-insensitive comparison."""
    file_a = tmp_path / "a.csv"
    file_b = tmp_path / "b.csv"
    
    file_a.write_text("name,value\nAlice,hello\n")
    file_b.write_text("name,value\nAlice,HELLO\n")
    
    # Case-sensitive - should differ
    diff_df, stats = diff_csv_side_by_side(
        file_a,
        file_b,
        compare_by_index=True,
        case_insensitive=False
    )
    assert stats['different'] > 0
    
    # Case-insensitive - should match
    diff_df, stats = diff_csv_side_by_side(
        file_a,
        file_b,
        compare_by_index=True,
        case_insensitive=True
    )
    assert stats['matching'] > 0


def test_max_rows(sample_files):
    """Test max_rows parameter."""
    file_a, file_b = sample_files
    
    diff_df, stats = diff_csv_side_by_side(
        file_a,
        file_b,
        compare_by_index=True,
        max_rows=3
    )
    
    # Should process only first 3 rows
    assert len(diff_df) <= 3


def test_export_to_excel(sample_files, tmp_path):
    """Test Excel export functionality."""
    file_a, file_b = sample_files
    
    diff_df, stats = diff_csv_side_by_side(
        file_a,
        file_b,
        compare_by_index=True,
        show_only_diffs=False
    )
    
    output_file = tmp_path / "diff_output.xlsx"
    
    export_diff_to_excel(
        diff_df,
        stats,
        output_file,
        file_a_name="Sample A",
        file_b_name="Sample B",
        highlight=True
    )
    
    assert output_file.exists()
    
    # Verify Excel has expected sheets
    xls = pd.ExcelFile(output_file)
    assert 'Comparison' in xls.sheet_names
    assert 'Summary' in xls.sheet_names


def test_invalid_key_column(sample_files):
    """Test error handling for invalid key column."""
    file_a, file_b = sample_files
    
    with pytest.raises(ValueError, match="Key column .* not found"):
        diff_csv_side_by_side(
            file_a,
            file_b,
            key_columns=['nonexistent_column'],
            compare_by_index=False
        )


def test_missing_file():
    """Test error handling for missing file."""
    with pytest.raises(FileNotFoundError):
        diff_csv_side_by_side(
            "nonexistent_a.csv",
            "nonexistent_b.csv",
            compare_by_index=True
        )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
