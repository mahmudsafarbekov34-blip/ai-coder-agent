from __future__ import annotations

import os


def get_api_key() -> str | None:
    return os.getenv("AUTH_TOKEN") or None


def is_auth_enabled() -> bool:
    return (os.getenv("AUTH_TOKEN") or "").strip() != ""


def validate_api_key(token: str | None) -> bool:
    if not is_auth_enabled():
        return True
    candidate = (token or "").replace("Bearer ", "").strip()
    return candidate == get_api_key()
