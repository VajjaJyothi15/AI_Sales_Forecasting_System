import pandas as pd
import numpy as np

try:
    from prophet import Prophet
except Exception:
    Prophet = None

from statsmodels.tsa.arima.model import ARIMA
from utils.column_mapper import standardize_columns


def prophet_forecast(df, periods=30):
    if Prophet is None:
        raise ValueError("Prophet is not installed. Install prophet or use LSTM forecasting.")

    df = standardize_columns(df)

    forecast_df = pd.DataFrame()

    forecast_df["ds"] = pd.to_datetime(
        df["Order_Date"]
    )

    forecast_df["y"] = df["Sales"]
    forecast_df = forecast_df.dropna()

    if len(forecast_df) < 2:
        raise ValueError("At least 2 valid dated rows are required for forecasting")

    model = Prophet()

    model.fit(forecast_df)

    future = model.make_future_dataframe(
        periods=periods
    )

    forecast = model.predict(future)

    return forecast[
        [
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]
    ]


def arima_forecast(df, periods=30):
    df = standardize_columns(df)

    sales = df["Sales"].dropna()

    if len(sales) < 3:
        raise ValueError("At least 3 rows are required for ARIMA forecasting")

    model = ARIMA(
        sales,
        order=(5,1,0)
    )

    fitted = model.fit()

    forecast = fitted.forecast(
        steps=periods
    )

    future_dates = pd.date_range(

        start=pd.to_datetime(
            df["Order_Date"]
        ).max(),

        periods=periods + 1,

        freq="D"
    )[1:]

    return pd.DataFrame({

        "Date": future_dates,

        "Forecast": forecast
    })


def _daily_sales(df):
    prepared = standardize_columns(df)

    daily = pd.DataFrame({
        "Date": pd.to_datetime(prepared["Order_Date"], errors="coerce"),
        "Sales": pd.to_numeric(prepared["Sales"], errors="coerce")
    }).dropna()

    if daily.empty:
        raise ValueError("At least one valid date and sales value is required for forecasting")

    daily = (
        daily.groupby("Date")["Sales"]
        .sum()
        .sort_index()
        .asfreq("D")
        .fillna(0)
    )

    return daily


def _windowed_training_data(values, window_size):
    X = []
    y = []

    for idx in range(window_size, len(values)):
        X.append(values[idx - window_size:idx])
        y.append(values[idx])

    return np.array(X), np.array(y)


def lstm_forecast(df, periods=30, window_size=14, epochs=30):
    sales = _daily_sales(df)

    if len(sales) < 4:
        raise ValueError("At least 4 dated rows are required for LSTM forecasting")

    window_size = min(window_size, max(2, len(sales) - 1))
    values = sales.values.astype(float)
    min_value = values.min()
    max_value = values.max()
    scale = max(max_value - min_value, 1)
    scaled = (values - min_value) / scale

    X, y = _windowed_training_data(scaled, window_size)

    if len(X) == 0:
        raise ValueError("Not enough rows to create LSTM training windows")

    method = "LSTM"

    try:
        from tensorflow.keras.layers import LSTM, Dense
        from tensorflow.keras.models import Sequential

        model = Sequential([
            LSTM(32, activation="tanh", input_shape=(window_size, 1)),
            Dense(1)
        ])
        model.compile(optimizer="adam", loss="mse")
        model.fit(X.reshape((X.shape[0], X.shape[1], 1)), y, epochs=epochs, verbose=0)

        history = list(scaled[-window_size:])
        predictions = []

        for _ in range(periods):
            x_input = np.array(history[-window_size:]).reshape((1, window_size, 1))
            next_value = float(model.predict(x_input, verbose=0)[0][0])
            next_value = min(max(next_value, 0), 1)
            history.append(next_value)
            predictions.append(next_value * scale + min_value)

    except Exception:
        from sklearn.neural_network import MLPRegressor

        method = "LSTM fallback"
        model = MLPRegressor(
            hidden_layer_sizes=(64, 32),
            max_iter=1000,
            random_state=42
        )
        model.fit(X, y)

        history = list(scaled[-window_size:])
        predictions = []

        for _ in range(periods):
            x_input = np.array(history[-window_size:]).reshape(1, -1)
            next_value = float(model.predict(x_input)[0])
            next_value = min(max(next_value, 0), 1)
            history.append(next_value)
            predictions.append(next_value * scale + min_value)

    future_dates = pd.date_range(
        start=sales.index.max(),
        periods=periods + 1,
        freq="D"
    )[1:]

    return pd.DataFrame({
        "Date": future_dates,
        "Forecast": predictions,
        "Model": method
    })
