import pytest

from app.db import ChromaDatabase
from app.learn import Learner

# --- Metadata helper ---
def make_chroma_metadata(meta: dict) -> dict:
    clean = {}
    for k, v in meta.items():
        if isinstance(v, list):
            clean[k] = ",".join(str(i) for i in v)
        elif isinstance(v, (str, int, float, bool)) or v is None:
            clean[k] = v
        else:
            clean[k] = str(v)
    return clean

class MockEmbedder:
    def embed(self, text: str):
        return [0.1] * 256  # dummy vector

TEST_TEXT = "This is a test note about hydroponics."
TEST_META = {"type": "note", "tags": ["test", "hydroponics"]}

def test_embedder_returns_embedding():
    embedder = MockEmbedder()
    vec = embedder.embed(TEST_TEXT)
    assert isinstance(vec, list)
    assert all(isinstance(x, float) for x in vec)
    assert len(vec) > 10

def test_db_add_and_query(tmp_path):
    db = ChromaDatabase(db_path=tmp_path / "test_chroma_data")
    dummy_vec = [0.1] * 256
    entry_id = db.add_entry(TEST_TEXT, dummy_vec, make_chroma_metadata(TEST_META))
    assert isinstance(entry_id, str)
    results = db.query_similar(dummy_vec)
    assert results
    assert any(r["metadata"]["type"] == "note" for r in results)

def test_learn_pipeline(tmp_path):
    embedder = MockEmbedder()
    db = ChromaDatabase(db_path=tmp_path / "test_chroma_data2")
    learner = Learner(embedder, db)
    result = learner.learn_text(TEST_TEXT, make_chroma_metadata(TEST_META))
    assert result["status"] == "success"
    vec = embedder.embed(TEST_TEXT)
    found = db.query_similar(vec)
    assert found
    assert any("hydroponics" in r["metadata"].get("tags", "") for r in found)
