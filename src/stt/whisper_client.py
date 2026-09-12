from faster_whisper import WhisperModel


class WhisperClient:
    """Transcribes speech to text using Faster-Whisper."""

    def __init__(
        self,
        model_size: str = "base",
    ):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_path: str) -> str:
        """Transcribe an audio file and return the recognized text."""

        segments, info = self.model.transcribe(
            audio_path,
            language="de",
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()
