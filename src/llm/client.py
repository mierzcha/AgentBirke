import os
import requests
from dotenv import load_dotenv

load_dotenv()

class OllamaClient:
    """
    A class used to represent an Ollama Client
    """
    def __init__(self, url: str, model: str):
        """
        Parameters:
            url (str): The URL of Ollama
            model (str): The used Ollama Model
        """
        self.url = url or os.getenv("OLLAMA_URL","http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    def generate(self, prompt: str) -> str:
        """Sends a prompt to Ollama, returns the answer
        Parameters:
            prompt (str): A prompt for Ollama
        Returns:
            str: Answer from Ollama
        """
        response = requests.post(
            f"{self.url}/api/generate",
            json={"model":: self.model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return data["response"]
