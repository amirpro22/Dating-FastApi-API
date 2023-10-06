from fastapi import FastAPI, WebSocket
from broadcaster import Broadcast
from fastapi.responses import HTMLResponse
from starlette.concurrency import run_until_first_complete
app = FastAPI()

# Используем Redis как backend для pub/sub
broadcast = Broadcast("redis://localhost:6379")

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = "hello"
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://192.168.0.219:8000/chat/ws?user_id=k`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
 
@app.on_event("startup")
async def startup_event():
    await broadcast.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await broadcast.disconnect()

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket,client_id: str):
    await websocket.accept()
    
    await run_until_first_complete(
        (chatroom_ws_receiver, {"websocket": websocket}),
        (chatroom_ws_sender, {"websocket": websocket}),
    )

async def chatroom_ws_receiver(websocket):
    async for message in websocket.iter_text():
        await broadcast.publish(channel="chatroom", message=message)


async def chatroom_ws_sender(websocket):
    async with broadcast.subscribe(channel="chatroom") as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)