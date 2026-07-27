from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket_manager import manager


router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/orders/{order_id}")
async def websocket_order(
    websocket: WebSocket,
    order_id: int
):
    await manager.connect(order_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(order_id, websocket)