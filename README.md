# AgentBirke

Version 1 (WIP)


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
pip install piper-tts
pip install faster-whisper
```

## Initialize Signals Database

The database, holding the environment signals is src/data/database/signals.db.

Initialize it with:
```bash
PYTHONPATH=. python scripts/init_database.py
```

## Set up Open WebUI for RAG

View "Kapitel 6.1 Einrichten von Open WebUI auf DIPA" for detailed instructions
TODO: Number might change

```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

## Start Dialogue App

```bash
PYTHONPATH=. streamlit run src/ui/dialog_app.py
```

For Microphone Access with http, you must use the localhost.

Inside a local Powershell, run:
```bash
ssh -L <PORT>:localhost:<PORT> <USERNAME>@dipa.th-brandenburg.de
```

PORT = port number, on which the streamlit application is running (see in other terminal)
USERNAME = Username on the Dipa-Server

and log in on the Dipa-Server.

Leave this local powershell open.

Open http://localhost:<PORT\>/ in your browser.

## Start Environment Simulation

```bash
PYTHONPATH=. streamlit run src/ui/simulation_app.py
```

Open the Network URL.

## Run Tests

```bash
PYTHONPATH=. python tests/\<test-name\>
```
