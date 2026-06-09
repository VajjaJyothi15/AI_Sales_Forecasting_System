import streamlit as st

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Sales Forecasting System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DATABASE INIT
# ==========================================

from database.create_tables import create_tables

create_tables()


# ==========================================
# IMPORT MODULES
# ==========================================

from modules import (
    home,
    upload,
    validation,
    preprocessing,
    eda,
    sales_analysis,
    region_analysis,
    model_training,
    forecasting,
    inventory,
    reports,
    dashboard,
    recommendations,
    kpi_tracking
)



# ==========================================
# NAVIGATION
# ==========================================

menu = st.sidebar.radio(

    "🚀 Navigation",

    [

        "🏠 Home",

        "📂 Upload Dataset",

        "📋 Data Validation",

        "⚙️ Data Preprocessing",

        "📊 EDA Analysis",

        "📈 Sales Analysis",

        "🌍 Region Analysis",

        "🤖 Model Training",

        "🔮 Forecasting",

        "📦 Inventory Intelligence",

        "📑 Reports",

        "🎯 KPI Tracking",

        "💡 Recommendations",

        "📊 Executive Dashboard"
    ]
)

# ==========================================
# ROUTING
# ==========================================

if menu == "🏠 Home":
    home.show()

elif menu == "📂 Upload Dataset":
    upload.show()

elif menu == "📋 Data Validation":
    validation.show()

elif menu == "⚙️ Data Preprocessing":
    preprocessing.show()

elif menu == "📊 EDA Analysis":
    eda.show()

elif menu == "📈 Sales Analysis":
    sales_analysis.show()

elif menu == "🌍 Region Analysis":
    region_analysis.show()

elif menu == "🤖 Model Training":
    model_training.show()

elif menu == "🔮 Forecasting":
    forecasting.show()

elif menu == "📦 Inventory Intelligence":
    inventory.show()

elif menu == "📑 Reports":
    reports.show()

elif menu == "🎯 KPI Tracking":
    kpi_tracking.show()

elif menu == "💡 Recommendations":
    recommendations.show()

elif menu == "📊 Executive Dashboard":
    dashboard.show()

# ==========================================
# LOGOUT
# ==========================================

st.sidebar.divider()

