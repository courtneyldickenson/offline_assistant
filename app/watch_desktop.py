import os
from app.utilities.config import load_config
from app.queue import add_to_queue, init_queue
from app.db import file_already_learned
from app.utilities.files import get_file_metadata, file_key

config = load_config()
FOLDERS = [os.path.expanduser(f) for f in config["folders"]]
SKIP_EXTS = tuple(config["skip_exts"])  # Correct usage for endswith

def should_skip_file(path):
    return path.lower().endswith(SKIP_EXTS)

def scan_and_queue():
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
                    if file_already_learned(key):
                        print(f"[SKIP] {fname} — already learned")
                        continue
                    add_to_queue(path)
                    print(f"[QUEUE] {fname}")
                except Exception as e:
                    print(f"[ERROR] {fname}: {e}")

if __name__ == "__main__":
    init_queue()
    scan_and_queue()
    print("[QUEUE] Scan complete.")
