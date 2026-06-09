import pandas as pd


def get_best_model(results_df):

    best = (

        results_df

        .sort_values(
            "R2",
            ascending=False
        )

        .iloc[0]
    )

    return best