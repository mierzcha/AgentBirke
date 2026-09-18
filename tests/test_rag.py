import os

import requests
from dotenv import load_dotenv


load_dotenv()


def main():
    url = os.getenv("OPENWEBUI_URL")
    api_key = os.getenv("OPENWEBUI_API_KEY")

    if not url:
        raise ValueError("OPENWEBUI_URL fehlt in .env")

    if not api_key:
        raise ValueError("OPENWEBUI_API_KEY fehlt in .env")

    response = requests.post(
        f"{url}/api/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama3.3:70b",
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Welche Maßnahmen wurden nach 1990 "
                        "zur Verbesserung der Wasserqualität "
                        "der Elbe eingeleitet?"
                    ),
                }
            ],
            "files": [
                {
                    "type": "collection",
                    "id": "ee2b5ac5-6bcc-42a8-ba24-6b11d3680a2e",
                }
            ],
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    answer = data["choices"][0]["message"]["content"]

    print("Antwort:")
    print(answer)


if __name__ == "__main__":
    main()