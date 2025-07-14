from app.embeddings import get_embedding
from app.db import add_entry

'''

Pipe new text through the embedder and store it in Chroma

'''

def learn_text(text: str, metadata: dict = None):
    if not metadata:
        metadata = {}
    embedding = get_embedding(text)
    entry_id = add_entry(text, embedding, metadata)
    return {"status": "success", "id": entry_id}
