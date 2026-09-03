"""QueueFlow FastAPI application."""

from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import alerts, analytics, auth, cameras, health, locations, measurements, queues, realtime
from app.core.config import get_settings
from app.core.observability import request_observability
from app.core.security import security_headers
from app.realtime.simulator import SimulatorProvider

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    simulator = SimulatorProvider(settings, realtime.manager)
    task = asyncio.create_task(simulator.run()) if settings.queueflow_simulation_enabled else None
    try:
        yield
    finally:
        simulator.stop()
        if task is not None:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


app = FastAPI(
    title="QueueFlow API",
    version="0.1.0",
    description="Backend API for QueueFlow queue monitoring. Wait times are service-rate estimates, not ML predictions.",
    lifespan=lifespan,
)
app.middleware("http")(request_observability)
app.middleware("http")(security_headers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(auth.users_router, prefix="/api")
app.include_router(locations.router, prefix="/api")
app.include_router(queues.router, prefix="/api")
app.include_router(cameras.router, prefix="/api")
app.include_router(measurements.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(realtime.router)
