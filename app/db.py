# app/db.py

import chromadb
import uuid
import os
from typing import Any, Dict, List, Optional, Union
from app.utilities.config import load_config

class ChromaDatabase:
    """
    Pluggable, config-driven wrapper for ChromaDB vector database.
    Supports adding, querying, and managing embedded documents for RAG.
    """

    def __init__(self, 
                 db_path: Optional[str] = None, 
                 collection_name: Optional[str] = None):
        """
        Args:
            db_path (str, optional): Path to ChromaDB folder. Reads from config if not provided.
            collection_name (str, optional): Name of Chroma collection to use.
        """
        config = load_config()
        self.db_path = db_path or os.environ.get(
            "CHROMA_DB_PATH", config.get("chroma_db_path", "chroma_data")
        )
        self.collection_name = collection_name or "assistant_data"
        try:
            self.client = chromadb.PersistentClient(path=self.db_path)
            self.collection = self.client.get_or_create_collection(self.collection_name)
        except Exception as e:
            print(f"[CHROMA ERROR] Could not connect to ChromaDB: {e}")
            raise

    def add_entry(
        self, 
        text: str, 
        embedding: List[float], 
        metadata: Dict[str, Any], 
        entry_id: Optional[str] = None
    ) -> str:
        """
        Add a new entry to the database.

        Args:
            text (str): The main document content.
            embedding (list of float): The vector embedding for the document.
            metadata (dict): Extra info for filtering/searching.
            entry_id (str, optional): Use your own UUID if you want.

        Returns:
            str: The entry's unique ID.
        """
        if entry_id is None:
            entry_id = str(uuid.uuid4())
        try:
            self.collection.add(
                embeddings=[embedding],
                documents=[text],
                ids=[entry_id],
                metadatas=[metadata]
            )
            return entry_id
        except Exception as e:
            print(f"[CHROMA ERROR] Add failed: {e}")
            return None

    def query_similar(
        self, 
        embedding: List[float], 
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find the most similar entries to a given embedding.

        Returns:
            List[dict]: Each with keys: text, metadata, distance
        """
        try:
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            output = []
            for doc, meta, dist in zip(
                results["documents"][0], results["metadatas"][0], results["distances"][0]
            ):
                output.append({
                    "text": doc,
                    "metadata": meta,
                    "distance": dist
                })
            return output
        except Exception as e:
            print(f"[CHROMA ERROR] Query failed: {e}")
            return []

    def get_by_id(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single entry by unique ID.

        Returns:
            dict or None
        """
        try:
            results = self.collection.get(ids=[entry_id], include=["documents", "metadatas"])
            if results["ids"]:
                return {
                    "id": results["ids"][0],
                    "text": results["documents"][0],
                    "metadata": results["metadatas"][0]
                }
            return None
        except Exception as e:
            print(f"[CHROMA ERROR] Get by ID failed: {e}")
            return None

    def all_entry_ids(self) -> List[str]:
        """Return all entry IDs in the collection."""
        try:
            return self.collection.get(include=[])["ids"]
        except Exception as e:
            print(f"[CHROMA ERROR] all_entry_ids failed: {e}")
            return []

    def delete_entry(self, entry_id: str) -> None:
        """Delete an entry by its unique ID."""
        try:
            self.collection.delete(ids=[entry_id])
        except Exception as e:
            print(f"[CHROMA ERROR] Delete failed: {e}")

    def file_already_learned(self, file_key: str) -> bool:
        """
        Returns True if a file with this file_key is already in the DB.

        Args:
            file_key (str): Unique key for the file.

        Returns:
            bool
        """
        try:
            results = self.collection.get(where={"file_key": file_key}, include=["metadatas"])
            return bool(results["ids"])
        except Exception as e:
            print(f"[CHROMA ERROR] file_already_learned failed: {e}")
            return False

