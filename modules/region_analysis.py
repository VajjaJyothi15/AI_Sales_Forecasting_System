import streamlit as st
import pandas as pd
import plotly.express as px
from utils.column_mapper import standardize_columns


def show():

    st.title("🌍 Region Analysis Dashboard")

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
    # REGION KPIs
    # ==========================

    region_summary = (

        df.groupby("region")

        .agg({

            "Sales": "sum",

            "Profit": "sum"

        })

        .reset_index()
    )

    top_region = (

        region_summary

        .sort_values(
            "Sales",
            ascending=False
        )

        .iloc[0]
    )

    bottom_region = (

        region_summary

        .sort_values(
            "Sales"
        )

        .iloc[0]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Regions",
        df["region"].nunique()
    )

    col2.metric(
        "Top Region",
        top_region["region"]
    )

    col3.metric(
        "Top Revenue",
        f"₹{top_region['Sales']:,.0f}"
    )

    col4.metric(
        "Bottom Region",
        bottom_region["region"]
    )

    st.divider()

    # ==========================
    # SALES BY REGION
    # ==========================

    st.subheader(
        "📈 Revenue by Region"
    )

    fig = px.bar(

        region_summary,

        x="region",

        y="Sales",

        color="region",

        title="Regional Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # PROFIT BY REGION
    # ==========================

    st.subheader(
        "💰 Profit by Region"
    )

    fig = px.pie(

        region_summary,

        names="region",

        values="Profit",

        title="Profit Contribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # SALES VS PROFIT
    # ==========================

    st.subheader(
        "📊 Sales vs Profit"
    )

    fig = px.scatter(

        region_summary,

        x="Sales",

        y="Profit",

        size="Sales",

        color="region",

        hover_name="region",

        title="Regional Performance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # TREEMAP
    # ==========================

    st.subheader(
        "🌳 Regional Treemap"
    )

    fig = px.treemap(

        region_summary,

        path=["region"],

        values="Sales"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # GEO MAP
    # ==========================

    st.subheader(
        "🗺️ Geo Analysis"
    )

    map_data = pd.DataFrame({

        "region": [

            "North",
            "South",
            "East",
            "West",
            "Central"
        ],

        "Latitude": [

            28.6,
            13.0,
            22.5,
            19.0,
            23.2
        ],

        "Longitude": [

            77.2,
            80.2,
            88.3,
            72.8,
            77.4
        ]
    })

    geo_df = pd.merge(

        region_summary,

        map_data,

        on="region",

        how="left"
    )

    geo_df = geo_df.dropna(subset=["Latitude", "Longitude"])

    if geo_df.empty:
        st.info("Geo map is available for North, South, East, West, and Central regions.")
        st.success(
            "Region Analysis Completed"
        )
        return

    fig = px.scatter_mapbox(

        geo_df,

        lat="Latitude",

        lon="Longitude",

        size="Sales",

        color="Sales",

        hover_name="region",

        zoom=3,

        height=500
    )

    fig.update_layout(
        mapbox_style="open-street-map"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success(
        "Region Analysis Completed"
    )
