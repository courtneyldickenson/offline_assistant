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
    return path.lower().endswith(tuple(SKIP_EXTS))

def file_key(meta):
    return f"{meta['path']}|{meta['size']}|{int(meta['mtime'])}"

def process_next_file():
    path = get_next_file()
    if not path:
        print("[QUEUE] No pending files.")
        return False

    if should_skip_file(path):
        print(f"[SKIP] {path} — app or executable")
        mark_done(path)
        return True  # keep going!

    try:
        snippet = get_file_snippet(path)
        if not snippet.strip():
            print(f"[SKIP] {path} — empty or unreadable")
            mark_done(path)
            return True

        metadata = get_file_metadata(path)  # returns mtime as string

        # Convert mtime string to int
        from app.utilities.files import parse_mtime_string
        metadata["mtime"] = parse_mtime_string(metadata["mtime"])
        key = file_key(metadata)


        metadata["file_key"] = key

        if file_already_learned(key):
            print(f"[SKIP] {path} — already learned")
            mark_done(path)
            return True

        response = learn_text(snippet, metadata)
        print(f"[LEARNED] {metadata['name']} → {response['id']}")
        mark_done(path)
        return True

    except Exception as e:
        print(f"[ERROR] {path}: {e}")
        return True  # don't get stuck, just keep going

if __name__ == "__main__":
    init_queue()
    while process_next_file():
        pass
