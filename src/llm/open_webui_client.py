import os
import requests
from dotenv import load_dotenv

load_dotenv()

class OpenWebUIClient:
    """Client for sending chat requests to Open WebUI."""
    def __init__(
        self, url: str | None = None, api_key: str | None = None, model: str | None = None, knowledge_id: str | None = None):
        """
        Parameters:
            url: URL of the Open WebUI instance.
            api_key: API key for Open WebUI.
            model: LLM model used by Open WebUI.
            knowledge_id: ID of the Knowledge Base used for RAG.
        """
        self.url = url or os.getenv("OPENWEBUI_URL")
        self.api_key = api_key or os.getenv("OPENWEBUI_API_KEY")
        self.model = model or os.getenv("OPENWEBUI_MODEL", "llama3.3:70b")
        self.knowledge_id = knowledge_id or os.getenv("OPENWEBUI_KNOWLEDGE_ID")
        if not self.url:
            raise ValueError("OPENWEBUI_URL fehlt in .env")
        if not self.api_key:
            raise ValueError("OPENWEBUI_API_KEY fehlt in .env")
        if not self.knowledge_id:
            raise ValueError("OPENWEBUI_KNOWLEDGE_ID fehlt in .env")

    def generate(self, prompt: str) -> str:
        """Send a prompt to Open WebUI and return the generated answer."""
        response = requests.post(
            f"{self.url}/api/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "files": [
                    {
                        "type": "collection",
                        "id": self.knowledge_id,
                    }
                ],
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]