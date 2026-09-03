# AgentBirke

Version 0 (WIP)

## Create Virtual Environment

Agent Birke requires Python 3.11 to run.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## Install Requirements

```bash
pip install -r requirements.txt
pip install open-webui
```

## Signalspeicher initialisieren

data/database/signals.db ist die Signalspeicher-Datenbank.
Sie wird initialisiert mit:

```bash
PYTHONPATH=. python scripts/init_database.py
```

## Open WebUI einrichten

```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

visit localhost:3000
create an Administrator Account
create an API Key
write API Key in your own .env

## Run Tests

Ollama testen
```bash
PYTHONPATH=. python tests/test_ollama.py
```

Signalspeicher testen
```bash
PYTHONPATH=. python tests/test_signals.py
```
