import pandas as pd


def remove_nulls(df):

    return df.dropna()


def fill_missing_values(df):

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    df[numeric_cols] = (
        df[numeric_cols]
        .fillna(
            df[numeric_cols]
            .mean()
        )
    )

    return df


def remove_duplicates(df):

    return df.drop_duplicates()


def feature_engineering(df):

    # Revenue

    if (
        "Quantity" in df.columns
        and
        "Unit_Price" in df.columns
    ):

        df["Revenue"] = (

            df["Quantity"]

            *

            df["Unit_Price"]
        )

    # Profit Margin

    if (
        "Profit" in df.columns
        and
        "Sales" in df.columns
    ):

        df["Profit_Margin"] = (

            df["Profit"]

            /

            df["Sales"]

        ) * 100

    # Inventory Turnover

    if (
        "Sales" in df.columns
        and
        "Inventory" in df.columns
    ):

        df["Inventory_Turnover"] = (

            df["Sales"]

            /

            df["Inventory"]
        )

    return df