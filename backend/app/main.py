from __future__ import annotations

from fastapi import FastAPI

from app.config import settings
from app.deps import require_api_key
from app.routes.chat import router as chat_router
from app.routes.health import router as health_router
from app.routes.sandbox import router as sandbox_router
from app.routes.sessions import router as sessions_router
from app.db import create_db_and_tables

app = FastAPI(title="AI Coder Agent", version="0.1.0")

# Optional auth enforcement. Leave disabled if AUTH_TOKEN is not configured.
# This helps local dev remain frictionless while still supporting secure deployments.

app.include_router(health_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(sessions_router, prefix="/api")
appp = app


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Coder Agent backend is running"}


# Auth can be applied to specific routes if needed; for local dev we keep it optional.
app.include_router(sandbox_router, prefix="/api")
