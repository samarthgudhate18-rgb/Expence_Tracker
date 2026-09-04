import sqlite3
from pathlib import Path


DATABASE = Path(__file__).resolve().parent.parent / "expenses.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT
""")

    connection.commit()
    connection.close()


def add_date_column():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("ALTER TABLE expenses ADD COLUMN date TEXT")
        connection.commit()
    except sqlite3.OperationalError:
        pass

    connection.close()


if __name__ == "__main__":
    create_table()
    add_date_column()