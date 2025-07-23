"""
learn.py — Handles embedding text and storing in ChromaDB using modular classes.
"""

from typing import Dict, Any, Optional

class Learner:
    """
    Learner: Pipes new text through the embedder and stores it in the database.
    """

    def __init__(self, embedder, db):
        """
        Args:
            embedder: An Embedder instance (must have .embed(text))
            db: A database instance (must have .add_entry(...))
        """
        self.embedder = embedder
        self.db = db

    def learn_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Embed and store the given text + metadata.
        Returns dict with status and new entry ID.

        Args:
            text (str): The text to learn/store.
            metadata (dict, optional): Extra metadata for DB.

        Returns:
            dict: { "status": "success"|"error", "id": str or None }
        """
        if not metadata:
            metadata = {}
        try:
            embedding = self.embedder.embed(text)
            if embedding is None:
                raise Exception("Embedding failed.")
            entry_id = self.db.add_entry(text, embedding, metadata)
            if entry_id is None:
                raise Exception("DB insert failed.")
            return {"status": "success", "id": entry_id}
        except Exception as e:
            print(f"[LEARN ERROR] {e}")
            return {"status": "error", "id": None, "error": str(e)}

