import sqlite3
from pathlib import path

# Pfad zur Datenbank
PROJECT_ROOT = Path(__file__).resolve.parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" /"database" / "signals.db"

def init_database():
    """Erstellt Signalspeicher 'signals.db' und dessen Tabellen"""

    DATABASE_PATH.parent.mkdir(parents=True, exists_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uv INTEGER,
            temperature INTEGER,
            humidity INTEGER,
            touch BOOLEAN,
            state TEXT,
            time DATETIME
        )
    """)

    connection.commit()
    connection.close()

    print(f"Signalspeicher initialisiert: {DATABASE_PATH}")

def __name__ == "__main__":
    init_database()
