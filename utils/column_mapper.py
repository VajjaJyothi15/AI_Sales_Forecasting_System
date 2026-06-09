import re

import pandas as pd


def clean_column_name(column):
    cleaned = str(column).strip().lower()
    cleaned = re.sub(r"[^0-9a-zA-Z]+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned


def get_column(df, keywords):
    """
    Automatically finds a column based on keywords
    Example: ["sales", "revenue", "amount"]
    """

    for col in df.columns:
        col_lower = clean_column_name(col)

        for key in keywords:
            if clean_column_name(key) in col_lower:
                return col

    return None


def _convert_numeric_like_columns(df):
    converted_df = df.copy()

    for col in converted_df.columns:
        if pd.api.types.is_numeric_dtype(converted_df[col]):
            continue

        cleaned = (
            converted_df[col]
            .astype(str)
            .str.replace(r"[\s,₹$£€%]", "", regex=True)
            .str.replace(r"^\((.*)\)$", r"-\1", regex=True)
        )
        converted = pd.to_numeric(cleaned, errors="coerce")
        original_non_empty = converted_df[col].notna().sum()

        if original_non_empty and converted.notna().sum() / original_non_empty >= 0.8:
            converted_df[col] = converted

    return converted_df


def standardize_columns(df):

    mapping = {
        "sales": ["sales", "revenue", "amount", "total_sales", "total_revenue", "net_sales"],
        "profit": ["profit", "earn", "margin", "income"],
        "quantity": ["quantity", "qty", "units", "items_sold", "order_quantity"],
        "region": ["region", "state", "country", "area", "market", "territory", "zone"],
        "inventory": ["inventory", "stock", "stock_level", "on_hand", "available_stock"],
        "product_name": ["product_name", "product", "item", "sku", "description"],
        "category": ["category", "segment", "department", "class"],
        "order_date": ["order_date", "date", "order_dt", "transaction_date", "sales_date"],
        "unit_price": ["unit_price", "price", "rate", "unit_cost", "selling_price"]
    }

    new_df = df.copy()
    new_df.columns = [clean_column_name(col) for col in new_df.columns]
    new_df = new_df.loc[:, ~pd.Index(new_df.columns).duplicated()].copy()
    new_df = _convert_numeric_like_columns(new_df)

    for standard_name, keywords in mapping.items():

        col = get_column(new_df, keywords)

        if col:
            new_df[standard_name] = new_df[col]

    numeric_source_cols = list(new_df.select_dtypes(include="number").columns)
    text_source_cols = [
        col
        for col in new_df.select_dtypes(exclude="number").columns
        if not any(key in clean_column_name(col) for key in ("date", "time", "day"))
    ]

    if "sales" not in new_df.columns:
        new_df["sales"] = new_df[numeric_source_cols[0]] if numeric_source_cols else 1

    if "profit" not in new_df.columns:
        new_df["profit"] = new_df[numeric_source_cols[1]] if len(numeric_source_cols) > 1 else 0

    if "quantity" not in new_df.columns:
        new_df["quantity"] = new_df[numeric_source_cols[2]] if len(numeric_source_cols) > 2 else 1

    if "inventory" not in new_df.columns:
        new_df["inventory"] = new_df[numeric_source_cols[3]] if len(numeric_source_cols) > 3 else 0

    if "unit_price" not in new_df.columns:
        new_df["unit_price"] = new_df[numeric_source_cols[4]] if len(numeric_source_cols) > 4 else new_df["sales"]

    if "product_name" not in new_df.columns:
        if text_source_cols:
            new_df["product_name"] = new_df[text_source_cols[0]].astype(str)
        else:
            new_df["product_name"] = [f"Row {idx + 1}" for idx in range(len(new_df))]

    if "category" not in new_df.columns:
        if len(text_source_cols) > 1:
            new_df["category"] = new_df[text_source_cols[1]].astype(str)
        else:
            new_df["category"] = "All"

    if "region" not in new_df.columns:
        if len(text_source_cols) > 2:
            new_df["region"] = new_df[text_source_cols[2]].astype(str)
        else:
            new_df["region"] = "All"

    if "order_date" not in new_df.columns:
        date_col = None
        for col in new_df.columns:
            if not any(key in clean_column_name(col) for key in ("date", "time", "day")):
                continue
            converted = pd.to_datetime(new_df[col], errors="coerce")
            if converted.notna().sum() > 0:
                date_col = col
                new_df["order_date"] = converted
                break

        if date_col is None:
            new_df["order_date"] = pd.date_range(
                start="2024-01-01",
                periods=len(new_df),
                freq="D"
            )

    numeric_columns = [
        "sales",
        "profit",
        "quantity",
        "inventory",
        "unit_price"
    ]

    for col in numeric_columns:
        if col in new_df.columns:
            new_df[col] = pd.to_numeric(new_df[col], errors="coerce").fillna(0)

    if "order_date" in new_df.columns:
        new_df["order_date"] = pd.to_datetime(new_df["order_date"], errors="coerce")

    compatibility_aliases = {
        "sales": "Sales",
        "profit": "Profit",
        "quantity": "Quantity",
        "inventory": "Inventory",
        "unit_price": "Unit_Price",
        "product_name": "Product_Name",
        "category": "Category",
        "region": "Region",
        "order_date": "Order_Date"
    }

    for source, alias in compatibility_aliases.items():
        if source in new_df.columns and alias not in new_df.columns:
            new_df[alias] = new_df[source]

    if "Product_Name" in new_df.columns and "Product" not in new_df.columns:
        new_df["Product"] = new_df["Product_Name"]

    return new_df
