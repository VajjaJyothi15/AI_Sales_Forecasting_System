import pandas as pd
from utils.column_mapper import standardize_columns

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.linear_model import (
    LinearRegression
)

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

try:
    from xgboost import (
        XGBRegressor
    )
except:
    XGBRegressor = None


def train_models(df):
    df = standardize_columns(df)

    required = [
        "Quantity",
        "Unit_Price",
        "Inventory",
        "Sales"
    ]

    for col in required:

        if col not in df.columns:

            raise ValueError(
                f"{col} column missing"
            )

    if len(df) < 2:
        raise ValueError("At least 2 rows are required to train models")

    X = df[
        [
            "Quantity",
            "Unit_Price",
            "Inventory"
        ]
    ]

    y = df["Sales"]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )
    )

    models = {

        "Linear Regression":
        LinearRegression(),

        "Random Forest":
        RandomForestRegressor(
            n_estimators=100,
            random_state=42
        ),

        "Gradient Boosting":
        GradientBoostingRegressor(
            random_state=42
        )
    }

    if XGBRegressor:

        models["XGBoost"] = (

            XGBRegressor(
                random_state=42
            )
        )

    results = []

    trained_models = {}

    for name, model in models.items():

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        mse = mean_squared_error(
            y_test,
            predictions
        )

        rmse = mse ** 0.5

        r2 = r2_score(
            y_test,
            predictions
        )

        results.append({

            "Model": name,

            "MAE": round(mae, 2),

            "MSE": round(mse, 2),

            "RMSE": round(rmse, 2),

            "R2": round(r2, 4)
        })

        trained_models[name] = model

    results_df = pd.DataFrame(
        results
    )

    return (
        results_df,
        trained_models
    )
