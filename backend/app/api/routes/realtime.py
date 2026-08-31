"""Queue update WebSocket endpoint."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.config import get_settings
from app.models.enums import UserRole
from app.realtime.websocket_manager import manager
from app.services.auth_service import decode_access_token

router = APIRouter()


@router.websocket("/ws/queues")
async def queue_updates(websocket: WebSocket) -> None:
    requested_protocols = [item.strip() for item in websocket.headers.get("sec-websocket-protocol", "").split(",")]
    auth_protocol = next((item for item in requested_protocols if item.startswith("queueflow.jwt.")), None)
    if auth_protocol is None:
        await websocket.close(code=4401)
        return
    try:
        payload = decode_access_token(auth_protocol.removeprefix("queueflow.jwt."), get_settings())
        if payload["role"] not in {role.value for role in UserRole}:
            raise ValueError("Unknown role")
    except ValueError:
        await websocket.close(code=4401)
        return
    await manager.connect(websocket, auth_protocol)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)
