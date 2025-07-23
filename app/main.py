# app/main.py

from fastapi import FastAPI, Body
from app.embeddings import Embedder
from app.db import ChromaDatabase
from app.learn import Learner
from app.queue import IngestQueue
from app.watch_desktop import scan_and_queue
from app.ingest_files import process_next_file

import threading
import time

app = FastAPI(title="Offline Assistant RAG API")

# --- INIT PIPELINE ---
embedder = Embedder()
db = ChromaDatabase()
learner = Learner(embedder, db)
queue = IngestQueue()

# --- BACKGROUND QUEUE WORKER ---
def queue_worker():
    while True:
        try:
            if len(queue) > 0:
                processed = process_next_file(queue, learner, db)
                # Optionally log or print progress
                if not processed:
                    time.sleep(1)
            else:
                time.sleep(1)
        except Exception as e:
            print("[Queue Worker Error]", e)
            time.sleep(2)

threading.Thread(target=queue_worker, daemon=True).start()

# --- ENDPOINTS ---

@app.post("/add")
def add_entry_endpoint(entry: dict = Body(...)):
    """
    Add a new note/task/log to memory.
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
    """
    text = payload.get("text")
    metadata = payload.get("metadata", {})
    if not text:
        return {"error": "Missing 'text'"}
    return learner.learn_text(text, metadata)

@app.post("/scan")
def run_full_scan():
    """
    Scan folders and queue new files for background ingestion.
    Returns immediately; ingestion happens in the background.
    """
    queue.init_queue()
    scan_and_queue(queue, db)
    # Do NOT drain the queue here, let the worker do it!
    return {"status": "queued", "queue_length": len(queue)}

@app.get("/health")
def health_check():
    """
    Health check endpoint for API, DB, embedding server, and queue.
    """
    health = {}
    # LLM health
    try:
        embedding = embedder.embed("test")
        health["embedding_server"] = "ok" if embedding is not None else "fail"
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
        qlen = len(queue)
        health["queue"] = f"processing ({qlen} files)" if qlen > 0 else "idle"
    except Exception as e:
        health["queue"] = f"fail: {e}"
    return health
