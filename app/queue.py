import sqlite3
import os

QUEUE_DB = os.environ.get("QUEUE_DB", "ingest_queue.sqlite3")

def init_queue():
    conn = sqlite3.connect(QUEUE_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

def add_to_queue(path):
    conn = sqlite3.connect(QUEUE_DB)
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO files (path) VALUES (?)", (path,))
        conn.commit()
    finally:
        conn.close()

def get_next_file():
    conn = sqlite3.connect(QUEUE_DB)
    c = conn.cursor()
    c.execute("SELECT path FROM files WHERE status='pending' LIMIT 1")
    row = c.fetchone()
    if row:
        path = row[0]
        c.execute("UPDATE files SET status='processing' WHERE path=?", (path,))
        conn.commit()
        conn.close()
        return path
    conn.close()
    return None

def mark_done(path):
    conn = sqlite3.connect(QUEUE_DB)
    c = conn.cursor()
    c.execute("UPDATE files SET status='done' WHERE path=?", (path,))
    conn.commit()
    conn.close()
