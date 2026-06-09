import streamlit as st
import pandas as pd
import plotly.express as px

from utils.insights import (
    generate_insights
)


def show():

    st.title(
        "🚀 AI-Powered Sales Forecasting & Inventory Optimization"
    )

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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Revenue",
            "₹25.8L",
            "+18%"
        )

    with col2:
        st.metric(
            "📦 Orders",
            "12,540",
            "+11%"
        )

    with col3:
        st.metric(
            "📈 Profit",
            "₹5.2L",
            "+9%"
        )

    with col4:
        st.metric(
            "🌍 Regions",
            "5"
        )

    st.divider()

    # -----------------------
    # OVERVIEW
    # -----------------------

    st.subheader(
        "📊 Executive Overview"
    )

    left, right = st.columns(
        [2,1]
    )

    with left:

        sample_data = pd.DataFrame({

            "Month":[

                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun"
            ],

            "Revenue":[

                120000,
                140000,
                180000,
                220000,
                260000,
                310000
            ]
        })

        fig = px.line(

            sample_data,

            x="Month",

            y="Revenue",

            markers=True,

            title="Revenue Growth Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.info(
            """
            🎯 Business Goals

            • Improve forecasting accuracy

            • Reduce inventory costs

            • Increase profitability

            • Improve demand planning

            • Optimize stock levels
            """
        )

    st.divider()

    # -----------------------
    # AI INSIGHTS
    # -----------------------

    st.subheader(
        "🤖 AI Insights"
    )

    if "data" in st.session_state:

        insights = generate_insights(
            st.session_state["data"]
        )

        for item in insights:

            st.success(item)

    else:

        st.warning(
            "Upload dataset to generate AI insights."
        )

    st.divider()

    # -----------------------
    # PLATFORM FEATURES
    # -----------------------

    st.subheader(
        "✨ Platform Capabilities"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.info(
            """
            📊 Analytics

            - EDA
            - Sales Analysis
            - Region Analysis
            """
        )

    with c2:

        st.info(
            """
            🤖 Machine Learning

            - Linear Regression
            - Random Forest
            - XGBoost
            - Model Comparison
            """
        )

    with c3:

        st.info(
            """
            📦 Inventory Intelligence

            - EOQ
            - Safety Stock
            - Reorder Point
            """
        )

    st.divider()

    
