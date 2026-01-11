from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..websocket_manager import manager

router = APIRouter(tags=["websocket", "status"])


@router.websocket("/status")
async def websocket_server_status(websocket: WebSocket):
    """
    WebSocket endpoint udostępniający status serwera.

    Args:
        websocket (WebSocket): Obiekt WebSocket reprezentujący połączenie z klientem.
    """

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text() # utrzymuje połączenie aktywne

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)