#!/usr/bin/env python3

import os
import json
import requests
from tqdm import tqdm
from PyPDF2 import PdfReader
from docx import Document

# --- CONFIG ---
SCAN_FOLDERS = [os.path.expanduser("~/Desktop")]
OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
NOMIC_MODEL = "nomic-embed-text"
SNIPPET_LEN = 500
OUT_PATH = os.path.expanduser("~/offline_assistant/data/file_embeddings.json")

def get_embedding(text):
    payload = {"model": NOMIC_MODEL, "prompt": text}
    r = requests.post(OLLAMA_EMBED_URL, json=payload)
    r.raise_for_status()
    return r.json()["embedding"]

def get_file_snippet(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext in [".txt", ".md", ".py", ".java", ".csv", ".json", ".log", ".html"]:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(SNIPPET_LEN).replace('\n', ' ')
        elif ext == ".pdf":
            reader = PdfReader(filepath)
            if reader.pages:
                text = reader.pages[0].extract_text() or ""
                return text[:SNIPPET_LEN].replace('\n', ' ')
        elif ext == ".docx":
            doc = Document(filepath)
            text = " ".join(p.text for p in doc.paragraphs[:10])
            return text[:SNIPPET_LEN].replace('\n', ' ')
    except Exception:
        return "[Error reading file]"
    return ""

def gather_files(folders):
    files = []
    for folder in folders:
        for root, dirs, filenames in os.walk(folder):
            dirs[:] = [
                d for d in dirs
                if not d.lower().endswith('.app')
                and not d.startswith('.')
                and d != 'node_modules'
            ]
            for fname in filenames:
                if fname.lower().endswith('.app') or fname.startswith('.'):
                    continue
                files.append(os.path.join(root, fname))
    return files

def file_metadata(path):
    stat = os.stat(path)
    return {
        "name": os.path.basename(path),
        "path": os.path.abspath(path),
        "ext": os.path.splitext(path)[1].lower(),
        "size": stat.st_size,
        "mtime": stat.st_mtime,
        "ctime": getattr(stat, 'st_ctime', stat.st_mtime),
        "parent": os.path.basename(os.path.dirname(path)),
        "parent_path": os.path.dirname(path)
    }

def main():
    files = gather_files(SCAN_FOLDERS)
    print(f"Found {len(files)} files.")
    data = []
    for path in tqdm(files, desc="Embedding files"):
        meta = file_metadata(path)
        snippet = get_file_snippet(path)
        prompt = (
            f"FILETYPE: {meta['ext']} | FILENAME: {meta['name']} | "
            f"PARENT: {meta['parent']} | SIZE: {meta['size']} bytes | "
            f"CONTENT: {snippet}"
        )
        try:
            emb = get_embedding(prompt)
        except Exception as e:
            print(f"[EMBED] Error embedding {path}: {e}")
            emb = []
        data.append({
            "meta": meta,
            "snippet": snippet,
            "embedding": emb
        })
    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} embedded files to {OUT_PATH}")

if __name__ == "__main__":
    main()
