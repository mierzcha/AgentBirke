import time

import streamlit as st

from src.agent.context import create_context
from src.dialog.prompt_builder import PromptBuilder
from src.dialog.state_machine import DialogStateMachine
from src.dialog.states import DialogState
from src.rules.evaluator import RuleEvaluator
from src.signals.repository import SignalRepository
from src.simulation.events import EnvironmentState


st.set_page_config(
    page_title="Agent Birke – Dialog",
    page_icon="🌳",
)

st.title("🌳 Agent Birke")
st.header("Dialogsystem")


# Zustandsautomat initialisieren
if "state_machine" not in st.session_state:
    st.session_state.state_machine = DialogStateMachine()

state_machine = st.session_state.state_machine


# Komponenten initialisieren
repository = SignalRepository()
rule_evaluator = RuleEvaluator()
prompt_builder = PromptBuilder()


# Dialogverlauf initialisieren
if "dialog_history" not in st.session_state:
    st.session_state.dialog_history = []


# Letzten Umweltzustand aus dem Signalspeicher lesen
signal = repository.get_latest()

if signal is not None:

    environment = EnvironmentState(
        uv=signal.uv,
        temperature=signal.temperature,
        soil_moisture=signal.soil_moisture,
        touch=signal.touch,
    )

else:

    # Fallback, falls noch kein Signal gespeichert wurde
    environment = EnvironmentState(
        uv=3,
        temperature=20,
        soil_moisture=70,
        touch=False,
    )


# Umweltbedingungen bestimmen
conditions = rule_evaluator.evaluate(
    soil_moisture=environment.soil_moisture,
    temperature=environment.temperature,
    uv=environment.uv,
)


# Aktuellen Kontext erstellen
context = create_context(
    dialog_state=state_machine.state,
    environment=environment,
    conditions=conditions,
)


# Berührungszustand
if "touch_active" not in st.session_state:
    st.session_state.touch_active = False


# Automatischer Übergang von Goodbye zu Idle
if state_machine.state == DialogState.GOODBYE:

    time.sleep(state_machine.GOODBYE_DURATION)

    state_machine.update()

    st.rerun()


# Aktueller Dialogzustand
st.subheader("Aktueller Dialogzustand")

st.info(state_machine.state.value)


# Umweltbedingungen
st.subheader("Umweltbedingungen")

st.write(
    f"UV: {context.environment.uv}"
)

st.write(
    f"Temperatur: {context.environment.temperature} °C"
)

st.write(
    f"Bodenfeuchtigkeit: {context.environment.soil_moisture} %"
)

st.write(
    f"Berührung: "
    f"{'Ja' if context.environment.touch else 'Nein'}"
)

st.write("Aktive Bedingungen:")

if context.conditions:

    for condition in context.conditions:
        st.write(f"• {condition}")


# Aktionen
st.subheader("Aktionen")

col1, col2, col3 = st.columns(3)


# Birke berühren / loslassen
with col1:

    if not st.session_state.touch_active:

        if st.button("Birke berühren"):

            st.session_state.touch_active = True

            state_machine.handle_event("touch")

            st.rerun()

    else:

        if st.button("Birke loslassen"):

            st.session_state.touch_active = False

            state_machine.handle_event("release")

            st.rerun()


# Gießen
with col2:

    if st.button("WIP Gießen"):

        st.write(
            "TODO: Gießen wird später mit "
            "dem EnvironmentSimulator verbunden."
        )


# Platzhalter
with col3:

    st.write("")


# Texteingabe
st.subheader("Sprache")

st.write(
    "Die Texteingabe ersetzt momentan die spätere "
    "Spracheingabe durch STT."
)

user_input = st.text_input(
    "Nutzereingabe",
    placeholder="Was möchtest du der Birke sagen?",
)


if st.button("Eingabe senden") and user_input:

    # Dialogzustand aktualisieren
    state_machine.handle_event("speech")

    # Umweltzustand erneut aus der Datenbank lesen
    signal = repository.get_latest()

    if signal is not None:

        environment = EnvironmentState(
            uv=signal.uv,
            temperature=signal.temperature,
            soil_moisture=signal.soil_moisture,
            touch=signal.touch,
        )

    # Umweltbedingungen erneut bestimmen
    conditions = rule_evaluator.evaluate(
        soil_moisture=environment.soil_moisture,
        temperature=environment.temperature,
        uv=environment.uv,
    )

    # Kontext erneut erstellen
    context = create_context(
        dialog_state=state_machine.state,
        environment=environment,
        conditions=conditions,
    )

    # Prompt erzeugen
    prompt = prompt_builder.build(
        user_input=user_input,
        context=context,
    )

    # Prompt speichern
    st.session_state.last_prompt = prompt

    # Nutzereingabe im Dialogverlauf speichern
    st.session_state.dialog_history.append(
        {
            "speaker": "Nutzer",
            "text": user_input,
        }
    )

    st.rerun()


# Generierter Prompt
if "last_prompt" in st.session_state:

    st.subheader("Generierter Prompt")

    st.code(
        st.session_state.last_prompt,
        language="text",
    )


# Dialogverlauf
st.subheader("Dialogverlauf")

if not st.session_state.dialog_history:

    st.write("Noch keine Dialogbeiträge.")

else:

    for message in st.session_state.dialog_history:

        st.write(
            f"**{message['speaker']}:** "
            f"{message['text']}"
        )


# Zustandsautomat
st.subheader("Zustandsautomat")

st.write(
    "Der aktuelle Zustand des Dialogautomaten ist:"
)

st.info(state_machine.state.value)


# Darstellung des Zustandsautomaten
current_state = state_machine.state.value

graph = f"""
digraph {{
    rankdir=LR;

    Idle [
        label="Idle",
        style="{'filled' if current_state == 'Idle' else 'solid'}"
    ];

    Greeting [
        label="Greeting",
        style="{'filled' if current_state == 'Greeting' else 'solid'}"
    ];

    Dialogue_active [
        label="Dialogue_active",
        style="{'filled' if current_state == 'Dialogue_active' else 'solid'}"
    ];

    Goodbye [
        label="Goodbye",
        style="{'filled' if current_state == 'Goodbye' else 'solid'}"
    ];

    Idle -> Greeting [
        label="Birke berühren"
    ];

    Greeting -> Dialogue_active [
        label="Spracheingabe"
    ];

    Dialogue_active -> Goodbye [
        label="Birke loslassen"
    ];

    Goodbye -> Idle [
        label="automatisch"
    ];
}}
"""

st.graphviz_chart(graph)


# Zustandsverlauf
st.subheader("Zustandsverlauf")

if not state_machine.history:

    st.write("Noch keine Zustandswechsel.")

else:

    for transition in state_machine.history:

        st.write(
            f"{transition.from_state.value} "
            f"-- {transition.event} --> "
            f"{transition.to_state.value}"
        )


# Entwicklerbereich
st.subheader("Entwicklerbereich")

st.write(
    "Hier kann der Dialogzustand für Testzwecke "
    "manuell verändert werden."
)

selected_state = st.selectbox(
    "Dialogzustand auswählen",
    list(DialogState),
    format_func=lambda state: state.value,
)

if st.button("Zustand übernehmen"):

    state_machine.state = selected_state

    st.rerun()


# Bearbeitungszeit
st.subheader("Bearbeitungszeit")

st.write(
    "TODO: Antwort- bzw. Bearbeitungszeit anzeigen"
)


# Spracheingabe und Sprachausgabe
st.subheader("Sprache")

st.write(
    "🎤 Spracheingabe: TODO – wird später durch STT ersetzt"
)

st.write(
    "🔊 Sprachausgabe: TODO – wird später durch TTS ersetzt"
)
