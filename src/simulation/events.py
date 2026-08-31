from dataclasses import dataclass


@dataclass
class EnvironmentState:
    """Represents the current simulated environmental conditions."""

    uv: int
    temperature: int
    soil_moisture: int
    touch: bool
