from src.signals.repository import SignalRepository
from src.simulation.simulator import EnvironmentSimulator


def main():
    repository = SignalRepository()

    simulator = EnvironmentSimulator(repository)

    simulator.set_uv(80)
    simulator.set_temperature(25)
    simulator.set_soil_moisture(30)
    simulator.set_touch(True)

    simulator.save_state("active_dialog")

    print("Simulierter Zustand wurde gespeichert.")

    latest = repository.get_latest()

    print("Gespeicherter Zustand:")
    print(latest)


if __name__ == "__main__":
    main()
