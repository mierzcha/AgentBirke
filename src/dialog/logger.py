from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_DIRECTORY = PROJECT_ROOT / "data" / "logs" / "dialogues"


class DialogueLogger:
    """Stores completed dialogues as text files."""

    def __init__(self, log_directory: Path = LOG_DIRECTORY):
        self.log_directory = log_directory

    def save_dialogue(
        self,
        dialog_history: list[dict[str, str]],
    ) -> Path | None:
        """Save one completed dialogue to a text file."""

        if not dialog_history:
            return None

        self.log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        file_path = (
            self.log_directory
            / f"dialogue_{timestamp}.txt"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "Dialog vom "
                + datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + "\n\n"
            )

            for message in dialog_history:

                file.write(
                    f"{message['speaker']}: "
                    f"{message['text']}\n"
                )

        return file_path
