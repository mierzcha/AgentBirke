# AgentBirke

Version 0 (WIP)

## Create Virtual Environment

Agent Birke requires Python 3.11 to run.

python3.11 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

## Install Requirements

pip install -r requirements.txt

## Signalspeicher initialisieren

data/database/signals.db ist die Signalspeicher-Datenbank.
Sie wird initialisiert mit:

python scripts/init_database.py

TODO Verbindung

## Open WebUI einrichten

pip install open-webui

pip install pysqlite3-binary

docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
Unable to find image 'ghcr.io/open-webui/open-webui:main' locally
main: Pulling from open-webui/open-webui

visit localhost:3000
create Administrator Account
Create an API Key




