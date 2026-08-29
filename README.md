# AgentBirke

Version 0

Agent Birke requires Python 3.11 to run.

Install other Requirements with

pip install -r requirements.txt

# Open WebUI einrichten

pip install open-webui

pip install pysqlite3-binary

TODO: venv?

docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
Unable to find image 'ghcr.io/open-webui/open-webui:main' locally
main: Pulling from open-webui/open-webui

visit localhost:3000
create Administrator Account
Create an API Key

# Signalspeicher initialisieren

python3 scripts/init_database.py
