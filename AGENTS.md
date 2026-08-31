**# QueueFlow — AGENTS.md**

**## 1. Project Overview**

**\*\*Project Name:\*\*** QueueFlow

**\*\*Repository:\*\*** \`https\://github.com/austine-roy/queueflow\`

QueueFlow is an AI-based smart queue monitoring and management system designed to monitor queues, estimate queue conditions, assist with queue management, and provide useful information to users and administrators.

This is an existing project. Continue development incrementally. Do not recreate the project from scratch.

**---**

**## 2. Current Project Status**

**### Milestone Progress**

- **Milestone 1 — COMPLETED**
- **Milestone 2 — COMPLETED**
- **Milestone 3 — COMPLETED**
- **Milestone 4 — COMPLETED**
- **Milestone 5 — COMPLETED**
- **Milestone 6 — COMPLETED**
- **Milestone 7 — COMPLETED**
- **Milestone 8 — COMPLETED & RUNTIME VERIFIED**
- **Milestone 9 — COMPLETED & VERIFIED**
- **Milestone 10 — COMPLETED & RUNTIME VERIFIED**
- **Milestone 11 — COMPLETED & RUNTIME VERIFIED**
- **Milestone 12 — COMPLETED & RUNTIME VERIFIED**
- **Milestone 13 — CURRENT / FINAL QA & PRODUCTION RELEASE**

**### Current Milestone**

**Milestone 13 — Final QA & Production Release**

Milestones 1–12 are complete and verified. Milestone 13 is the final QA and production-release phase.

The goal is to validate the complete QueueFlow system end-to-end, resolve release-blocking issues, finalize documentation, and prepare the project for production/demo delivery.

Scope:

1. **End-to-end QA**
   - Verify critical workflows from camera observation through queue state, alerts, analytics, and dashboard updates.
   - Verify authentication, RBAC, protected APIs, and WebSocket behavior.
   - Test important success and failure paths.

2. **Production deployment verification**
   - Run a fresh production Docker Compose deployment.
   - Verify migrations, PostgreSQL, FastAPI, Nginx, health/readiness, metrics, logging, and WebSockets.
   - Verify the deployment starts cleanly from a fresh environment.

3. **Security regression**
   - Verify authentication/RBAC.
   - Verify security headers and production HSTS.
   - Verify login rate limiting.
   - Verify secrets are not exposed.
   - Confirm the Milestone 11 security hardening remains intact.

4. **Performance regression**
   - Run the existing Milestone 12 performance/regression checks.
   - Verify analytics behavior and the measurement-history index.
   - Verify multi-client WebSocket behavior.
   - Verify concurrent observation ingestion.
   - Treat single-process baselines as regression indicators, not production capacity guarantees.

5. **Backup and recovery**
   - Verify the documented PostgreSQL backup/restore procedure where safely possible.
   - Do not perform destructive operations against real project data.
   - Confirm recovery documentation is accurate.

6. **UI/UX and release polish**
   - Review major frontend workflows for obvious usability or visual issues.
   - Fix release-blocking UI problems without redesigning working functionality unnecessarily.
   - Verify responsive behavior where relevant to the project.

7. **Documentation and demo readiness**
   - Finalize README and deployment documentation.
   - Ensure setup, environment configuration, authentication, operations, troubleshooting, and backup/restore instructions are accurate.
   - Prepare the project for demonstration/submission.
   - Record known limitations clearly.

8. **Final verification**
   - Run the complete backend/AI test suite.
   - Run frontend tests.
   - Run frontend lint.
   - Run the production frontend build.
   - Perform fresh Docker runtime verification.
   - Resolve all release-blocking failures before marking the milestone complete.

Do not introduce new major features during Milestone 13. Focus on verification, bug fixing, release hardening, documentation, and project completion.

The goal is to validate and improve QueueFlow's behavior under realistic load while preserving all completed functionality.

Scope:

1. **Performance baseline**
   - Establish practical baselines for API latency, queue observation ingestion, analytics, WebSocket updates, and relevant AI operations.
   - Identify the main performance bottlenecks before making optimizations.

2. **API and backend performance**
   - Profile important API paths.
   - Optimize slow database queries and application code where evidence supports it.
   - Avoid premature optimization.
   - Preserve existing API behavior.

3. **Database performance**
   - Review query patterns and indexes.
   - Identify inefficient queries and N+1 behavior where applicable.
   - Add only justified indexes or query optimizations.
   - Verify migrations remain safe and non-destructive.

4. **WebSocket reliability and scalability**
   - Test concurrent authenticated WebSocket connections.
   - Test reconnect/disconnect behavior.
   - Verify broadcasts remain reliable under multiple clients.
   - Identify connection/resource leaks.
   - Preserve WebSocket authentication and existing message behavior.

5. **Queue observation and camera throughput**
   - Test concurrent camera/observation ingestion.
   - Measure processing latency and throughput.
   - Identify bottlenecks in queue-state updates, persistence, and broadcasting.
   - Verify the system handles realistic multi-camera activity.

6. **AI/inference performance**
   - Measure relevant AI inference latency and resource usage.
   - Identify practical CPU/GPU and memory bottlenecks.
   - Optimize only where supported by measurements.
   - Preserve existing AI behavior and accuracy.

7. **Resource and failure testing**
   - Evaluate CPU and memory behavior under representative load.
   - Test service recovery and graceful failure scenarios.
   - Verify database-unavailable and WebSocket failure behavior.
   - Check for resource leaks and unbounded in-memory state.

8. **Performance testing**
   - Add focused backend performance/load tests where appropriate.
   - Add WebSocket concurrency tests.
   - Add observation-ingestion throughput tests.
   - Establish reasonable regression thresholds without making tests unnecessarily brittle.

9. **Production Docker verification**
   - Run a fresh production Compose stack.
   - Verify performance-critical paths under representative load.
   - Confirm health, readiness, metrics, logging, authentication, RBAC, and WebSocket behavior remain functional.
   - Verify the stack recovers cleanly from appropriate controlled failures.

10. **Documentation**
   - Document performance baselines and significant optimizations.
   - Document known capacity limits and bottlenecks.
   - Document recommended production resource expectations where evidence supports them.
   - Update README, deployment documentation, roadmap, and AGENTS.md.

Do not introduce unnecessary infrastructure. Use measurements to guide optimization and preserve the existing production architecture.

The goal is to make QueueFlow easier to operate, diagnose, and monitor in production without disrupting the completed functionality from Milestones 1–12.

Scope:

1. **Structured application logging**
   - Add consistent backend logging.
   - Include useful request, authentication, WebSocket, queue, camera, and error context.
   - Do not log passwords, JWTs, secrets, or other sensitive credentials.

2. **Health and readiness monitoring**
   - Maintain/extend backend health checks.
   - Distinguish application health from dependency readiness where appropriate.
   - Include PostgreSQL and other required service dependencies in readiness checks when appropriate.

3. **Metrics**
   - Add useful operational metrics for API requests, errors, WebSocket connections, queue observations, processing latency, and relevant application activity.
   - Prefer a lightweight implementation that fits the existing architecture.

4. **Production monitoring**
   - Provide a practical way to inspect application health and operational metrics in the deployed Docker environment.
   - Add monitoring configuration or documentation where appropriate.
   - Avoid introducing a large monitoring stack unless the repository requirements justify it.

5. **Error visibility**
   - Make backend failures diagnosable through logs and appropriate error responses.
   - Ensure frontend connection/API failures remain visible to operators without exposing sensitive details.

6. **Deployment observability**
   - Verify logging and health behavior through the production Docker Compose stack.
   - Document useful commands for checking service health, logs, and operational status.

7. **Testing**
   - Add backend tests for health/readiness and observability-related behavior where applicable.
   - Add regression tests for affected functionality.
   - Run the complete backend/AI and frontend test suites.
   - Run frontend lint and production build.
   - Perform a production Docker smoke test when Docker is available.

8. **Documentation**
   - Update README and deployment documentation.
   - Document health endpoints, logs, metrics, troubleshooting, and operational checks.
   - Update AGENTS.md with the Milestone 10 implementation and verification status.

Do not introduce unnecessary infrastructure. Inspect the existing deployment and application architecture first and implement the smallest maintainable observability solution.

**---**

**## 3. Primary Development Rule**

**\*\*Continue from the existing codebase. Do not restart or recreate Milestones 1–12.\*\***

Before making changes:

1\. Read this \`AGENTS.md\`.

2\. Read \`README.md\` and relevant documentation.

3\. Inspect the repository structure.

4\. Run \`git status\`.

5\. Inspect recent Git commits.

6\. Identify the current branch.

7\. Verify the actual implementation of Milestones 1–12.

8\. Determine the current milestone and remaining work from the repository roadmap and documentation.

9\. Understand the architecture before modifying it.

Preserve existing working functionality unless there is a clear technical reason to change it.

**---**

**## 4. Git Repository and Workflow**

Repository:

\`https\://github.com/austine-roy/queueflow\`

Useful commands:

\`\`\`bash

git status

git branch

git log --oneline -10

git remote -v

\`\`\`

Before committing:

\`\`\`bash

git status

git diff

\`\`\`

Use clear commit messages:

\`\`\`text

feat: add real-time queue updates

fix: resolve websocket reconnection issue

refactor: improve queue service

test: add websocket integration tests

docs: update milestone 4 documentation

\`\`\`

Do not commit:

\- API keys

\- passwords

\- authentication tokens

\- secrets

\- \`.env\` files containing secrets

\- private credentials

\- unnecessary build/cache files

\- large generated artifacts

Always check \`.gitignore\` before committing.

**---**

**## 5. Development Workflow**

Follow:

**\*\*Inspect → Understand → Modify → Test → Document → Commit → Push\*\***

Do not make broad changes without first understanding the existing implementation.

For every feature:

1\. Inspect related files.

2\. Identify existing abstractions.

3\. Reuse existing components where appropriate.

4\. Implement the smallest maintainable change.

5\. Run relevant tests.

6\. Check for regressions.

7\. Update documentation when necessary.

8\. Update this file if project state changes.

**---**

**## 6. Architecture Rules**

Do not replace the existing architecture simply because another technology or structure may be preferable.

Before making architectural changes:

1\. Explain why the change is necessary.

2\. Identify affected components.

3\. Consider compatibility with existing functionality.

4\. Make the smallest reasonable change.

5\. Test the affected components.

Keep concerns separated where practical:

\- Frontend/UI

\- Backend/API

\- Queue/business logic

\- AI/ML

\- Database/persistence

\- Real-time communication

\- Configuration

\- Tests

Follow the architecture already present in the repository.

**---**

**## 7. Milestone 1–3 Continuity**

Milestones 1, 2, and 3 were completed in the previous development sessions.

**\*\*Do not assume their exact contents without verification.\*\***

A new Codex session must inspect:

\- Git history

\- Existing source files

\- README/documentation

\- Tests

\- Configuration

\- Database models

\- Frontend components

\- Backend routes/services

The repository is the source of truth.

If documentation and code disagree, verify the implementation and update the documentation.

**---**

**## 8. Milestone 4 — Real-Time Queue Layer (COMPLETED)**

Milestone 4 is the current development target.

**### 8.1 WebSocket Backend**

Implement or verify a FastAPI WebSocket endpoint:

\`\`\`text

/ws/queues

\`\`\`

Requirements:

\- Manage WebSocket connections safely.

\- Support multiple connected clients where appropriate.

\- Broadcast queue updates.

\- Handle client disconnects.

\- Avoid crashing the server when a connection closes unexpectedly.

\- Keep real-time communication separate from unrelated business logic.

Use existing backend patterns whenever possible.

**### 8.2 Connection Manager**

If not already implemented, create a reusable WebSocket connection manager responsible for:

\- accepting connections

\- tracking active clients

\- removing disconnected clients

\- broadcasting updates

\- handling connection failures

Do not create duplicate connection-management implementations.

**### 8.3 Multi-Queue Simulator**

Implement or verify a configurable simulator capable of generating gradual queue changes for multiple queues.

The simulator should:

\- support multiple queues

\- generate realistic gradual changes

\- avoid unrealistic random jumps unless intentionally configured

\- use configurable intervals/settings

\- integrate with existing queue models/services

\- be easy to replace with real AI-generated measurements later

The simulator is for development/testing and must remain clearly separated from production AI inference.

**### 8.4 Persist Measurements**

Queue measurements generated by the simulator should be persisted using the project's existing database/data layer where applicable.

Before changing the schema:

1\. Inspect existing models.

2\. Check existing migrations.

3\. Reuse existing measurement structures if possible.

4\. Avoid destructive schema changes.

**### 8.5 React Live Updates**

The frontend should consume WebSocket updates and update queue information without requiring a full page refresh.

Handle:

\- initial connection

\- incoming queue measurements

\- multiple queues

\- connection status

\- disconnection

\- reconnection

\- stale/unavailable data

Follow the existing React/component architecture.

**### 8.6 Reconnection and Fallback**

The frontend must behave gracefully if the WebSocket connection fails.

Expected behavior:

\- detect disconnection

\- attempt reconnection according to a reasonable strategy

\- avoid excessive reconnect loops

\- show connection status where appropriate

\- retain sensible last-known data when appropriate

\- fall back to an existing HTTP/API mechanism if the project architecture supports it

Do not hide connection failures from the user or silently produce misleading live data.

**### 8.7 Queue Transition Alerts**

Implement alerts based on meaningful queue-state transitions rather than repeatedly alerting on every measurement.

Examples may include:

\- queue becomes crowded

\- queue returns to normal

\- waiting time crosses a configured threshold

\- queue status changes

Avoid alert spam.

Use existing notification/alert infrastructure if available.

**---**

**## 9. AI/ML Development**

QueueFlow may use AI/ML for queue monitoring and analysis.

When working with AI/ML:

\- Inspect the current implementation first.

\- Do not replace models without understanding the reason.

\- Keep inference logic separate from UI code.

\- Avoid hardcoded machine-specific model paths.

\- Use configuration/environment variables where appropriate.

\- Handle missing models gracefully.

\- Consider CPU/GPU usage and inference latency.

\- Keep real-time processing efficient.

Important performance considerations:

\- inference speed

\- memory usage

\- detection accuracy

\- frame rate

\- CPU/GPU utilization

\- latency

\- scalability

\- reliability

**---**

**## 10. Frontend Development**

When modifying the frontend:

\- Follow the existing framework and component structure.

\- Reuse components.

\- Keep components modular.

\- Avoid unnecessary business logic inside UI components.

\- Maintain responsive design.

\- Handle loading states.

\- Handle empty states.

\- Handle errors.

\- Handle real-time connection states.

\- Follow the existing API/data-fetching approach.

Do not introduce a new frontend framework without explicit justification.

**---**

**## 11. Backend Development**

When modifying the backend:

\- Follow the existing API architecture.

\- Keep business logic separate from routes/controllers where practical.

\- Validate inputs.

\- Handle errors consistently.

\- Avoid exposing sensitive information.

\- Reuse existing services.

\- Preserve API compatibility when possible.

\- Use asynchronous operations where appropriate.

**---**

**## 12. Database**

Before modifying database structures:

1\. Inspect existing models.

2\. Inspect migrations.

3\. Understand relationships.

4\. Avoid destructive changes.

5\. Preserve existing data.

6\. Test migrations.

7\. Update documentation if required.

Never hardcode database credentials.

**---**

**## 13. APIs and WebSockets**

Before adding an API or WebSocket feature:

\- Inspect existing endpoints.

\- Follow established naming conventions.

\- Follow existing request/response formats.

\- Validate inputs.

\- Return useful errors.

\- Avoid breaking existing consumers.

\- Document new endpoints where appropriate.

For WebSockets, also consider:

\- connection lifecycle

\- disconnect handling

\- reconnect behavior

\- message format

\- validation

\- multiple clients

\- server-side exceptions

\- stale connections

**---**

**## 14. Environment Configuration**

Do not hardcode environment-specific values.

Examples:

\`\`\`text

DATABASE\_URL

API\_KEY

MODEL\_PATH

REDIS\_URL

PORT

SECRET\_KEY

\`\`\`

Use the project's existing configuration system.

If \`.env.example\` exists, update it when adding required variables.

Never commit real secrets.

**---**

**## 15. Testing**

Before marking a feature complete:

1\. Run existing tests.

2\. Test the changed functionality.

3\. Check for regressions.

4\. Check server logs.

5\. Verify the application starts.

6\. Verify frontend behavior where applicable.

For Milestone 4, test at minimum:

\- WebSocket connection

\- WebSocket disconnect

\- WebSocket reconnection

\- queue update broadcasting

\- multiple queues

\- simulator behavior

\- measurement persistence

\- frontend live updates

\- fallback behavior

\- transition alerts

Do not remove or disable tests simply because they fail after a change.

**---**

**## 16. Debugging**

When an error occurs:

1\. Read the complete error.

2\. Identify the source file/function.

3\. Inspect related code.

4\. Reproduce the problem.

5\. Make the smallest appropriate fix.

6\. Test the fix.

7\. Check for regressions.

Do not blindly modify unrelated files.

**---**

**## 17. Dependencies**

Before adding a dependency:

\- Check whether the functionality already exists.

\- Check current dependencies.

\- Prefer maintained packages.

\- Avoid duplicate packages.

\- Use the existing package manager.

Update the lockfile when appropriate.

**---**

**## 18. Documentation**

Keep documentation synchronized with the implementation.

Update documentation when significant functionality changes, especially:

\- setup instructions

\- environment variables

\- architecture

\- API endpoints

\- WebSocket endpoints

\- AI/ML setup

\- database setup

\- simulator configuration

\- testing

\- deployment

Never document functionality that has not been verified.

**---**

**## 19. Project State Tracking**

Update this section after major development sessions.

**### Completed**

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
Milestone 10 — Completed & Runtime Verified
Milestone 11 — Completed & Runtime Verified
Milestone 12 — Completed & Runtime Verified
```

**### Current**

```text
Milestone 13 — Final QA & Production Release
```

**### Known Issues**

Update this section with verified issues only.

```text
Two moderate React Router dependency advisories remain. Resolving them requires a breaking React Router v7 upgrade and was previously documented rather than applied unsafely.
Milestone 12 performance baselines are single-process regression checks and are not production capacity guarantees.
```

**### Next Steps**

```text
1. Verify the completed Milestones 1–12 implementation.
2. Execute Milestone 13 end-to-end QA and release verification.
3. Fix only release-blocking defects and regressions.
4. Perform fresh production Docker verification.
5. Finalize documentation and demo/submission readiness.
6. Update AGENTS.md with final results.
7. Commit and push the completed project.
```

**---**

**## 20. Completed Milestone History**

### Milestone 4 — Real-Time Queue Layer

Completed real-time queue functionality including WebSocket updates, connection management, multi-queue simulation, persisted measurements, frontend live updates, reconnection/fallback handling, and transition-based alerts.

### Milestone 5

Completed. Verify the repository and Git history for exact implementation details when needed.

### Milestone 6 — Camera Observation Ingestion

Completed and pushed.

- Added camera configuration and observation ingestion.
- Added `POST /api/cameras/{id}/observations`.
- Validated cameras and persisted measurements.
- Updated queue state.
- Broadcast live queue and alert events.
- Added camera assignment and end-to-end WebSocket broadcast tests.
- 30 backend/AI tests passed; frontend tests and lint passed.
- Commit: `e54ca001 feat: ingest camera queue observations`

### Milestone 7 — Advanced Queue Operations

Completed and pushed.

- Added server-side historical analytics and updated the dashboard.
- Added alert filtering, resolution, and automatic recovery resolution.
- Added multi-camera operational filters.
- Improved wait estimates using observed queue-departure history with a safe configured fallback.
- 36 backend/AI tests passed; frontend tests, lint, and production build passed.
- Commit: `5c440a05 feat: add advanced queue operations`

### Milestone 8 — Production Deployment

Completed and runtime verified.

- Added production Docker Compose services for PostgreSQL, FastAPI, and Nginx-served React.
- Added health checks, startup migrations, and same-origin `/api` and `/ws` proxying.
- Added secure `.env.example`, `.gitignore`, Docker build exclusions, and deployment runbook.
- Production images built successfully.
- Fresh Compose stack health checks passed.
- Direct and proxied API health responses passed.
- WebSocket handshake through Nginx passed.
- Fixed the initial PostgreSQL migration enum-creation defect.
- Temporary containers and database volume were removed after verification.
- Commits: `bb7eb7e3 feat: add production deployment stack` and `25ae2eb2 fix: support PostgreSQL initial migration`

### Milestone 9 — Authentication & Role-Based Access Control

Completed and verified.

- Added Argon2/JWT authentication.
- Added `admin` / `operator` / `viewer` RBAC.
- Added safe administrator bootstrap.
- Added Alembic users migration.
- Protected REST APIs.
- Authenticated `/ws/queues` using a WebSocket subprotocol token.
- Added in-memory frontend authentication, login/logout, protected routes, role-aware navigation, and access-denied UI.
- Backend/AI: 41 tests passed.
- Frontend: 8 tests passed.
- Frontend lint and production build passed.
- Fresh Docker/PostgreSQL migration, login, authenticated WebSocket, and rejected unauthenticated WebSocket verified.
- Updated README, backend documentation, deployment documentation, roadmap, and AGENTS.md.
- Commit: `be7cdd56 feat: add authentication and role-based access control`

### Milestone 11 — Security & Production Hardening

Completed and runtime verified.

- Security headers and production HSTS.
- Configurable login rate limiting with `429` / `Retry-After`.
- Least-privilege Compose hardening and localhost-only PostgreSQL.
- Backup/restore documentation.
- Focused security tests.
- Fresh Docker verification for health, readiness, metrics, headers, logs, rate limiting, and WebSockets.
- Backend/AI: 46 passed.
- Frontend: 8 passed; lint/build passed.
- Two moderate React Router advisories remain and were documented because resolving them requires a breaking v7 upgrade.
- Commit: `fc941999 feat: harden production security`

### Milestone 12 — Performance & Reliability

Current milestone. Implement only the approved scope above after inspecting the actual codebase and establishing performance baselines.

### Milestone 10 — Observability & Production Monitoring

Milestone 10 is defined as the production observability and monitoring phase.

Implement structured logging, health/readiness monitoring, useful operational metrics, production monitoring/troubleshooting support, error visibility, deployment observability, relevant tests, and documentation.

Do not introduce unnecessary infrastructure. Preserve the completed Milestones 1–12.

---

**## 21. Codex Session Handoff**

At the end of every significant Codex session, update this file with:

- Completed work
- Tests and verification performed
- Remaining work
- Known issues
- Commit hash
- Exact next task or milestone state

For Milestone 10, the next task is to implement the approved **Observability & Production Monitoring** scope incrementally after inspecting the existing deployment and application architecture.

Do not claim a milestone is complete unless implementation and verification support that claim.

---

**## 22. New Codex Session Procedure**

Every new Codex session should:

```text
1. Read AGENTS.md.
2. Read README.md and relevant documentation.
3. Inspect the project structure.
4. Run git status.
5. Inspect the current branch.
6. Inspect recent commits.
7. Verify Milestones 1–12 against the actual codebase.
8. Inspect the roadmap and current application, security, performance, and deployment state for Milestone 13.
9. Confirm the Milestone 13 scope: Final QA & Production Release.
10. Present a concise release verification plan based on the actual codebase.
11. Implement only release-blocking fixes and approved QA/release work.
12. Run the complete verification suite and fresh Docker runtime verification.
13. Perform final documentation and demo/submission readiness checks.
14. Update documentation.
15. Update AGENTS.md.
16. Commit changes.
17. Push to GitHub when appropriate.
```

Never restart the project.

Never recreate completed milestones unless a verified bug requires it.

Do not expand Milestone 13 into new feature development without explicit instruction.

---

**## 23. Golden Rule**

The QueueFlow repository is the source of truth.

When continuing work:

**Inspect → Understand → Modify → Test → Document → Commit → Push**

Build on the existing implementation, preserve working functionality, and never invent undefined roadmap scope.
