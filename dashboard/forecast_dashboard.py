import streamlit as st
import plotly.graph_objects as go

def forecast_dashboard(
        actual,
        forecast):

    st.subheader(
        "🔮 Sales Forecast"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=actual.index,
            y=actual.values,
            name="Actual Sales"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast.index,
            y=forecast.values,
            name="Forecast Sales"
        )
    )

    fig.update_layout(
        title="Sales Forecast"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )