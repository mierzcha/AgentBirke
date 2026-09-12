import streamlit as st

from src.dialog.state_machine import DialogStateMachine
from src.dialog.prompt_builder import PromptBuilder
from src.llm.client import OllamaClient
from src.rules.evaluator import RuleEvaluator
from src.signals.repository import SignalRepository
from src.dialog.logger import DialogueLogger
from src.tts.piper_client import PiperClient
from src.stt.whisper_client import WhisperClient


def initialize_session_state() -> None:
    """Initialize the session state of the dialog application."""

    defaults = {
        "state_machine": DialogStateMachine(),
        "dialog_history": [],
        "last_prompt": None,
        "last_answer": None,
        "goodbye_done": False,
        "history_clear_at": None,
        "last_processing_time": None,
        "last_audio_path": None,
        "last_audio_id": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


@st.cache_resource
def create_repository() -> SignalRepository:
    """Create the signal repository."""

    return SignalRepository()


@st.cache_resource
def create_rule_evaluator() -> RuleEvaluator:
    """Create the rule evaluator."""

    return RuleEvaluator()


@st.cache_resource
def create_prompt_builder() -> PromptBuilder:
    """Create the prompt builder."""

    return PromptBuilder()


@st.cache_resource
def create_ollama_client() -> OllamaClient:
    """Create the Ollama client."""

    return OllamaClient()


@st.cache_resource
def create_dialogue_logger() -> DialogueLogger:
    """Create the dialogue logger."""

    return DialogueLogger()


@st.cache_resource
def create_piper_client() -> PiperClient:
    """Create the Piper client."""

    return PiperClient(
        model_path="models/piper/de_DE-ramona-low.onnx"
    )


@st.cache_resource
def create_whisper_client() -> WhisperClient:
    """Create the Whisper client."""

    return WhisperClient()
