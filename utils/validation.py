import pandas as pd
import numpy as np


def get_missing_values(df):

    return df.isnull().sum()


def get_duplicate_rows(df):

    return df.duplicated().sum()


def detect_outliers(df, column):

    Q1 = df[column].quantile(0.25)

    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    outliers = df[

        (df[column] < Q1 - 1.5 * IQR)

        |

        (df[column] > Q3 + 1.5 * IQR)

    ]

    return outliers


def validate_dates(df, date_column):

    invalid_dates = []

    for value in df[date_column]:

        try:

            pd.to_datetime(value)

        except:

            invalid_dates.append(value)

    return invalid_dates