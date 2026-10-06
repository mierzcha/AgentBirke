import streamlit as st
from src.dialog.state_machine import DialogStateMachine
from src.dialog.prompt_builder import PromptBuilder
from src.llm.open_webui_client import OpenWebUIClient
from src.rules.evaluator import RuleEvaluator
from src.signals.repository import SignalRepository
from src.dialog.logger import DialogueLogger
from src.tts.piper_client import PiperClient
from src.stt.whisper_client import WhisperClient
import json
from pathlib import Path

HCI_CONFIG_PATH = Path("config/hci.json")
LOGGING_CONFIG_PATH = Path("config/logging.json")

def initialize_session_state(hci_config: dict) -> None:
    """Initialize the session state of the dialog application."""
    engagement_config = hci_config["hci"]["engagement"]
    defaults = {
        "state_machine": DialogStateMachine(),
        "dialog_history": [],
        "interactions": [],
        "last_prompt": None,
        "last_answer": None,
        "goodbye_done": False,
        "history_clear_at": None,
        "last_processing_time": None,
        "last_prompt_building_time": None,
        "last_llm_response_time": None,
        "last_tts_time": None,
        "last_context": None,
        "last_audio_path": None,
        "last_audio_id": None,
        "engagement": engagement_config["default"]
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
            
@st.cache_resource
def create_hci_config() -> dict:
    """Load the declarative HCI configuration."""
    with open(HCI_CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
        
@st.cache_resource
def create_logging_config() -> dict:
    """Load the declarative logging configuration."""
    with open(LOGGING_CONFIG_PATH , "r", encoding="utf-8") as file:
        return json.load(file)
        
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
def create_open_webui_client() -> OpenWebUIClient:
    """Create the Open WebUI client."""
    return OpenWebUIClient()

@st.cache_resource
def create_dialogue_logger(logging_config: dict) -> DialogueLogger:
    """Create the dialogue logger."""
    return DialogueLogger(logging_config=logging_config)

@st.cache_resource
def create_piper_client() -> PiperClient:
    """Create the Piper client."""
    return PiperClient(model_path="models/piper/de_DE-ramona-low.onnx")

@st.cache_resource
def create_whisper_client() -> WhisperClient:
    """Create the Whisper client."""
    return WhisperClient()