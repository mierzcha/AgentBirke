from dataclasses import dataclass

@dataclass
class EnvironmentState:
    uv: int
    temperature: int
    soil_moisture: int