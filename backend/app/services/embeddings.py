import os
from typing import List

import openai
from app.config import settings


def embed_text(text: str) -> List[float]:
    """Create embeddings using OpenAI Embeddings API.

    Returns a list[float]. On failure, returns a small deterministic vector fallback.
    """
    if not settings.openai_api_key:
        # fallback deterministic vector for scaffold/testing
        return [float(len(text) % 256) / 255.0]

    openai.api_key = settings.openai_api_key
    model = getattr(settings, "embedding_model", "text-embedding-3-small")

    try:
        resp = openai.Embedding.create(model=model, input=text)
        return resp.data[0].embedding
    except Exception:
        # fallback
        return [float(len(text) % 256) / 255.0]
