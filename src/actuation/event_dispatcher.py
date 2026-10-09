from src.actuation.actuator import Actuator

class EventDispatcher:
    """Dispatch events to registered actuators."""
    def __init__(self) -> None:
        self._actuators: dict[str, Actuator] = {}

    def register(self, name: str, actuator: Actuator) -> None:
        """Register an actuator under a unique name."""
        if name in self._actuators:
            raise ValueError(f"An actuator named '{name}' is already registered.")
        self._actuators[name] = actuator

    def dispatch(self, actuator_name: str, action: str, **parameters) -> None:
        """Dispatch an action to a registered actuator."""
        actuator = self._actuators.get(actuator_name)
        if actuator is None:
            raise ValueError(f"No actuator named '{actuator_name}' is registered.")
        actuator.execute(action, **parameters)

    def stop(self, actuator_name: str) -> None:
        """Stop a registered actuator."""
        actuator = self._actuators.get(actuator_name)
        if actuator is None:
            raise ValueError(f"No actuator named '{actuator_name}' is registered.")
        actuator.stop()
