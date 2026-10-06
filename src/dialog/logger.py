from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from src.dialog.states import DialogState
from src.agent.context import AgentContext

PROJECT_ROOT = Path(__file__).resolve().parents[2]

@dataclass
class InteractionSnapshot:
    """Contains all information belonging to one dialogue interaction."""
    dialog_state: DialogState
    engagement: int
    context: AgentContext
    prompt: str
    answer: str
    prompt_building_time: float
    llm_response_time: float
    tts_time: float
    processing_time: float
    user_input: str

class DialogueLogger:
    """Stores completed dialogues as text files."""
    def __init__(self, logging_config: dict):
        self.logging_config = logging_config
        directory = self.logging_config["dialogue_logging"]["directory"]
        self.log_directory = PROJECT_ROOT / directory

    def save_dialogue(self, dialog_history: list[dict[str, str]], interactions: list[InteractionSnapshot]) -> Path | None:
        """Save one completed dialogue including all interaction snapshots."""
        if not dialog_history:
            return None
        self.log_directory.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = self.log_directory / f"dialogue_{timestamp}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Dialog vom " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            sections = self.logging_config["dialogue_logging"]["sections"]
            for index, interaction in enumerate(interactions, start=1):
                file.write(f"Interaktion {index}\n\n")
                self._write_dialog_state(file, sections["dialog_state"], interaction)
                self._write_hci(file, sections["hci"], interaction)
                self._write_environment(file, sections["environment"], interaction)
                self._write_conditions(file, sections["conditions"], interaction)
                self._write_timings(file, sections["timings"], interaction)
                self._write_prompt(file, sections["prompt"], interaction)
                self._write_dialog(file, sections["dialog"], interaction)
                file.write("\n")
        return file_path

    @staticmethod
    def _write_dialog_state(file, config: dict, interaction: InteractionSnapshot) -> None:
        """Write the current dialogue state."""
        if not config["enabled"]:
            return
        file.write(f"[{config['title']}]\n")
        file.write(f"{interaction.dialog_state.value}\n\n")

    @staticmethod
    def _write_hci(file, config: dict, interaction: InteractionSnapshot) -> None:
        """Write HCI-related values."""
        if not config["enabled"]:
            return
        file.write(f"[{config['title']}]\n")
        file.write(f"Engagement: {interaction.engagement}\n\n")

    @staticmethod
    def _write_environment(file, config: dict, interaction: InteractionSnapshot) -> None:
        """Write the environment / signal values."""
        if not config["enabled"]:
            return
        environment = interaction.context.environment
        file.write(f"[{config['title']}]\n")
        file.write(f"UV-Index: {environment.uv}\n")
        file.write(f"Temperatur: {environment.temperature} °C\n")
        file.write(f"Bodenfeuchtigkeit: {environment.soil_moisture} %\n\n")

    @staticmethod
    def _write_conditions(file, config: dict, interaction: InteractionSnapshot) -> None:
        """Write the conditions derived from the environment."""
        if not config["enabled"]:
            return
        file.write(f"[{config['title']}]\n")
        if interaction.context.conditions:
            for condition in interaction.context.conditions:
                file.write(f"- {condition}\n")
        else:
            file.write("Keine Bedingungen.\n")
        file.write("\n")

    @staticmethod
    def _write_timings(file, config: dict, interaction: InteractionSnapshot) -> None:
        """Write processing times."""
        if not config["enabled"]:
            return
        file.write(f"[{config['title']}]\n")
        file.write(f"Prompt-Erstellung: {interaction.prompt_building_time:.4f} Sekunden\n")
        file.write(f"LLM-Antwort: {interaction.llm_response_time:.4f} Sekunden\n")
        file.write(f"Piper-Audio: {interaction.tts_time:.4f} Sekunden\n")
        file.write(f"Gesamt: {interaction.processing_time:.4f} Sekunden\n")
        file.write("\n")

    @staticmethod
    def _write_prompt(file, config: dict, interaction: InteractionSnapshot) -> None:
        """Write the generated prompt."""
        if not config["enabled"]:
            return
        file.write(f"[{config['title']}]\n")
        file.write(f"{interaction.prompt}\n\n")

    @staticmethod
    def _write_dialog(file, config: dict, interaction: InteractionSnapshot) -> None:
        """Write the actual user interaction and agent response."""
        if not config["enabled"]:
            return
        file.write(f"[{config['title']}]\n")
        file.write(f"Nutzer: {interaction.user_input}\n")
        file.write(f"Birke: {interaction.answer}\n\n")