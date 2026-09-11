import subprocess
from pathlib import Path


class PiperClient:
    """Generates speech from text using Piper TTS."""

    def __init__(
        self,
        model_path: str,
        output_directory: str = "data/audio",
    ):
        self.model_path = Path(model_path)
        self.output_directory = Path(output_directory)

    def generate(self, text: str, output_filename: str) -> Path:
        """Convert text into a WAV file using Piper."""

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            self.output_directory
            / output_filename
        )

        subprocess.run(
            [
                "piper",
                "--model",
                str(self.model_path),
                "--output_file",
                str(output_path),
            ],
            input=text,
            text=True,
            check=True,
        )

        return output_path