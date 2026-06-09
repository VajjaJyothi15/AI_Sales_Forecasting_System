import streamlit as st
import pandas as pd
from utils.column_mapper import standardize_columns

from utils.preprocessing import (
    remove_nulls,
    fill_missing_values,
    remove_duplicates,
    feature_engineering
)


def show():

    st.title(
        "⚙️ Data Preprocessing"
    )

    if "data" not in st.session_state:

        st.warning(
            "Upload Dataset First"
        )

        return

    df = standardize_columns(st.session_state["data"])
    st.session_state["data"] = df

    if df.empty:
        st.warning("Uploaded dataset has no rows to preprocess.")
        return

    st.subheader(
        "Current Dataset"
    )

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Cleaning Operations"
    )

    col1, col2 = st.columns(2)

    with col1:

        remove_null_btn = st.button(
            "Remove Null Values"
        )

        fill_null_btn = st.button(
            "Fill Missing Values"
        )

    with col2:

        duplicate_btn = st.button(
            "Remove Duplicates"
        )

        feature_btn = st.button(
            "Generate Features"
        )

    if remove_null_btn:

        df = remove_nulls(df)

        st.success(
            "Null Values Removed"
        )

    if fill_null_btn:

        df = fill_missing_values(df)

        st.success(
            "Missing Values Filled"
        )

    if duplicate_btn:

        df = remove_duplicates(df)

        st.success(
            "Duplicates Removed"
        )

    if feature_btn:

        df = feature_engineering(df)

        st.success(
            "Features Generated"
        )

    st.session_state["data"] = df

    st.divider()

    st.subheader(
        "Processed Dataset"
    )

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    st.divider()

    csv = df.to_csv(
        index=False
    )

    st.download_button(

        label=
        "⬇ Download Processed Dataset",

        data=csv,

        file_name=
        "processed_sales_data.csv",

        mime="text/csv"
    )

    st.success(
        "Preprocessing Completed"
    )
