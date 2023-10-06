



import datetime
from pyexpat.errors import messages
from typing import List, Optional
import uuid
from fastapi import WebSocket
from sqlalchemy import func, insert, join, select, update,case,and_
from app.chat.models import Messages, Participants,Threads
from app.chat.schemas import SMessage, SParticipant, SCommonThread, SThreadsData, SThreadsDataFromDb
from app.dao.base import DB
from app.redis import redis_pool
import json
from app.users.models import Photos, Users
from app.users.utils import get_photo_url

class ChatDAO(DB):

    
    @classmethod
    def get_user_conn_key(cls,user_id:str) -> str:
        return f"WEBSOCKET_CONN_{user_id}"

    @classmethod
    async def set_user_wesocket(cls,user_id:str,webscoket:WebSocket):
        print(webscoket)
        KEY = cls.get_user_conn_key(user_id)
        serialazed_websocket = str(webscoket)
        await redis_pool.set(KEY,serialazed_websocket)

    
    @classmethod
    async def get_user_wesocket(cls,user_id:str):
        KEY = cls.get_user_conn_key(user_id)
        webSocket = await redis_pool.get(KEY)
        WebSocket
    
    @classmethod
    async def get_users_by_chat(cls,chat_id:uuid.UUID,sender_id:uuid.UUID,with_sender:bool=True) -> List[Participants]:
        if with_sender:
            query = select("*").where(Participants.thread_id == chat_id) # , Participants.user_id != sender_id
        else:
            query = select("*").where(Participants.thread_id == chat_id,Participants.user_id != sender_id)
        
        res = await DB._all(query)
        return res
    
    @classmethod
    async def get_common_thread(cls,user_id:uuid.UUID,companion_user_id:uuid.UUID) -> uuid.UUID:
        subquery_user1 = func.sum(case((Participants.user_id == user_id, 1), else_=0))
        subquery_user2 = func.sum(case((Participants.user_id == companion_user_id, 1), else_=0))

        query = select(Participants.thread_id).group_by(Participants.thread_id).having(subquery_user1 > 0, subquery_user2 > 0)
        
        res = await DB._scalar(query)
        
        return res
    
    @classmethod
    async def add_common_thread(cls,user_id:uuid.UUID,companion_user_id:uuid.UUID) -> uuid.UUID:
        thread_id = uuid.uuid4()
        query_one = insert(Threads).values(
            thread_id = thread_id
        )
        query_two = insert(Participants).values(
            thread_id = thread_id,
            user_id = user_id
        )
        query_three = insert(Participants).values(
            thread_id = thread_id,
            user_id = companion_user_id
        )
        await DB._execute([query_one,query_two,query_three])
        
        return thread_id
    
    @classmethod
    async def add_message(cls,message_id:uuid.UUID,user_id:uuid.UUID,thread_id:uuid.UUID,message_text:str) -> uuid.UUID:
        query = insert(Messages).values(
            message_id=message_id,
            thread_id=thread_id,
            user_id=user_id,
            text=message_text
        )
        await DB._execute([query])
        
        return thread_id
    
    @classmethod
    async def get_threads(cls,user_id:uuid.UUID,limit: int=10, offset:int=0) -> List[SThreadsDataFromDb]:
        
        sub_query = select(Messages.thread_id).distinct(
            Messages.thread_id).join(
            Participants,Messages.thread_id == Participants.thread_id
            ).where(Participants.user_id == user_id)
        
        query = select(Participants.user_id,
                       Participants.thread_id,
                       Users.email,
                       Photos.photo_path).join(
            Users,Users.user_id == Participants.user_id
                       ).join(
            Photos,Photos.owner_id == Participants.user_id
                       ).join(
            Threads,Threads.thread_id == Participants.thread_id
                       ).where(
            Participants.thread_id.in_(sub_query),
            Participants.user_id != user_id
            ).order_by(Threads.updated_at.desc()).offset(offset).limit(limit)
        
        result = await DB._all(query)
        return result
    
    @classmethod
    async def get_messages(cls,thread_id:uuid.UUID,limit:int,offset_created_at:datetime.datetime=None) -> List[SMessage]:
        
        if offset_created_at:
            print(offset_created_at)
            query = select("*").where(
                Messages.thread_id == thread_id,
                Messages.created_at < offset_created_at
            ).order_by(
                Messages.created_at.desc()
            ).limit(limit)
        else:
            query = select("*").where(
                Messages.thread_id == thread_id
            ).order_by(
                Messages.created_at.desc()
            ).limit(limit)

        result = await DB._all(query)
        return result
    @classmethod
    async def update_thread(cls,thread_id:uuid.UUID,time_now:datetime.datetime) -> List[SThreadsDataFromDb]:
        
        query = update(Threads).where(Threads.thread_id == thread_id).values(updated_at = time_now)
        
        result = await DB._execute([query])
        return result
    