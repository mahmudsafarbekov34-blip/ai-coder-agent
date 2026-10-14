"""Simple Pinecone-backed vector store wrapper.

This is scaffolding — ensure PINECONE_API_KEY and PINECONE_ENV are set before using.
"""
from typing import List, Optional

from app.config import settings

try:
    import pinecone
except Exception:  # pragma: no cover - optional dependency
    pinecone = None


class VectorStore:
    def __init__(self):
        if not settings.pinecone_api_key or not settings.pinecone_env:
            self._client = None
            return

        if pinecone is None:
            raise RuntimeError("pinecone client is not installed")

        pinecone.init(api_key=settings.pinecone_api_key, environment=settings.pinecone_env)
        self._index_name = settings.pinecone_index
        self._index = pinecone.Index(self._index_name)

    def upsert(self, ids: List[str], vectors: List[List[float]], metadata: Optional[List[dict]] = None):
        if self._index is None:
            return None
        items = []
        for i, vec in enumerate(vectors):
            meta = metadata[i] if metadata and i < len(metadata) else None
            items.append((ids[i], vec, meta))
        return self._index.upsert(items=items)

    def query(self, vector: List[float], top_k: int = 5, include_metadata: bool = True):
        if self._index is None:
            return []
        return self._index.query(vector=vector, top_k=top_k, include_metadata=include_metadata)


# Convenience singleton
_vector_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
