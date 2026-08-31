"""WebSocket connection registry, independent of queue business logic."""

from fastapi import WebSocket
from typing import Optional


class WebSocketManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, subprotocol: Optional[str] = None) -> None:
        if subprotocol is None:
            await websocket.accept()
        else:
            await websocket.accept(subprotocol=subprotocol)
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, event: dict) -> None:
        for connection in list(self.active_connections):
            try:
                await connection.send_json(event)
            except Exception:
                self.disconnect(connection)


manager = WebSocketManager()
