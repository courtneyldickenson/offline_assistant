# app/utilities/file_metadata.py
import os
import time

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
