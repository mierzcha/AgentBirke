from datetime import datetime

from .database import get_connection
from .models import Signal


class SignalRepository:
    """Provides access to stored environmental and interaction signals."""

    def save(self, signal: Signal) -> None:
        """Store a signal in the database."""

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO signals (
                uv,
                temperature,
                soil_moisture,
                touch,
                state,
                time
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                signal.uv,
                signal.temperature,
                signal.soil_moisture,
                signal.touch,
                signal.state,
                signal.time,
            ),
        )

        connection.commit()
        connection.close()

    def get_latest(self) -> Signal | None:
        """Return the most recently stored signal."""

        connection = get_connection()

        row = connection.execute(
            """
            SELECT uv, temperature, soil_moisture, touch, state, time
            FROM signals
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

        connection.close()

        if row is None:
            return None

        return Signal(
            uv=row[0],
            temperature=row[1],
            soil_moisture=row[2],
            touch=bool(row[3]),
            state=row[4],
            time=datetime.fromisoformat(row[5]),
        )

    def get_recent(self, limit: int = 10) -> list[Signal]:
        """Return the most recently stored signals."""
        connection = get_connection()

        rows = connection.execute(
            """
            SELECT uv, temperature, soil_moisture, touch, state, time
            FROM signals
            ORDER BY id DESC
            LIMIT ?
            """,
           (limit,),
        ).fetchall()

        connection.close()

        return [
            Signal(
                uv=row[0],
                temperature=row[1],
                soil_moisture=row[2],
                touch=bool(row[3]),
                state=row[4],
                time=datetime.fromisoformat(row[5]),
            )
        for row in rows
        ]
