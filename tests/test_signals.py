from datetime import datetime
from src.signals.models import Signal
from src.signals.repository import SignalRepository

def main():
    repository = SignalRepository()
    signal = Signal(
        uv=2,
        temperature=22,
        soil_moisture=50,
        state="active_dialog",
        time=datetime.now(),
    )
    repository.save(signal)
    latest = repository.get_latest()
    print("Gespeichertes Signal:")
    print(latest)

if __name__ == "__main__":
    main()