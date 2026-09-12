import streamlit as st

st.title("Mikrofontest")

audio = st.audio_input(
    "Mikrofon testen",
    sample_rate=16000,
)

if audio is not None:
    st.success("Aufnahme erhalten!")

    st.audio(
        audio,
        format="audio/wav",
    )
