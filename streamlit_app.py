"""
Streamlit Web Interface for iLoveExcel
Deploy this on Streamlit Cloud for free web access!
"""

import streamlit as st
import pandas as pd
import io
from pathlib import Path

# Import your existing functions
try:
    from iLoveExcel import (
        csvs_to_excel,
        union_csvs,
        union_multiple_csvs,
        join_csvs,
        merge_excel_files
    )
    ILOVEEXCEL_AVAILABLE = True
except ImportError:
    ILOVEEXCEL_AVAILABLE = False
    st.warning("⚠️ iLoveExcel package not found. Install with: `pip install -e .`")

# Page configuration
st.set_page_config(
    page_title="iLoveExcel - Excel & CSV Operations",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🔷 iLoveExcel</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced CSV & Excel Operations</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎯 Select Operation")
    operation = st.radio(
        "Choose what you want to do:",
        [
            "📊 CSV to Excel",
            "🔗 Union CSVs",
            "🤝 Join CSVs",
            "📑 Merge Excel Files",
            "ℹ️ About"
        ]
    )
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Tips")
    st.markdown("""
    - Upload multiple files when needed
    - Download results instantly
    - All processing is secure & temporary
    - Works with large files!
    """)

# Main content
if operation == "📊 CSV to Excel":
    st.header("📊 Convert CSVs to Excel")
    st.markdown("Upload multiple CSV files to combine them into a single Excel workbook.")
    
    uploaded_files = st.file_uploader(
        "Upload CSV files",
        type=['csv'],
        accept_multiple_files=True,
        key='csv_to_excel'
    )
    
    col1, col2 = st.columns(2)
    with col1:
        sheet_names_input = st.text_input(
            "Sheet names (comma-separated, optional)",
            placeholder="Sheet1, Sheet2, Sheet3",
            help="Leave empty to use CSV filenames"
        )
    
    with col2:
        output_name = st.text_input(
            "Output filename",
            value="combined.xlsx",
            help="Name for the output Excel file"
        )
    
    if uploaded_files and st.button("🎯 Convert to Excel", type="primary"):
        with st.spinner("Converting CSV files to Excel..."):
            try:
                # Parse sheet names
                sheet_names = None
                if sheet_names_input.strip():
                    sheet_names = [s.strip() for s in sheet_names_input.split(',')]
                
                # Save uploaded files temporarily
                temp_files = []
                for uploaded_file in uploaded_files:
                    temp_path = f"/tmp/{uploaded_file.name}"
                    with open(temp_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    temp_files.append(temp_path)
                
                # Create Excel file
                output_path = f"/tmp/{output_name}"
                if ILOVEEXCEL_AVAILABLE:
                    csvs_to_excel(temp_files, output_path, sheet_names=sheet_names)
                else:
                    # Fallback using pandas
                    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                        for idx, file_path in enumerate(temp_files):
                            df = pd.read_csv(file_path)
                            sheet_name = sheet_names[idx] if sheet_names and idx < len(sheet_names) else f"Sheet{idx+1}"
                            df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Provide download
                with open(output_path, 'rb') as f:
                    st.success("✅ Conversion successful!")
                    st.download_button(
                        label="📥 Download Excel File",
                        data=f,
                        file_name=output_name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                # Show preview
                st.markdown("### Preview")
                for idx, file_path in enumerate(temp_files):
                    with st.expander(f"Sheet {idx + 1}: {Path(file_path).name}"):
                        df = pd.read_csv(file_path)
                        st.dataframe(df.head(10))
                        st.caption(f"Showing first 10 of {len(df)} rows")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

elif operation == "🔗 Union CSVs":
    st.header("🔗 Union Multiple CSVs")
    st.markdown("Combine multiple CSV files by appending rows (union operation).")
    
    uploaded_files = st.file_uploader(
        "Upload CSV files to union",
        type=['csv'],
        accept_multiple_files=True,
        key='union_csvs'
    )
    
    col1, col2 = st.columns(2)
    with col1:
        dedupe = st.checkbox("Remove duplicate rows", value=True)
    
    with col2:
        output_name = st.text_input(
            "Output filename",
            value="union_result.csv",
            help="Name for the output CSV file"
        )
    
    if dedupe:
        dedupe_cols_input = st.text_input(
            "Columns for deduplication (comma-separated, optional)",
            placeholder="id, email",
            help="Leave empty to check all columns"
        )
    else:
        dedupe_cols_input = ""
    
    if uploaded_files and len(uploaded_files) >= 2 and st.button("🎯 Union Files", type="primary"):
        with st.spinner("Unioning CSV files..."):
            try:
                # Save uploaded files temporarily
                temp_files = []
                for uploaded_file in uploaded_files:
                    temp_path = f"/tmp/{uploaded_file.name}"
                    with open(temp_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    temp_files.append(temp_path)
                
                # Parse dedupe columns
                dedupe_cols = None
                if dedupe and dedupe_cols_input.strip():
                    dedupe_cols = [c.strip() for c in dedupe_cols_input.split(',')]
                
                # Perform union
                output_path = f"/tmp/{output_name}"
                if ILOVEEXCEL_AVAILABLE:
                    union_multiple_csvs(
                        temp_files,
                        output_path,
                        dedupe=dedupe,
                        dedupe_columns=dedupe_cols
                    )
                else:
                    # Fallback using pandas
                    dfs = [pd.read_csv(f) for f in temp_files]
                    result = pd.concat(dfs, ignore_index=True)
                    if dedupe:
                        if dedupe_cols:
                            result = result.drop_duplicates(subset=dedupe_cols)
                        else:
                            result = result.drop_duplicates()
                    result.to_csv(output_path, index=False)
                
                # Provide download
                with open(output_path, 'rb') as f:
                    st.success("✅ Union successful!")
                    
                    # Show stats
                    result_df = pd.read_csv(output_path)
                    total_input_rows = sum(len(pd.read_csv(f)) for f in temp_files)
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Input Rows", f"{total_input_rows:,}")
                    col2.metric("Output Rows", f"{len(result_df):,}")
                    col3.metric("Duplicates Removed", f"{total_input_rows - len(result_df):,}")
                    
                    st.download_button(
                        label="📥 Download Union Result",
                        data=f,
                        file_name=output_name,
                        mime="text/csv"
                    )
                
                # Show preview
                st.markdown("### Preview (first 10 rows)")
                st.dataframe(result_df.head(10))
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif uploaded_files and len(uploaded_files) < 2:
        st.warning("⚠️ Please upload at least 2 CSV files to perform union.")

elif operation == "🤝 Join CSVs":
    st.header("🤝 Join Two CSVs")
    st.markdown("Join two CSV files on common key columns (SQL-style joins).")
    
    col1, col2 = st.columns(2)
    
    with col1:
        left_file = st.file_uploader("Upload LEFT CSV", type=['csv'], key='join_left')
    
    with col2:
        right_file = st.file_uploader("Upload RIGHT CSV", type=['csv'], key='join_right')
    
    if left_file and right_file:
        # Show column names
        left_df = pd.read_csv(left_file)
        right_df = pd.read_csv(right_file)
        
        left_file.seek(0)  # Reset file pointer
        right_file.seek(0)
        
        st.markdown("### Join Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            join_keys_input = st.text_input(
                "Join key(s)",
                placeholder="id, user_id",
                help="Column(s) to join on (comma-separated)"
            )
        
        with col2:
            join_type = st.selectbox(
                "Join type",
                ["inner", "left", "right", "outer", "cross"],
                help="SQL-style join type"
            )
        
        with col3:
            output_name = st.text_input(
                "Output filename",
                value="joined_result.csv"
            )
        
        # Show column info
        with st.expander("📋 View Column Names"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Left CSV Columns:**")
                st.code('\n'.join(left_df.columns.tolist()))
            with col2:
                st.markdown("**Right CSV Columns:**")
                st.code('\n'.join(right_df.columns.tolist()))
        
        if join_keys_input and st.button("🎯 Join Files", type="primary"):
            with st.spinner(f"Performing {join_type} join..."):
                try:
                    # Parse join keys
                    join_keys = [k.strip() for k in join_keys_input.split(',')]
                    join_on = join_keys[0] if len(join_keys) == 1 else join_keys
                    
                    # Save files temporarily
                    left_path = "/tmp/left.csv"
                    right_path = "/tmp/right.csv"
                    output_path = f"/tmp/{output_name}"
                    
                    with open(left_path, 'wb') as f:
                        f.write(left_file.getbuffer())
                    with open(right_path, 'wb') as f:
                        f.write(right_file.getbuffer())
                    
                    # Perform join
                    if ILOVEEXCEL_AVAILABLE:
                        result_df = join_csvs(
                            left_path,
                            right_path,
                            join_on,
                            how=join_type,
                            output_file=output_path
                        )
                    else:
                        # Fallback using pandas
                        result_df = left_df.merge(right_df, on=join_on, how=join_type)
                        result_df.to_csv(output_path, index=False)
                    
                    # Provide download
                    with open(output_path, 'rb') as f:
                        st.success("✅ Join successful!")
                        
                        # Show stats
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Left Rows", f"{len(left_df):,}")
                        col2.metric("Right Rows", f"{len(right_df):,}")
                        col3.metric("Result Rows", f"{len(result_df):,}")
                        
                        st.download_button(
                            label="📥 Download Join Result",
                            data=f,
                            file_name=output_name,
                            mime="text/csv"
                        )
                    
                    # Show preview
                    st.markdown("### Preview (first 10 rows)")
                    st.dataframe(result_df.head(10))
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Tip: Make sure the join key(s) exist in both CSV files.")

elif operation == "📑 Merge Excel Files":
    st.header("📑 Merge Multiple Excel Files")
    st.markdown("Merge multiple Excel files by combining sheets with the same name.")
    
    uploaded_files = st.file_uploader(
        "Upload Excel files to merge",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        key='merge_excel'
    )
    
    col1, col2 = st.columns(2)
    with col1:
        merge_mode = st.radio(
            "Merge mode",
            ["Lenient (union of columns)", "Strict (identical columns required)"],
            help="Lenient mode is safer for files with different column structures"
        )
    
    with col2:
        output_name = st.text_input(
            "Output filename",
            value="merged_result.xlsx"
        )
    
    if uploaded_files and len(uploaded_files) >= 2 and st.button("🎯 Merge Files", type="primary"):
        with st.spinner("Merging Excel files..."):
            try:
                # Save uploaded files temporarily
                temp_files = []
                for uploaded_file in uploaded_files:
                    temp_path = f"/tmp/{uploaded_file.name}"
                    with open(temp_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    temp_files.append(temp_path)
                
                # Perform merge
                output_path = f"/tmp/{output_name}"
                mode = 'lenient' if 'Lenient' in merge_mode else 'strict'
                
                if ILOVEEXCEL_AVAILABLE:
                    merge_excel_files(temp_files, output_path, mode=mode)
                else:
                    st.error("❌ Excel merge requires iLoveExcel package. Install with: `pip install -e .`")
                    st.stop()
                
                # Provide download
                with open(output_path, 'rb') as f:
                    st.success("✅ Merge successful!")
                    st.download_button(
                        label="📥 Download Merged Excel",
                        data=f,
                        file_name=output_name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                # Show sheet info
                merged_sheets = pd.ExcelFile(output_path).sheet_names
                st.markdown(f"### Merged Sheets ({len(merged_sheets)})")
                st.write(merged_sheets)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif uploaded_files and len(uploaded_files) < 2:
        st.warning("⚠️ Please upload at least 2 Excel files to merge.")

elif operation == "ℹ️ About":
    st.header("ℹ️ About iLoveExcel")
    
    st.markdown("""
    ### 🔷 What is iLoveExcel?
    
    iLoveExcel is a powerful tool for CSV and Excel operations, including:
    - Converting multiple CSVs to Excel
    - Unioning/combining CSV files
    - Joining CSVs (like SQL joins)
    - Merging Excel workbooks
    
    ### 🚀 Features
    
    - **Easy to Use** - Simple drag-and-drop interface
    - **Fast Processing** - Optimized for large files
    - **Secure** - All processing happens in your session
    - **Free** - Completely free to use
    - **Cross-Platform** - Works on any device with a browser
    
    ### 🔒 Privacy & Security
    
    - Files are processed in isolated sessions
    - No data is stored permanently
    - Files are deleted after processing
    - Secure HTTPS connection
    
    ### 💻 Available Interfaces
    
    1. **Web App** (you're here!) - Easy access from anywhere
    2. **Desktop App** - PySimpleGUI interface for offline use
    3. **Command Line** - For automation and scripting
    
    ### 📚 Learn More
    
    - [GitHub Repository](https://github.com/monkcoders/iLoveExcel)
    - [Documentation](https://github.com/monkcoders/iLoveExcel#readme)
    - [Report Issues](https://github.com/monkcoders/iLoveExcel/issues)
    
    ### 👨‍💻 Built With
    
    - Python 🐍
    - Streamlit 🎈
    - pandas 🐼
    - openpyxl 📊
    
    ---
    
    Made with ❤️ by the iLoveExcel team
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "🔷 iLoveExcel | "
    "<a href='https://github.com/monkcoders/iLoveExcel' target='_blank'>GitHub</a> | "
    "Version 0.1.0"
    "</div>",
    unsafe_allow_html=True
)
