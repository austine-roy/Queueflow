# API documentation

The interactive API contract is available from the running backend at `/docs`. The principal resources are authentication, accounts, health, queues, queue measurements, alerts, and cameras.

## Authentication and authorization

`POST /api/auth/login` returns a bearer JWT and the current account after verifying an Argon2 password hash. Send that JWT in `Authorization: Bearer <token>` for protected API calls. `GET /api/auth/me` returns the active account, and `POST /api/auth/logout` returns `204`; the browser clears its in-memory token.

Missing/invalid credentials return `401`; valid credentials without the required role return `403`. Admins have full management access, operators can perform daily measurement/observation/alert operations, and viewers have read-only queue, camera, alert, and analytics access. `/api/users` is administrator-only.

`/ws/queues` is also protected. Pass the token as the WebSocket subprotocol `queueflow.jwt.<token>` (not as a URL query parameter).

## Camera observation ingestion

`POST /api/cameras/{camera_id}/observations` accepts a completed AI observation:

```json
{
  "person_count": 12,
  "density": 0.6
}
```

The camera must be active and assigned to a queue. On success, QueueFlow persists a queue measurement, updates the queue state, and broadcasts a `queue_update` event on `/ws/queues`; a queue transition can produce a subsequent `alert` event. A missing camera returns `404`; inactive or unassigned cameras return `409`.

Use `POST /api/cameras` to configure a camera. A camera's `queue_id`, when present, must reference a queue at its `location_id`.

## Advanced operations

- `GET /api/analytics/queues?measurement_limit=200` returns each queue's historical measurements, peak count, average wait time, and latest measurement timestamp.
- `GET /api/alerts?active=true&queue_id=<id>` filters alerts by lifecycle and queue.
- `POST /api/alerts/{alert_id}/resolve` resolves an active alert. Queue recovery also resolves its active transition alerts automatically.
- `GET /api/cameras?location_id=<id>&queue_id=<id>&active=true` filters a multi-camera deployment.
