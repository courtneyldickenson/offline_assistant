import os
from app.learn import learn_text
from app.utilities.file_snippets import get_file_snippet
from app.utilities.file_metadata import get_file_metadata
from app.utilities.config import load_config
from app.db import file_already_learned
from app.queue import get_next_file, mark_done, init_queue

config = load_config()
SKIP_EXTS = config["skip_exts"]

def should_skip_file(path):
    return path.lower().endswith(SKIP_EXTS)

def file_key(meta):
    return f"{meta['path']}|{meta['size']}|{int(meta['mtime'])}"

def process_next_file():
    path = get_next_file()
    if not path:
        print("[QUEUE] No pending files.")
        return

    if should_skip_file(path):
        print(f"[SKIP] {path} — app or executable")
        mark_done(path)
        return

    try:
        snippet = get_file_snippet(path)
        if not snippet.strip():
            print(f"[SKIP] {path} — empty or unreadable")
            mark_done(path)
            return

        metadata = get_file_metadata(path)
        key = file_key(metadata)
        metadata["file_key"] = key

        if file_already_learned(key):
            print(f"[SKIP] {path} — already learned")
            mark_done(path)
            return

        response = learn_text(snippet, metadata)
        print(f"[LEARNED] {metadata['name']} → {response['id']}")
        mark_done(path)

    except Exception as e:
        print(f"[ERROR] {path}: {e}")
        mark_done(path)

if __name__ == "__main__":
    init_queue()
    while True:
        process_next_file()
