from datetime import datetime

from src.signals.models import Signal
from src.signals.repository import SignalRepository
from .events import EnvironmentState


class EnvironmentSimulator:
    """Simulates environmental and interaction signals."""

    def __init__(self, repository: SignalRepository):
        self.repository = repository

        self.state = EnvironmentState(
            uv=50,
            temperature=20,
            soil_moisture=70,
            touch=False,
        )

    def set_uv(self, value: int):
        """Set the simulated UV value."""
        self.state.uv = value

    def set_temperature(self, value: int):
        """Set the simulated temperature."""
        self.state.temperature = value

    def set_soil_moisture(self, value: int):
        """Set the simulated soil moisture."""
        self.state.soil_moisture = value

    def set_touch(self, value: bool):
        """Set the simulated touch state."""
        self.state.touch = value

    def save_state(self, dialog_state: str = "unknown"):
        """Save the current environment state to the Signalspeicher."""

        signal = Signal(
            uv=self.state.uv,
            temperature=self.state.temperature,
            soil_moisture=self.state.soil_moisture,
            touch=self.state.touch,
            state=dialog_state,
            time=datetime.now(),
        )

        self.repository.save(signal)
