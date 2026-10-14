# AI Coder Agent

A collaborative AI coding assistant with web search, retrieval-augmented generation (RAG), sandbox execution, and a PostgreSQL-backed session store.

## What is included

- FastAPI backend with `/api/chat`, `/api/health`, `/api/sessions/{id}`
- PostgreSQL-backed session persistence using SQLModel
- Optional OpenAI integration for chat and embeddings
- Optional Bing/Pinecone integration hooks
- React frontend with Monaco editor shell and chat panel
- Redis worker skeleton
- Docker Compose local environment
- Optional API-token auth layer (`AUTH_TOKEN`)
- Sandbox runner for Python snippets

## Local startup

```bash
cp .env.example .env

docker compose up --build
```

Then open:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health check: http://localhost:8000/api/health

## Example API calls

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Write a Python function to reverse a string."}'
```

```bash
curl -X POST http://localhost:8000/api/sandbox/run \
  -H "Content-Type: application/json" \
  -d '{"code":"print(2 + 2)"}'
```

## Security notes

- Keep real credentials in `.env` or GitHub Secrets, never committed to the repository.
- `AUTH_TOKEN` is optional; if set, the API will require it for protected routes.
- Use Docker or a more isolated runtime for executing untrusted code in real deployments.

## Production hardening roadmap

- Add robust sandboxing with gVisor/Firecracker or Kubernetes pods
- Add OAuth / SSO
- Add rate limiting and audit logs
- Add vector index creation automation
- Add deployment manifests for AWS/GCP/Azure

## License

MIT
