import os
import time
from PyPDF2 import PdfReader
from docx import Document

def get_file_snippet(filepath, snippet_len=500):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext in [".txt", ".md", ".py", ".java", ".csv", ".json", ".log", ".html"]:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(snippet_len).replace('\n', ' ')
        elif ext == ".pdf":
            reader = PdfReader(filepath)
            if reader.pages:
                text = reader.pages[0].extract_text() or ""
                return text[:snippet_len].replace('\n', ' ')
        elif ext == ".docx":
            doc = Document(filepath)
            text = " ".join(p.text for p in doc.paragraphs[:10])
            return text[:snippet_len].replace('\n', ' ')
    except Exception:
        return "[Error reading file]"
    return ""

def get_file_metadata(path):
    stat = os.stat(path)
    ext = os.path.splitext(path)[1].lower()
    size = stat.st_size
    mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
    ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(getattr(stat, 'st_ctime', stat.st_mtime)))
    parent = os.path.basename(os.path.dirname(path))
    parent_path = os.path.dirname(path)
    return {
        "name": os.path.basename(path),
        "path": os.path.abspath(path),
        "ext": ext,
        "size": size,
        "mtime": mtime,
        "ctime": ctime,
        "parent": parent,
        "parent_path": parent_path
    }
