from abc import ABC, abstractmethod

class LEDOutput(ABC):
    """Interface for hardware implementation"""
    @abstractmethod
    def set_leds(self, leds: list[tuple[int, int, int]]) -> None:
        """Set the RGB values of all LEDs"""

class MockLEDOutput(LEDOutput):
    """Mock implementation that prints the LED values"""
    def set_leds(self, leds: list[tuple[int, int, int]]) -> None:
        print(f"LED output: {leds}")