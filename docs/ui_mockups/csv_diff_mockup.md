# CSV Side-by-Side Diff UI Mockup

## ⚠️ USER APPROVAL REQUIRED

**This is a design mockup for the CSV diff UI feature.**  
**Implementation of the interactive diff UI will NOT proceed until this mockup is approved by the repository owner.**

---

## Overview

The CSV Side-by-Side Diff feature will allow users to compare two CSV files row-by-row and highlight differences. This document presents the proposed UI layout and workflow.

---

## UI Layout (ASCII Mockup)

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  iLoveExcel - CSV Side-by-Side Diff Comparison                      [_][□][X] │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ INPUT FILES                                                              │ │
│  ├──────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                          │ │
│  │  Left File (A):   [____________sample_a.csv____________] [Browse...]    │ │
│  │  Right File (B):  [____________sample_b.csv____________] [Browse...]    │ │
│  │                                                                          │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ COMPARISON SETTINGS                                                      │ │
│  ├──────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                          │ │
│  │  Compare Mode:  ( ) By Row Index   (•) By Key Column(s)                 │ │
│  │                                                                          │ │
│  │  Key Column(s): [___id, email___]  (comma-separated)                    │ │
│  │                                                                          │ │
│  │  [✓] Show Only Differences      [ ] Show All Rows                        │ │
│  │  [✓] Ignore Whitespace          [ ] Case Insensitive                     │ │
│  │  [ ] Ignore Column Order         [ ] Include Metadata (row numbers)      │ │
│  │                                                                          │ │
│  │  Max Rows to Display: [____1000____]  (0 = unlimited)                   │ │
│  │                                                                          │ │
│  │  Export Options:                                                         │ │
│  │  [✓] Highlight differences in Excel export                               │ │
│  │  Output File: [__comparison_result.xlsx__] [Browse...]                  │ │
│  │                                                                          │ │
│  │                [ Compare ] [ Export to Excel ] [ Clear ]                 │ │
│  │                                                                          │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ DIFF RESULTS                                                             │ │
│  ├──────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                          │ │
│  │  Summary: 150 total rows compared • 12 differences found                │ │
│  │          138 matching • 5 only in A • 7 only in B                       │ │
│  │                                                                          │ │
│  │  ┌────────┬──────────────────────────────────────────────────────────┐  │ │
│  │  │ Row    │ Column       │ File A Value    │ File B Value    │ Status│  │ │
│  │  ├────────┼──────────────────────────────────────────────────────────┤  │ │
│  │  │ 3      │ name         │ John Smith      │ John Smyth      │ DIFF  │  │ │
│  │  │ 3      │ email        │ john@email.com  │ john@email.com  │ MATCH │  │ │
│  │  │ 3      │ age          │ 30              │ 30              │ MATCH │  │ │
│  │  │ 5      │ salary       │ 50000           │ 55000           │ DIFF  │  │ │
│  │  │ 8      │ city         │ New York        │ Los Angeles     │ DIFF  │  │ │
│  │  │ 12     │ (all)        │ [Row exists]    │ [Missing]       │ ONLY_A│  │ │
│  │  │ 15     │ (all)        │ [Missing]       │ [Row exists]    │ ONLY_B│  │ │
│  │  │ ...    │ ...          │ ...             │ ...             │ ...   │  │ │
│  │  └────────┴──────────────────────────────────────────────────────────┘  │ │
│  │                                                                          │ │
│  │  [Scroll for more ↕]                                                     │ │
│  │                                                                          │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │
│  Progress: ████████████████████████░░░░░░░░  80%                              │
│                                                                                │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │ LOG                                                                      │ │
│  ├──────────────────────────────────────────────────────────────────────────┤ │
│  │ Loading files...                                                         │ │
│  │ File A: 150 rows, 5 columns                                              │ │
│  │ File B: 152 rows, 5 columns                                              │ │
│  │ Aligning by key column(s): id, email                                     │ │
│  │ Comparison complete: 12 differences found                                │ │
│  │                                                                          │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │
│                               [Close]                                          │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Layout Sections

### 1. **INPUT FILES** (Top Panel)
- **Left File (A):** File path input + Browse button
- **Right File (B):** File path input + Browse button
- Both support CSV and Excel formats
- File validation on selection

### 2. **COMPARISON SETTINGS** (Middle Panel)
Contains all comparison configuration options:

#### Compare Mode:
- **By Row Index:** Compare rows at same position (1-1, 2-2, etc.)
- **By Key Column(s):** Align rows using specified key column(s) for comparison

#### Key Column(s):
- Text input for comma-separated column names
- Only enabled when "By Key Column(s)" is selected
- Example: `id, email` or just `user_id`

#### Options Checkboxes:
- **Show Only Differences:** Filter view to show only rows with differences
- **Show All Rows:** Display all rows (matched and unmatched)
- **Ignore Whitespace:** Trim whitespace before comparison
- **Case Insensitive:** Ignore case when comparing string values
- **Ignore Column Order:** Match columns by name regardless of position
- **Include Metadata:** Add row index columns to output

#### Display Limit:
- Numeric input for maximum rows to display (performance)
- 0 = unlimited

#### Export Options:
- Checkbox to enable/disable Excel highlighting
- Output file path selector
- Separate buttons for Compare (in-UI) vs Export (to file)

### 3. **DIFF RESULTS** (Main Display Panel)
Two-part display:

#### Summary Stats (Top):
- Total rows compared
- Number of differences found
- Matching rows count
- Rows only in A (missing from B)
- Rows only in B (missing from A)

#### Results Table (Scrollable):
Columns:
- **Row:** Row number/index from original files
- **Column:** Column name where difference occurs
- **File A Value:** Value from left file
- **File B Value:** Value from right file
- **Status:** DIFF | MATCH | ONLY_A | ONLY_B

**Color Coding (in implementation):**
- 🟢 MATCH - Green background
- 🟡 DIFF - Yellow/Orange background
- 🔵 ONLY_A - Blue background
- 🔴 ONLY_B - Red background

**Features:**
- Sortable by any column
- Filterable
- Scrollable (virtualized for performance with large diffs)
- Right-click context menu: Copy, Export selected rows

### 4. **PROGRESS BAR**
- Shows progress during file loading and comparison
- Percentage display

### 5. **LOG PANEL** (Bottom)
- Real-time log messages
- File statistics
- Comparison progress updates
- Error messages
- Auto-scrolls to latest

---

## User Workflow

### Typical Usage:
1. User selects operation "CSV Side-by-Side Diff" from main menu
2. This UI window opens
3. User selects File A and File B
4. User chooses comparison mode (row index or key-based)
5. If key-based, user enters key column name(s)
6. User adjusts options (show only diffs, ignore whitespace, etc.)
7. User clicks **"Compare"**
8. Results appear in Diff Results panel
9. User reviews differences
10. User clicks **"Export to Excel"** to save highlighted comparison
11. Excel file created with:
    - Sheet 1: Side-by-side comparison with highlighted cells
    - Sheet 2: Summary statistics
    - Sheet 3: Rows only in A
    - Sheet 4: Rows only in B

### Export File Format (Excel):
```
┌─────────────────────────────────────────────────────────────┐
│ Sheet: Side-by-Side Comparison                             │
├─────────────────────────────────────────────────────────────┤
│ Row_A | Col1_A | Col2_A | Row_B | Col1_B | Col2_B | Status │
│   1   │  ABC   │  123   │   1   │  ABC   │  123   │ MATCH  │
│   2   │  DEF   │  456   │   2   │  DEF   │  999   │ DIFF   │  ← Yellow highlight
│   3   │  GHI   │  789   │   -   │   -    │   -    │ ONLY_A │  ← Blue highlight
│   -   │   -    │   -    │   4   │  JKL   │  321   │ ONLY_B │  ← Red highlight
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Notes (for developer)

### Technology Stack:
- **GUI Framework:** Tkinter with ttk widgets
- **Table Widget:** `ttk.Treeview` with virtual scrolling for large datasets
- **Diff Logic:** `src/iLoveExcel/diffs.py` module (already implemented)
- **Excel Export:** openpyxl for formatting and highlighting

### Performance Considerations:
- Limit in-memory display to configured max_rows
- Use pandas chunked reading for very large files
- Implement virtual scrolling in Treeview (only render visible rows)
- Background thread for comparison to avoid UI blocking

### Key Functions (to be implemented):
```python
# In gui_tk.py
def show_csv_diff_window():
    """Launch the CSV diff comparison window."""
    # Creates Tk Toplevel window with mockup layout

def on_compare_clicked():
    """Handle Compare button - runs diff in worker thread."""
    # Calls diffs.diff_csv_side_by_side()
    # Populates results table

def on_export_clicked():
    """Handle Export button - writes Excel with highlighting."""
    # Calls diffs.export_diff_to_excel()

def populate_diff_results_table(diff_df):
    """Populate Treeview with diff results."""
    # Adds rows with color tags

# In diffs.py (already implemented)
def diff_csv_side_by_side(...) -> pd.DataFrame:
    """Returns DataFrame with _A and _B suffixed columns."""

def export_diff_to_excel(diff_df, output_path, highlight=True):
    """Writes Excel with conditional formatting."""
```

---

## Alternative View Modes (Future Enhancement)

### Split-Pane View:
```
┌────────────────────────────────────┬────────────────────────────────────┐
│ File A (Left)                      │ File B (Right)                     │
├────────────────────────────────────┼────────────────────────────────────┤
│ Row | Col1 | Col2 | Col3          │ Row | Col1 | Col2 | Col3          │
│  1  │ ABC  │ 123  │ X              │  1  │ ABC  │ 123  │ X              │
│  2  │ DEF  │ 456  │ Y  ← DIFF →   │  2  │ DEF  │ 999  │ Y              │
│  3  │ GHI  │ 789  │ Z              │  -  │  -   │  -   │ -   ← ONLY_A  │
│  -  │  -   │  -   │ -   ← ONLY_B →│  3  │ JKL  │ 321  │ W              │
└────────────────────────────────────┴────────────────────────────────────┘
```

This view mode could be added later based on user feedback.

---

## Questions for Review

Before implementation proceeds, please confirm:

1. ✅ **Layout:** Is the proposed 3-panel layout (Input → Settings → Results) acceptable?
2. ✅ **Features:** Are the comparison options (key-based, ignore whitespace, etc.) sufficient?
3. ✅ **Display:** Is the table format for results clear and useful?
4. ✅ **Export:** Is the Excel export format (4 sheets with highlighting) appropriate?
5. ✅ **Workflow:** Does the user workflow make sense?

### Optional Enhancements (Future):
- Add "Unified Diff" view (like git diff)
- Add column-level diff summary
- Add export to HTML report
- Add "Accept A" / "Accept B" buttons for conflict resolution
- Add file history/recent comparisons

---

## Approval

**Status:** ⏸️ **AWAITING USER APPROVAL**

Once this mockup is approved, implementation will proceed in:
1. `src/iLoveExcel/gui_tk.py` - Add `show_csv_diff_window()` function
2. Integration with main Tkinter GUI menu
3. Unit tests for diff UI interactions

**Please review and provide feedback or approval to proceed.** ✅

---

**Next Steps After Approval:**
1. Implement `show_csv_diff_window()` in `gui_tk.py`
2. Wire up to main GUI menu button
3. Add keyboard shortcuts (Ctrl+D for diff)
4. Add tests for diff UI components
5. Update user documentation

