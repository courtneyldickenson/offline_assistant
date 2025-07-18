# app/utilities/files.py

import os
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional

# Optional: PDF and DOCX extraction support
try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

def get_file_metadata(path: str) -> Dict[str, Any]:
    """
    Return a metadata dict for the file at 'path'.
    Includes:
        - name: Filename only
        - path: Full path
        - mtime: Last modified time as a UNIX timestamp (int)
        - size: File size in bytes (int)
    """
    stat = os.stat(path)
    return {
        "name": os.path.basename(path),
        "path": os.path.abspath(path),
        "mtime": int(stat.st_mtime),
        "size": stat.st_size
    }

def file_key(meta: Dict[str, Any]) -> str:
    """
    Return a unique key for the file based on name, size, and mtime.
    """
    key_str = f"{meta['name']}:{meta['size']}:{int(meta['mtime'])}"
    return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

def parse_mtime_string(mtime_str: str) -> int:
    """
    Convert 'YYYY-MM-DD HH:MM:SS' string to UNIX timestamp (int).
    """
    dt = datetime.strptime(mtime_str, "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp())

def get_file_snippet(filepath: str, snippet_len: int = 500) -> str:
    """
    Extract a text snippet from a file for embedding/preview.
    Handles .txt, .md, .py, .csv, .json, .log, .html, .pdf, and .docx.
    Returns: A string of up to `snippet_len` chars, or error string.
    """
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext in [".txt", ".md", ".py", ".java", ".csv", ".json", ".log", ".html"]:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(snippet_len).replace('\n', ' ')
        elif ext == ".pdf" and PdfReader:
            reader = PdfReader(filepath)
            if reader.pages:
                text = reader.pages[0].extract_text() or ""
                return text[:snippet_len].replace('\n', ' ')
        elif ext == ".docx" and Document:
            doc = Document(filepath)
            text = " ".join(p.text for p in doc.paragraphs[:10])
            return text[:snippet_len].replace('\n', ' ')
        else:
            return f"[Error: Unsupported file type {ext}]"
    except Exception as e:
        return f"[Error reading file: {e}]"
