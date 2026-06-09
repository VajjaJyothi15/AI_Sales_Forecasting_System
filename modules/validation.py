import streamlit as st
import pandas as pd
from utils.column_mapper import standardize_columns

from utils.validation import (
    get_missing_values,
    get_duplicate_rows,
    detect_outliers,
    validate_dates
)

from utils.data_quality import (
    calculate_data_quality
)


def show():

    st.title(
        "📋 Data Validation"
    )

    if "data" not in st.session_state:

        st.warning(
            "Upload Dataset First"
        )

        return

    df = standardize_columns(st.session_state["data"])
    st.session_state["data"] = df

    if df.empty:
        st.warning("Uploaded dataset has no rows to validate.")
        return

    st.subheader(
        "📊 Validation Summary"
    )

    quality_score = (
        calculate_data_quality(df)
    )

    st.metric(
        "Data Quality Score",
        f"{quality_score}%"
    )

    st.divider()

    # Missing Values

    st.subheader(
        "🔍 Missing Values"
    )

    missing = (
        get_missing_values(df)
    )

    st.dataframe(
        missing.reset_index(),
        use_container_width=True
    )

    st.divider()

    # Duplicates

    st.subheader(
        "📄 Duplicate Rows"
    )

    duplicates = (
        get_duplicate_rows(df)
    )

    st.metric(
        "Duplicate Rows",
        duplicates
    )

    st.divider()

    # Outlier Detection

    st.subheader(
        "📈 Outlier Detection"
    )

    numeric_cols = (

        df.select_dtypes(
            include="number"
        )

        .columns
    )

    if len(numeric_cols) > 0:

        selected_column = st.selectbox(

            "Select Numeric Column",

            numeric_cols
        )

        outliers = detect_outliers(

            df,

            selected_column
        )

        st.metric(

            "Outliers Found",

            len(outliers)
        )

        st.dataframe(

            outliers,

            use_container_width=True
        )

    st.divider()

    # Date Validation

    date_columns = [

        col

        for col in df.columns

        if "date" in col.lower()
    ]

    if len(date_columns) > 0:

        st.subheader(
            "📅 Date Validation"
        )

        selected_date = (

            st.selectbox(

                "Select Date Column",

                date_columns
            )
        )

        invalid_dates = (

            validate_dates(

                df,

                selected_date
            )
        )

        st.metric(

            "Invalid Dates",

            len(invalid_dates)
        )

        if len(invalid_dates) > 0:

            st.write(
                invalid_dates
            )

    st.divider()

    st.success(
        "Validation Completed Successfully"
    )
