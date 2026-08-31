# QueueFlow

QueueFlow is an AI-assisted queue monitoring and management system. It is being developed in small, independently testable milestones. The backend/database foundation, dashboard, real-time layer, video-analysis baseline, camera-observation ingestion, advanced operations layer, and role-based authentication are implemented.

## Planned capabilities

- Monitor queue measurements from camera or video inputs.
- Show queue size, length, density, estimated wait, status, and alerts.
- Provide a live dashboard, REST API, historical analytics, and replaceable AI pipeline.

## Architecture

QueueFlow is organized by responsibility:

```text
Camera/video → AI pipeline → Backend API → PostgreSQL → Dashboard
                                  └──────→ WebSocket → Dashboard
```

The AI layer will publish measurements, while the backend owns queue state, threshold-based status calculation, persistence, and external APIs. See [the architecture notes](docs/architecture/overview.md) for details.

## Technology direction

| Area | Planned technology |
| --- | --- |
| Dashboard | React, TypeScript, Vite, Tailwind CSS, charts |
| API | Python, FastAPI, Pydantic, SQLAlchemy |
| Data | PostgreSQL |
| Vision | Python, OpenCV, replaceable detection/tracking adapter |

Backend dependencies are listed in `backend/requirements.txt`; the React dashboard dependencies and commands are in `frontend/package.json`. AI dependencies will be added only when their milestone begins.

## Repository layout

```text
frontend/        React dashboard (future)
backend/         FastAPI application and tests (future)
ai/              Detection, tracking, and queue analytics modules
database/        Database schemas and future migrations
infrastructure/  Container and deployment assets (future)
docs/            Architecture, API, and development documentation
scripts/         Developer and automation scripts
```

## Getting started

For backend development, use Python 3.11+, then follow the setup, migration, seed, run, and test instructions in `backend/README.md`. Local PostgreSQL can be started with `docker compose up -d postgres`; only PostgreSQL is containerized at this stage. Copy `.env.example` to `.env` and never commit it.

For the dashboard, use Node.js 20+, configure `frontend/.env` with `VITE_API_BASE_URL`, then run `npm install` and `npm run dev` in `frontend/`. Full frontend instructions are in `frontend/README.md`.

## Development workflow

1. Work in one module at a time and keep module interfaces explicit.
2. Add focused tests with each subsystem.
3. Run the relevant checks before requesting review.
4. Do not commit credentials, generated model weights, or local database data.

The current work plan is in [docs/development/roadmap.md](docs/development/roadmap.md). Production setup and operational checks are documented in [infrastructure/README.md](infrastructure/README.md).

## Status

Milestone 10 — Observability and production monitoring verified. The backend provides structured JSON logs, liveness (`/api/health`), PostgreSQL readiness (`/api/ready`), and Prometheus-compatible metrics (`/api/metrics`); see the infrastructure runbook for production checks.
