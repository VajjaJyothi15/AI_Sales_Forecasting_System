import streamlit as st
import pandas as pd
import plotly.express as px
from utils.column_mapper import get_column, standardize_columns


def show():

    st.title("📊 Exploratory Data Analysis")

    if "data" not in st.session_state:
        st.warning("Upload Dataset First")
        return

    df = standardize_columns(st.session_state["data"])
    st.session_state["data"] = df

    if df.empty:
        st.warning("Uploaded dataset has no rows to analyze.")
        return

    filtered_df = df.copy()

    # ---------------- KPI SAFE COLUMNS ----------------
    sales_col = "sales" if "sales" in df.columns else None
    profit_col = "profit" if "profit" in df.columns else None

    # ---------------- KPI ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Revenue",
        f"₹{df[sales_col].sum():,.0f}" if sales_col else "N/A"
    )

    col2.metric(
        "Profit",
        f"₹{df[profit_col].sum():,.0f}" if profit_col else "N/A"
    )

    col3.metric("Records", len(df))

    st.divider()

    # ---------------- SALES TREND ----------------
    if sales_col and "order_date" in df.columns:

        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

        trend = df.groupby("order_date")[sales_col].sum().reset_index()

        fig = px.line(trend, x="order_date", y=sales_col, title="Sales Trend")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- REGION ----------------
    if "region" in df.columns and sales_col:

        region_sales = df.groupby("region")[sales_col].sum().reset_index()

        fig = px.pie(region_sales, names="region", values=sales_col, title="Region Analysis")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- PRODUCT ----------------
    if "product_name" in df.columns and sales_col:

        prod = df.groupby("product_name")[sales_col].sum().reset_index()

        fig = px.bar(prod, x="product_name", y=sales_col, title="Product Sales")
        st.plotly_chart(fig, use_container_width=True)

    st.success("EDA Completed Successfully")
