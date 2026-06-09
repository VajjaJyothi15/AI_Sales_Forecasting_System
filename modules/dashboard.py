import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from dashboard.kpi_dashboard import (
    get_kpis
)

from utils.insights import (
    generate_insights
)
from utils.column_mapper import standardize_columns


def show():

    st.title(
        "📊 Executive Dashboard"
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

    kpis = get_kpis(df)

    # =====================
    # KPI CARDS
    # =====================

    c1,c2,c3 = st.columns(3)

    c4,c5,c6 = st.columns(3)

    c1.metric(
        "💰 Revenue",
        f"₹{kpis['total_sales']:,.0f}"
    )

    c2.metric(
        "📈 Profit",
        f"₹{kpis['Profit']:,.0f}"
    )

    c3.metric(
        "🧾 Orders",
        kpis["Orders"]
    )

    c4.metric(
        "📦 Products",
        kpis["Products"]
    )

    c5.metric(
        "🌍 Regions",
        kpis["Regions"]
    )

    c6.metric(
        "🛒 Avg Order",
        f"₹{kpis['AvgOrder']:,.0f}"
    )

    st.divider()

    # =====================
    # REVENUE GAUGE
    # =====================

    st.subheader(
        "Revenue Achievement"
    )

    revenue_target = st.number_input(

        "Revenue Target",

        value=1000000
    )

    revenue_percent = 0

    if revenue_target > 0:
        revenue_percent = (

            kpis["Sales"]

            /

            revenue_target

        ) * 100

    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=revenue_percent,

            title={
                "text":
                "Target Achievement %"
            },

            gauge={
                "axis":
                {"range":[0,100]}
            }
        )
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    st.divider()

    # =====================
    # SALES TREND
    # =====================

    if (
        "Order_Date"
        in df.columns
    ):

        trend = px.line(

            df,

            x="Order_Date",

            y="Sales",

            title=
            "Revenue Trend"
        )

        st.plotly_chart(
            trend,
            use_container_width=True
        )

    st.divider()

    # =====================
    # REGION PERFORMANCE
    # =====================

    region = (

        df.groupby(
            "Region"
        )["Sales"]

        .sum()

        .reset_index()
    )

    fig = px.bar(

        region,

        x="Region",

        y="Sales",

        color="Region",

        title=
        "Region Performance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # =====================
    # FORECAST OVERVIEW
    # =====================

    if (
        "forecast_data"
        in st.session_state
    ):

        st.subheader(
            "Forecast Overview"
        )

        st.dataframe(

            st.session_state[
                "forecast_data"
            ]
            .head()
        )

    st.divider()

    # =====================
    # INVENTORY STATUS
    # =====================

    if (
        "Inventory"
        in df.columns
    ):

        low_stock = len(

            df[
                df["Inventory"]
                < 50
            ]
        )

        st.metric(

            "Low Stock Items",

            low_stock
        )

    st.divider()

    # =====================
    # AI INSIGHTS
    # =====================

    st.subheader(
        "🤖 AI Insights"
    )

    insights = (
        generate_insights(df)
    )

    for insight in insights:

        st.success(
            insight
        )

    st.success(
        "Executive Dashboard Ready"
    )
