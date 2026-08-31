# Infrastructure

QueueFlow ships as three Docker Compose services: PostgreSQL, the FastAPI backend, and an Nginx-served React dashboard. Nginx proxies `/api` and `/ws` to the backend, so browser API and WebSocket traffic stays same-origin in production.

## Start the stack

```bash
cp .env.example .env
# Replace POSTGRES_PASSWORD and AUTH_SECRET_KEY with long, unique random values.
docker compose up --build -d
docker compose ps
curl http://localhost:8000/api/health
curl http://localhost:8000/api/ready
curl http://localhost:8000/api/metrics
```

Open `http://localhost:8080`. The backend applies Alembic migrations before starting. The simulator remains disabled unless explicitly configured; never use the development simulator as a production measurement source.

## Operational checks

```bash
docker compose logs --tail=100 backend
docker compose logs --tail=100 backend | grep 'request_complete\|request_error'
docker compose exec postgres pg_isready -U queueflow -d queueflow
docker compose down
```

`docker compose down -v` also removes the persisted PostgreSQL volume and should only be used when data deletion is intended.

## Security, backups, and recovery

Compose runs the API as a non-root user, prevents privilege escalation, and binds PostgreSQL only to `127.0.0.1`; use the API rather than exposing the database publicly. Login attempts are limited by `AUTH_LOGIN_RATE_LIMIT_ATTEMPTS` (default `5`) per `AUTH_LOGIN_RATE_LIMIT_WINDOW_SECONDS` (default `60`).

Create a portable backup without stopping the stack:

```bash
docker compose exec -T postgres pg_dump -U queueflow -d queueflow -Fc > queueflow-backup.dump
```

Restore only into an isolated replacement database or a confirmed recovery environment. This overwrites objects in the target database:

```bash
docker compose exec -T postgres createdb -U queueflow queueflow_recovery
docker compose exec -T postgres pg_restore -U queueflow -d queueflow_recovery --clean --if-exists < queueflow-backup.dump
```

Dependency audit: `pip-audit -r backend/requirements.txt` and `npm audit --omit=dev` should be run during releases. No dependency upgrades are made automatically because QueueFlow uses bounded version ranges and upgrades require compatibility verification.

`/api/health` is a liveness probe; `/api/ready` also checks PostgreSQL. `/api/metrics` exposes lightweight JSON request/error, WebSocket, observation, and latency counters for operational inspection. Backend logs are structured JSON and omit credentials, tokens, and secrets.

## Configuration

All values belong in the untracked root `.env` file. See `.env.example` for port, origin, database, and authentication settings. `AUTH_SECRET_KEY` is required and must be at least 32 characters; it signs access JWTs. The Compose database URL includes the password, so use a URL-safe password or URL-encode reserved characters. Bootstrap the initial administrator only with the explicit `python -m app.bootstrap_admin` command described in `backend/README.md`; never place bootstrap credentials in Compose configuration.
