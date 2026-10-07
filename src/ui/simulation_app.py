import json
from pathlib import Path
import streamlit as st
from src.signals.repository import SignalRepository
from src.simulation.simulator import EnvironmentSimulator

CONFIG_PATH = Path("config/simulation.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    simulation_config = json.load(file)
# Page configuration
st.set_page_config(page_title="Agent Birke – Umweltsimulation",page_icon="🌳")
# Create simulation components
repository = SignalRepository()
simulator = EnvironmentSimulator(repository)
# Page title
st.title("🌳 Agent Birke")
st.header("Umweltsimulation")
# Read configuration
uv_config = simulation_config["uv"]
temperature_config = simulation_config["temperature"]
soil_moisture_config = simulation_config["soil_moisture"]
# Read latest values from database
latest_signal = repository.get_latest()
if latest_signal is None:
    uv_value = uv_config["default"]
    temperature_value = temperature_config["default"]
    soil_moisture_value = soil_moisture_config["default"]
else:
    uv_value = latest_signal.uv
    temperature_value = latest_signal.temperature
    soil_moisture_value = latest_signal.soil_moisture
# Environmental value sliders
uv = st.slider("UV-Index",min_value=uv_config["min"],max_value=uv_config["max"],value=uv_value)
temperature = st.slider("Temperatur (°C)",min_value=temperature_config["min"],max_value=temperature_config["max"],value=temperature_value)
soil_moisture = st.slider("Bodenfeuchtigkeit (%)",min_value=soil_moisture_config["min"],max_value=soil_moisture_config["max"],value=soil_moisture_value)
# Save button
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
    st.metric("UV-Index",uv)
    st.metric("Temperatur",f"{temperature} °C")
with col2:
    st.metric("Bodenfeuchtigkeit",f"{soil_moisture} %")