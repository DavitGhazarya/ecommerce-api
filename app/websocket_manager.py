from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[int, list[WebSocket]] = {}

    async def connect(self, order_id: int, websocket: WebSocket):
        await websocket.accept()

        if order_id not in self.connections:
            self.connections[order_id] = []

        self.connections[order_id].append(websocket)

    def disconnect(self, order_id: int, websocket: WebSocket):
        if order_id in self.connections:
            if websocket in self.connections[order_id]:
                self.connections[order_id].remove(websocket)

            if not self.connections[order_id]:
                del self.connections[order_id]

    async def send_order_update(
        self,
        order_id: int,
        message: dict
    ):
        if order_id not in self.connections:
            return

        for websocket in self.connections[order_id]:
            await websocket.send_json(message)


manager = ConnectionManager()   