import streamlit as st

from src.dialog.state_machine import DialogStateMachine
from src.dialog.states import DialogState


st.set_page_config(
    page_title="Agent Birke – Dialog",
    page_icon="🌳",
)

st.title("🌳 Agent Birke")
st.header("Dialogsteuerung")

if "state_machine" not in st.session_state:
    st.session_state.state_machine = DialogStateMachine()

state_machine = st.session_state.state_machine


st.subheader("Aktueller Dialogzustand")

st.info(state_machine.state.value)

#todo Umweltbedingungen, log

touchBtnTxt="Birke berühren"


st.subheader("Aktionen")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(touchBtnTxt): #todo: Button soll verschwinden wenn berührung aktiv, stattdessen soll der button Birke loslassen werden
        state_machine.handle_event("touch")
        touchBtnTxt="Birke loslassen"
        st.rerun()

with col2:
    if st.button("Spracheingabe"):
        state_machine.handle_event("speech")
        #todo 
        st.rerun()

with col3:
    if st.button("WIP Giessen"):
        #todo
        print(f"soil_moisture erhöhen")


st.subheader("Dialogzustand manuell setzen")

selected_state = st.selectbox(
    "Zustand auswählen",
    list(DialogState),
    format_func=lambda state: state.value,
)

if st.button("Zustand übernehmen"):
    state_machine.state = selected_state
    st.rerun()


st.subheader("Zustandsautomat")

st.write(
    "Der aktuelle Zustand wird durch die DialogStateMachine "
    "verwaltet."
)

st.write(f"**Aktueller Zustand:** {state_machine.state.value}")
