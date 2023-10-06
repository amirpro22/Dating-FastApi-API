import datetime

from fastapi import FastAPI

from app.chat.router import broadcast

from app.users.router import router as router_users
from app.auth.router import router as router_auth
from app.chat.router import router as router_chat




app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await broadcast.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await broadcast.disconnect()


app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_chat)

