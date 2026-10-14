from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_requires_message() -> None:
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"].lower()
