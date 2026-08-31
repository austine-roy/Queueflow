# QueueFlow backend

The backend provides the QueueFlow REST API, PostgreSQL persistence, Alembic migrations, configurable capacity-based queue status, and a transparent service-rate wait estimate. Video analysis runs outside the API process; configured camera sources submit their AI observations to the backend for persistence and live delivery.

## Requirements

- Python 3.11+
- Docker Desktop (for local PostgreSQL)

## Setup

From the repository root, create configuration and start PostgreSQL:

```bash
cp .env.example .env
docker compose up -d postgres
```

Create a virtual environment and install the backend dependencies:

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`DATABASE_URL` and `AUTH_SECRET_KEY` are required and are read from the environment (or root `.env`). `AUTH_SECRET_KEY` must be a unique, high-entropy signing secret of at least 32 characters; never commit `.env`.

## Database and seed data

Apply all migrations, then optionally load idempotent development examples:

```bash
cd backend
alembic upgrade head
python -m app.seed
```

The seed command creates one demo location, two queues, and one simulated camera only when they are absent. It is explicit and is not run automatically.

## Authentication and roles

Passwords are hashed with Argon2. Access tokens are short-lived HS256 JWTs signed with the required `AUTH_SECRET_KEY`; the browser keeps its token only in memory.

Create the first administrator explicitly from environment variables. The command refuses to overwrite an existing account and refuses to bootstrap when any account already exists:

```bash
export AUTH_BOOTSTRAP_ADMIN_EMAIL=admin@example.com
export AUTH_BOOTSTRAP_ADMIN_PASSWORD='use-a-strong-unique-password'
python -m app.bootstrap_admin
```

`POST /api/auth/login` accepts an email and password. `GET /api/auth/me` and `POST /api/auth/logout` require `Authorization: Bearer <token>`; logout clears the browser token because JWTs are stateless for this milestone. An admin can manage accounts through `/api/users`.

| Role | Access |
| --- | --- |
| `admin` | Full queue/camera configuration, account management, and all operational/read access. |
| `operator` | Queue, camera, alert, analytics, and live-view reads; may submit measurements/observations and resolve alerts. |
| `viewer` | Read-only queue, camera, alert, analytics, and live-view access. |

Protected HTTP routes return `401` for missing or invalid credentials and `403` for an authenticated account without permission. The `/ws/queues` endpoint requires the JWT in the `Sec-WebSocket-Protocol` value `queueflow.jwt.<token>`; tokens are deliberately never accepted in query parameters.

## Real-time simulator and WebSocket

Set `QUEUEFLOW_SIMULATION_ENABLED=true` to start the development-only simulator with the API. It updates every non-closed queue gradually, persists changed measurements, and broadcasts events to every authenticated client connected to `ws://<host>:<port>/ws/queues`.

| Variable | Default | Purpose |
| --- | --- | --- |
| `QUEUEFLOW_SIMULATION_ENABLED` | `false` | Enable the development simulator. |
| `QUEUEFLOW_SIMULATION_INTERVAL` | `2` | Seconds between simulator cycles. |
| `QUEUEFLOW_SIMULATION_ARRIVAL_RATE` | `18` | Simulated arrivals per minute. |
| `QUEUEFLOW_SIMULATION_SERVICE_RATE` | `12` | Simulated departures per minute. |

Each event is JSON with a `type` of `queue_update` or `alert`. Measurements submitted to the REST API also broadcast through this same path. Alerts are emitted only when a queue enters a `CROWDED` or `CRITICAL` state, preventing repeated alerts while it remains in that state.

## Advanced queue operations

- `GET /api/analytics/queues` returns persisted per-queue measurement history, peak population, and average wait time in one response for dashboard analytics.
- `GET /api/alerts?active=true` filters active transition alerts; `POST /api/alerts/{alert_id}/resolve` resolves one explicitly. A return to a non-concerning queue status resolves its active transition alerts automatically.
- `GET /api/cameras?queue_id=<id>&active=true` supports operational views across multiple camera sources.

Wait estimates use the configured service rate until historical measurements show repeated queue decreases. The resulting observed departure rate then informs the estimate; it remains a transparent heuristic rather than an ML prediction.

## Camera observation ingestion

Configure a camera with `POST /api/cameras`, assigning it to a queue at the same location. An external video/AI worker then submits each analyzed observation without holding an API request open for video processing:

```json
POST /api/cameras/{camera_id}/observations
{
  "person_count": 12,
  "density": 0.6
}
```

The backend validates that the camera is active and assigned to a queue, persists the measurement, recalculates queue status/wait time, and broadcasts the resulting `queue_update` plus any transition alert over `/ws/queues`. See `docs/api/README.md` for the full endpoint summary.

## Run the API

```bash
cd backend
uvicorn app.main:app --reload
```

Open [Swagger UI](http://127.0.0.1:8000/docs) or [ReDoc](http://127.0.0.1:8000/redoc). The health endpoint is `GET /api/health`.

## Test

```bash
cd backend
pytest
```

Tests use an isolated in-memory SQLite database and do not require Docker or PostgreSQL. Production uses PostgreSQL through Alembic migrations.

## Package layout

- `app/api`: HTTP routes
- `app/core`: settings and database session management
- `app/models`: SQLAlchemy entities and controlled enums
- `app/schemas`: validated API data contracts
- `app/services`: queue status, wait-estimation, and measurement logic
- `alembic`: reproducible database migrations
