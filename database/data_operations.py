import pandas as pd

from database.db_connection import (
    get_connection
)


# --------------------
# SALES DATA
# --------------------

def save_sales_data(df):

    conn = get_connection()

    df.to_sql(
        "sales_data",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()


def get_sales_data():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM sales_data",
        conn
    )

    conn.close()

    return df


# --------------------
# FORECAST DATA
# --------------------

def save_forecast_results(df):

    conn = get_connection()

    df.to_sql(
        "forecast_results",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()


def get_forecast_results():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM forecast_results
        """,
        conn
    )

    conn.close()

    return df


# --------------------
# MODEL RESULTS
# --------------------

def save_model_results(df):

    conn = get_connection()

    df.to_sql(
        "model_results",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()


def get_model_results():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM model_results
        """,
        conn
    )

    conn.close()

    return df