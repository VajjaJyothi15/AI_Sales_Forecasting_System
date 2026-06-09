from utils.safe_columns import safe_sum, safe_col


def get_kpis(df):

    total_sales = safe_sum(df, ["sales", "revenue", "amount"])
    total_profit = safe_sum(df, ["profit", "earn"])

    region_col = safe_col(df, ["region", "state", "country"])
    inventory_col = safe_col(df, ["inventory", "stock"])
    product_col = safe_col(df, ["product", "item", "sku"])

    orders = len(df)
    products = df[product_col].nunique() if product_col else 0
    regions = df[region_col].nunique() if region_col else 0
    avg_order = total_sales / orders if orders else 0

    kpis = {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_records": len(df),
        "region_col": region_col,
        "inventory_col": inventory_col,
        "Sales": total_sales,
        "Profit": total_profit,
        "Orders": orders,
        "Products": products,
        "Regions": regions,
        "AvgOrder": avg_order
    }

    return kpis
