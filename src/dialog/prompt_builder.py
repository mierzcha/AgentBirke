import json
from pathlib import Path
from src.agent.context import AgentContext

CONFIG_PATH = Path("config/rules.json")

class PromptBuilder:
    """Builds the prompt that is sent to the language model."""

    def __init__(self, config_path: Path = CONFIG_PATH):
        """Load condition descriptions from the JSON configuration file."""
        self.rules = self._load_rules(config_path)

    def _load_rules(self, config_path: Path) -> dict:
        """Load the rules from a JSON configuration file."""
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _build_condition_description(self, conditions: list[str]) -> str:
        """Build a description from the currently active conditions."""
        configured_conditions = self.rules["conditions"]
        descriptions = []
        for condition_label in conditions:
            for condition in configured_conditions.values():
                if condition["label"] == condition_label:
                    descriptions.append(condition["description"])
                    break
        if not descriptions:
            return ""
        return " ".join(descriptions)

    def build(self,user_input: str, context: AgentContext, dialog_history: list[dict[str, str]]) -> str:
        """Build a complete prompt for the language model."""
        if context.dialog_state.value == "Greeting":
            task_description = """
Der Nutzer hat die Interaktion begonnen und ein neues Gespräch
beginnt.

Begrüße den Nutzer freundlich.

Die Begrüßung soll nur aus einer kurzen Begrüßung bestehen.
Beginne keine weiteren Gesprächsthemen und beantworte noch keine
inhaltliche Frage.

Verwende den bisherigen Gesprächsverlauf nicht für die Begrüßung.
"""
        elif context.dialog_state.value == "Dialogue_active":
            task_description = """
Das Gespräch mit dem Nutzer ist bereits aktiv.

Beantworte die aktuelle Nutzereingabe direkt und passend.

Begrüße den Nutzer NICHT erneut.
Beginne deine Antwort NICHT mit "Hallo" oder einer anderen
Begrüßung.

Lasse die Angabe, aus welcher Wissensbasis dein Wissen stammt
(wie etwa "[1]") weg.

Berücksichtige den bisherigen Gesprächsverlauf. Informationen,
die der Nutzer im bisherigen Gespräch genannt hat, dürfen in
späteren Antworten verwendet werden.
"""
        elif context.dialog_state.value == "Goodbye":
            task_description = """
Das Gespräch mit dem Nutzer wird beendet.

Verabschiede dich freundlich und kurz vom Nutzer.

Beginne kein neues Gesprächsthema und stelle keine weitere Frage.
"""
        else:
            task_description = """
Es findet aktuell kein aktives Gespräch statt.

Antworte nur, wenn eine Antwort in diesem Zustand erforderlich ist.
"""
        condition_description = self._build_condition_description(context.conditions)
        conversation = ""
        for message in dialog_history:
            conversation += (
                f"{message['speaker']}: {message['text']}\n"
            )
        if not conversation:
            conversation = "Noch kein bisheriger Gesprächsverlauf."
            
        # Building the full prompt
        prompt = f"""
Du bist Agent Birke, eine freundliche künstliche Birke.

Du führst natürliche und kurze Gespräche mit einem Nutzer.
Antworte freundlich und verständlich.

Aktuelle Umweltwerte:
- UV-Index: {context.environment.uv}
- Temperatur: {context.environment.temperature} °C
- Bodenfeuchtigkeit: {context.environment.soil_moisture} %

{condition_description}

Bisheriger Gesprächsverlauf:
{conversation}

Aktuelle Nutzereingabe:
{user_input}

{task_description}

Formuliere jetzt nur die Antwort von Agent Birke.
"""
        return prompt.strip()