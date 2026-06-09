import streamlit as st
import plotly.express as px

from models.forecasting_models import prophet_forecast, lstm_forecast
from utils.column_mapper import standardize_columns


def _plot_forecast(forecast, model_type):
    if model_type == "Prophet":
        return px.line(
            forecast,
            x="ds",
            y="yhat",
            title="Prophet Forecast"
        )

    return px.line(
        forecast,
        x="Date",
        y="Forecast",
        title="LSTM Forecast"
    )


def show():
    st.title("Sales Forecasting")

    if "data" not in st.session_state:
        st.warning("Upload Dataset First")
        return

    df = standardize_columns(st.session_state["data"])
    st.session_state["data"] = df

    if df.empty:
        st.warning("Uploaded dataset has no rows to forecast.")
        return

    forecast_days = st.selectbox(
        "Forecast Horizon",
        [7, 30, 90, 180, 365]
    )

    model_type = st.selectbox(
        "Forecast Model",
        ["Prophet", "LSTM"]
    )

    if st.button("Generate Forecast"):
        try:
            if model_type == "Prophet":
                forecast = prophet_forecast(df, forecast_days)
                display_forecast = forecast.tail(forecast_days)
            else:
                forecast = lstm_forecast(df, forecast_days)
                display_forecast = forecast

            st.subheader("Forecast Results")
            st.dataframe(display_forecast, use_container_width=True)

            fig = _plot_forecast(forecast, model_type)
            st.plotly_chart(fig, use_container_width=True)

            if (
                model_type == "LSTM"
                and "Model" in forecast.columns
                and forecast["Model"].iloc[0] == "LSTM fallback"
            ):
                st.info(
                    "TensorFlow is not installed, so a neural fallback model was used. Install tensorflow to run the true LSTM model."
                )

            st.session_state["forecast_data"] = forecast
            st.session_state["forecast_model"] = model_type

            st.success("Forecast Generated Successfully")

        except Exception as e:
            st.error(str(e))
