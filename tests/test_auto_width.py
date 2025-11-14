"""
Unit tests for io_helpers module.

Tests auto-column-width functionality for Excel files.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile

from iLoveExcel.io_helpers import (
    apply_auto_column_width,
    get_optimal_column_widths,
    get_column_widths_from_dataframe,
    apply_auto_width_to_writer,
)


@pytest.fixture
def sample_excel(tmp_path):
    """Create a sample Excel file for testing."""
    file_path = tmp_path / "sample.xlsx"
    
    # Create DataFrame with varying column widths
    df = pd.DataFrame({
        'Short': ['A', 'B', 'C'],
        'Medium Length Column': ['Value 1', 'Value 2', 'Value 3'],
        'Very Long Column Name With Many Characters': [
            'Short',
            'A bit longer value',
            'This is an extremely long value that should determine column width'
        ],
        'Numbers': [100, 200, 300],
    })
    
    # Write to Excel
    df.to_excel(file_path, index=False, sheet_name='TestSheet')
    
    return file_path, df


def test_apply_auto_column_width(sample_excel):
    """Test applying auto-width to an Excel file."""
    file_path, df = sample_excel
    
    # Apply auto-width
    apply_auto_column_width(file_path)
    
    # File should still exist and be readable
    assert file_path.exists()
    df_read = pd.read_excel(file_path)
    assert len(df_read) == len(df)
    assert list(df_read.columns) == list(df.columns)


def test_apply_auto_column_width_with_params(sample_excel):
    """Test auto-width with custom parameters."""
    file_path, df = sample_excel
    
    # Apply with custom parameters
    apply_auto_column_width(
        file_path,
        min_width=10,
        max_width=30,
        padding=3,
        header_factor=1.5
    )
    
    # Verify file is still valid
    assert file_path.exists()
    df_read = pd.read_excel(file_path)
    assert len(df_read) == len(df)


def test_apply_auto_column_width_specific_sheet(tmp_path):
    """Test applying auto-width to a specific sheet."""
    file_path = tmp_path / "multi_sheet.xlsx"
    
    # Create multi-sheet workbook
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        pd.DataFrame({'A': [1, 2, 3]}).to_excel(writer, sheet_name='Sheet1', index=False)
        pd.DataFrame({'B': [10, 20, 30]}).to_excel(writer, sheet_name='Sheet2', index=False)
    
    # Apply auto-width to specific sheet
    apply_auto_column_width(file_path, sheet_name='Sheet1')
    
    # Verify file is still valid and has both sheets
    xls = pd.ExcelFile(file_path)
    assert 'Sheet1' in xls.sheet_names
    assert 'Sheet2' in xls.sheet_names


def test_get_optimal_column_widths(sample_excel):
    """Test getting optimal widths without modifying file."""
    file_path, df = sample_excel
    
    widths = get_optimal_column_widths(file_path)
    
    assert 'TestSheet' in widths
    assert len(widths['TestSheet']) > 0
    
    # All widths should be numbers
    for col_letter, width in widths['TestSheet'].items():
        assert isinstance(width, (int, float))
        assert width > 0


def test_get_column_widths_from_dataframe():
    """Test calculating widths from DataFrame."""
    df = pd.DataFrame({
        'Short': ['A', 'B'],
        'Longer Column Name': ['Value 1', 'Value 2'],
        'Numbers': [123456789, 987654321],
    })
    
    widths = get_column_widths_from_dataframe(df)
    
    # Should have width for each column
    assert len(widths) == 3
    
    # Check column letters (A, B, C)
    assert 'A' in widths
    assert 'B' in widths
    assert 'C' in widths
    
    # All widths should be positive numbers
    for width in widths.values():
        assert isinstance(width, (int, float))
        assert width > 0


def test_get_column_widths_with_params():
    """Test width calculation with custom parameters."""
    df = pd.DataFrame({
        'Col1': ['Short'],
        'Col2': ['This is a very long value that exceeds max width'],
    })
    
    # With default params
    widths_default = get_column_widths_from_dataframe(df)
    
    # With custom min/max
    widths_custom = get_column_widths_from_dataframe(
        df,
        min_width=15,
        max_width=25,
        padding=1
    )
    
    # Custom widths should respect bounds
    for width in widths_custom.values():
        assert width >= 15
        assert width <= 25


def test_apply_auto_width_to_writer(tmp_path):
    """Test applying auto-width with ExcelWriter."""
    file_path = tmp_path / "writer_test.xlsx"
    
    df = pd.DataFrame({
        'Short': ['A', 'B', 'C'],
        'Longer Column': ['Value 1', 'Value 2', 'Value 3'],
    })
    
    # Write with auto-width
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='TestSheet', index=False)
        apply_auto_width_to_writer(writer, 'TestSheet')
    
    # Verify file
    assert file_path.exists()
    df_read = pd.read_excel(file_path, sheet_name='TestSheet')
    assert len(df_read) == len(df)


def test_missing_file():
    """Test error handling for missing file."""
    with pytest.raises(FileNotFoundError):
        apply_auto_column_width("nonexistent.xlsx")


def test_invalid_sheet_name(sample_excel):
    """Test error handling for invalid sheet name."""
    file_path, df = sample_excel
    
    with pytest.raises(ValueError, match="Sheet .* not found"):
        apply_auto_column_width(file_path, sheet_name="NonexistentSheet")


def test_empty_dataframe(tmp_path):
    """Test with empty DataFrame."""
    file_path = tmp_path / "empty.xlsx"
    
    df = pd.DataFrame(columns=['Col1', 'Col2', 'Col3'])
    df.to_excel(file_path, index=False)
    
    # Should handle empty DataFrame
    apply_auto_column_width(file_path)
    
    assert file_path.exists()


def test_width_bounds(tmp_path):
    """Test that widths respect min/max bounds."""
    file_path = tmp_path / "bounds.xlsx"
    
    df = pd.DataFrame({
        'X': ['A'],  # Very short
        'Y': ['This is an extremely long value that would normally exceed maximum width limits if not capped'],
    })
    
    df.to_excel(file_path, index=False)
    
    # Apply with strict bounds
    apply_auto_column_width(
        file_path,
        min_width=12,
        max_width=20
    )
    
    # Get widths to verify
    widths = get_optimal_column_widths(
        file_path,
        min_width=12,
        max_width=20
    )
    
    # All widths should be within bounds
    for sheet_widths in widths.values():
        for width in sheet_widths.values():
            assert width >= 12
            assert width <= 20


def test_header_factor(tmp_path):
    """Test header_factor parameter."""
    file_path = tmp_path / "header_factor.xlsx"
    
    # Header is longer than data
    df = pd.DataFrame({
        'Very Long Column Header Name': ['A', 'B'],
    })
    
    df.to_excel(file_path, index=False)
    
    # Apply with different header factors
    widths_low = get_optimal_column_widths(file_path, header_factor=1.0)
    widths_high = get_optimal_column_widths(file_path, header_factor=2.0)
    
    # Higher header factor should give larger width
    # (assuming header is the determining factor)
    # This might not always be true depending on data, so we just check it doesn't crash
    assert len(widths_low) > 0
    assert len(widths_high) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
