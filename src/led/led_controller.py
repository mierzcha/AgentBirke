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
    
@dataclass(frozen=True)
class HCIColorPoint:
    """Defines one color point of an HCI color scale."""
    engagement: int
    color: tuple[int, int, int]

class LedController:
    """Controlls LED effects of Agent Birke. Colors of the LEDs are dependent on the hci value engagement"""
    # animation csv files have this format (one line per frame for animations)
    REQUIRED_COLUMNS = {"frame", "duration_ms", "led", "r", "g", "b"}
    def __init__(self, led_config: dict, hci_config: dict, output: LEDOutput):
        self._stop_event = threading.Event()
        self._effect_thread = None
        self.led_config = led_config
        self.hci_config = hci_config
        self.output = output
        led_settings = self.led_config["led"]
        self.led_count = led_settings["count"]
        engagement_config = self.hci_config["hci"]["engagement"]
        self.engagement_min = engagement_config["min"]
        self.engagement_max = engagement_config["max"]
        self.effects_config = led_settings["effects"]
        self.hci_scale_config = led_settings["hci_scale"]
        self.hci_scales = self._load_hci_scales()

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
       
    def _load_hci_scales(self) -> dict[str, list[HCIColorPoint]]:
        """Load and validate all HCI color scales."""
        if not self.hci_scale_config["enabled"]:
            return {}
        filename = self.hci_scale_config["file"]
        file_path = LED_EFFECT_DIRECTORY / filename
        if not file_path.exists():
            raise FileNotFoundError(f"HCI scale file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                raise ValueError(f"HCI scale file '{file_path}' has no header.")
            required_columns = {"scale", "engagement", "r", "g", "b"}
            missing_columns = (required_columns - set(reader.fieldnames))
            if missing_columns:
                raise ValueError(f"HCI scale file '{file_path}' is missing columns: {sorted(missing_columns)}")
            scales: dict[str, list[HCIColorPoint]] = {}
            for row in reader:
                scale_name = row["scale"].strip()
                if not scale_name:
                    raise ValueError(f"HCI scale file '{file_path}' contains an empty scale name.")
                engagement = self._parse_int(row["engagement"],"engagement",file_path)
                engagement = self.validate_engagement(engagement)
                red = self._parse_rgb(row["r"],"r",file_path)
                green = self._parse_rgb(row["g"],"g",file_path)
                blue = self._parse_rgb(row["b"],"b",file_path)
                scales.setdefault(scale_name,[]).append(HCIColorPoint(engagement=engagement,color=(red, green, blue)))
            if not scales:
                raise ValueError(f"HCI scale file '{file_path}' contains no data.")
        for scale_name, points in scales.items():
            points.sort(key=lambda point: point.engagement)
            if len(points) < 2:
                raise ValueError(f"HCI scale '{scale_name}' needs at least two color points.")
            engagements = [point.engagement for point in points]
            if len(engagements) != len(set(engagements)):
                raise ValueError(f"HCI scale '{scale_name}' contains duplicate engagement values.")
        return scales

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

    def validate_engagement(self, engagement: int) -> int:
        """Validate and clamp an engagement value."""
        return max(self.engagement_min, min(engagement, self.engagement_max))
        
    def set_leds(self, leds: list[tuple[int, int, int]]) -> None:
        """Set the RGB values of all LEDs"""
        if len(leds) != self.led_count:
            raise ValueError(f"Expected {self.led_count} LEDs, got {len(leds)}.")
        self.output.set_leds(leds)

    def set_engagement(self, engagement: int) -> None: 
        """Set the LED color on a green to red scale according to the current engagement"""
        color = self.get_engagement_color(engagement)
        leds = [color] * self.led_count
        self.set_leds(leds)
        
    def get_engagement_color(self, engagement: int, scale: str | None = None) -> tuple[int, int, int]:
        """Return the RGB color for the given engagement."""
        engagement = self.validate_engagement(engagement)
        if not self.hci_scales:
            raise ValueError("No HCI color scales are configured.")
        if scale is None:
            scale = self.hci_scale_config["default_scale"]
        if scale not in self.hci_scales:
            raise ValueError(f"HCI color scale '{scale}' is not configured.")
        points = self.hci_scales[scale]
        if engagement <= points[0].engagement:
            return points[0].color
        if engagement >= points[-1].engagement:
            return points[-1].color
        for first, second in zip(points, points[1:]):
            if (first.engagement <= engagement <= second.engagement):
                distance = (second.engagement - first.engagement)
                position = (engagement - first.engagement) / distance
                red = int(first.color[0] + (second.color[0] - first.color[0]) * position)
                green = int(first.color[1] + (second.color[1] - first.color[1]) * position)
                blue = int(first.color[2] + (second.color[2] - first.color[2]) * position)
                return red, green, blue
        raise ValueError(f"Could not determine color for engagement {engagement}.")
        
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