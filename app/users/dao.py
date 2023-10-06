


import datetime
from typing import List, Optional
import uuid
from sqlalchemy import insert, join, select, update
from app.dao.base import DB
from app.users.models import History, Photos, Users
from app.users.schemas import SAnceta, SAncetaProcessing, SLike, SLiker
from app.users.enums import Action
from app.database import async_session_maker
from sqlalchemy.orm import Session, Query,aliased,with_expression
class UsersDAO(DB):

    @classmethod
    async def get_user_by_email(cls,email:str) -> Optional[Users]:
        stmt = select(Users).where(Users.email == email)
        res = await cls._scalar_one_or_none(stmt)
        return res
    
    @classmethod
    async def get_user_by_id(cls,user_id:uuid.UUID) -> Optional[Users]:
        stmt = select(Users.user_id,
                      Users.email,
                      Users.gender,
                      Users.likes,
                      Users.dislikes,
                      Users.last_seen,
                      Users.registered_at
                      ).where(Users.user_id == user_id)
        res = await cls._one(stmt)
        return res
    
    @classmethod
    async def get_user_photo(cls,user_id:uuid.UUID) -> Optional[Photos]:
        stmt = select(Photos
                      ).where(Photos.owner_id == user_id,Photos.is_main == True).limit(1)
        res = await cls._scalar_one_or_none(stmt)
        return res

    @classmethod
    async def register_user(
        cls,
        user_id:uuid.UUID,
        email:str,
        password:str,
        gender:str,
        photo_id:uuid.UUID,
        photo_path:str
        ) -> Users:
        stmt_add_user = insert(Users).values(
            user_id = user_id,
            email = email,
            password = password,
            gender = gender
        )
        
        stmt_add_photo = insert(Photos).values(
            photo_id = photo_id,
            owner_id = user_id,
            photo_path = photo_path,
            is_main=True,
            is_active=True
        )
        await cls._execute([stmt_add_user,stmt_add_photo])
        return
    
    @classmethod
    async def get_ancetas_for_user(cls,user_id:uuid.UUID,limit:int) -> List[SAnceta]:
        '''
        SELECT photo_id,photo_path,owner_id,email FROM Photos
        INNER JOIN Users
        ON Photos.owner_id = Users.user_id
        WHERE is_main = True
        AND is_active = True
        AND owner_id != 'e494e71e-2aa0-44f3-807a-631324ae82b7'
        AND photo_id not IN (SELECT photo_id FROM History WHERE valuer_id = 'e494e71e-2aa0-44f3-807a-631324ae82b7')
        ORDER by last_seen DESC
        '''

        
        subquery = select(History.evaluated_user_id).where(History.valuer_id == user_id)
        stmt = select(Photos.photo_id,
                      Photos.photo_path,
                      Photos.owner_id,
                      Users.email).join(Users,Photos.owner_id == Users.user_id).where(
            Photos.is_main == True,
            Photos.is_active == True,
            Photos.owner_id != user_id,
            Photos.owner_id.not_in(subquery)
                      ).order_by(Users.last_seen.desc()).limit(limit)
        
        for_bulk = []
        res = []
        async with async_session_maker() as session:
            async with session.begin():
                session : Session
                result : List[SAncetaProcessing] = (await session.execute(stmt)).all()
                for i in result:
                    history_uuid = uuid.uuid4()
                    res.append(
                        SAnceta(
                        action_id=history_uuid,
                        photo_id=i.photo_id,
                        owner_id=i.owner_id,
                        email=i.email,
                        photo_path=i.photo_path
                        )
                    )
                    for_bulk.append(
                        History(
                        action_id=history_uuid,
                        action=Action.processing.name,
                        seen=False,
                        valuer_id=user_id,
                        evaluated_user_id=i.owner_id)
                    )
                session.add_all(for_bulk)
                await session.commit()
        
        return res
    @classmethod
    async def add_action(cls,
                          action:str,
                          valuer_id:uuid.UUID,
                          evaluated_user_id:uuid.UUID,
                          seen:bool=False
                          ) -> List[SAnceta]:

        stmt_history = insert(History).values(
            action_id = uuid.uuid4(),
            action = action,
            seen = seen,
            valuer_id = valuer_id,
            evaluated_user_id = evaluated_user_id
        )

        stmt_user_action = update(Users).where(
            Users.user_id == evaluated_user_id,
        ).values(
            likes = (1 + Users.likes) if action == Action.like.value else Users.likes,
            dislikes = (1 + Users.dislikes) if action == Action.dislike.value else Users.dislikes
        )
        
        stmt_user_last_seen = update(Users).where(
            Users.user_id == valuer_id
        ).values(
            last_seen = datetime.datetime.utcnow()
        )

        await cls._execute([stmt_history,stmt_user_action,stmt_user_last_seen])
        


    @classmethod
    async def update_action(cls,
                          action_id:uuid.UUID,
                          action:str
                          ) -> List[SAnceta]:

        stmt_history = update(History).where(
            History.action_id == action_id
        ).values(
            action=action,
            action_time=datetime.datetime.utcnow()
        )

        await cls._execute([stmt_history])
    
    @classmethod
    async def update_action_seen(cls,
                          action_id:uuid.UUID,
                          seen:bool
                          ) -> List[SAnceta]:

        stmt_history = update(History).where(
            History.action_id == action_id
        ).values(
            seen=seen,
            action_time=datetime.datetime.utcnow()
        )

        await cls._execute([stmt_history])
        

    
    @classmethod
    async def get_likes(cls,
                          user_id:uuid.UUID,
                          limit:int,
                          offset:int
                          ) -> List[SLike]:

        '''
        WITH upater AS (UPDATE History
SET seen = true
WHERE action_id IN 
	(SELECT action_id FROM History 
	 WHERE evaluated_user_id = '08a7ff80-9b16-4e44-967b-9fa955f7608d'
	 AND seen = false
	 AND action = 'like'
	 LIMIT 3)
RETURNING valuer_id)

SELECT users.email,valuer_id FROM upater
INNER JOIN Users ON (upater.valuer_id = Users.user_id) 
'''
        
        sub_stmt = select(History.action_id,History.valuer_id,Photos.photo_path,Users.email).where(
            History.evaluated_user_id == user_id,
            History.seen == False,
            History.action == Action.like.value
        ).join(
            Photos,Photos.owner_id == History.valuer_id
        ).join(
            Users,Users.user_id == History.valuer_id
        ).order_by(
            History.action_time.desc()
        ).offset(offset).limit(limit)
        
        stmt_update = update(History).values(
            seen = True
        ).where(
            History.action_id.in_(sub_stmt)
        ).returning(History.valuer_id)


        
        # res = []
        updated_result = await cls._all(sub_stmt)
        # for i in updated_result:
        #     user = await cls.get_user_by_id(i.valuer_id)
        #     photo = await cls.get_user_photo(user.user_id)
        #     like = SLike(valuer_id=i.valuer_id,email=user.email,photo_path=photo.photo_path)
        #     res.append(like)
        
        return updated_result
    

    