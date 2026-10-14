from __future__ import annotations

from datetime import datetime
import json
from typing import Any

from sqlmodel import SQLModel, Field, Session as SQLSession, create_engine, select

from app.config import settings

DATABASE_URL = settings.database_url or "sqlite:///./data.db"

# sqlite needs check_same_thread flag. For postgres this is ignored.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


class SessionModel(SQLModel, table=True):
    id: str = Field(primary_key=True)
    last_message: str | None = None
    last_response: str | None = None
    sources: str | None = None  # JSON serialized list
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def save_session(session_id: str, payload: dict[str, Any]) -> None:
    now = datetime.utcnow()
    with SQLSession(engine) as session:
        obj = session.get(SessionModel, session_id)
        sources = payload.get("sources") or []
        if obj:
            obj.last_message = payload.get("last_message")
            obj.last_response = payload.get("last_response")
            obj.sources = json.dumps(sources)
            obj.updated_at = now
        else:
            obj = SessionModel(
                id=session_id,
                last_message=payload.get("last_message"),
                last_response=payload.get("last_response"),
                sources=json.dumps(sources),
                created_at=now,
                updated_at=now,
            )
            session.add(obj)
        session.commit()


def get_session(session_id: str) -> dict[str, Any] | None:
    with SQLSession(engine) as session:
        obj = session.get(SessionModel, session_id)
        if not obj:
            return None
        return {
            "session_id": obj.id,
            "last_message": obj.last_message,
            "last_response": obj.last_response,
            "sources": json.loads(obj.sources) if obj.sources else [],
            "created_at": obj.created_at.isoformat(),
            "updated_at": obj.updated_at.isoformat(),
        }
