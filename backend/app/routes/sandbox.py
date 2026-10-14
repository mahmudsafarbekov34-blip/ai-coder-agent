from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

from app.services.sandbox import run_python_snippet

router = APIRouter(tags=["sandbox"])


class SandboxRequest(BaseModel):
    code: str = Field(..., min_length=1)


class SandboxResponse(BaseModel):
    output: str


@router.post("/sandbox/run", response_model=SandboxResponse)
def run_sandbox(request: SandboxRequest) -> SandboxResponse:
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    output = run_python_snippet(request.code)
    return SandboxResponse(output=output)
