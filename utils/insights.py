import pandas as pd

from utils.column_mapper import standardize_columns


def _percent_change(current, previous):
    if previous == 0:
        return 100.0 if current > 0 else 0.0

    return ((current - previous) / previous) * 100


def _change_text(metric, name, current, previous):
    change = _percent_change(current, previous)
    direction = "increased" if change >= 0 else "decreased"

    return (
        f"{metric} {direction} {abs(change):.1f}% in {name} "
        f"(current Rs. {current:,.0f}, previous Rs. {previous:,.0f})."
    )


def _split_recent_period(df):
    work = df.copy()
    work["Order_Date"] = pd.to_datetime(work["Order_Date"], errors="coerce")
    work = work.dropna(subset=["Order_Date"])

    if len(work) < 2:
        return None, None

    midpoint = work["Order_Date"].min() + (
        work["Order_Date"].max() - work["Order_Date"].min()
    ) / 2

    previous = work[work["Order_Date"] <= midpoint]
    current = work[work["Order_Date"] > midpoint]

    if previous.empty or current.empty:
        return None, None

    return current, previous


def _group_change_insights(current, previous, group_col, metric_col="Sales", limit=3):
    current_group = current.groupby(group_col)[metric_col].sum()
    previous_group = previous.groupby(group_col)[metric_col].sum()
    all_groups = current_group.index.union(previous_group.index)

    changes = []

    for group in all_groups:
        current_value = float(current_group.get(group, 0))
        previous_value = float(previous_group.get(group, 0))
        changes.append((
            abs(_percent_change(current_value, previous_value)),
            _change_text("Sales", group, current_value, previous_value)
        ))

    return [
        text
        for _, text in sorted(changes, reverse=True)[:limit]
    ]


def generate_insights(df):
    df = standardize_columns(df)

    insights = []

    total_sales = float(pd.to_numeric(df["Sales"], errors="coerce").fillna(0).sum())
    total_profit = float(pd.to_numeric(df["Profit"], errors="coerce").fillna(0).sum())

    insights.append(f"Total revenue generated: Rs. {total_sales:,.0f}.")
    insights.append(f"Total profit generated: Rs. {total_profit:,.0f}.")

    if "Region" in df.columns and not df.empty:
        region_sales = df.groupby("Region")["Sales"].sum()
        top_region = region_sales.idxmax()
        insights.append(f"Top performing region: {top_region}.")

    if "Product_Name" in df.columns and not df.empty:
        product_sales = df.groupby("Product_Name")["Sales"].sum()
        top_product = product_sales.idxmax()
        insights.append(f"Best selling product: {top_product}.")

    current, previous = _split_recent_period(df)

    if current is not None and previous is not None:
        insights.append(
            _change_text(
                "Overall sales",
                "the latest period",
                float(current["Sales"].sum()),
                float(previous["Sales"].sum())
            )
        )

        if "Region" in df.columns:
            insights.extend(_group_change_insights(current, previous, "Region"))

        if "Product_Name" in df.columns:
            insights.extend(_group_change_insights(current, previous, "Product_Name", limit=2))

    return insights
