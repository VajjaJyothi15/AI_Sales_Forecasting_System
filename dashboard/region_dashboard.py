import streamlit as st
import plotly.express as px

from utils.column_mapper import standardize_columns


def region_dashboard(df):
    df = standardize_columns(df)

    if df.empty:
        st.warning("Uploaded dataset has no rows to analyze.")
        return

    st.subheader("Region Analysis")

    region_sales = (
        df.groupby("Region")
        .agg({"Sales": "sum", "Profit": "sum"})
        .reset_index()
    )

    fig1 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Sales",
        title="Revenue by Region"
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        region_sales,
        x="Region",
        y="Profit",
        color="Profit",
        title="Profit by Region"
    )

    st.plotly_chart(fig2, use_container_width=True)

    best_region = region_sales.sort_values("Sales", ascending=False).iloc[0]["Region"]
    worst_region = region_sales.sort_values("Sales", ascending=True).iloc[0]["Region"]

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"Top Region: {best_region}")

    with col2:
        st.error(f"Bottom Region: {worst_region}")
