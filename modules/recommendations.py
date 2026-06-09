import streamlit as st
from utils.column_mapper import standardize_columns

from utils.recommendation_engine import (
    generate_recommendations
)


def show():

    st.title(
        "💡 Business Recommendations"
    )

    if "data" not in st.session_state:

        st.warning(
            "Upload dataset first"
        )

        return

    df = standardize_columns(st.session_state["data"])
    st.session_state["data"] = df

    if df.empty:
        st.warning("Uploaded dataset has no rows for recommendations.")
        return

    recommendations = (

        generate_recommendations(

            df,
            st.session_state.get("forecast_data")
        )
    )

    for item in recommendations:

        st.success(item)
