from sklearn.ensemble import (
    RandomForestRegressor
)


def demand_prediction(
        X_train,
        y_train,
        X_future):

    model = RandomForestRegressor()

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_future
    )

    return predictions