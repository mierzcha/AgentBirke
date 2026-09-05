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

# Berührung

if "touch_active" not in st.session_state:
    st.session_state.touch_active = False


# Aktueller Dialogzustand

st.subheader("Aktueller Dialogzustand")

st.info(state_machine.state.value)

# Umweltbedingungen

st.subheader("Umweltbedingungen")

st.write("TODO: Aktive Umweltbedingungen anzeigen")

# Aktionen

st.subheader("Aktionen")

col1, col2, col3 = st.columns(3)


with col1:

    if not st.session_state.touch_active:

        if st.button("Birke berühren"):
            st.session_state.touch_active = True

            state_machine.handle_event("touch")

            st.rerun()

    else:

        if st.button("Birke loslassen"):
            st.session_state.touch_active = False

            st.rerun()


with col2:

    if st.button("Spracheingabe"):

        # Spracheingabe wird später durch STT ersetzt
        state_machine.handle_event("speech")

        st.rerun()


with col3:

    if st.button("WIP Gießen"):

        # TODO Wird später mit dem EnvironmentSimulator verbunden
        st.write("Bodenfeuchtigkeit erhöhen")


# Dialogverlauf

st.subheader("Dialogverlauf")

st.write("TODO: Dialogverlauf anzeigen")

# Zustandsautomat

st.subheader("Zustandsautomat")

st.write(
    "Der aktuelle Zustand des Dialogautomaten ist:"
)

st.info(state_machine.state.value)

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

st.write("TODO: Antwort- bzw. Bearbeitungszeit anzeigen")

# Spracheingabe und -ausgabe

st.subheader("Sprache")

st.write("🎤 Spracheingabe: TODO")

st.write("🔊 Sprachausgabe: TODO")