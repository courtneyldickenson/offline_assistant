# app/main.py

from fastapi import FastAPI, Body
from app.embeddings import Embedder
from app.db import ChromaDatabase
from app.learn import Learner
from app.queue import IngestQueue
from app.watch_desktop import scan_and_queue
from app.ingest_files import process_next_file

app = FastAPI(title="Offline Assistant RAG API")

# init pipelien
embedder = Embedder()
db = ChromaDatabase()
learner = Learner(embedder, db)
queue = IngestQueue()

@app.post("/add")
def add_entry_endpoint(entry: dict = Body(...)):
    """
    Add a new note/task/log to memory.
    Body example:
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
    metadata = {k: v for k, v in entry.items() if k not in ["text", "embedding", "id"]}
    result = learner.learn_text(text, metadata)
    return result

@app.post("/search")
def search_endpoint(query: dict = Body(...)):
    """
    Semantic search over learned entries.
    Body example:
    { "query": "dog food reminder" }
    """
    q = query.get("query")
    if not q:
        return {"error": "Missing 'query'."}
    embedding = embedder.embed(q)
    results = db.query_similar(embedding)
    return {"results": results}

@app.post("/learn")
def learn_endpoint(payload: dict = Body(...)):
    """
    Add a simple learning entry (used by watcher or tools).
    Body example:
    {
      "text": "something to learn",
      "metadata": {"type": "note", "tags": ["python"]}
    }
    """
    text = payload.get("text")
    metadata = payload.get("metadata", {})
    if not text:
        return {"error": "Missing 'text'"}
    return learner.learn_text(text, metadata)

@app.post("/scan")
def run_full_scan():
    """
    Scan configured folders, queue new files, and ingest all unprocessed items.
    """
    queue.init_queue()
    scan_and_queue(queue, db)
    processed = 0
    while process_next_file(queue, learner, db):
        processed += 1
    return {"status": "complete", "processed": processed}

@app.get("/health")
def health_check():
    """
    Health check endpoint for API, DB, and embedding server.
    Returns basic service availability.
    """
    health = {}
    # LLM health
    try:
        embedding = embedder.embed("test")
        health["embedding_server"] = "ok" if embedding else "fail"
    except Exception as e:
        health["embedding_server"] = f"fail: {e}"
    # Chroma health
    try:
        db.all_entry_ids()
        health["chroma_db"] = "ok"
    except Exception as e:
        health["chroma_db"] = f"fail: {e}"
    # Queue health
    try:
        queue.init_queue()
        health["queue"] = "ok"
    except Exception as e:
        health["queue"] = f"fail: {e}"
    return health
