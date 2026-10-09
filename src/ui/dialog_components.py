import math
import json
from pathlib import Path
import streamlit as st
from src.dialog.state_machine import DialogStateMachine
from src.dialog.prompt_builder import PromptBuilder
from src.llm.open_webui_client import OpenWebUIClient
from src.rules.evaluator import RuleEvaluator
from src.signals.repository import SignalRepository
from src.dialog.logger import DialogueLogger
from src.tts.piper_client import PiperClient
from src.stt.whisper_client import WhisperClient
from src.led.led_controller import LedController
from src.led.led_controller import LEDFrame
from src.led.led_output import MockLEDOutput

HCI_CONFIG_PATH = Path("config/hci.json")
LOGGING_CONFIG_PATH = Path("config/logging.json")
LED_CONFIG_PATH = Path("config/led.json")

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
        "engagement": engagement_config["default"],
        "show_touch_animation": False
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
def create_led_config() -> dict:
    """Load the declarative LED configuration."""
    with open(LED_CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
        
@st.cache_resource
def create_led_controller(led_config: dict) -> LedController:
    """Create the LED controller."""
    output=MockLEDOutput()
    return LedController(led_config=led_config,output=output)
        
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

def render_led_ring(leds: list[tuple[int, int, int]], size: int = 300) -> None:
    """Render a static 24-LED ring."""
    if len(leds) != 24: #TODO get from led.json
        raise ValueError(f"Expected 24 LEDs, got {len(leds)}.")

    center = size / 2
    radius = size * 0.35
    led_size = size * 0.08
    html = f"""
    <div style="
        position: relative;
        width: {size}px;
        height: {size}px;
        margin: auto;
    ">
    """
    for index, (red, green, blue) in enumerate(leds):
        angle = 2 * math.pi * index / 24 - math.pi / 2
        x = center + radius * math.cos(angle) - led_size / 2
        y = center + radius * math.sin(angle) - led_size / 2

        html += f"""
        <div style="
            position: absolute;
            left: {x}px;
            top: {y}px;
            width: {led_size}px;
            height: {led_size}px;
            border-radius: 50%;
            background: rgb({red}, {green}, {blue});
            box-shadow: 0 0 10px rgb({red}, {green}, {blue});
        "></div>
        """
    html += "</div>"
    st.html(html)


def render_led_animation(frames: list[LEDFrame], size: int = 300) -> None:
    """Render an LED animation as a CSS animation."""
    if not frames:
        return

    if any(len(frame.leds) != 24 for frame in frames):
        raise ValueError("Every LED frame must contain exactly 24 LEDs.")

    center = size / 2
    radius = size * 0.35
    led_size = size * 0.08
    total_duration = sum(frame.duration_ms for frame in frames)
    html = ""
    for led_index in range(24):
        animation_name = f"led_animation_{led_index}"
        html += f"""
        <style>
            @keyframes {animation_name} {{
        """
        elapsed = 0
        for frame in frames:
            start = elapsed / total_duration * 100
            elapsed += frame.duration_ms
            end = elapsed / total_duration * 100
            red, green, blue = frame.leds[led_index]
            html += f"""
                {start:.3f}% {{
                    background: rgb({red}, {green}, {blue});
                    box-shadow: 0 0 10px rgb({red}, {green}, {blue});
                }}

                {end:.3f}% {{
                    background: rgb({red}, {green}, {blue});
                    box-shadow: 0 0 10px rgb({red}, {green}, {blue});
                }}
            """
        html += """
            }
        </style>
        """
    html += f"""
    <div style="
        position: relative;
        width: {size}px;
        height: {size}px;
        margin: auto;
    ">
    """
    for index in range(24):
        angle = (2 * math.pi * index / 24 - math.pi / 2)
        x = (center + radius * math.cos(angle) - led_size / 2)
        y = (center + radius * math.sin(angle) - led_size / 2)
        animation_name = f"led_animation_{index}"
        html += f"""
        <div style="
            position: absolute;
            left: {x}px;
            top: {y}px;
            width: {led_size}px;
            height: {led_size}px;
            border-radius: 50%;
            background: black;
            animation: {animation_name}
                {total_duration}ms
                linear
                1;
            animation-fill-mode: forwards;
        "></div>
        """
    html += "</div>"
    st.html(html)