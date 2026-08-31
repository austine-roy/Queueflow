"""Queue update WebSocket endpoint."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.realtime.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws/queues")
async def queue_updates(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)
