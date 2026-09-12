import time

import streamlit as st

from src.agent.context import create_context
from src.dialog.prompt_builder import PromptBuilder
from src.dialog.state_machine import DialogStateMachine
from src.dialog.states import DialogState
from src.llm.client import OllamaClient
from src.rules.evaluator import RuleEvaluator
from src.signals.repository import SignalRepository
from src.simulation.events import EnvironmentState
from src.dialog.logger import DialogueLogger
from src.tts.piper_client import PiperClient
from src.stt.whisper_client import WhisperClient


# Temp (später aus configuration Skript) (TODO)
DEFAULT_UV = 3
DEFAULT_TEMPERATURE = 20
DEFAULT_SOIL_MOISTURE = 50
DEFAULT_TOUCH = False

DIALOG_HISTORY_DISPLAY_TIME = 15


st.set_page_config(
    page_title="Agent Birke - Dialog",
    page_icon="🌳",
)


st.title("🌳 Agent Birke")
st.header("Dialogsystem")


# Initializing State Machine

if "state_machine" not in st.session_state:
    st.session_state.state_machine = DialogStateMachine()

if "dialog_history" not in st.session_state:
    st.session_state.dialog_history = []

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

if "goodbye_done" not in st.session_state:
    st.session_state.goodbye_done = False

if "history_clear_at" not in st.session_state:
    st.session_state.history_clear_at = None

if "last_processing_time" not in st.session_state:
    st.session_state.last_processing_time = None

if "last_audio_path" not in st.session_state:
    st.session_state.last_audio_path = None

if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None


state_machine = st.session_state.state_machine


# Initializing components

repository = SignalRepository()
rule_evaluator = RuleEvaluator()
prompt_builder = PromptBuilder()
ollama_client = OllamaClient()
dialogue_logger = DialogueLogger()

piper_client = PiperClient(
    model_path="models/piper/de_DE-ramona-low.onnx"
)

whisper_client = WhisperClient()


def get_environment() -> EnvironmentState:
    """Read the latest environment state from the Signalspeicher."""

    signal = repository.get_latest()

    if signal is None:

        return EnvironmentState(
            uv=DEFAULT_UV,
            temperature=DEFAULT_TEMPERATURE,
            soil_moisture=DEFAULT_SOIL_MOISTURE,
            touch=DEFAULT_TOUCH,
        )

    return EnvironmentState(
        uv=signal.uv,
        temperature=signal.temperature,
        soil_moisture=signal.soil_moisture,
        touch=signal.touch,
    )


def create_agent_context():
    """Create the current context of Agent Birke."""

    environment = get_environment()

    conditions = rule_evaluator.evaluate(
        soil_moisture=environment.soil_moisture,
        temperature=environment.temperature,
        uv=environment.uv,
    )

    return create_context(
        dialog_state=state_machine.state,
        environment=environment,
        conditions=conditions,
    )


def generate_response(user_input: str) -> str:
    """Create a prompt, generate a response and create speech output."""

    start_time = time.perf_counter()

    context = create_agent_context()

    prompt = prompt_builder.build(
        user_input=user_input,
        context=context,
        dialog_history=st.session_state.dialog_history,
    )

    st.session_state.last_prompt = prompt

    with st.spinner("🌱 Birke denkt nach..."):

        answer = ollama_client.generate(prompt)

        audio_path = piper_client.generate(
            text=answer,
            output_filename=(
                f"response_{int(time.time() * 1000)}.wav"
            ),
        )

    processing_time = time.perf_counter() - start_time

    st.session_state.last_answer = answer
    st.session_state.last_processing_time = processing_time
    st.session_state.last_audio_path = audio_path

    return answer


def transcribe_audio(audio_input) -> str:
    """Save an audio recording and transcribe it with Faster-Whisper."""

    audio_path = "data/audio/input.wav"

    with open(audio_path, "wb") as file:
        file.write(audio_input.getbuffer())

    with st.spinner("🌱 Birke hört zu..."):

        text = whisper_client.transcribe(
            audio_path
        )

    return text.strip()


def add_to_history(speaker: str, text: str) -> None:
    """Add one message to the conversation history."""

    st.session_state.dialog_history.append(
        {
            "speaker": speaker,
            "text": text,
        }
    )


# Audio output

if st.session_state.last_audio_path is not None:

    st.audio(
        st.session_state.last_audio_path,
        format="audio/wav",
        autoplay=True,
    )


# Current state

st.subheader("Aktueller Zustand")

st.write(
    f"**Dialogzustand:** `{state_machine.state.value}`"
)


# Visualization of State and State transitions

st.subheader("Zustandsautomat")

st.write(
    f"**Aktueller Zustand:** `{state_machine.state.value}`"
)


states = [
    DialogState.IDLE,
    DialogState.GREETING,
    DialogState.DIALOGUE_ACTIVE,
    DialogState.GOODBYE,
]


columns = st.columns(4)


for column, state in zip(columns, states):

    with column:

        if state == state_machine.state:

            st.success(
                f"**{state.value}**\n\nAktueller Zustand"
            )

        else:

            st.info(state.value)


if state_machine.history:

    with st.expander("**Bisherige Zustandsübergänge:**"):

        for transition in state_machine.history:

            st.write(
                f"`{transition.from_state.value}` "
                f"— **{transition.event}** → "
                f"`{transition.to_state.value}`"
            )

else:

    st.write("Noch keine Zustandsübergänge.")


# Environment

st.subheader("Umgebung")

environment = get_environment()

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "UV-Index",
        environment.uv,
    )


with col2:

    st.metric(
        "Temperatur",
        f"{environment.temperature} °C",
    )


with col3:

    st.metric(
        "Bodenfeuchtigkeit",
        f"{environment.soil_moisture} %",
    )


# Touch

st.subheader("Berührung")


if state_machine.state == DialogState.IDLE:

    if st.button("Birke berühren"):

        state_machine.handle_event("touch")

        st.session_state.goodbye_done = False
        st.session_state.history_clear_at = None

        st.session_state.last_audio_id = None

        st.rerun()


elif state_machine.state in [
    DialogState.GREETING,
    DialogState.DIALOGUE_ACTIVE,
]:

    if st.button("Birke loslassen"):

        state_machine.handle_event("release")

        st.session_state.goodbye_done = False

        st.rerun()


elif state_machine.state == DialogState.GOODBYE:

    st.info("Das Gespräch wird beendet.")


# Dialogue history

if st.session_state.dialog_history:

    st.subheader("Gesprächsverlauf")

    for message in st.session_state.dialog_history:

        if message["speaker"] == "Nutzer":

            st.write(
                f"**Nutzer:** {message['text']}"
            )

        else:

            st.write(
                f"**Birke:** {message['text']}"
            )


# Greeting

if state_machine.state == DialogState.GREETING:

    if st.session_state.last_answer is None:

        answer = generate_response("")

        add_to_history(
            "Birke",
            answer,
        )

        st.rerun()


    st.write("Was möchtest du der Birke sagen?")


    # Text input

    user_input = st.text_input(
        "Texteingabe",
        key="greeting_text_input",
    )


    submitted = st.button(
        "Eingabe senden",
        key="greeting_text_button",
    )


    # Voice input

    audio_input = st.audio_input(
        "Oder sprich mit der Birke",
        sample_rate=16000,
        key="greeting_audio",
    )


    # Handle text input

    if submitted and user_input.strip():

        state_machine.handle_event("speech")

        answer = generate_response(
            user_input
        )

        add_to_history(
            "Nutzer",
            user_input,
        )

        add_to_history(
            "Birke",
            answer,
        )

        st.rerun()


    # Handle voice input

    if audio_input is not None:

        audio_id = audio_input.file_id

        if audio_id != st.session_state.last_audio_id:

            st.session_state.last_audio_id = audio_id

            recognized_text = transcribe_audio(
                audio_input
            )

            st.write(
                f"**Erkannt:** {recognized_text}"
            )

            if recognized_text:

                state_machine.handle_event("speech")

                answer = generate_response(
                    recognized_text
                )

                add_to_history(
                    "Nutzer",
                    recognized_text,
                )

                add_to_history(
                    "Birke",
                    answer,
                )

                st.rerun()


# Dialogue active

elif state_machine.state == DialogState.DIALOGUE_ACTIVE:

    st.subheader("Gespräch")


    # Text input

    user_input = st.text_input(
        "Texteingabe",
        key="dialog_text_input",
    )


    submitted = st.button(
        "Eingabe senden",
        key="dialog_text_button",
    )


    # Voice input

    audio_input = st.audio_input(
        "Oder sprich mit der Birke",
        sample_rate=16000,
        key="dialog_audio",
    )


    # Handle text input

    if submitted and user_input.strip():

        answer = generate_response(
            user_input
        )

        add_to_history(
            "Nutzer",
            user_input,
        )

        add_to_history(
            "Birke",
            answer,
        )

        st.rerun()


    # Handle voice input

    if audio_input is not None:

        audio_id = audio_input.file_id

        if audio_id != st.session_state.last_audio_id:

            st.session_state.last_audio_id = audio_id

            recognized_text = transcribe_audio(
                audio_input
            )

            st.write(
                f"**Erkannt:** {recognized_text}"
            )

            if recognized_text:

                answer = generate_response(
                    recognized_text
                )

                add_to_history(
                    "Nutzer",
                    recognized_text,
                )

                add_to_history(
                    "Birke",
                    answer,
                )

                st.rerun()


# Goodbye

elif state_machine.state == DialogState.GOODBYE:

    st.subheader("Verabschiedung")


    if not st.session_state.goodbye_done:

        answer = generate_response("")

        add_to_history(
            "Birke",
            answer,
        )

        dialogue_logger.save_dialogue(
            st.session_state.dialog_history
        )

        st.session_state.goodbye_done = True

        state_machine.handle_event(
            "goodbye_finished"
        )

        st.session_state.history_clear_at = (
            time.time() + DIALOG_HISTORY_DISPLAY_TIME
        )

        st.rerun()


# Delete dialogue history after display time

if state_machine.state == DialogState.IDLE:

    if st.session_state.history_clear_at is not None:

        if time.time() >= st.session_state.history_clear_at:

            st.session_state.dialog_history = []
            st.session_state.last_prompt = None
            st.session_state.last_answer = None
            st.session_state.last_audio_path = None
            st.session_state.last_audio_id = None
            st.session_state.history_clear_at = None

            st.rerun()

        else:

            time.sleep(0.5)

            st.rerun()


# Developer view

with st.expander("Entwickleransicht anzeigen"):

    st.subheader("Entwickleransicht")

    st.write(
        f"Aktueller Zustand: `{state_machine.state.value}`"
    )


    st.write("**Mögliche Zustandsübergänge:**")


    st.write(
        "`Idle` — **touch** → `Greeting`"
    )

    st.write(
        "`Greeting` — **speech** → `Dialogue_active`"
    )

    st.write(
        "`Greeting` — **release** → `Goodbye`"
    )

    st.write(
        "`Dialogue_active` — **speech** → `Dialogue_active`"
    )

    st.write(
        "`Dialogue_active` — **release** → `Goodbye`"
    )

    st.write(
        "`Goodbye` — **goodbye_finished** → `Idle`"
    )


    if st.session_state.last_processing_time is not None:

        st.write(
            f"Bearbeitungszeit: "
            f"{st.session_state.last_processing_time:.2f} Sekunden"
        )


    if st.session_state.last_prompt:

        with st.expander("Prompt anzeigen"):

            st.text(
                st.session_state.last_prompt
            )


    if st.button("Gespräch zurücksetzen"):

        st.session_state.state_machine = (
            DialogStateMachine()
        )

        st.session_state.dialog_history = []

        st.session_state.last_prompt = None

        st.session_state.last_answer = None

        st.session_state.last_processing_time = None

        st.session_state.last_audio_path = None

        st.session_state.last_audio_id = None

        st.session_state.goodbye_done = False

        st.session_state.history_clear_at = None

        st.rerun()
