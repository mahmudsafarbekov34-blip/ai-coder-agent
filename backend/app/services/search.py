from __future__ import annotations

import httpx

from app.config import settings


def search_web(query: str, top_k: int = 5) -> list[dict[str, str]]:
    """Search the web using the configured provider.

    For now, Bing is the default implementation. If no API key is configured we return a
    safe, deterministic fallback result that keeps the system usable in local development.
    """
    if settings.search_provider.lower() != "bing" or not settings.bing_api_key:
        return [
            {
                "title": "Fallback result",
                "url": "https://example.com/search-result",
                "snippet": f"No search provider is configured for query: {query}",
            }
        ]

    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": settings.bing_api_key}
    params = {"q": query, "count": top_k}

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
        results: list[dict[str, str]] = []
        for item in payload.get("webPages", {}).get("value", [])[:top_k]:
            results.append(
                {
                    "title": item.get("name", "Untitled"),
                    "url": item.get("url", ""),
                    "snippet": item.get("snippet", ""),
                }
            )
        return results or [
            {
                "title": "Fallback result",
                "url": "https://example.com/search-result",
                "snippet": "Search returned no results.",
            }
        ]
    except Exception:
        return [
            {
                "title": "Search failed",
                "url": "https://example.com/search-result",
                "snippet": "External search is unavailable; this is a fallback result.",
            }
        ]
