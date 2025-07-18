# app/embeddings.py

import requests
from typing import Union, List, Optional
from app.utilities.config import load_config

class Embedder:
    """
    Generic embedder for text using a local or remote embedding server (e.g., Ollama, Nomic).
    Reads config from config.yaml.
    """

    def __init__(self, url: Optional[str] = None, model: Optional[str] = None):
        config = load_config()
        self.url = url or config.get("embedding_url", "http://localhost:11434/api/embeddings")
        self.model = model or config.get("embedding_model", "nomic-embed-text:v1.5")
        self.timeout = 15  # seconds

    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]], None]:
        """
        Embed text or list of texts. Returns embedding(s) or None on failure.

        Args:
            text (str or list of str): Text to embed.

        Returns:
            list of floats (for single input) or list of list of floats (for batch).
        """
        if not text:
            raise ValueError("No text provided for embedding.")

        is_batch = isinstance(text, list)
        payload = {"model": self.model, "prompt": text}

        try:
            r = requests.post(self.url, json=payload, timeout=self.timeout)
            r.raise_for_status()
            data = r.json()
            # Ollama/Nomic will return 'embedding' for single, 'embeddings' for batch
            if is_batch and "embeddings" in data:
                return data["embeddings"]
            elif not is_batch and "embedding" in data:
                return data["embedding"]
            else:
                raise ValueError(f"Unexpected embedding response format: {data}")
        except Exception as e:
            print(f"[EMBEDDINGS ERROR] {e}")
            return None

# Backwards compatible functional API if you want to use elsewhere:
_embedder = Embedder()

def get_embedding(text: Union[str, List[str]]):
    """
    Embed text or list of texts using default config.
    """
    return _embedder.embed(text)
