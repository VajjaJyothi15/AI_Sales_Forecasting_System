import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.kpi_dashboard import get_kpis
from utils.column_mapper import standardize_columns
from utils.insights import generate_insights


def show():
    st.title("AI-Powered Sales Forecasting & Inventory Optimization")

    st.markdown(
        """
        ### Enterprise Business Intelligence Platform

        Predict future sales, optimize inventory,
        monitor KPIs, and generate AI-powered business insights.
        """
    )

    st.divider()
    # -----------------------
    # PLATFORM FEATURES
    # -----------------------
    st.subheader("Platform Capabilities")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            """
            Analytics

            - EDA
            - Sales Analysis
            - Region Analysis
            """
        )

    with c2:
        st.info(
            """
            Machine Learning

            - Linear Regression
            - Random Forest
            - XGBoost
            - Model Comparison
            """
        )

    with c3:
        st.info(
            """
            Inventory Intelligence

            - EOQ
            - Safety Stock
            - Reorder Point
            """
        )

    st.divider()
