import pandas as pd

from utils.column_mapper import standardize_columns


def _forecast_values(forecast_df):
    if forecast_df is None or forecast_df.empty:
        return None

    if "yhat" in forecast_df.columns:
        return pd.to_numeric(forecast_df["yhat"], errors="coerce").dropna()

    if "Forecast" in forecast_df.columns:
        return pd.to_numeric(forecast_df["Forecast"], errors="coerce").dropna()

    return None


def generate_recommendations(df, forecast_df=None):
    df = standardize_columns(df)

    recommendations = []

    sales = pd.to_numeric(df["Sales"], errors="coerce").fillna(0)
    profit = pd.to_numeric(df["Profit"], errors="coerce").fillna(0)
    inventory = pd.to_numeric(df["Inventory"], errors="coerce").fillna(0)

    avg_inventory = inventory.mean()

    if avg_inventory < 100:
        recommendations.append("Increase stock coverage for fast-moving products.")
    elif avg_inventory > 500:
        recommendations.append("Review slow-moving inventory and plan markdowns or bundles.")
    else:
        recommendations.append("Inventory levels are broadly healthy.")

    if sales.sum() > 0:
        profit_margin = (profit.sum() / sales.sum()) * 100

        if profit_margin < 10:
            recommendations.append("Improve margins by reviewing discounts, pricing, and supplier costs.")
        else:
            recommendations.append("Maintain current pricing discipline; profit margin is stable.")

    if "Product_Name" in df.columns:
        product_sales = df.groupby("Product_Name")["Sales"].sum().sort_values(ascending=False)

        if not product_sales.empty:
            recommendations.append(
                f"Prioritize marketing and availability for top product: {product_sales.index[0]}."
            )

    if "Region" in df.columns:
        region_sales = df.groupby("Region")["Sales"].sum().sort_values()

        if len(region_sales) > 1:
            recommendations.append(
                f"Investigate low-performing region: {region_sales.index[0]}."
            )

    if "Order_Date" in df.columns and len(df) >= 4:
        trend_df = df.copy()
        trend_df["Order_Date"] = pd.to_datetime(trend_df["Order_Date"], errors="coerce")
        trend_df = trend_df.dropna(subset=["Order_Date"]).sort_values("Order_Date")

        if len(trend_df) >= 4:
            midpoint = len(trend_df) // 2
            previous_sales = trend_df.iloc[:midpoint]["Sales"].sum()
            current_sales = trend_df.iloc[midpoint:]["Sales"].sum()

            if current_sales < previous_sales:
                recommendations.append("Sales are declining in the latest period; launch retention campaigns and review lost-demand causes.")
            else:
                recommendations.append("Recent sales momentum is positive; protect stock and campaign budget for winning segments.")

    forecast_values = _forecast_values(forecast_df)

    if forecast_values is not None and len(forecast_values) >= 2:
        if forecast_values.iloc[-1] > forecast_values.iloc[0]:
            recommendations.append("Forecast is rising; prepare inventory and staffing for higher demand.")
        else:
            recommendations.append("Forecast is softening; control purchase orders and focus on conversion campaigns.")

    return recommendations
