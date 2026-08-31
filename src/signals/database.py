import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "database" / "signals.db"


def get_connection():
    """Create and return a connection to the Signalspeicher database."""
    return sqlite3.connect(DATABASE_PATH)


def init_database():
    """Create the signals table if it does not already exist."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uv INTEGER,
            temperature INTEGER,
            soil_moisture INTEGER,
            touch BOOLEAN,
            state TEXT,
            time DATETIME
        )
    """)

    connection.commit()
    connection.close()
