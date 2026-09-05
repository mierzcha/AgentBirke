import time

import streamlit as st

from src.dialog.state_machine import DialogStateMachine
from src.dialog.states import DialogState


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

# Dialogverlauf initialisieren
if "dialog_history" not in st.session_state:
    st.session_state.dialog_history = []

# Berührung
if "touch_active" not in st.session_state:
    st.session_state.touch_active = False

# Automatische Zustandsübergänge
if state_machine.state == DialogState.GOODBYE:

    time.sleep(state_machine.GOODBYE_DURATION)

    state_machine.update()

    st.rerun()

# Aktueller Dialogzustand
st.subheader("Aktueller Dialogzustand")

st.info(state_machine.state.value)

# Umweltbedingungen
st.subheader("Umweltbedingungen")

st.write("TODO: Aktive Umweltbedingungen anzeigen")

# Aktionen
st.subheader("Aktionen")

col1, col2, col3 = st.columns(3)

# Berührung
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


# Spracheingabe
with col2:

    if st.button("Spracheingabe"):
	      #TODO 

        user_input = "Hallo Birke"

        st.session_state.dialog_history.append(
            {
                "speaker": "Nutzer",
                "text": user_input,
            }
        )

        state_machine.handle_event("speech")

        st.rerun()


# Gießen
with col3:

    if st.button("WIP Gießen"):

        # TODO: Wird später mit dem EnvironmentSimulator verbunden.
        st.write("Bodenfeuchtigkeit erhöhen")

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

# Spracheingabe und -ausgabe
st.subheader("Sprache")

st.write("🎤 Spracheingabe: TODO")

st.write("🔊 Sprachausgabe: TODO")