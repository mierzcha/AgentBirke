import time
import csv
import threading
from dataclasses import dataclass
from pathlib import Path
from src.led.led_output import LEDOutput

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LED_EFFECT_DIRECTORY = PROJECT_ROOT / "config" / "led_effects"

@dataclass(frozen=True)
class LEDFrame:
    """Contains the LED values of one animation frame."""
    frame: int
    duration_ms: int
    # list of rgb value-tuples for leds
    leds: list[tuple[int, int, int]]

@dataclass(frozen=True)
class LEDEffect:
    """Contains all frames belonging to one LED effect."""
    name: str
    frames: list[LEDFrame]

class LedController:
    """Controlls LED effects of Agent Birke. Colors of the LEDs are dependent on the hci value engagement"""
    # animation csv files have this format (one line per frame for animations)
    REQUIRED_COLUMNS = {"frame", "duration_ms", "led", "r", "g", "b"}
    def __init__(self, led_config: dict, output: LEDOutput):
        self._stop_event = threading.Event()
        self._effect_thread = None
        self.led_config = led_config
        self.output = output
        led_settings = self.led_config["led"]
        self.led_count = led_settings["count"]
        self.effects_config = led_settings["effects"]

    def load_effect(self, effect_name: str) -> LEDEffect:
        """Load and validate an LED effect from its configured CSV file."""
        if effect_name not in self.effects_config:
            raise ValueError(f"LED effect '{effect_name}' is not configured.")
        effect_config = self.effects_config[effect_name]
        if not effect_config["enabled"]:
            raise ValueError(f"LED effect '{effect_name}' is disabled.")
        filename = effect_config["file"]
        file_path = LED_EFFECT_DIRECTORY / filename
        if not file_path.exists():
            raise FileNotFoundError(f"LED effect file not found: {file_path}")
        frames = self._load_csv(file_path)
        return LEDEffect(name=effect_name, frames=frames)

    def _load_csv(self, file_path: Path) -> list[LEDFrame]:
        """Load all animation frames from a CSV file. Validate the settings."""
        with open(file_path, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                raise ValueError(f"LED effect file '{file_path}' has no header.")
            missing_columns = self.REQUIRED_COLUMNS - set(reader.fieldnames)
            if missing_columns:
                raise ValueError(f"LED effect file '{file_path}' is missing columns: {sorted(missing_columns)}")
            rows = list(reader)
        if not rows:
            raise ValueError(f"LED effect file '{file_path}' contains no data.")
        grouped_frames: dict[int, list[dict]] = {}
        for row in rows:
            frame_number = self._parse_int(row["frame"], "frame", file_path)
            grouped_frames.setdefault(frame_number, []).append(row)
        frames = []
        for frame_number in sorted(grouped_frames):
            frame_rows = grouped_frames[frame_number]
            duration_values = {self._parse_int(row["duration_ms"], "duration_ms", file_path) for row in frame_rows}
            if len(duration_values) != 1:
                raise ValueError(f"Frame {frame_number} in '{file_path}' has different duration values.")
            duration_ms = duration_values.pop()
            if duration_ms <= 0:
                raise ValueError(f"Frame {frame_number} in '{file_path}' has an invalid duration: {duration_ms} ms.")
            leds = [None] * self.led_count
            for row in frame_rows:
                led_number = self._parse_int(row["led"], "led", file_path)
                if not 0 <= led_number < self.led_count:
                    raise ValueError(f"LED index {led_number} in '{file_path}' is outside the valid "
                        f"range 0-{self.led_count - 1}.")
                if leds[led_number] is not None:
                    raise ValueError(f"LED {led_number} occurs more than once in frame {frame_number}.")
                red = self._parse_rgb(row["r"], "r", file_path)
                green = self._parse_rgb(row["g"], "g", file_path)
                blue = self._parse_rgb(row["b"], "b", file_path)
                leds[led_number] = (red, green, blue)
            missing_leds = [index for index, value in enumerate(leds) if value is None]
            if missing_leds:
                raise ValueError(f"Frame {frame_number} in '{file_path}' is missing LED values for: {missing_leds}")
            frames.append(LEDFrame(frame=frame_number, duration_ms=duration_ms, leds=leds))
        return frames

    @staticmethod
    def _parse_int(value: str, field_name: str, file_path: Path) -> int:
        """Parse an integer value from the CSV."""
        try:
            return int(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid integer for '{field_name}' in '{file_path}': {value!r}") from error

    @staticmethod
    def _parse_rgb(value: str, channel: str, file_path: Path) -> int:
        """Parse and validate one RGB channel."""
        try:
            rgb_value = int(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid RGB value for '{channel}' in '{file_path}': {value!r}") from error
        if not 0 <= rgb_value <= 255:
            raise ValueError(f"RGB value for '{channel}' in '{file_path}' must be between 0 and 255: {rgb_value}")
        return rgb_value

    def get_effect_names(self) -> list[str]:
        """Return the names of all configured LED effects."""
        return list(self.effects_config.keys())

    def is_effect_enabled(self, effect_name: str) -> bool:
        """Return whether an LED effect is enabled."""
        if effect_name not in self.effects_config:
            return False
        return self.effects_config[effect_name]["enabled"]

    def set_leds(self, leds: list[tuple[int, int, int]]) -> None:
        """Set the RGB values of all LEDs"""
        if len(leds) != self.led_count:
            raise ValueError(f"Expected {self.led_count} LEDs, got {len(leds)}.")
        self.output.set_leds(leds)
        
    def stop_effect(self) -> None:
        """Stop the currently running LED effect."""
        self._stop_event.set()
    
    def play_effect(self, effect_name: str) -> None:
        """Start an animated LED effect inside a thread"""
        if self._effect_thread is not None and self._effect_thread.is_alive():
            self.stop_effect()
        effect = self.load_effect(effect_name)
        self._stop_event.clear()
        self._effect_thread = threading.Thread(target=self._run_effect, args=(effect,), daemon=True)
        self._effect_thread.start()
        
    def _run_effect(self, effect: LEDEffect) -> None:
        """Run LED Effect frame by frame"""
        for frame in effect.frames:
            if self._stop_event.is_set():
                break
            self.output.set_leds(frame.leds)
            if self._stop_event.wait(frame.duration_ms / 1000):
                break