from dataclasses import dataclass
from datetime import datetime


@dataclass
class Signal:
    """Represents one environmental or interaction signal."""

    uv: int
    temperature: int
    soil_moisture: int
    touch: bool
    state: str
    time: datetime
