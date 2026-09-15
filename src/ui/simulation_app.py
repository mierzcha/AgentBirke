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

uv_config = simulation_config["uv"]

uv = st.slider(
    "UV-Index",
    min_value=uv_config["min"],
    max_value=uv_config["max"],
    value=uv_config["default"]
)

temperature_config = simulation_config["temperature"]

uv = st.slider(
    "Temperatur (°C)",
    min_value=uv_config["min"],
    max_value=uv_config["max"],
    value=uv_config["default"]
)

soil_moisture_config = simulation_config["soil_moisture"]
soil_moisture = st.slider(
    "Bodenfeuchtigkeit (%)",
    min_value=soil_moisture_config["min"],
    max_value=soil_moisture_config["max"],
    value=soil_moisture_config["default"],
)

# Save Button
if st.button("Absenden"):
    simulator.set_uv(uv)
    simulator.set_temperature(temperature)
    simulator.set_soil_moisture(soil_moisture)
    simulator.save_state("test")
    st.success("Zustand gespeichert.")

# Current values
st.subheader("Aktuelle Werte")

col1, col2 = st.columns(2)

with col1:
    st.metric("UV-Index", f"{uv}")
    st.metric("Temperatur", f"{temperature} °C")

with col2:
    st.metric("Bodenfeuchtigkeit", f"{soil_moisture} %")
