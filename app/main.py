# app/main.py

from fastapi import FastAPI, Body
from app.db import add_entry, query_similar
from app.embeddings import get_embedding
from app.learn import learn_text
from app.watch_desktop import scan_and_queue
from app.ingest_files import process_next_file
from app.queue import init_queue, get_next_file
import uuid

app = FastAPI(title="Offline Assistant RAG API")

@app.post("/add")
def add_entry_endpoint(entry: dict = Body(...)):
    """
    Add a new note/task/log to memory.
    Example:
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
    Semantic search over learned entries.
    Example:
    { "query": "dog food reminder" }
    """
    q = query.get("query")
    if not q:
        return {"error": "Missing 'query'."}
    embedding = get_embedding(q)
    results = query_similar(embedding)
    return {"results": results}

@app.post("/learn")
def learn_endpoint(payload: dict = Body(...)):
    """
    Add a simple learning entry (used by watcher or tools).
    {
      "text": "something to learn",
      "metadata": {"type": "note", "tags": ["python"]}
    }
    """
    text = payload.get("text")
    metadata = payload.get("metadata", {})
    if not text:
        return {"error": "Missing 'text'"}
    return learn_text(text, metadata)

@app.post("/scan")
def run_full_scan():
    """
    Scan configured folders, queue new files, and ingest all unprocessed items.
    """
    init_queue()      # Ensure the queue DB exists
    scan_and_queue()  # Scan and queue files
    processed = 0
    while process_next_file():
        processed += 1
    return {"status": "complete", "processed": processed}


