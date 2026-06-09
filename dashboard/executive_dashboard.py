import streamlit as st
from dashboard.kpi_dashboard import show_kpis
from dashboard.sales_dashboard import sales_dashboard
from dashboard.region_dashboard import region_dashboard

def executive_dashboard(df):

    st.title(
        "📊 Executive Dashboard"
    )

    show_kpis(df)

    st.divider()

    sales_dashboard(df)

    st.divider()

    region_dashboard(df)