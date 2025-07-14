import requests

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
NOMIC_MODEL = "nomic-embed-text"

def get_embedding(text):
    payload = {"model": NOMIC_MODEL, "prompt": text}
    r = requests.post(OLLAMA_EMBED_URL, json=payload)
    r.raise_for_status()
    return r.json()["embedding"]
