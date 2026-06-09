from sklearn.metrics import (
    mean_absolute_error,
    r2_score
)


def forecast_accuracy(
        actual,
        predicted):

    mae = mean_absolute_error(
        actual,
        predicted
    )

    r2 = r2_score(
        actual,
        predicted
    )

    return {

        "MAE": round(mae, 2),

        "R2": round(r2, 4)
    }