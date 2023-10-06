
import asyncio
import datetime
import json
from typing import List, Union
import uuid
from app.chat.dependencies import validate_action
from app.chat.enums import ActionType
from app.chat.models import Messages
from app.users.utils import get_photo_url
from broadcaster import Broadcast
from fastapi import APIRouter, Depends, Header, Query, Request, WebSocket
from fastapi.responses import HTMLResponse
from starlette.concurrency import run_until_first_complete
from starlette.websockets import WebSocketDisconnect
from app.chat.dao import ChatDAO
from app.chat.schemas import SChatData, SCommonThread, SMessage, SMessageBody, SThreadsData, SWsMessage, SWsTyping
from app.users.models import Users

from app.auth.dependencies import get_current_user, ws_get_current_user,ws_authorization_header
from fastapi import status
from app.config import settings

broadcast = Broadcast(settings.REDIS_URL)
print(settings.REDIS_URL)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/common_thread",response_model=SCommonThread)
async def processing_chat(chatData : SChatData,user : Users = Depends(get_current_user)):
    common_thread = await ChatDAO.get_common_thread(user.user_id,chatData.companion_user_id)
    if common_thread is None:
        common_thread = await ChatDAO.add_common_thread(user_id=user.user_id,
                                        companion_user_id=chatData.companion_user_id)
    return SCommonThread(common_thread_id=common_thread)

@router.get("/threads",response_model=List[SThreadsData])
async def processing_chat(request:Request,limit:int,page:int=0,user : Users = Depends(get_current_user)):
    threads = await ChatDAO.get_threads(user.user_id,limit,offset=limit*page)
    result = [
    SThreadsData(
        user_id=i.user_id,
        thread_id=i.thread_id,
        email=i.email,
        photo_url=await get_photo_url(i.photo_path, request),
        last_message=(await ChatDAO.get_messages(thread_id=i.thread_id,limit=1))[0]
        ) 
        for i in threads]
    return result
    

@router.post("/messages",response_model=List[SMessage])
async def processing_chat(bodyParams : SMessageBody,user : Users = Depends(get_current_user)):
    messages = await ChatDAO.get_messages(
        bodyParams.thread_id,
        bodyParams.limit,
        bodyParams.offset_created_at
    )

    return messages

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,token: str = Depends(ws_authorization_header)):
    await websocket.accept()
    try:
        user = await ws_get_current_user(token)
    except Exception as e:
        await websocket.send_text("ERROR")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION,reason="Authorization failed")
        return
    await run_until_first_complete(
        (chatroom_ws_receiver, {"websocket": websocket}),
        (chatroom_ws_sender, {"websocket": websocket,"user_id" : str(user.user_id)}),)
    
    
    


async def chatroom_ws_receiver(websocket:WebSocket):
    
    async for message in websocket.iter_text():
        json_message = json.loads(message)
        action = validate_action(json_message.get('action'))
        
        if action == ActionType.message.value:
            model = SWsMessage(**json_message)
            chats = await ChatDAO.get_users_by_chat(chat_id=model.dialogId,sender_id=model.sender_id)
            await ChatDAO.add_message(
                message_id=model.message_id,
                user_id=model.sender_id,
                thread_id=model.dialogId,
                message_text=model.message
            )
            await ChatDAO.update_thread(thread_id=model.dialogId,time_now=datetime.datetime.utcnow())
        
        elif action == ActionType.typing.value:
            model = SWsTyping(**json_message)
            chats = await ChatDAO.get_users_by_chat(chat_id=model.dialogId,sender_id=model.sender_id,with_sender=False)

        
        
        
        for chat in chats:
            participant_user_id = str(chat.user_id)
            await broadcast.publish(channel=participant_user_id, message=message)


async def chatroom_ws_sender(websocket:WebSocket,user_id:str):
    async with broadcast.subscribe(channel=user_id) as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)

  