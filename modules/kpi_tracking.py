import streamlit as st


def show():

    st.title(
        "🎯 KPI Target Tracking"
    )

    target = st.number_input(
        "Sales Target"
    )

    achieved = st.number_input(
        "Current Sales"
    )

    progress = 0

    if target > 0:

        progress = achieved / target

    st.progress(progress)

    st.metric(
        "Achievement %",
        round(progress * 100, 2)
    )