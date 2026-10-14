from app.config import settings
import openai
from typing import List


def _ensure_key():
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in environment")


def generate_response(prompt: str, system_prompt: str | None = None) -> str:
    """Call OpenAI Chat API to generate a response. Falls back to scaffold message if key missing.

    Replace or extend with streaming, tool usage, safety checks, and RAG context injection.
    """
    if not settings.openai_api_key:
        # fallback to scaffold message
        return (
            "AI model provider is not configured yet. "
            "Add OPENAI_API_KEY in the environment and connect the real model provider."
        )

    openai.api_key = settings.openai_api_key

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        resp = openai.ChatCompletion.create(
            model=settings.model_name,
            messages=messages,
            max_tokens=800,
            temperature=0.2,
        )
        # API returns choices
        text = resp.choices[0].message.get("content", "").strip()
        return text
    except Exception as exc:  # pragma: no cover - external call
        return f"LLM call failed: {exc}"
