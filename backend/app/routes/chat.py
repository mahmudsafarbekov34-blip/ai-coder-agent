from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException

from app.db import db
from app.models import ChatRequest, ChatResponse
from app.services.embeddings import embed_text
from app.services.llm import generate_response
from app.services.search import search_web
from app.services.vectorstore import get_vector_store

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    session_id = request.session_id or str(uuid.uuid4())

    # Search & retrieval step (best-effort, safe fallback)
    search_results = search_web(request.message, top_k=3)
    context_text = "\n".join(
        f"{item['title']}: {item['snippet']} ({item['url']})" for item in search_results
    )
    vector = embed_text(request.message)

    # Best effort vector store write/query
    try:
        vector_store = get_vector_store()
        vector_store.upsert([session_id], [vector], metadata=[{"text": request.message, "session_id": session_id}])
        query_result = vector_store.query(vector, top_k=3)
        if query_result:
            for item in query_result.get("matches", []):
                meta = item.get("metadata")
                if meta and meta.get("url"):
                    search_results.append({
                        "title": meta.get("title", "Related result"),
                        "url": meta.get("url"),
                        "snippet": meta.get("snippet", ""),
                    })
    except Exception:
        query_result = []

    system_prompt = (
        "You are an AI coding assistant. Use the provided context to answer accurately. "
        "If the context is weak or missing, say so clearly and keep the answer concise."
    )

    response_text = generate_response(
        prompt=f"User question: {request.message}\n\nContext:\n{context_text}",
        system_prompt=system_prompt,
    )

    payload = {
        "session_id": session_id,
        "last_message": request.message,
        "last_response": response_text,
        "sources": [item.get("url", "") for item in search_results if item.get("url")],
    }
    db.save_session(session_id, payload)

    return ChatResponse(
        response=response_text,
        session_id=session_id,
        sources=[item.get("url", "") for item in search_results if item.get("url")],
    )
