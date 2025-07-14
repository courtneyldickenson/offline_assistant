# app/main.py

from fastapi import FastAPI, Body
from app.rag import rag_query
import json
from pathlib import Path

DATA_PATH = Path("data/sample_data.json")

app = FastAPI(title="RAG Assistant API")

@app.get("/query")
def query(q: str):
    return rag_query(q)

@app.post("/add")
def add_entry(entry: dict = Body(...)):
    """
    Add a new note, task, or log to sample_data.json.
    Example body:
    {
      "type": "note",
      "text": "Something new I learned.",
      "date": "2025-07-15",
      "tags": ["learning"]
    }
    """
    # Load existing data
    if DATA_PATH.exists():
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []
    # Append new entry
    data.append(entry)
    # Save it back
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)
    return {"status": "success", "entry": entry}
