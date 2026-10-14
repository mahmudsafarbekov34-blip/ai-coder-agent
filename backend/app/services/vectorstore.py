from __future__ import annotations

from typing import Any

try:
    import pinecone
except Exception:  # pragma: no cover - optional dependency
    pinecone = None

from app.config import settings


class VectorStore:
    def __init__(self) -> None:
        self._index = None
        if not settings.pinecone_api_key:
            return
        if not settings.pinecone_env:
            raise ValueError("PINECONE_ENV must be set when Pinecone is enabled.")
        if pinecone is None:
            raise RuntimeError("pinecone-client is not installed")

        pinecone.init(api_key=settings.pinecone_api_key, environment=settings.pinecone_env)
        self._index = pinecone.Index(settings.pinecone_index)

    def upsert(self, ids: list[str], vectors: list[list[float]], metadata: list[dict[str, Any]] | None = None):
        if self._index is None:
            return None
        items = []
        for idx, vec in enumerate(vectors):
            item_meta = metadata[idx] if metadata and idx < len(metadata) else None
            items.append((ids[idx], vec, item_meta))
        return self._index.upsert(items=items)

    def query(self, vector: list[float], top_k: int = 5, include_metadata: bool = True):
        if self._index is None:
            return []
        return self._index.query(vector=vector, top_k=top_k, include_metadata=include_metadata)


_vector_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
