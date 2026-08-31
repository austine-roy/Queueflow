# QueueFlow — AGENTS.md

## 1. Project Overview

**Project Name:** QueueFlow

**Repository:** `https://github.com/austine-roy/queueflow`

QueueFlow is an AI-based smart queue monitoring and management system designed to monitor queues, estimate queue conditions, assist with queue management, and provide useful information to users and administrators.

The project should be developed as a production-oriented application with a clean architecture, maintainable code, and clear separation between frontend, backend, AI/ML, database, and supporting services where applicable.

---

## 2. Primary Development Rule

**Continue from the existing codebase. Do not recreate the project from scratch.**

Before making changes:

1. Inspect the repository structure.
2. Read this `AGENTS.md`.
3. Read the `README.md` if available.
4. Inspect `git status`.
5. Inspect recent commits.
6. Identify the existing technologies and architecture.
7. Understand the implementation before modifying it.

Preserve existing working functionality unless there is a clear reason to change it.

---

## 3. Git Workflow

The main GitHub repository is:

`https://github.com/austine-roy/queueflow`

Before starting substantial work:

```bash
git status
git branch
git log --oneline -10
```

Before making a commit:

```bash
git status
```

Use clear commit messages, for example:

```text
feat: add queue monitoring dashboard
fix: resolve queue detection issue
refactor: improve queue service
docs: update project documentation
```

Do not commit:

* API keys
* passwords
* authentication tokens
* `.env` files containing secrets
* private credentials
* large generated files
* unnecessary build/cache directories

Always check `.gitignore` before committing.

---

## 4. Development Principles

Follow these principles throughout the project:

### Code Quality

* Keep code readable and maintainable.
* Prefer simple solutions over unnecessary complexity.
* Avoid duplicated logic.
* Use meaningful variable, function, class, and component names.
* Keep functions focused on a single responsibility.
* Do not introduce dependencies without a reason.
* Follow the conventions already established in the repository.

### Existing Architecture

Do not replace the existing architecture simply because another technology or structure may be preferable.

If an architectural change is necessary:

1. Explain why it is needed.
2. Identify affected components.
3. Make the smallest reasonable change.
4. Test the affected functionality.

---

## 5. Working With AI/ML Components

QueueFlow may contain AI/ML components for queue monitoring and analysis.

When working on AI/ML functionality:

* Inspect the existing implementation before changing models.
* Do not replace an existing model without understanding why it was selected.
* Keep model inference separate from UI code where practical.
* Avoid hardcoding model paths or machine-specific paths.
* Make configuration environment-based where appropriate.
* Handle missing models and inference failures gracefully.
* Avoid unnecessary CPU/GPU intensive processing.
* Consider performance and latency for real-time queue monitoring.

When optimizing AI functionality, consider:

* inference speed
* memory usage
* detection accuracy
* frame processing rate
* CPU/GPU utilization
* scalability
* reliability

---

## 6. Queue Monitoring

The core purpose of QueueFlow is queue monitoring and management.

Queue-related functionality should consider:

* number of people in a queue
* queue length
* waiting time estimation
* queue status
* service counters
* queue changes over time
* user notifications where implemented
* administrator monitoring
* historical queue information where implemented

Do not assume a feature already exists. Inspect the codebase first.

---

## 7. Frontend Development

When modifying the frontend:

* Follow the existing UI framework and component structure.
* Reuse existing components where possible.
* Keep components modular.
* Avoid putting business logic unnecessarily inside presentation components.
* Maintain responsive design.
* Handle loading, empty, and error states.
* Keep API calls organized according to the existing project structure.
* Do not introduce a new frontend framework unless explicitly required.

---

## 8. Backend Development

When modifying the backend:

* Follow the existing API architecture.
* Keep business logic separate from routing/controllers where practical.
* Validate user input.
* Handle errors consistently.
* Avoid exposing sensitive information.
* Keep database operations organized.
* Use asynchronous operations where appropriate.
* Maintain backward compatibility with existing frontend/API consumers when possible.

---

## 9. Database

When working with the database:

1. Inspect the existing schema/models first.
2. Do not delete existing data or tables without explicit approval.
3. Use migrations if the project already uses migrations.
4. Keep database configuration outside source code when appropriate.
5. Avoid hardcoded credentials.
6. Test schema changes against the existing application.

---

## 10. APIs

Before modifying or creating an API:

* Inspect existing endpoints.
* Follow existing naming conventions.
* Follow the existing request/response format.
* Validate inputs.
* Return useful error responses.
* Avoid breaking existing clients.

Document new APIs when appropriate.

---

## 11. Environment Configuration

Environment-specific values should not be hardcoded.

Examples include:

```text
DATABASE_URL
API_KEY
MODEL_PATH
REDIS_URL
PORT
SECRET_KEY
```

Use the project's existing environment/configuration mechanism.

If an `.env.example` file exists, update it when adding new required environment variables.

Never commit actual secrets.

---

## 12. Testing

Before considering a feature complete:

1. Run the existing tests.
2. Test the changed functionality.
3. Check for obvious regressions.
4. Check logs/errors.
5. Verify the application starts successfully.

Use the project's existing testing framework.

Do not remove or disable tests simply because they fail after a change.

If a test fails:

* determine the cause
* fix the implementation when appropriate
* update the test only when the expected behavior has genuinely changed

---

## 13. Debugging

When encountering an error:

1. Read the complete error message.
2. Identify the originating file/function.
3. Inspect related code.
4. Reproduce the problem if possible.
5. Make the smallest appropriate fix.
6. Test the fix.

Do not blindly modify multiple unrelated files.

Avoid temporary hacks unless they are clearly marked and necessary.

---

## 14. Dependency Management

Before adding a dependency:

* Check whether the functionality already exists in the project.
* Check existing dependencies.
* Prefer established and maintained packages.
* Avoid adding multiple packages for the same purpose.
* Use the project's existing package manager.

After adding a dependency, update the appropriate lockfile.

---

## 15. Documentation

Keep documentation updated when significant functionality changes.

Important documentation should include:

* project setup
* installation
* environment variables
* running the application
* architecture
* API usage
* AI/ML setup
* database setup
* deployment instructions where applicable

Do not write documentation that claims functionality exists unless it has been verified in the codebase.

---

## 16. Current Project State

**Important:** This section should be updated whenever a major feature is completed.

### Completed

* Initial QueueFlow repository created.
* Project code is being maintained in GitHub.
* Repository: `austine-roy/queueflow`

### Currently Working On

Update this section with the current task.

Example:

```text
Currently working on:
- Queue detection
- Dashboard integration
- Backend API integration
```

### Known Issues

Update this section whenever an important issue is discovered.

```text
No known issues documented yet.
```

### Next Steps

Update this section at the end of significant development sessions.

```text
1. Inspect current implementation.
2. Identify incomplete functionality.
3. Continue the highest-priority feature.
4. Test changes.
5. Commit and push changes.
6. Update AGENTS.md.
```

---

## 17. Codex Session Handoff

At the end of a significant Codex session, update this file with:

### What was changed

List the features, files, and important modifications.

### What works

List functionality that has been tested successfully.

### What remains

List unfinished features and known problems.

### Next recommended task

Clearly state what the next Codex session should work on.

Example:

```text
Session Handoff

Completed:
- Implemented queue detection API.
- Added queue status endpoint.
- Connected dashboard to backend.

Tested:
- Backend starts successfully.
- Queue API returns expected response.

Remaining:
- Improve waiting-time estimation.
- Add error handling to dashboard.
- Add historical queue statistics.

Next Task:
Implement waiting-time estimation using the existing queue data.
```

---

## 18. New Codex Session Procedure

When a new Codex session starts, follow this sequence:

```text
1. Read AGENTS.md.
2. Inspect README.md.
3. Inspect project structure.
4. Run git status.
5. Inspect recent commits.
6. Identify the current project state.
7. Read the relevant source files.
8. Understand the existing implementation.
9. Continue the current task.
10. Test the changes.
11. Update AGENTS.md if the project state changed.
12. Commit the completed work.
13. Push to GitHub when appropriate.
```

Never assume that the previous session completed a task merely because it is mentioned in documentation. Verify the actual code.

---

## 19. Important Rule for Future Codex Sessions

**Do not start over.**

The repository and its Git history are the source of truth.

When continuing work:

> Inspect → Understand → Modify → Test → Document → Commit → Push

Preserve working functionality and build incrementally on the existing QueueFlow implementation.

