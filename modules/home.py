import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.kpi_dashboard import get_kpis
from utils.column_mapper import standardize_columns
from utils.insights import generate_insights


def _format_currency(value):
    value = float(value or 0)

    if abs(value) >= 10000000:
        return f"Rs {value / 10000000:.2f}Cr"

    if abs(value) >= 100000:
        return f"Rs {value / 100000:.2f}L"

    return f"Rs {value:,.0f}"


def _change_delta(df, metric_col):
    if df.empty or metric_col not in df.columns or len(df) < 2:
        return None

    midpoint = len(df) // 2
    previous = pd.to_numeric(df.iloc[:midpoint][metric_col], errors="coerce").fillna(0).sum()
    current = pd.to_numeric(df.iloc[midpoint:][metric_col], errors="coerce").fillna(0).sum()

    if previous == 0:
        return None

    change = ((current - previous) / previous) * 100
    return f"{change:+.1f}%"


def _get_home_data():
    if "data" not in st.session_state:
        return None

    df = standardize_columns(st.session_state["data"])
    st.session_state["data"] = df
    return df


def _build_revenue_trend(df):
    trend_data = df.copy()
    trend_data["Order_Date"] = pd.to_datetime(
        trend_data["Order_Date"],
        errors="coerce"
    )
    trend_data = trend_data.dropna(subset=["Order_Date"])

    if trend_data.empty:
        trend_data = (
            df.reset_index()
            .rename(columns={"index": "Record"})
            .assign(Record=lambda data: data["Record"] + 1)
        )
        return trend_data, "Record", "Sales", "Revenue by Uploaded Records"

    trend_data = (
        trend_data
        .assign(Month=trend_data["Order_Date"].dt.to_period("M").dt.to_timestamp())
        .groupby("Month", as_index=False)["Sales"]
        .sum()
    )
    return trend_data, "Month", "Sales", "Revenue Growth Trend"


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
    # KPI CARDS
    # -----------------------
    df = _get_home_data()

    if df is not None and not df.empty:
        kpis = get_kpis(df)
        sales_delta = _change_delta(df, "Sales")
        profit_delta = _change_delta(df, "Profit")
        revenue_value = _format_currency(kpis["Sales"])
        orders_value = f"{kpis['Orders']:,}"
        profit_value = _format_currency(kpis["Profit"])
        regions_value = f"{kpis['Regions']:,}"
    else:
        kpis = None
        sales_delta = "+18%"
        profit_delta = "+9%"
        revenue_value = "Rs 25.8L"
        orders_value = "12,540"
        profit_value = "Rs 5.2L"
        regions_value = "5"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Revenue", revenue_value, sales_delta)

    with col2:
        st.metric("Orders", orders_value)

    with col3:
        st.metric("Profit", profit_value, profit_delta)

    with col4:
        st.metric("Regions", regions_value)

    st.divider()

    # -----------------------
    # OVERVIEW
    # -----------------------
    st.subheader("Executive Overview")

    left, right = st.columns([2, 1])

    with left:
        if df is not None and not df.empty:
            chart_data, x_col, y_col, title = _build_revenue_trend(df)
        else:
            chart_data = pd.DataFrame({
                "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                "Revenue": [120000, 140000, 180000, 220000, 260000, 310000]
            })
            x_col = "Month"
            y_col = "Revenue"
            title = "Revenue Growth Trend"

        fig = px.line(
            chart_data,
            x=x_col,
            y=y_col,
            markers=True,
            title=title
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        if df is not None and not df.empty:
            file_name = st.session_state.get("uploaded_file_name", "Uploaded dataset")
            top_region = None

            if "Region" in df.columns and "Sales" in df.columns:
                region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
                if not region_sales.empty:
                    top_region = f"{region_sales.index[0]} ({_format_currency(region_sales.iloc[0])})"

            st.info(
                f"""
                Current Dataset

                - {file_name}
                - {df.shape[0]:,} rows x {df.shape[1]:,} columns
                - Average order: {_format_currency(kpis["AvgOrder"] if kpis else 0)}
                - Top region: {top_region or "Not available"}
                """
            )
        else:
            st.info(
                """
                Business Goals

                - Improve forecasting accuracy
                - Reduce inventory costs
                - Increase profitability
                - Improve demand planning
                - Optimize stock levels
                """
            )

    st.divider()

    # -----------------------
    # AI INSIGHTS
    # -----------------------
    st.subheader("AI Insights")

    if df is not None and not df.empty:
        insights = generate_insights(df)

        for item in insights:
            st.success(item)
    else:
        st.warning("Upload dataset to generate AI insights.")

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
