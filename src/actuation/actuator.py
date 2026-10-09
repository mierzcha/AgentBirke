
from abc import ABC, abstractmethod


class Actuator(ABC):
    """Abstract interface for actuators used by Agent Birke."""

    @abstractmethod
    def execute(self, action: str, **parameters) -> None:
        """Execute an actuator-specific action."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop the currently running actuator action."""
        pass
