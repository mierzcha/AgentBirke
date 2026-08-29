import os
import requests
from dotenv import load_dotenv


load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")


def test_ollama():
    print("Testing Ollama...")
    print(f"URL: {OLLAMA_URL}")
    print(f"Model: {OLLAMA_MODEL}")

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": "Sag kurz Hallo. Du bist die Testinstanz von Agent Birke.",
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        print("\nOllama funktioniert!")
        print("Antwort:")
        print(data["response"])

    except requests.exceptions.ConnectionError:
        print("\nFehler: Ollama ist nicht erreichbar.")
        print(f"Überprüfte URL: {OLLAMA_URL}")

    except requests.exceptions.Timeout:
        print("\nFehler: Ollama hat zu lange gebraucht.")

    except requests.exceptions.HTTPError as error:
        print(f"\nHTTP-Fehler: {error}")
        print(response.text)

    except Exception as error:
        print(f"\nUnerwarteter Fehler: {error}")


if __name__ == "__main__":
    test_ollama()
