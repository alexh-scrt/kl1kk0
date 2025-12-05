# KL1KK0 Dev & Ops HOWTO

This document is the quick-start and reference for developing, running, and deploying the KL1KK0 stack (SvelteKit frontend + FastAPI backend).

## Prerequisites
- Node.js >= 18.13 (prefer Node 20)
- npm
- Python 3.10+ (virtualenv recommended)
- Make sure `backend/requirements.txt` and `web/package.json` are installed per instructions below.

## Project Layout
- `web/` — SvelteKit frontend (amber gridlines theme, single-page app with AI prompt).
- `backend/` — FastAPI backend (stub `/ask` endpoint + `/health`).
- `design/` — brand, business, and web design docs.

## Local Development

### 1) Install dependencies
```bash
# frontend
cd web
npm install

# backend
cd ../backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run backend (dev)
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- Health check: `GET http://localhost:8000/health`
- Ask endpoint (stub): `POST http://localhost:8000/ask` with JSON `{ "prompt": "Hello" }`

### 3) Run frontend (dev)
```bash
cd web
npm run dev -- --host --port 5173
```
- The Svelte page currently posts to `/api/ask`. In dev, set up a proxy or configure the frontend to call the backend origin (see “Config” below).

### 4) Frontend ↔ Backend wiring in dev
- Option A: Add a Vite proxy in `web/vite.config.ts` to forward `/api/ask` to `http://localhost:8000/ask`.
- Option B: Change the fetch URL in `+page.svelte` to `http://localhost:8000/ask` while developing. Prefer proxy for production parity.

## Configuration

Recommended env variables (add as needed):
- Backend:
  - `PORT` (default 8000)
  - `LOG_LEVEL` (info|debug|warning|error)
  - Secrets for LLM providers (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) — do not commit.
- Frontend:
  - `VITE_API_BASE` to point the browser to the backend origin in production.

### Vite proxy example (dev)
In `web/vite.config.ts`:
```ts
server: {
  proxy: {
    '/api/ask': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```
This forwards `/api/ask` in the browser to `http://localhost:8000/ask`.

## Production

### Backend (FastAPI)
- Run with uvicorn or gunicorn+uvicorn workers:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```
- Place behind a reverse proxy (NGINX, Caddy, or a cloud load balancer).
- Set environment secrets for your LLM/tooling integration.
- Consider process supervision with systemd, Docker, or PM2 (for node-based proxies).

### Frontend (SvelteKit)
- Build the static output (or SSR deploy) depending on your hosting:
```bash
cd web
npm run build
```
- If using adapter-auto, output depends on host (e.g., Vercel/Netlify). For Node hosting, add `@sveltejs/adapter-node` and run the built server:
```bash
npm install @sveltejs/adapter-node
# configure svelte.config.js for adapter-node
npm run build
node build
```
- Serve behind TLS and set `VITE_API_BASE` to the backend origin.

## Logging
- Backend: add FastAPI/uvicorn logging config; pipe to stdout/stderr for containerized deploys. Use `LOG_LEVEL` env.
- Frontend: use browser console only for dev; avoid verbose logging in production builds.

## Testing
- Frontend: `npm run check` (type/lint) and add component tests if needed.
- Backend: add pytest suite; for now, manual checks via curl or HTTP clients.

## Next Steps (to implement)
- Wire `/api/ask` to real LLM + RAG/tool orchestration (vector stores, MCP servers).
- Add auth/rate limiting if exposing publicly.
- Add observability: request logging, traces, and metrics for both frontend and backend.
- Dockerize: multi-stage builds for frontend and backend with a shared docker-compose for local parity.
