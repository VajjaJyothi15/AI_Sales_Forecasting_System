import sqlite3

from database.db_connection import (
    get_connection
)


def create_user(
        username,
        password,
        role):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            password,
            role
        )
        VALUES
        (
            ?, ?, ?
        )
        """,
        (
            username,
            password,
            role
        )
    )

    conn.commit()

    conn.close()