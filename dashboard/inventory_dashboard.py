import streamlit as st
import plotly.express as px

from utils.column_mapper import standardize_columns


def inventory_dashboard(df):
    df = standardize_columns(df)

    if df.empty:
        st.warning("Uploaded dataset has no rows to analyze.")
        return

    st.subheader("Inventory Intelligence")

    fig = px.bar(
        df,
        x="Product",
        y="Inventory",
        color="Inventory",
        title="Current Inventory"
    )

    st.plotly_chart(fig, use_container_width=True)

    low_stock = df[df["Inventory"] < 50]

    if len(low_stock) > 0:
        st.warning(f"{len(low_stock)} products are below stock threshold")
        st.dataframe(low_stock[["Product", "Inventory"]])
    else:
        st.success("No low stock products")

    over_stock = df[df["Inventory"] > 1000]

    if len(over_stock) > 0:
        st.info(f"{len(over_stock)} products are overstocked")
