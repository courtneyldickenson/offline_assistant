import os
from app.learn import learn_text
from app.utilities import get_file_snippet, get_file_metadata

FOLDER = os.path.expanduser("~/Desktop/Crochet_patterns")


def ingest_folder():
    for root, _, files in os.walk(FOLDER):
        for fname in files:
            path = os.path.join(root, fname)
            try:
                snippet = get_file_snippet(path)
                if snippet.strip():
                    metadata = get_file_metadata(path)
                    response = learn_text(snippet, metadata)
                    print(f"[LEARNED] {metadata['name']} → {response['id']}")
                else:
                    print(f"[SKIP] {fname} — empty or unreadable")
            except Exception as e:
                print(f"[ERROR] {fname}: {e}")

if __name__ == "__main__":
    ingest_folder()
