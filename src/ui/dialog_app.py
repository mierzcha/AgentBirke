import streamlit as st

from src.agent.context import create_context
from src.dialog.prompt_builder import PromptBuilder
from src.dialog.state_machine import DialogStateMachine
from src.dialog.states import DialogState
from src.llm.client import OllamaClient
from src.rules.evaluator import RuleEvaluator
from src.signals.repository import SignalRepository
from src.simulation.events import EnvironmentState


#Temp (später aus configuration skript) (TODO)
DEFAULT_UV = 3
DEFAULT_TEMPERATURE = 20
DEFAULT_SOIL_MOISTURE = 50
DEFAULT_TOUCH = False

st.set_page_config(
    page_title="Agent Birke - Dialog",
    page_icon="🌳",
)


st.title("🌳 Agent Birke")
st.write("Dialogsystem")

"""initialize State Machine"""
# TODO: Initialisierungen als Methoden schreiben?
if "state_machine" not in st.session_state:
    st.session_state.state_machine = DialogStateMachine()

if "dialog_history" not in st.session_state:
    st.session_state.dialog_history = []

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

state_machine = st.session_state.state_machine

"""initialize components"""
repository = SignalRepository()
rule_evaluator = RuleEvaluator()
prompt_builder = PromptBuilder()
ollama_client = OllamaClient()


def get_environment() -> EnvironmentState:
    """Read the latest environment state from the signal memory (Signalspeicher.db)."""

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


def create_agent_context() :
    """Create the current context of Agent Birke."""
    
    #TODO nicht gebraucht?
    # Berührungszustand 
		#if "touch_active" not in st.session_state:
		#    st.session_state.touch_active = False

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
    """Create a prompt and generate a response with Ollama."""

    context = create_agent_context()

    prompt = prompt_builder.build(
        user_input=user_input,
        context=context,
        dialog_history=st.session_state.dialog_history,
    )

    st.session_state.last_prompt = prompt

    with st.spinner("🌱 Birke denkt nach..."):
        answer = ollama_client.generate(prompt)

    st.session_state.last_answer = answer

    return answer


def add_to_history(speaker: str, text: str) -> None:
    """Add one message to the conversation history."""

    st.session_state.dialog_history.append(
        {
            "speaker": speaker,
            "text": text,
        }
    )


st.subheader("Aktueller Zustand")

st.write(
    f"**Dialogzustand:** `{state_machine.state.value}`"
)

# TODO
# Darstellung des Zustandsautomaten (Graf neu)


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


st.subheader("Berührung")


if state_machine.state == DialogState.IDLE:

    if st.button("Birke berühren"):

        state_machine.handle_event("touch")

        st.rerun()


elif state_machine.state in [
    DialogState.GREETING,
    DialogState.DIALOGUE_ACTIVE,
]:

    if st.button("Birke loslassen"):

        state_machine.handle_event("release")

        st.rerun()


elif state_machine.state == DialogState.GOODBYE:

    st.info("Das Gespräch wird beendet.")


if state_machine.state == DialogState.GREETING:

    st.subheader("Begrüßung")

    if st.session_state.last_answer is None:

        answer = generate_response("")

        add_to_history("Birke", answer)

        state_machine.handle_event("greeting_finished")

        st.rerun()


elif state_machine.state == DialogState.DIALOGUE_ACTIVE:

    st.subheader("Gespräch")

    user_input = st.text_input(
        "Was möchtest du der Birke sagen?",
        key="user_input",
    )

    if st.button("Eingabe senden"):

        if user_input.strip():

            answer = generate_response(user_input)

            add_to_history("Nutzer", user_input)
            add_to_history("Birke", answer)

            st.session_state.user_input = ""

            st.rerun()


elif state_machine.state == DialogState.GOODBYE:

    st.subheader("Verabschiedung")

    if st.session_state.last_answer is None:

        answer = generate_response("")

        add_to_history("Birke", answer)

        state_machine.handle_event("goodbye_finished")

        st.session_state.dialog_history = []
        st.session_state.last_prompt = None
        st.session_state.last_answer = None
        # TODO Automatischer Übergang von Goodbye zu Idle testen

        st.rerun()


if st.session_state.dialog_history:

    st.subheader("Gesprächsverlauf")

    for message in st.session_state.dialog_history:

        if message["speaker"] == "Nutzer":
            st.write(f"**Nutzer:** {message['text']}")

        else:
            st.write(f"**Birke:** {message['text']}")


if st.session_state.last_prompt:

    with st.expander("Prompt anzeigen"):
        st.text(st.session_state.last_prompt)


st.subheader("Entwickleransicht")

st.write(
    f"Aktueller Zustand: `{state_machine.state.value}`"
)

if st.button("Gespräch zurücksetzen"):

    st.session_state.state_machine = DialogStateMachine()
    st.session_state.dialog_history = []
    st.session_state.last_prompt = None
    st.session_state.last_answer = None

    st.rerun()