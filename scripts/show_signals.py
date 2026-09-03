import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/database/signals.db")


connection = sqlite3.connect(DATABASE_PATH)

rows = connection.execute(
    """
    SELECT id, uv, temperature, soil_moisture, touch, state, time
    FROM signals
    ORDER BY id DESC
    """
).fetchall()

connection.close()


print("Signalspeicher:")
print("-" * 80)

for row in rows:
    print(
        f"ID: {row[0]} | "
        f"UV-Index: {row[1]} | "
        f"Temperatur: {row[2]} °C | "
        f"Bodenfeuchtigkeit: {row[3]} % | "
        f"Touch: {bool(row[4])} | "
        f"State: {row[5]} | "
        f"Time: {row[6]}"
    )
