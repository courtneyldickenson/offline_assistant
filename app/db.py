# app/db.py

import chromadb
import uuid

# Initialize ChromaDB persistent client (data will be stored in ./chroma_data/)
client = chromadb.PersistentClient(path="chroma_data")

# You can use one collection for all data, or create more if you want to separate types
collection = client.get_or_create_collection("assistant_data")


def add_entry(text, embedding, metadata, entry_id=None):
    """
    Add a new entry to the database.
    - text: the main content (string)
    - embedding: list of floats
    - metadata: dict (e.g., {"type": "note", "date": "2025-07-14", ...})
    - entry_id: unique string. If None, a UUID will be generated.
    """
    if entry_id is None:
        entry_id = str(uuid.uuid4())
    collection.add(
        embeddings=[embedding],
        documents=[text],
        ids=[entry_id],
        metadatas=[metadata]
    )
    return entry_id


def query_similar(embedding, n_results=5):
    """
    Find the most similar entries to the given embedding.
    Returns a list of dicts with: text, metadata, distance.
    """
    results = collection.query(
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


def get_by_id(entry_id):
    """
    Retrieve a single entry by its unique ID.
    Returns a dict with text, metadata, and id.
    """
    results = collection.get(ids=[entry_id], include=["documents", "metadatas"])
    if results["ids"]:
        return {
            "id": results["ids"][0],
            "text": results["documents"][0],
            "metadata": results["metadatas"][0]
        }
    return None


def all_entry_ids():
    """Return all entry IDs in the collection."""
    return collection.get(include=[])["ids"]


def delete_entry(entry_id):
    """Delete an entry by its unique ID."""
    collection.delete(ids=[entry_id])

