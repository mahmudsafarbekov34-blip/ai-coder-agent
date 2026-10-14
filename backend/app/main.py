from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.chat import router as chat_router
from app.routes.health import router as health_router
from app.routes.sessions import router as sessions_router
from app.db import create_db_and_tables

app = FastAPI(title="AI Coder Agent", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(sessions_router, prefix="/api")


@app.on_event("startup")
def on_startup() -> None:
    # ensure database tables are created
    create_db_and_tables()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Coder Agent backend is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=True)
