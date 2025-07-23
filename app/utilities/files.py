# app/utilities/files.py

import os
import hashlib
from datetime import datetime

def get_file_metadata(path):
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
        "mtime": int(stat.st_mtime),  # Numeric UNIX timestamp
        "size": stat.st_size
    }

def get_file_snippet(path, max_length=500):
    """
    Return a snippet (up to max_length characters) from the file at 'path'.
    Attempts UTF-8 read first, then falls back to latin-1.
    Returns empty string if file is binary or unreadable.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            snippet = f.read(max_length)
            # Check if file looks like text: no weird binary chars
            if any(ord(c) < 9 for c in snippet):  # basic control chars check
                return ""
            return snippet
    except UnicodeDecodeError:
        # Try a fallback encoding
        try:
            with open(path, "r", encoding="latin-1") as f:
                snippet = f.read(max_length)
                return snippet
        except Exception:
            return ""
    except Exception:
        return ""


def file_key(meta):
    """
    Return a unique key for the file based on name, size, and mtime.
    """
    # Use mtime as integer, safe for hashing
    key_str = f"{meta['name']}:{meta['size']}:{int(meta['mtime'])}"
    return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

# Optionally: function to convert string mtime to timestamp if needed
def parse_mtime_string(mtime_str):
    """
    Convert 'YYYY-MM-DD HH:MM:SS' string to UNIX timestamp (int).
    """
    dt = datetime.strptime(mtime_str, "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp())
