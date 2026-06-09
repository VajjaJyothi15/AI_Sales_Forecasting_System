from database.db_connection import (
    get_connection
)

conn = get_connection()

cursor = conn.cursor()

cursor.execute(
    """
    INSERT OR IGNORE INTO users
    (
        username,
        password,
        role
    )
    VALUES
    (
        'admin',
        'admin123',
        'Admin'
    )
    """
)

conn.commit()

conn.close()

print(
    "Admin User Created"
)