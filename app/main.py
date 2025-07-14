from fastapi import FastAPI, Body
from app.db import add_entry, query_similar
from app.embeddings import get_embedding
import uuid

app = FastAPI(title="Offline Assistant RAG API")

@app.post("/add")
def add_entry_endpoint(entry: dict = Body(...)):
    """
    Add a new note/task/log. Example:
    {
      "text": "Water the cucumbers every morning.",
      "type": "note",
      "date": "2025-07-14",
      "tags": ["plants", "routine"]
    }
    """
    text = entry.get("text")
    if not text:
        return {"error": "Missing 'text'."}
    embedding = get_embedding(text)
    metadata = {k: v for k, v in entry.items() if k not in ["text", "embedding", "id"]}
    entry_id = entry.get("id") or str(uuid.uuid4())
    add_entry(text, embedding, metadata, entry_id)
    return {"status": "success", "id": entry_id}

@app.post("/search")
def search_endpoint(query: dict = Body(...)):
    """
    Search for relevant notes/tasks/logs.
    Example:
    { "query": "dog food reminder" }
    """
    q = query.get("query")
    if not q:
        return {"error": "Missing 'query'."}
    embedding = get_embedding(q)
    results = query_similar(embedding)
    return {"results": results}
