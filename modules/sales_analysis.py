import streamlit as st
import pandas as pd
import plotly.express as px
from utils.column_mapper import standardize_columns


def show():

    st.title("📈 Sales Analysis Dashboard")

    if "data" not in st.session_state:

        st.warning(
            "Upload Dataset First"
        )

        return

    df = standardize_columns(st.session_state["data"])
    st.session_state["data"] = df

    if df.empty:
        st.warning("Uploaded dataset has no rows to analyze.")
        return

    # ==========================
    # KPI SECTION
    # ==========================

    total_sales = df["Sales"].sum()

    total_profit = df["Profit"].sum()

    total_orders = len(df)

    avg_order_value = (
        total_sales / total_orders
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        "Revenue",
        f"₹{total_sales:,.0f}"
    )

    col2.metric(
        "Profit",
        f"₹{total_profit:,.0f}"
    )

    col3.metric(
        "Orders",
        total_orders
    )

    col4.metric(
        "Avg Order Value",
        f"₹{avg_order_value:,.0f}"
    )

    st.divider()

    # ==========================
    # BEST SELLING PRODUCTS
    # ==========================

    st.subheader(
        "🏆 Best Selling Products"
    )

    best_products = (

        df.groupby(
            "Product_Name"
        )["Sales"]

        .sum()

        .sort_values(
            ascending=False
        )

        .head(10)

        .reset_index()
    )

    fig = px.bar(

        best_products,

        x="Product_Name",

        y="Sales",

        title=
        "Top 10 Products"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # WORST SELLING PRODUCTS
    # ==========================

    st.subheader(
        "📉 Worst Selling Products"
    )

    worst_products = (

        df.groupby(
            "Product_Name"
        )["Sales"]

        .sum()

        .sort_values()

        .head(10)

        .reset_index()
    )

    fig = px.bar(

        worst_products,

        x="Product_Name",

        y="Sales",

        title=
        "Bottom Products"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # REGION PERFORMANCE
    # ==========================

    st.subheader(
        "🌍 Region Performance"
    )

    region_sales = (

        df.groupby(
            "Region"
        )["Sales"]

        .sum()

        .reset_index()
    )

    fig = px.pie(

        region_sales,

        names="Region",

        values="Sales",

        title=
        "Revenue Contribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # CUSTOMER DEMAND
    # ==========================

    st.subheader(
        "👥 Customer Demand"
    )

    demand = (

        df.groupby(
            "Product_Name"
        )["Quantity"]

        .sum()

        .reset_index()
    )

    fig = px.area(

        demand,

        x="Product_Name",

        y="Quantity",

        title=
        "Product Demand"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # TREEMAP
    # ==========================

    st.subheader(
        "🌳 Sales Treemap"
    )

    tree = (

        df.groupby(
            [
                "Category",
                "Product_Name"
            ]
        )["Sales"]

        .sum()

        .reset_index()
    )

    fig = px.treemap(

        tree,

        path=[
            "Category",
            "Product_Name"
        ],

        values="Sales"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # SUNBURST
    # ==========================

    st.subheader(
        "☀️ Category Hierarchy"
    )

    fig = px.sunburst(

        tree,

        path=[
            "Category",
            "Product_Name"
        ],

        values="Sales"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success(
        "Sales Analysis Completed"
    )
