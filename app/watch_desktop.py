# app/watch_desktop.py

import os
from app.utilities.config import load_config
from app.queue import IngestQueue
from app.db import ChromaDatabase
from app.utilities.files import get_file_metadata, file_key

config = load_config()
FOLDERS = [os.path.expanduser(f) for f in config["folders"]]
SKIP_EXTS = tuple(config["skip_exts"])

def should_skip_file(path):
    return path.lower().endswith(SKIP_EXTS)

def scan_and_queue(queue: IngestQueue, db: ChromaDatabase):
    """
    Scan watched folders, skip files as per config,
    add any not-yet-learned files to the ingest queue.
    """
    for folder in FOLDERS:
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if not d.lower().endswith('.app')]
            for fname in files:
                path = os.path.join(root, fname)
                if should_skip_file(path):
                    print(f"[SKIP] {fname} — config-skip")
                    continue
                try:
                    metadata = get_file_metadata(path)
                    key = file_key(metadata)
                    if db.file_already_learned(key):
                        print(f"[SKIP] {fname} — already learned")
                        continue
                    queue.add_to_queue(path)
                    print(f"[QUEUE] {fname}")
                except Exception as e:
                    print(f"[ERROR] {fname}: {e}")

if __name__ == "__main__":
    queue = IngestQueue()
    db = ChromaDatabase()
    queue.init_queue()
    scan_and_queue(queue, db)
    print("[QUEUE] Scan complete.")
