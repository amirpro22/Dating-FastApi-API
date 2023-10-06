import datetime
from typing import Optional
import uuid
from fastapi import Query
from pydantic import BaseModel

from app.chat.enums import ActionType



class SWsMessage(BaseModel):
    message_id : uuid.UUID
    action : ActionType 
    sender_id : uuid.UUID
    dialogId : uuid.UUID
    message : str

class SWsTyping(BaseModel):
    action : ActionType 
    sender_id : uuid.UUID
    dialogId : uuid.UUID
    typing : bool

class SParticipant(BaseModel):
    participant_id = uuid.UUID
    thread_id = uuid.UUID
    user_id = uuid.UUID


class SChatData(BaseModel):
    companion_user_id : uuid.UUID
    

class SCommonThread(BaseModel):
    common_thread_id : uuid.UUID
    class Config:
        orm_mode = True

class SThreadsDataFromDb(BaseModel):
    user_id : uuid.UUID
    thread_id : uuid.UUID
    email : str
    photo_path : str
    class Config:
        orm_mode = True

class SMessage(BaseModel):
    message_id : uuid.UUID
    thread_id : uuid.UUID
    user_id : uuid.UUID
    text : str
    created_at : datetime.datetime
    updated_at : datetime.datetime
    deleted_at : Optional[datetime.datetime]
    class Config:
        orm_mode = True

class SThreadsData(BaseModel):
    user_id : uuid.UUID
    thread_id : uuid.UUID
    email : str
    photo_url : str
    last_message : SMessage
    



class SMessageBody(BaseModel):
    thread_id:uuid.UUID
    limit:int
    offset_created_at: Optional[datetime.datetime]
    class Config:
        orm_mode = True

