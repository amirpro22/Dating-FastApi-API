


from typing import Any, List, Optional

from app.database import async_session_maker
from sqlalchemy.orm import Session, Query

class DB:
    
    @classmethod
    async def _scalar_one_or_none(cls,query: Query):
        async with async_session_maker() as session:
            session : Session
            result = (await session.execute(query)).scalar_one_or_none()
            return result
    
    @classmethod
    async def _one(cls,query: Query):
        async with async_session_maker() as session:
            session : Session
            result = (await session.execute(query)).first()
            return result
    
    @classmethod
    async def _scalar(cls,query: Query):
        async with async_session_maker() as session:
            session : Session
            result = (await session.execute(query)).scalar()
            return result

    @classmethod
    async def _all(cls,query) -> List[Any]:
        async with async_session_maker() as s:
            s : Session
            r = await s.execute(query)
        return r.all()

    @classmethod
    async def _all_and_commit(cls,query) -> List[Any]:
        async with async_session_maker() as s:
            s : Session
            r = await s.execute(query)
            await s.commit()
        return r.all()

    @classmethod
    async def _execute(cls,query_list:List[Query]):
        async with async_session_maker() as session:
            async with session.begin():
                for i in query_list:
                    await session.execute(i)
                await session.commit()

    # @classmethod
    # async def _execute_and_bulk(cls,execute_query:Query,return_query:Query) -> List[Any]:
    #     async with async_session_maker() as session:
    #         session : Session
    #         result : SAnceta = (await session.execute(return_query)).all()

    #         await session.commit()
    #     return result