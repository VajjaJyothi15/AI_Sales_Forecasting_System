import streamlit as st
import plotly.express as px

from utils.column_mapper import standardize_columns


def sales_dashboard(df):
    df = standardize_columns(df)

    if df.empty:
        st.warning("Uploaded dataset has no rows to analyze.")
        return

    st.subheader("Sales Analytics")

    sales_by_product = (
        df.groupby("Product_Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig1 = px.bar(
        sales_by_product,
        x="Product_Name",
        y="Sales",
        title="Sales by Product"
    )

    st.plotly_chart(fig1, use_container_width=True)

    sales_by_category = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        sales_by_category,
        values="Sales",
        names="Category",
        title="Category Contribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.treemap(
        df,
        path=["Category", "Product_Name"],
        values="Sales",
        title="Product Hierarchy"
    )

    st.plotly_chart(fig3, use_container_width=True)
