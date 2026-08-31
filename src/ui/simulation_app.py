import streamlit as st


from src.signals.repository import SignalRepository
from src.simulation.simulator import EnvironmentSimulator

# Page configuration
st.set_page_config(
    page_title="Agent Birke – Umweltsimulation",
    page_icon="🌳",
)

# Create simulation components
repository = SignalRepository()
simulator = EnvironmentSimulator(repository)

# Page Title
st.title("🌳 Agent Birke")
st.header("Umweltsimulation")

uv = st.slider(
    "UV-Index",
    min_value=0,
    max_value=15,
    value=3
)

temperature = st.slider(
    "Temperatur (°C)",
    min_value=-20,
    max_value=45,
    value=20,
)

soil_moisture = st.slider(
    "Bodenfeuchtigkeit (%)",
    min_value=0,
    max_value=100,
    value=70,
)

touch = st.checkbox("Berührung simulieren")

# Save Button
if st.button("Absenden"):
    simulator.set_uv(uv)
    simulator.set_temperature(temperature)
    simulator.set_soil_moisture(soil_moisture)
    simulator.set_touch(touch)
    simulator.save_state("test")
    st.success("Zustand gespeichert.")

# Current values
st.subheader("Aktuelle Werte")

col1, col2 = st.columns(2)

with col1:
    st.metric("UV", f"{uv} W/m²")
    st.metric("Temperatur", f"{temperature} °C")

with col2:
    st.metric("Bodenfeuchtigkeit", f"{soil_moisture} %")
    st.metric("Berührung", "Ja" if touch else "Nein")
