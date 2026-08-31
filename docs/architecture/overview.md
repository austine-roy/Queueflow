# QueueFlow architecture

## System boundaries

The system is centered on a **queue**, not a camera. Cameras are measurement sources attached to a location or queue; the backend is the source of truth for queue configuration and state.

```text
Video/camera → detection → tracking → queue-region measurement
             → density calculation → backend ingestion
             → persistence + status/wait estimation → REST/WebSocket → dashboard
```

## Module responsibilities

| Module | Responsibility | Does not own |
| --- | --- | --- |
| AI | Detection, tracking, region measurements, density inputs | API state or database writes |
| Backend | Validation, status thresholds, wait estimation, APIs | Vendor-specific vision logic |
| Database | Durable queue configuration and historical measurements | Business rules |
| Frontend | Live operations dashboard and admin controls | Queue calculations |

## Key decisions

1. **Replaceable vision adapters:** detection models remain behind a module boundary so a mock source, YOLO, or another detector can be substituted.
2. **Measured vs. estimated data:** person counts and density are measurements; initial wait time is a transparent service-rate estimate, not an AI prediction.
3. **Configurable status:** NORMAL, BUSY, CROWDED, CRITICAL, and CLOSED will be derived from queue-specific thresholds rather than scattered constants.
4. **Incremental delivery:** local service behavior and tests precede Docker and real-camera integration.
