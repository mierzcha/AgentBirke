import time

from src.agent.context import create_context
from src.rules.evaluator import RuleEvaluator
from src.signals.repository import SignalRepository
from src.simulation.events import EnvironmentState
from src.dialog.prompt_builder import PromptBuilder
from src.llm.client import OllamaClient
from src.tts.piper_client import PiperClient
from src.stt.whisper_client import WhisperClient


class DialogService:
    """Provides the core functions for processing a dialogue."""

    def __init__(
        self,
        repository: SignalRepository,
        rule_evaluator: RuleEvaluator,
        prompt_builder: PromptBuilder,
        ollama_client: OllamaClient,
        piper_client: PiperClient,
        whisper_client: WhisperClient,
    ):
        self.repository = repository
        self.rule_evaluator = rule_evaluator
        self.prompt_builder = prompt_builder
        self.ollama_client = ollama_client
        self.piper_client = piper_client
        self.whisper_client = whisper_client

    def get_environment(self) -> EnvironmentState:
        """Read the latest environment state from the Signalspeicher."""

        signal = self.repository.get_latest()

        if signal is None:

            return EnvironmentState(
                uv=3,
                temperature=20,
                soil_moisture=50,
                touch=False,
            )

        return EnvironmentState(
            uv=signal.uv,
            temperature=signal.temperature,
            soil_moisture=signal.soil_moisture,
            touch=signal.touch,
        )

    def create_agent_context(self, dialog_state):
        """Create the current context of Agent Birke."""

        environment = self.get_environment()

        conditions = self.rule_evaluator.evaluate(
            soil_moisture=environment.soil_moisture,
            temperature=environment.temperature,
            uv=environment.uv,
        )

        return create_context(
            dialog_state=dialog_state,
            environment=environment,
            conditions=conditions,
        )

    def generate_response(
        self,
        user_input: str,
        dialog_state,
        dialog_history: list[dict[str, str]],
    ):
        """Generate a text response and speech output."""

        start_time = time.perf_counter()

        context = self.create_agent_context(
            dialog_state
        )

        prompt = self.prompt_builder.build(
            user_input=user_input,
            context=context,
            dialog_history=dialog_history,
        )

        answer = self.ollama_client.generate(
            prompt
        )

        audio_path = self.piper_client.generate(
            text=answer,
            output_filename=(
                f"response_{int(time.time() * 1000)}.wav"
            ),
        )

        processing_time = (
            time.perf_counter() - start_time
        )

        return (
            answer,
            audio_path,
            processing_time,
            prompt,
        )

    def transcribe_audio(self, audio_input) -> str:
        """Transcribe an audio recording with Faster-Whisper."""

        audio_path = "data/audio/input.wav"

        with open(audio_path, "wb") as file:
            file.write(audio_input.getbuffer())

        text = self.whisper_client.transcribe(
            audio_path
        )

        return text.strip()