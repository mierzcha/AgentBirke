import json
from pathlib import Path


CONFIG_PATH = Path("config/rules.json")


class RuleEvaluator:
    """Evaluates environmental signals using configurable rules."""

    def __init__(self, config_path: Path = CONFIG_PATH):
        self.rules = self._load_rules(config_path)

    def _load_rules(self, config_path: Path) -> dict:
        """Load the rules from a JSON configuration file."""

        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def evaluate(
        self,
        soil_moisture: int,
        temperature: int,
        uv: int,
    ) -> list[str]:
        """Return all environmental conditions that currently apply."""

        conditions = []

        soil_rules = self.rules["soil_moisture"]

        if soil_moisture < soil_rules["thirsty_below"]:
            conditions.append("Thirsty")

        if soil_moisture > soil_rules["drowning_above"]:
            conditions.append("Drowning")

        temperature_rules = self.rules["temperature"]

        if temperature < temperature_rules["too_cold_below"]:
            conditions.append("Too_Cold")

        if temperature > temperature_rules["too_hot_above"]:
            conditions.append("Too_Hot")

        uv_rules = self.rules["uv"]

        if uv < uv_rules["too_dark_below"]:
            conditions.append("Too_Dark")

        if uv > uv_rules["too_bright_above"]:
            conditions.append("Too_Bright")

        if not conditions:
            conditions.append("Happy")

        return conditions
