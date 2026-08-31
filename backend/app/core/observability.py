"""Lightweight, dependency-free application metrics and structured logging."""

import json
import logging
import sys
import time
import uuid
from collections import Counter


logger = logging.getLogger("queueflow")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False


class Metrics:
    def __init__(self) -> None:
        self.requests = Counter()
        self.errors = Counter()
        self.observations = 0
        self.websocket_connections = 0
        self.websocket_active = 0
        self.request_latency_seconds = 0.0

    def snapshot(self) -> dict:
        return {"requests_total": sum(self.requests.values()), "errors_total": sum(self.errors.values()), "observations_total": self.observations, "websocket_connections_total": self.websocket_connections, "websocket_active": self.websocket_active, "request_latency_seconds_total": round(self.request_latency_seconds, 6)}

    def prometheus(self) -> str:
        lines = ["# TYPE queueflow_http_requests_total counter"]
        lines += [f'queueflow_http_requests_total{{status_code="{code}"}} {count}' for code, count in sorted(self.requests.items())]
        lines += ["# TYPE queueflow_http_errors_total counter"]
        lines += [f'queueflow_http_errors_total{{status_code="{code}"}} {count}' for code, count in sorted(self.errors.items())]
        lines += ["# TYPE queueflow_http_request_duration_seconds_total counter", f"queueflow_http_request_duration_seconds_total {self.request_latency_seconds}", "# TYPE queueflow_websocket_connections_active gauge", f"queueflow_websocket_connections_active {self.websocket_active}", "# TYPE queueflow_queue_observations_total counter", f"queueflow_queue_observations_total {self.observations}"]
        return "\n".join(lines) + "\n"


metrics = Metrics()


def log(event: str, **context: object) -> None:
    logger.info(json.dumps({"event": event, **context}, default=str, separators=(",", ":")))


async def request_observability(request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        metrics.errors["500"] += 1
        log("request_error", request_id=request_id, method=request.method, path=request.url.path)
        raise
    elapsed = time.perf_counter() - started
    metrics.requests[response.status_code] += 1
    if response.status_code >= 400:
        metrics.errors[str(response.status_code)] += 1
    metrics.request_latency_seconds += elapsed
    response.headers["X-Request-ID"] = request_id
    log("request_complete", request_id=request_id, method=request.method, path=request.url.path, status_code=response.status_code, duration_ms=round(elapsed * 1000, 2))
    return response
