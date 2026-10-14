from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path


def _run_with_python(code: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        temp_path = tmp.name

    try:
        result = subprocess.run(["python", temp_path], capture_output=True, text=True, timeout=10)
        if result.stdout:
            return result.stdout.strip()
        if result.stderr:
            return result.stderr.strip()
        return "Execution completed without output."
    except subprocess.TimeoutExpired:
        return "Execution timed out."
    finally:
        try:
            Path(temp_path).unlink(missing_ok=True)
        except Exception:
            pass


def _run_with_docker(code: str) -> str:
    # Best-effort secure-ish local execution using a containerized Python environment.
    try:
        proc = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "-i",
                "python:3.11-slim",
                "python",
                "-c",
                code,
            ],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if proc.stdout:
            return proc.stdout.strip()
        if proc.stderr:
            return proc.stderr.strip()
        return "Execution completed without output."
    except Exception:
        return _run_with_python(code)


def run_python_snippet(code: str) -> str:
    """Run Python code in a safe-ish local sandbox.

    Preference order:
    1. Docker container runner
    2. local subprocess fallback
    """
    if os.getenv("USE_DOCKER_SANDBOX", "true").lower() == "true":
        try:
            return _run_with_docker(code)
        except Exception:
            return _run_with_python(code)
    return _run_with_python(code)
