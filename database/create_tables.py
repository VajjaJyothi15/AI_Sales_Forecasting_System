from database.db_connection import (
    get_connection
)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # SALES DATA
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales_data(

            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
        """
    )

    # =========================
    # FORECAST RESULTS
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS forecast_results(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            model_name TEXT,

            forecast_date TEXT,

            predicted_sales REAL
        )
        """
    )

    # =========================
    # INVENTORY ANALYSIS
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory_analysis(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            product_name TEXT,

            inventory INTEGER,

            reorder_point REAL,

            safety_stock REAL
        )
        """
    )

    # =========================
    # MODEL RESULTS
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS model_results(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            model_name TEXT,

            mae REAL,

            mse REAL,

            rmse REAL,

            r2 REAL
        )
        """
    )

    # =========================
    # REPORTS
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reports(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            report_name TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()

