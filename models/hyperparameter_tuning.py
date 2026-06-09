from sklearn.model_selection import (
    GridSearchCV
)

from sklearn.ensemble import (
    RandomForestRegressor
)


def tune_random_forest(
        X_train,
        y_train):

    params = {

        "n_estimators":
        [100, 200, 300],

        "max_depth":
        [5, 10, 15]
    }

    grid = GridSearchCV(

        RandomForestRegressor(),

        params,

        cv=3,

        scoring="r2"
    )

    grid.fit(
        X_train,
        y_train
    )

    return grid.best_estimator_