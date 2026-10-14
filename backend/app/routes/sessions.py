from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db import get_session

router = APIRouter(tags=["sessions"])


@router.get("/sessions/{session_id}")
def get_session_route(session_id: str) -> dict[str, object]:
    session = get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
