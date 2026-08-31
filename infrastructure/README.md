# Infrastructure

QueueFlow ships as three Docker Compose services: PostgreSQL, the FastAPI backend, and an Nginx-served React dashboard. Nginx proxies `/api` and `/ws` to the backend, so browser API and WebSocket traffic stays same-origin in production.

## Start the stack

```bash
cp .env.example .env
# Replace POSTGRES_PASSWORD with a long, URL-safe random value.
docker compose up --build -d
docker compose ps
curl http://localhost:8000/api/health
```

Open `http://localhost:8080`. The backend applies Alembic migrations before starting. The simulator remains disabled unless explicitly configured; never use the development simulator as a production measurement source.

## Operational checks

```bash
docker compose logs --tail=100 backend
docker compose exec postgres pg_isready -U queueflow -d queueflow
docker compose down
```

`docker compose down -v` also removes the persisted PostgreSQL volume and should only be used when data deletion is intended.

## Configuration

All values belong in the untracked root `.env` file. See `.env.example` for port, origin, and database settings. The Compose database URL includes the password, so use a URL-safe password or URL-encode reserved characters.
