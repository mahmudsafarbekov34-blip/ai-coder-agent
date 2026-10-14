from typing import Any

from fastapi import APIRouter, HTTPException

from app.db import db
from app.services.embeddings import embed_text
from app.services.llm import generate_response
from app.services.vectorstore import get_vector_store

router = APIRouter(tags=["chat"])


@router.post("/chat")
def chat(request: Any) -> Any:
    message = request.get("message") if isinstance(request, dict) else request.message
    session_id = request.get("session_id") if isinstance(request, dict) else request.session_id

    if not message or not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # simple pipeline: embed -> (optional) upsert and query -> call llm with context
    vec = embed_text(message)

    # upsert to vector store (best-effort)
    vs = get_vector_store()
    try:
        vs.upsert([session_id or "tmp-1"], [vec], metadata=[{"text": message}])
    except Exception:
        pass

    # query similar (best-effort)
    sources = []
    try:
        qres = vs.query(vec, top_k=3) if vs else []
        # collect URLs if available in metadata
        if getattr(qres, "matches", None):
            for m in qres.matches:
                meta = getattr(m, "metadata", None)
                if meta and meta.get("url"):
                    sources.append(meta.get("url"))
    except Exception:
        qres = None

    response_text = generate_response(message)

    payload = {
        "session_id": session_id or "",
        "last_message": message,
        "last_response": response_text,
    }
    db.save_session(session_id or "", payload)

    return {"response": response_text, "session_id": session_id or "", "sources": sources}
