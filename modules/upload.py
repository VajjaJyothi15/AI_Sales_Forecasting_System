import pandas as pd
import streamlit as st

from database.data_operations import save_sales_data
from utils.data_quality import calculate_data_quality
from utils.helpers import load_dataset


def _clear_uploaded_file():
    for key in (
        "data",
        "uploaded_file_name",
        "uploaded_file_type",
        "uploaded_file_size",
        "forecast_data",
        "forecast_model"
    ):
        st.session_state.pop(key, None)

    st.session_state["upload_widget_key"] += 1


def _show_dataset_details(df):
    st.subheader("Dataset Summary")

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

    st.subheader("Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.divider()

    st.subheader("Data Types")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(dtype_df, use_container_width=True)

    st.divider()


def show():
    st.title("Data Upload Center")

    st.markdown(
        """
        Upload your sales dataset for analysis,
        forecasting, and inventory optimization.
        """
    )

    if "upload_widget_key" not in st.session_state:
        st.session_state["upload_widget_key"] = 0

    if "data" in st.session_state:
        current_name = st.session_state.get("uploaded_file_name", "Uploaded dataset")
        st.success(f"Current file: {current_name}")

        if st.button("Remove Uploaded File"):
            _clear_uploaded_file()
            st.rerun()

        st.divider()

    uploaded_file = st.file_uploader(
        "Upload Dataset",
        type=["csv", "tsv", "txt", "xlsx", "xls"],
        key=f"dataset_uploader_{st.session_state['upload_widget_key']}"
    )

    if uploaded_file is not None:
        try:
            df = load_dataset(uploaded_file)
            df.columns = df.columns.str.strip()

            st.session_state["data"] = df
            st.session_state["uploaded_file_name"] = uploaded_file.name
            st.session_state["uploaded_file_type"] = uploaded_file.type
            st.session_state["uploaded_file_size"] = uploaded_file.size

            st.success("Dataset Uploaded Successfully")
            st.divider()
            _show_dataset_details(df)

            if st.button("Save Dataset to Database"):
                save_sales_data(df)
                st.success("Dataset Saved to SQLite Database")

        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.info(
                "Please upload a valid CSV, TSV, TXT, XLSX, or XLS file with at least one header row."
            )

    elif "data" in st.session_state:
        _show_dataset_details(st.session_state["data"])

        if st.button("Save Current Dataset to Database"):
            save_sales_data(st.session_state["data"])
            st.success("Dataset Saved to SQLite Database")

    else:
        st.info("Please upload a CSV, TSV, TXT, or Excel file.")
