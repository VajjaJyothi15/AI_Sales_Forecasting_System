import pandas as pd
from utils.column_mapper import clean_column_name


def find_col(df, keywords):
    for col in df.columns:
        for key in keywords:
            if clean_column_name(key) in clean_column_name(col):
                return col
    return None


def safe_sum(df, keywords):
    col = find_col(df, keywords)
    if col:
        values = (
            df[col]
            .astype(str)
            .str.replace(r"[\s,₹$£€%]", "", regex=True)
        )
        return pd.to_numeric(values, errors="coerce").fillna(0).sum()
    return 0


def safe_col(df, keywords):
    return find_col(df, keywords)
