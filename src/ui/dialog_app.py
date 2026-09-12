import time

import streamlit as st

from src.dialog.state_machine import DialogStateMachine
from src.dialog.states import DialogState
from src.dialog.service import DialogService

from src.ui.dialog_components import (
    initialize_session_state,
    create_repository,
    create_rule_evaluator,
    create_prompt_builder,
    create_ollama_client,
    create_dialogue_logger,
    create_piper_client,
    create_whisper_client,
)


DIALOG_HISTORY_DISPLAY_TIME = 15


st.set_page_config(
    page_title="Agent Birke - Dialog",
    page_icon="🌳",
)

st.title("🌳 Agent Birke")
st.header("Dialogsystem")


# Initialize session state

initialize_session_state()

state_machine = st.session_state.state_machine


# Initialize components

repository = create_repository()
rule_evaluator = create_rule_evaluator()
prompt_builder = create_prompt_builder()
ollama_client = create_ollama_client()
dialogue_logger = create_dialogue_logger()
piper_client = create_piper_client()
whisper_client = create_whisper_client()

dialog_service = DialogService(
    repository=repository,
    rule_evaluator=rule_evaluator,
    prompt_builder=prompt_builder,
    ollama_client=ollama_client,
    piper_client=piper_client,
    whisper_client=whisper_client,
)


def add_to_history(
    speaker: str,
    text: str,
) -> None:
    """Add one message to the conversation history."""

    st.session_state.dialog_history.append(
        {
            "speaker": speaker,
            "text": text,
        }
    )


def generate_agent_response(
    user_input: str,
) -> str:
    """Generate an agent response and store its result."""

    (
        answer,
        audio_path,
        processing_time,
        prompt,
    ) = dialog_service.generate_response(
        user_input=user_input,
        dialog_state=state_machine.state,
        dialog_history=st.session_state.dialog_history,
    )

    st.session_state.last_answer = answer
    st.session_state.last_audio_path = audio_path
    st.session_state.last_processing_time = processing_time
    st.session_state.last_prompt = prompt

    return answer

def process_input(
    user_input: str,
) -> None:
    """Process a user input and generate the response."""

    if state_machine.state == DialogState.GREETING:

        state_machine.handle_event("speech")

    answer = generate_agent_response(
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

def process_audio_input(
    audio_input,
) -> None:
    """Transcribe and process a new audio recording."""

    audio_id = audio_input.file_id

    if audio_id == st.session_state.last_audio_id:
        return

    st.session_state.last_audio_id = audio_id

    with st.spinner("🌱 Birke hört zu..."):

        recognized_text = (
            dialog_service.transcribe_audio(
                audio_input
            )
        )

    st.write(
        f"**Erkannt:** {recognized_text}"
    )

    if recognized_text:

        process_input(
            recognized_text
        )


def show_audio_output() -> None:
    """Display the latest generated speech output."""

    if st.session_state.last_audio_path is not None:

        st.audio(
            st.session_state.last_audio_path,
            format="audio/wav",
            autoplay=True,
        )


def show_current_state() -> None:
    """Display the current dialogue state."""

    st.subheader("Aktueller Zustand")

    st.write(
        f"**Dialogzustand:** `{state_machine.state.value}`"
    )


def show_state_machine() -> None:
    """Display the current state and state transitions."""

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

        with st.expander(
            "**Bisherige Zustandsübergänge:**"
        ):

            for transition in state_machine.history:

                st.write(
                    f"`{transition.from_state.value}` "
                    f"— **{transition.event}** → "
                    f"`{transition.to_state.value}`"
                )

    else:

        st.write(
            "Noch keine Zustandsübergänge."
        )


def show_environment() -> None:
    """Display the current environmental values."""

    st.subheader("Umgebung")

    environment = dialog_service.get_environment()

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


def show_touch_control() -> None:
    """Display and handle the touch control."""

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

        st.info(
            "Das Gespräch wird beendet."
        )


def show_dialogue_history() -> None:
    """Display the current dialogue history."""

    if not st.session_state.dialog_history:
        return

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


def show_text_and_voice_input(
    text_key: str,
    audio_key: str,
) -> None:
    """Display text and voice input controls."""

    user_input = st.text_input(
        "Texteingabe",
        key=text_key,
    )

    submitted = st.button(
        "Eingabe senden",
        key=f"{text_key}_button",
    )

    audio_input = st.audio_input(
        "Oder sprich mit der Birke",
        sample_rate=16000,
        key=audio_key,
    )

    if submitted and user_input.strip():

        process_input(
            user_input
        )

    if audio_input is not None:

        process_audio_input(
            audio_input
        )


def handle_greeting() -> None:
    """Handle the greeting state."""

    if st.session_state.last_answer is None:

        answer = generate_agent_response(
            ""
        )

        add_to_history(
            "Birke",
            answer,
        )

        st.rerun()

    st.write(
        "Was möchtest du der Birke sagen?"
    )

    show_text_and_voice_input(
        text_key="greeting_text_input",
        audio_key="greeting_audio",
    )


def handle_dialogue_active() -> None:
    """Handle the active dialogue state."""

    st.subheader("Gespräch")

    show_text_and_voice_input(
        text_key="dialog_text_input",
        audio_key="dialog_audio",
    )


def handle_goodbye() -> None:
    """Handle the goodbye state."""

    st.subheader("Verabschiedung")

    if not st.session_state.goodbye_done:

        answer = generate_agent_response(
            ""
        )

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
            time.time()
            + DIALOG_HISTORY_DISPLAY_TIME
        )

        st.rerun()


def clear_old_dialogue_history() -> None:
    """Clear the dialogue history after the display time."""

    if state_machine.state != DialogState.IDLE:
        return

    if st.session_state.history_clear_at is None:
        return

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


def show_developer_view() -> None:
    """Display the developer information."""

    with st.expander(
        "Entwickleransicht anzeigen"
    ):

        st.subheader(
            "Entwickleransicht"
        )

        st.write(
            f"Aktueller Zustand: "
            f"`{state_machine.state.value}`"
        )

        st.write(
            "**Mögliche Zustandsübergänge:**"
        )

        st.write(
            "`Idle` — **touch** → `Greeting`"
        )

        st.write(
            "`Greeting` — **speech** → "
            "`Dialogue_active`"
        )

        st.write(
            "`Greeting` — **release** → "
            "`Goodbye`"
        )

        st.write(
            "`Dialogue_active` — **speech** → "
            "`Dialogue_active`"
        )

        st.write(
            "`Dialogue_active` — **release** → "
            "`Goodbye`"
        )

        st.write(
            "`Goodbye` — **goodbye_finished** → "
            "`Idle`"
        )

        if (
            st.session_state.last_processing_time
            is not None
        ):

            st.write(
                f"Bearbeitungszeit: "
                f"{st.session_state.last_processing_time:.2f} "
                f"Sekunden"
            )

        if st.session_state.last_prompt:

            with st.expander(
                "Prompt anzeigen"
            ):

                st.text(
                    st.session_state.last_prompt
                )

        if st.button(
            "Gespräch zurücksetzen"
        ):

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


# Display application

show_audio_output()

show_current_state()

show_state_machine()

show_environment()

show_touch_control()

show_dialogue_history()


# Handle current dialogue state

if state_machine.state == DialogState.GREETING:

    handle_greeting()

elif state_machine.state == DialogState.DIALOGUE_ACTIVE:

    handle_dialogue_active()

elif state_machine.state == DialogState.GOODBYE:

    handle_goodbye()


clear_old_dialogue_history()

show_developer_view()
