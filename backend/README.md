# QueueFlow backend

The backend provides the QueueFlow REST API, PostgreSQL persistence, Alembic migrations, configurable capacity-based queue status, and a transparent service-rate wait estimate. It does not yet process video or make ML predictions.

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

`DATABASE_URL` is required and is read from the environment (or root `.env`). Set it to the same PostgreSQL credentials as `POSTGRES_*`; never commit `.env`.

## Database and seed data

Apply all migrations, then optionally load idempotent development examples:

```bash
cd backend
alembic upgrade head
python -m app.seed
```

The seed command creates one demo location, two queues, and one simulated camera only when they are absent. It is explicit and is not run automatically.

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
