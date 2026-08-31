# API documentation

The interactive API contract is available from the running backend at `/docs`. The principal resources are health, queues, queue measurements, alerts, and cameras.

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
