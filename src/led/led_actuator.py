from src.actuation.actuator import Actuator
from src.led.led_controller import LedController

class LEDActuator(Actuator):
    """LED Actuator Class"""
    def __init__(self, led_controller: LedController):
        self.led_controller=led_controller

    def execute(self, action: str, **parameters) -> None:
        """Execute an actuator-specific action."""
        if action == "play_effect":
            effect_name = parameters["effect_name"]
            self.led_controller.play_effect(effect_name)
        else:
            raise ValueError(f"Unsupported LED action: '{action}'.")

    def stop(self) -> None:
        """Stop the currently running actuator action."""
        self.led_controller.stop_effect()
