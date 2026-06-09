import streamlit as st
import pandas as pd

from utils.data_quality import calculate_data_quality
from utils.helpers import load_dataset
from database.data_operations import save_sales_data


def show():

    st.title("📂 Data Upload Center")

    st.markdown("""
    Upload your sales dataset for analysis,
    forecasting, and inventory optimization.
    """)

    uploaded_file = st.file_uploader(
        "Upload Dataset",
        type=["csv", "tsv", "txt", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        try:

            # --------------------------
            # READ FILE PROPERLY
            # --------------------------

            df = load_dataset(uploaded_file)

            # --------------------------
            # CLEAN COLUMN NAMES
            # --------------------------
            df.columns = df.columns.str.strip()

            # --------------------------
            # SAVE TO SESSION
            # --------------------------
            st.session_state["data"] = df

            st.success("Dataset Uploaded Successfully")

            st.divider()

            # --------------------------
            # DATASET SUMMARY
            # --------------------------
            st.subheader("📊 Dataset Summary")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Rows", df.shape[0])

            with col2:
                st.metric("Columns", df.shape[1])

            with col3:
                st.metric("Missing Values", int(df.isnull().sum().sum()))

            with col4:
                quality = calculate_data_quality(df)
                st.metric("Data Quality", f"{quality}%")

            st.divider()

            # --------------------------
            # PREVIEW
            # --------------------------
            st.subheader("📄 Dataset Preview")
            st.dataframe(df.head(20), use_container_width=True)

            st.divider()

            # --------------------------
            # DATA TYPES
            # --------------------------
            st.subheader("📋 Data Types")

            dtype_df = pd.DataFrame({
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str)
            })

            st.dataframe(dtype_df, use_container_width=True)

            st.divider()

            # --------------------------
            # SAVE TO DB
            # --------------------------
            if st.button("💾 Save Dataset to Database"):
                save_sales_data(df)
                st.success("Dataset Saved to SQLite Database")

        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.info(
                "Please upload a valid CSV, TSV, TXT, XLSX, or XLS file with at least one header row."
            )

    else:
        st.info("Please upload a CSV, TSV, TXT, or Excel file.")
