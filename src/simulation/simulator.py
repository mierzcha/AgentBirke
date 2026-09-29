from datetime import datetime
from src.signals.models import Signal
from src.signals.repository import SignalRepository
from .events import EnvironmentState
import json
from pathlib import Path

class EnvironmentSimulator:
    """Simulates environmental and interaction signals."""
    def __init__(self, repository: SignalRepository):
        self.repository = repository
        config_path = Path("config/simulation.json")
        with open(config_path, "r", encoding="utf-8") as file:
            config = json.load(file)
        self.state = EnvironmentState(uv=config["uv"]["default"],
            temperature=config["temperature"]["default"],
            soil_moisture=config["soil_moisture"]["default"])

    def set_uv(self, value: int):
        """Set the simulated UV value."""
        self.state.uv = value

    def set_temperature(self, value: int):
        """Set the simulated temperature."""
        self.state.temperature = value

    def set_soil_moisture(self, value: int):
        """Set the simulated soil moisture."""
        self.state.soil_moisture = value

    def save_state(self, dialog_state: str = "unknown"):
        """Save the current environment state to the Signalspeicher."""
        signal = Signal(
            uv=self.state.uv,
            temperature=self.state.temperature,
            soil_moisture=self.state.soil_moisture,
            state=dialog_state,
            time=datetime.now(),
        )
        self.repository.save(signal)