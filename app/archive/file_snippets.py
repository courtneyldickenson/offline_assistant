# app/utilities/file_snippets.py
import os
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
