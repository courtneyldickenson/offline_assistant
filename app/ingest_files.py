# app/ingest_files.py

import os

from app.learn import learn_text


from app.learn import Learner
from app.embeddings import Embedder
from app.db import ChromaDatabase
from app.queue import IngestQueue
from app.utilities.files import get_file_metadata, parse_mtime_string, get_file_snippet
from app.utilities.config import load_config

config = load_config()
SKIP_EXTS = tuple(config["skip_exts"])

def should_skip_file(path):
    return path.lower().endswith(SKIP_EXTS)

def file_key(meta):
    return f"{meta['path']}|{meta['size']}|{int(meta['mtime'])}"

def process_next_file(queue: IngestQueue, learner: Learner, db: ChromaDatabase):
    """
    Process the next file in the ingest queue.
    - Skips unreadable or already-learned files
    - Extracts a snippet
    - Embeds and stores new content
    """
    path = queue.get_next_file()
    if not path:
        print("[QUEUE] No pending files.")
        return False

    if should_skip_file(path):
        print(f"[SKIP] {path} — app or executable")
        queue.mark_done(path)
        return True  # keep going!

    try:
        snippet = get_file_snippet(path)
        if not snippet.strip():
            print(f"[SKIP] {path} — empty or unreadable")
            queue.mark_done(path)
            return True

        metadata = get_file_metadata(path)
        if isinstance(metadata["mtime"], str):
            metadata["mtime"] = parse_mtime_string(metadata["mtime"])
        key = file_key(metadata)
        metadata["file_key"] = key

        if db.file_already_learned(key):
            print(f"[SKIP] {path} — already learned")
            queue.mark_done(path)
            return True

        result = learner.learn_text(snippet, metadata)
        if result["status"] == "success":
            print(f"[LEARNED] {metadata['name']} → {result['id']}")
        else:
            print(f"[ERROR] {metadata['name']} — {result.get('error', 'unknown error')}")
        queue.mark_done(path)
        return True

    except Exception as e:
        print(f"[ERROR] {path}: {e}")
        queue.mark_done(path)
        return True  # don't get stuck, just keep going

if __name__ == "__main__":
    queue = IngestQueue()
    db = ChromaDatabase()
    embedder = Embedder()
    learner = Learner(embedder, db)

    queue.init_queue()
    while process_next_file(queue, learner, db):
        pass
