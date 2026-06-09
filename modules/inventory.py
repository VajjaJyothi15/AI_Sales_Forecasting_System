import streamlit as st
import pandas as pd
import plotly.express as px

from models.inventory_model import (
    inventory_analysis
)
from utils.column_mapper import standardize_columns


def show():

    st.title(
        "📦 Inventory Intelligence"
    )

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

    # -------------------
    # KPI CALCULATIONS
    # -------------------

    metrics = (
        inventory_analysis(df)
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    col1.metric(

        "Safety Stock",

        metrics[
            "Safety Stock"
        ]
    )

    col2.metric(

        "Reorder Point",

        metrics[
            "Reorder Point"
        ]
    )

    col3.metric(

        "EOQ",

        metrics[
            "EOQ"
        ]
    )

    st.divider()

    # -------------------
    # STOCK STATUS
    # -------------------

    st.subheader(
        "inventory Status"
    )

    low_stock = df[
        df["inventory"] < 50
    ]

    overstock = df[
        df["inventory"] > 500
    ]

    healthy = df[

        (df["inventory"] >= 50)

        &

        (df["inventory"] <= 500)
    ]

    col1, col2, col3 = (
        st.columns(3)
    )

    col1.error(
        f"Low Stock: {len(low_stock)}"
    )

    col2.warning(
        f"Overstock: {len(overstock)}"
    )

    col3.success(
        f"Healthy: {len(healthy)}"
    )

    st.divider()

    # -------------------
    # INVENTORY CHART
    # -------------------

    st.subheader(
        "Stock Levels"
    )

    chart = px.bar(

        df,

        x="Product_Name",

        y="inventory",

        color="inventory",

        title=
        "Current Inventory"
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    # -------------------
    # LOW STOCK ALERTS
    # -------------------

    st.subheader(
        "🚨 Low Stock Alerts"
    )

    if len(low_stock) > 0:

        st.dataframe(
            low_stock[
                [
                    "Product_Name",
                    "inventory"
                ]
            ]
        )

    else:

        st.success(
            "No Low Stock Items"
        )

    st.divider()

    # -------------------
    # OVERSTOCK ALERTS
    # -------------------

    st.subheader(
        "⚠️ Overstock Alerts"
    )

    if len(overstock) > 0:

        st.dataframe(
            overstock[
                [
                    "Product_Name",
                    "inventory"
                ]
            ]
        )

    else:

        st.success(
            "No Overstock Items"
        )

    st.divider()

    # -------------------
    # RECOMMENDATIONS
    # -------------------

    st.subheader(
        "💡 Inventory Recommendations"
    )

    if len(low_stock) > 0:

        st.warning(
            """
            Reorder products with
            low stock immediately.
            """
        )

    if len(overstock) > 0:

        st.info(
            """
            Run promotions to
            reduce excess inventory.
            """
        )

    if (
        len(low_stock) == 0
        and
        len(overstock) == 0
    ):

        st.success(
            """
            Inventory levels are
            optimized.
            """
        )

    st.success(
        "Inventory Analysis Completed"
    )
