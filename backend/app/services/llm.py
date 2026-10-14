from __future__ import annotations

from openai import OpenAI

from app.config import settings


def generate_response(prompt: str, system_prompt: str | None = None) -> str:
    """Generate a completion using the OpenAI chat API.

    This intentionally falls back to a scaffold message when no API key is configured,
    so that local development and tests continue to work.
    """
    if not settings.openai_api_key:
        return (
            "AI model provider is not configured yet. "
            "Add OPENAI_API_KEY in the environment to enable the real model."
        )

    client = OpenAI(api_key=settings.openai_api_key)
    messages: list[dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=settings.model_name,
            messages=messages,
            temperature=0.2,
            max_tokens=800,
        )
        content = response.choices[0].message.content
        return (content or "").strip() or "No response returned by the model."
    except Exception as exc:  # pragma: no cover - external call
        return f"LLM call failed: {exc}"
