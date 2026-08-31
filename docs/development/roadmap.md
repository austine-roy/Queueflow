# Development roadmap

## Milestone 1 — Foundation

- [x] Initialize repository and Git-friendly layout.
- [x] Add configuration, ignore rules, architecture notes, and module documentation.

## Milestone 2 — Backend and database foundation

- [x] Create FastAPI, SQLAlchemy, PostgreSQL, and Alembic foundation.
- [x] Define location, queue, camera, measurement, and alert entities.
- [x] Add health, queue CRUD, and queue measurement endpoints with pytest coverage.
- [x] Add a PostgreSQL-only Docker Compose service and explicit development seed command.

## Milestone 3 — Frontend

- [x] Initialize the React/Vite/TypeScript/Tailwind dashboard.
- [x] Add responsive dashboard, queues, details, analytics, alerts, and settings views.
- [x] Add Axios integration, polling, loading/error states, tests, and build checks.

## Milestone 4 — Mock real-time system

- [x] Generate realistic simulated queue measurements.
- [x] Persist simulated and REST-ingested measurements, then broadcast them over WebSockets.
- [x] Add reconnecting frontend updates, REST polling fallback, connection status, and transition alerts.

## Milestone 5 — AI foundations

- [x] Add video-file detection, tracking, queue regions, counting, and density tests.

## Milestone 6 — Integration

- [x] Connect camera/AI measurements, backend persistence, WebSocket delivery, and dashboard.

## Milestone 7 — Advanced capabilities

- [x] Add alert lifecycle management, server-side historical analytics, multi-camera filtering, and history-informed wait estimates.

## Milestone 8 — Deployment

- [x] Add production Docker Compose configuration, health checks, and deployment documentation.
- [x] Build the production images and run the complete Docker Compose smoke test, including proxied API and WebSocket checks.

## Milestone 9 — Authentication & role-based access control

- [x] Add Argon2-hashed accounts, JWT authentication, and safe environment-driven administrator bootstrap.
- [x] Protect REST and WebSocket access with `admin`, `operator`, and `viewer` roles.
- [x] Add in-memory frontend authentication state, protected routes, role-aware controls, and access-denied handling.
- [x] Add authentication/RBAC tests and verify backend, frontend, lint, and production build checks.
