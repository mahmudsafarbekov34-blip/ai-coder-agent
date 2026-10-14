from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.db import db

router = APIRouter(tags=["sessions"])


@router.get("/sessions/{session_id}")
def get_session(session_id: str) -> dict[str, Any]:
    session = db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
