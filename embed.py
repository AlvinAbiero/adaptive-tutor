import requests

OLLAMA_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "nomic-embed-text"

def embed(texts):
    r = requests.post(
        OLLAMA_URL, 
        json={"model": EMBED_MODEL, "input": texts}, 
        timeout=120
        )
    r.raise_for_status()
    return r.json()["embeddings"]