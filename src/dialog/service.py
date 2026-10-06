import time
from src.agent.context import create_context
from src.rules.evaluator import RuleEvaluator
from src.signals.repository import SignalRepository
from src.simulation.events import EnvironmentState
from src.dialog.prompt_builder import PromptBuilder
from src.llm.open_webui_client import OpenWebUIClient
from src.tts.piper_client import PiperClient
from src.stt.whisper_client import WhisperClient

class DialogService:
    """Provides the core functions for processing a dialogue."""

    def __init__(
        self, repository: SignalRepository, rule_evaluator: RuleEvaluator, prompt_builder: PromptBuilder, 
        open_webui_client: OpenWebUIClient, piper_client: PiperClient, whisper_client: WhisperClient, hci_config: dict
    ):
        self.repository = repository
        self.rule_evaluator = rule_evaluator
        self.prompt_builder = prompt_builder
        self.open_webui_client = open_webui_client
        self.piper_client = piper_client
        self.whisper_client = whisper_client
        self.hci_config = hci_config

    def get_environment(self) -> EnvironmentState:
        """Read the latest environment state from the Signalspeicher."""
        signal = self.repository.get_latest()
        if signal is None:
            return EnvironmentState(uv=3, temperature=20, soil_moisture=50) #TODO Werte aus config lesen

        return EnvironmentState(uv=signal.uv, temperature=signal.temperature, soil_moisture=signal.soil_moisture)

    def update_engagement(self, event: str, engagement: int) -> int:
        """Update the internal engagement according to an HCI event."""
        rules = self.hci_config["hci"]["rules"]
        engagement_config = self.hci_config["hci"]["engagement"]
        for rule in rules:
            if rule["event"] == event:
                engagement += rule["change"]
                engagement = max(engagement_config["min"], min(engagement, engagement_config["max"]))
        return engagement
                
    def create_agent_context(self, dialog_state, engagement: int):
        """Create the current context of Agent Birke."""
        environment = self.get_environment()
        conditions = self.rule_evaluator.evaluate(
            soil_moisture=environment.soil_moisture, temperature=environment.temperature, uv=environment.uv
        )
        return create_context(dialog_state=dialog_state, environment=environment, conditions=conditions, engagement=engagement)

    def generate_response(self, user_input: str, dialog_state, dialog_history: list[dict[str, str]], engagement: int):
        """Generate a text response and speech output. 
        Returns llm answer, generated Audio Output Path, prompt building time, llm response time, tts time,
        total processing time.
        """
        start_time = time.perf_counter()
        # A normal conversation turn changes the internal engagement before the prompt is generated
        if user_input:
            engagement = self.update_engagement("conversation_turn", engagement)
        context = self.create_agent_context(dialog_state, engagement)
        
        prompt_start = time.perf_counter()
        prompt = self.prompt_builder.build(user_input=user_input, context=context, dialog_history=dialog_history)
        prompt_building_time = time.perf_counter() - prompt_start
        
        llm_start = time.perf_counter()
        answer = self.open_webui_client.generate(prompt)
        llm_response_time = time.perf_counter() - llm_start
        
        tts_start = time.perf_counter()
        audio_path = self.piper_client.generate(text=answer, output_filename=(f"response_{int(time.time() * 1000)}.wav"))
        tts_time = time.perf_counter() - tts_start
       
        processing_time = (time.perf_counter() - start_time) # total processing time 
        
        return answer, audio_path, prompt_building_time, llm_response_time, tts_time, processing_time, prompt, engagement, context

    def transcribe_audio(self, audio_input) -> str:
        """Transcribe an audio recording with Faster-Whisper."""
        audio_path = "data/audio/input.wav"
        with open(audio_path, "wb") as file:
            file.write(audio_input.getbuffer())
        text = self.whisper_client.transcribe(audio_path)
        return text.strip()