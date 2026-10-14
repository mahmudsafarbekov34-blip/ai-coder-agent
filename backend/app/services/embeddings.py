from __future__ import annotations

from openai import OpenAI

from app.config import settings


def embed_text(text: str) -> list[float]:
    """Create embeddings using the OpenAI embeddings API when configured."""
    if not settings.openai_api_key:
        return [float(len(text) % 256) / 255.0]

    client = OpenAI(api_key=settings.openai_api_key)
    try:
        response = client.embeddings.create(
            model=settings.embedding_model,
            input=text,
        )
        return list(response.data[0].embedding)
    except Exception:
        return [float(len(text) % 256) / 255.0]
