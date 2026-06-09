import pandas as pd

from database.db_connection import (
    get_connection
)


def insert_dataframe(
        table_name,
        df):

    conn = get_connection()

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    conn.close()


def fetch_all(table_name):

    conn = get_connection()

    query = (
        f"SELECT * FROM {table_name}"
    )

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    return df


def delete_record(
        table_name,
        record_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        f"""
        DELETE FROM {table_name}
        WHERE id=?
        """,
        (record_id,)
    )

    conn.commit()

    conn.close()