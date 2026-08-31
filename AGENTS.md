# QueueFlow — AGENTS.md

## 1. Project Overview

**Project Name:** QueueFlow

**Repository:** `https://github.com/austine-roy/queueflow`

QueueFlow is an AI-based smart queue monitoring and management system designed to monitor queues, estimate queue conditions, assist with queue management, and provide useful information to users and administrators.

This is an existing project. Continue development incrementally. Do not recreate the project from scratch.

---

## 2. Current Project Status

### Milestone Progress

- **Milestone 1 — COMPLETED**
- **Milestone 2 — COMPLETED**
- **Milestone 3 — COMPLETED**
- **Milestone 4 — COMPLETED**
- **Milestone 5 — COMPLETED**
- **Milestone 6 — COMPLETED**
- **Milestone 7 — COMPLETED**
- **Milestone 8 — COMPLETED & RUNTIME VERIFIED**
- **Milestone 9 — COMPLETED & VERIFIED**

The exact implementation of completed milestones must always be verified against the actual codebase rather than assumed from this document.

### Current Milestone

**Milestone 9 — Authentication & Role-Based Access Control (COMPLETED)**

Implemented Argon2 password hashing, short-lived JWT access tokens with a required signing secret, administrator bootstrap, and `admin`/`operator`/`viewer` authorization. REST endpoints enforce consistent `401`/`403` responses, and `/ws/queues` authenticates with a `Sec-WebSocket-Protocol` token rather than a query parameter. The React application keeps tokens in memory, has protected routes, role-aware navigation, login/logout, and an access-denied page.

---

## 3. Primary Development Rule

**Continue from the existing codebase. Do not restart or recreate Milestones 1–8.**

Before making changes:

1. Read this `AGENTS.md`.
2. Read `README.md` and relevant documentation.
3. Inspect the repository structure.
4. Run `git status`.
5. Inspect recent Git commits.
6. Identify the current branch.
7. Verify the actual implementation of Milestones 1–8.
8. Identify existing Milestone 4 work.
9. Understand the architecture before modifying it.

Preserve existing working functionality unless there is a clear technical reason to change it.

---

## 4. Git Repository and Workflow

Repository:

`https://github.com/austine-roy/queueflow`

Useful commands:

```bash
git status
git branch
git log --oneline -10
git remote -v
```

Before committing:

```bash
git status
git diff
```

Use clear commit messages:

```text
feat: add real-time queue updates
fix: resolve websocket reconnection issue
refactor: improve queue service
test: add websocket integration tests
docs: update milestone 4 documentation
```

Do not commit:

- API keys
- passwords
- authentication tokens
- secrets
- `.env` files containing secrets
- private credentials
- unnecessary build/cache files
- large generated artifacts

Always check `.gitignore` before committing.

---

## 5. Development Workflow

Follow:

**Inspect → Understand → Modify → Test → Document → Commit → Push**

Do not make broad changes without first understanding the existing implementation.

For every feature:

1. Inspect related files.
2. Identify existing abstractions.
3. Reuse existing components where appropriate.
4. Implement the smallest maintainable change.
5. Run relevant tests.
6. Check for regressions.
7. Update documentation when necessary.
8. Update this file if project state changes.

---

## 6. Architecture Rules

Do not replace the existing architecture simply because another technology or structure may be preferable.

Before making architectural changes:

1. Explain why the change is necessary.
2. Identify affected components.
3. Consider compatibility with existing functionality.
4. Make the smallest reasonable change.
5. Test the affected components.

Keep concerns separated where practical:

- Frontend/UI
- Backend/API
- Queue/business logic
- AI/ML
- Database/persistence
- Real-time communication
- Configuration
- Tests

Follow the architecture already present in the repository.

---

## 7. Milestone 1–3 Continuity

Milestones 1, 2, and 3 were completed in the previous development sessions.

**Do not assume their exact contents without verification.**

A new Codex session must inspect:

- Git history
- Existing source files
- README/documentation
- Tests
- Configuration
- Database models
- Frontend components
- Backend routes/services

The repository is the source of truth.

If documentation and code disagree, verify the implementation and update the documentation.

---

## 8. Milestone 4 — Real-Time Queue Layer (COMPLETED)

Milestone 4 is the current development target.

### 8.1 WebSocket Backend

Implement or verify a FastAPI WebSocket endpoint:

```text
/ws/queues
```

Requirements:

- Manage WebSocket connections safely.
- Support multiple connected clients where appropriate.
- Broadcast queue updates.
- Handle client disconnects.
- Avoid crashing the server when a connection closes unexpectedly.
- Keep real-time communication separate from unrelated business logic.

Use existing backend patterns whenever possible.

### 8.2 Connection Manager

If not already implemented, create a reusable WebSocket connection manager responsible for:

- accepting connections
- tracking active clients
- removing disconnected clients
- broadcasting updates
- handling connection failures

Do not create duplicate connection-management implementations.

### 8.3 Multi-Queue Simulator

Implement or verify a configurable simulator capable of generating gradual queue changes for multiple queues.

The simulator should:

- support multiple queues
- generate realistic gradual changes
- avoid unrealistic random jumps unless intentionally configured
- use configurable intervals/settings
- integrate with existing queue models/services
- be easy to replace with real AI-generated measurements later

The simulator is for development/testing and must remain clearly separated from production AI inference.

### 8.4 Persist Measurements

Queue measurements generated by the simulator should be persisted using the project's existing database/data layer where applicable.

Before changing the schema:

1. Inspect existing models.
2. Check existing migrations.
3. Reuse existing measurement structures if possible.
4. Avoid destructive schema changes.

### 8.5 React Live Updates

The frontend should consume WebSocket updates and update queue information without requiring a full page refresh.

Handle:

- initial connection
- incoming queue measurements
- multiple queues
- connection status
- disconnection
- reconnection
- stale/unavailable data

Follow the existing React/component architecture.

### 8.6 Reconnection and Fallback

The frontend must behave gracefully if the WebSocket connection fails.

Expected behavior:

- detect disconnection
- attempt reconnection according to a reasonable strategy
- avoid excessive reconnect loops
- show connection status where appropriate
- retain sensible last-known data when appropriate
- fall back to an existing HTTP/API mechanism if the project architecture supports it

Do not hide connection failures from the user or silently produce misleading live data.

### 8.7 Queue Transition Alerts

Implement alerts based on meaningful queue-state transitions rather than repeatedly alerting on every measurement.

Examples may include:

- queue becomes crowded
- queue returns to normal
- waiting time crosses a configured threshold
- queue status changes

Avoid alert spam.

Use existing notification/alert infrastructure if available.

---

## 9. AI/ML Development

QueueFlow may use AI/ML for queue monitoring and analysis.

When working with AI/ML:

- Inspect the current implementation first.
- Do not replace models without understanding the reason.
- Keep inference logic separate from UI code.
- Avoid hardcoded machine-specific model paths.
- Use configuration/environment variables where appropriate.
- Handle missing models gracefully.
- Consider CPU/GPU usage and inference latency.
- Keep real-time processing efficient.

Important performance considerations:

- inference speed
- memory usage
- detection accuracy
- frame rate
- CPU/GPU utilization
- latency
- scalability
- reliability

---

## 10. Frontend Development

When modifying the frontend:

- Follow the existing framework and component structure.
- Reuse components.
- Keep components modular.
- Avoid unnecessary business logic inside UI components.
- Maintain responsive design.
- Handle loading states.
- Handle empty states.
- Handle errors.
- Handle real-time connection states.
- Follow the existing API/data-fetching approach.

Do not introduce a new frontend framework without explicit justification.

---

## 11. Backend Development

When modifying the backend:

- Follow the existing API architecture.
- Keep business logic separate from routes/controllers where practical.
- Validate inputs.
- Handle errors consistently.
- Avoid exposing sensitive information.
- Reuse existing services.
- Preserve API compatibility when possible.
- Use asynchronous operations where appropriate.

---

## 12. Database

Before modifying database structures:

1. Inspect existing models.
2. Inspect migrations.
3. Understand relationships.
4. Avoid destructive changes.
5. Preserve existing data.
6. Test migrations.
7. Update documentation if required.

Never hardcode database credentials.

---

## 13. APIs and WebSockets

Before adding an API or WebSocket feature:

- Inspect existing endpoints.
- Follow established naming conventions.
- Follow existing request/response formats.
- Validate inputs.
- Return useful errors.
- Avoid breaking existing consumers.
- Document new endpoints where appropriate.

For WebSockets, also consider:

- connection lifecycle
- disconnect handling
- reconnect behavior
- message format
- validation
- multiple clients
- server-side exceptions
- stale connections

---

## 14. Environment Configuration

Do not hardcode environment-specific values.

Examples:

```text
DATABASE_URL
API_KEY
MODEL_PATH
REDIS_URL
PORT
SECRET_KEY
```

Use the project's existing configuration system.

If `.env.example` exists, update it when adding required variables.

Never commit real secrets.

---

## 15. Testing

Before marking a feature complete:

1. Run existing tests.
2. Test the changed functionality.
3. Check for regressions.
4. Check server logs.
5. Verify the application starts.
6. Verify frontend behavior where applicable.

For Milestone 4, test at minimum:

- WebSocket connection
- WebSocket disconnect
- WebSocket reconnection
- queue update broadcasting
- multiple queues
- simulator behavior
- measurement persistence
- frontend live updates
- fallback behavior
- transition alerts

Do not remove or disable tests simply because they fail after a change.

---

## 16. Debugging

When an error occurs:

1. Read the complete error.
2. Identify the source file/function.
3. Inspect related code.
4. Reproduce the problem.
5. Make the smallest appropriate fix.
6. Test the fix.
7. Check for regressions.

Do not blindly modify unrelated files.

---

## 17. Dependencies

Before adding a dependency:

- Check whether the functionality already exists.
- Check current dependencies.
- Prefer maintained packages.
- Avoid duplicate packages.
- Use the existing package manager.

Update the lockfile when appropriate.

---

## 18. Documentation

Keep documentation synchronized with the implementation.

Update documentation when significant functionality changes, especially:

- setup instructions
- environment variables
- architecture
- API endpoints
- WebSocket endpoints
- AI/ML setup
- database setup
- simulator configuration
- testing
- deployment

Never document functionality that has not been verified.

---

## 19. Project State Tracking

Update this section after major development sessions.

### Completed

```text
Milestone 1 — Completed
Milestone 2 — Completed
Milestone 3 — Completed
Milestone 4 — Completed
Milestone 5 — Completed
Milestone 6 — Completed
Milestone 7 — Completed
Milestone 8 — Completed & Runtime Verified
Milestone 9 — Completed & Verified
```

### Current

```text
Milestone 9 — Completed & Verified
```

### Known Issues

Update this section with verified issues.

```text
Frontend test output includes existing React Router future-flag and zero-size chart warnings; tests pass.
```

### Next Steps

Update this section as work progresses.

```text
1. Inspect and define the next milestone before making changes.
2. Preserve the authentication contract and role matrix unless a verified requirement calls for a change.
```

---

## 20. Milestone 4 Completion

Milestone 4 has been completed.

The next Codex session must treat Milestones 1–8 as completed unless the repository reveals a verified defect or unfinished implementation.

Do not recreate Milestone 4.

Before beginning Milestone 5, inspect the actual codebase, tests, documentation, and Git history to determine the exact remaining scope.

---

## 21. Milestone 6 Completion

Milestone 6 has been completed and pushed to GitHub.

Completed:

- Added camera configuration and observation ingestion.
- Added `POST /api/cameras/{id}/observations`.
- The observation endpoint validates the camera.
- Measurements are persisted.
- Queue state is updated.
- Live queue and alert events are broadcast.
- Added camera assignment tests.
- Added end-to-end WebSocket broadcast tests.

Verification:

- 30 backend/AI tests passed.
- Frontend tests passed.
- Frontend lint passed.

Commit:

```text
e54ca001 feat: ingest camera queue observations
```

Important handoff note:

The pre-existing uncommitted changes in `AGENTS.md` were intentionally preserved and were not part of the Milestone 6 commit.

Do not discard or overwrite those changes without explicit instruction.

The next development target is Milestone 7.

---

## 21. Milestone 5 Completion

Milestone 5 has been completed.

The next Codex session must treat Milestones 1–8 as completed unless the repository reveals a verified defect or unfinished implementation.

Do not recreate Milestone 5.

Milestone 6 has now been completed. Before beginning Milestone 7, inspect the actual codebase, tests, documentation, and Git history to determine the exact Milestone 9 requirements.

---

## 23. Milestone 7 Completion

Milestone 7 has been completed and pushed to GitHub.

Completed:

- Added server-side historical analytics.
- Updated the dashboard to use server-side historical analytics.
- Added alert filtering.
- Added alert resolution.
- Added automatic recovery resolution for alerts.
- Added multi-camera operational filters.
- Improved wait-time estimates using observed queue-departure history.
- Added a safe configured fallback for wait-time estimation when sufficient observed history is unavailable.

Verification:

- 36 backend/AI tests passed.
- Frontend tests passed.
- Frontend lint passed.
- Production frontend build passed.

Commit:

```text
5c440a05 feat: add advanced queue operations
```

The next development target is Milestone 8.

Do not recreate Milestone 7 unless a verified defect requires changes.

---

## 23. Codex Session Handoff

### Milestone 9 session handoff

Completed:
- Added Alembic user/account migration, Argon2 password hashing, JWT login/current-user/logout endpoints, and safe environment-driven administrator bootstrap.
- Enforced the admin/operator/viewer role matrix across REST endpoints and authenticated `/ws/queues` through a WebSocket subprotocol.
- Added in-memory frontend authentication, login/logout, protected routes, role-aware settings navigation, and an unauthorized state.
- Updated authentication, deployment, API, and roadmap documentation.

Tested:
- `backend/.venv/bin/python -m pytest backend/tests ai/tests` — 41 passed.
- `npm test`, `npm run lint`, and `npm run build` in `frontend/` — passed.
- A fresh isolated Docker Compose PostgreSQL stack applied Alembic revision `20260901_0002`, bootstrapped an admin from transient environment variables, verified login, and verified authenticated/rejected WebSocket handshakes.
- Authentication success/failure, 401/403 behavior, admin/operator/viewer permissions, authenticated WebSocket access, and unauthenticated WebSocket rejection are covered by backend tests.

Remaining:
- No verified Milestone 9 implementation work remains.

Known issues:
- Frontend tests emit existing React Router future-flag and zero-size chart warnings; they do not fail tests.

Next task:
Inspect and define the next milestone before making changes.

At the end of every significant Codex session, update this file.

Record:

### Completed

What was implemented.

### Tested

What was actually tested successfully.

### Remaining

What is unfinished.

### Known Issues

Any verified bugs or limitations.

### Next Task

The exact next recommended task.

Example:

```text
Session Handoff

Completed:
- Implemented /ws/queues.
- Added WebSocket connection manager.
- Added multi-queue simulator.

Tested:
- WebSocket connection/disconnection.
- Multiple clients.
- Queue update broadcast.

Remaining:
- Frontend reconnection UI.
- Transition-based alerts.

Next Task:
Implement frontend WebSocket reconnection and connection-status handling.
```

Do not claim something is complete unless it has been verified.

---

## 24. New Codex Session Procedure

Every new Codex session should:

```text
1. Read AGENTS.md.
2. Read README.md.
3. Inspect the project structure.
4. Run git status.
5. Inspect the current branch.
6. Inspect recent commits.
7. Verify Milestones 1–8.
8. Inspect current Milestone 9 implementation.
9. Determine the exact Milestone 9 requirements from project documentation and Git history.
10. Identify what remains.
11. Implement only the required next step.
12. Run relevant tests.
13. Update documentation.
14. Update AGENTS.md.
15. Commit changes.
16. Push to GitHub when appropriate.
```

Never restart the project.

Never recreate completed milestones unless a verified bug requires it.

---

## 25. Golden Rule

The QueueFlow repository is the source of truth.

When continuing work:

**Inspect → Understand → Modify → Test → Document → Commit → Push**

Build on the existing implementation and preserve working functionality.
