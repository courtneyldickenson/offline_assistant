# app/queue.py

import sqlite3
import os
from typing import Optional
from app.utilities.config import load_config

class IngestQueue:
    """
    A modular, SQLite-backed queue for ingest jobs. 
    Reads DB location from config or environment, with full error handling.
    """

    def __init__(self, db_path: Optional[str] = None):
        config = load_config()
        self.db_path = db_path or os.environ.get(
            "QUEUE_DB", config.get("queue_db", "ingest_queue.sqlite3")
        )
        self.init_queue()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def init_queue(self):
        """Initialize the queue table if it doesn't exist."""
        try:
            conn = self._connect()
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY,
                    path TEXT UNIQUE,
                    status TEXT DEFAULT 'pending'
                )
            ''')
            conn.commit()
        except Exception as e:
            print(f"[QUEUE ERROR] Failed to initialize queue: {e}")
        finally:
            conn.close()

    def add_to_queue(self, path: str):
        """Add a file to the queue if not already present."""
        try:
            conn = self._connect()
            c = conn.cursor()
            c.execute("INSERT OR IGNORE INTO files (path) VALUES (?)", (path,))
            conn.commit()
        except Exception as e:
            print(f"[QUEUE ERROR] Failed to add '{path}': {e}")
        finally:
            conn.close()

    def get_next_file(self) -> Optional[str]:
        """
        Get the next pending file and mark as 'processing'.
        Returns None if queue is empty.
        """
        try:
            conn = self._connect()
            c = conn.cursor()
            c.execute("SELECT path FROM files WHERE status='pending' LIMIT 1")
            row = c.fetchone()
            if row:
                path = row[0]
                c.execute("UPDATE files SET status='processing' WHERE path=?", (path,))
                conn.commit()
                return path
            return None
        except Exception as e:
            print(f"[QUEUE ERROR] Failed to get next file: {e}")
            return None
        finally:
            conn.close()

    def mark_done(self, path: str):
        """Mark the given file as processed."""
        try:
            conn = self._connect()
            c = conn.cursor()
            c.execute("UPDATE files SET status='done' WHERE path=?", (path,))
            conn.commit()
        except Exception as e:
            print(f"[QUEUE ERROR] Failed to mark '{path}' as done: {e}")
        finally:
            conn.close()

    def __len__(self):
        """
        Return the number of files in the queue with status 'pending' or 'processing'.
        """
        try:
            conn = self._connect()
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM files WHERE status IN ('pending', 'processing')")
            count = c.fetchone()[0]
            return count
        except Exception as e:
            print(f"[QUEUE ERROR] Failed to get queue length: {e}")
            return 0
        finally:
            conn.close()


# Backwards-compatible procedural API
try:
    _queue = IngestQueue()
    def init_queue():
        _queue.init_queue()

    def add_to_queue(path):
        _queue.add_to_queue(path)

    def get_next_file():
        return _queue.get_next_file()

    def mark_done(path):
        _queue.mark_done(path)
except Exception:
    pass
