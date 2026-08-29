import os
import requests
from dotenv import load_dotenv

load_dotenv()

class OllamaClient:
    """
    A class used to represent an Ollama Client

    Attributes

    says_str : str
        a formatted string to print out what the animal says
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
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
