import pandas as pd
import numpy as np
from utils.column_mapper import standardize_columns


def calculate_safety_stock(
        avg_demand,
        lead_time,
        service_factor=1.65):

    return (
        service_factor *
        np.sqrt(lead_time) *
        avg_demand
    )


def calculate_reorder_point(
        avg_demand,
        lead_time,
        safety_stock):

    return (
        avg_demand *
        lead_time
    ) + safety_stock


def calculate_eoq(
        annual_demand,
        ordering_cost,
        holding_cost):

    return np.sqrt(

        (
            2 *
            annual_demand *
            ordering_cost
        )

        /

        holding_cost
    )


def inventory_analysis(df):
    df = standardize_columns(df)

    avg_demand = (
        df["Quantity"]
        .mean()
    )

    lead_time = 7

    safety_stock = (
        calculate_safety_stock(
            avg_demand,
            lead_time
        )
    )

    reorder_point = (
        calculate_reorder_point(
            avg_demand,
            lead_time,
            safety_stock
        )
    )

    annual_demand = (
        df["Quantity"]
        .sum()
    )

    eoq = calculate_eoq(

        annual_demand,

        500,

        20
    )

    return {

        "Safety Stock":
        round(safety_stock, 2),

        "Reorder Point":
        round(reorder_point, 2),

        "EOQ":
        round(eoq, 2)
    }
