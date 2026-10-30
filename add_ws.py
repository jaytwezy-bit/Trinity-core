ws_code = '''
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/live-stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Trinity Stream Event: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
'''

with open("server.py", "r") as f:
    content = f.read()

if "/ws/live-stream" not in content:
    with open("server.py", "a") as f:
        f.write(ws_code)
    print("[SUCCESS] WebSocket live-stream endpoint added.")
else:
    print("[INFO] WebSocket endpoint already exists.")
