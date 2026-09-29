import json
import operator
from pathlib import Path

CONFIG_PATH = Path("config/rules.json")

class RuleEvaluator:
    """Evaluates environmental signals using configurable rules."""
    
    def __init__(self, config_path: Path = CONFIG_PATH):
         """Load the condition rules from the configuration file."""
         self.rules = self._load_rules(config_path)

    def _load_rules(self, config_path: Path) -> dict:
        """Load the rules from a JSON configuration file."""
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
            
    def _compare(self, value: int, op: str, threshold: int) -> bool:
        """Compare a value with a threshold using the configured operator."""
        operators = {
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge,
            "==": operator.eq,
            "!=": operator.ne,
        }
        if op not in operators:
            raise ValueError(f"Unsupported operator: {op}")
        return operators[op](value, threshold)

    def evaluate(self, soil_moisture: int, temperature: int, uv: int) -> list[str]:
        """Return all environmental conditions that currently apply."""
        environment = {
            "soil_moisture": soil_moisture,
            "temperature": temperature,
            "uv": uv,
        }
        active_conditions = []
        for condition in self.rules["conditions"].values():
            # The fallback condition "Happy" has no rule to evaluate.
            if "variable" not in condition:
                continue
                
            variable = condition["variable"]
            op = condition["op"]
            threshold = condition["threshold"]
            if variable not in environment:
                raise ValueError(f"Unknown environment variable: {variable}")

            value = environment[variable]
            if self._compare(value, op, threshold):
                active_conditions.append(condition["label"])

        if not active_conditions:
            active_conditions.append(
                self.rules["conditions"]["happy"]["label"]
            )

        return active_conditions