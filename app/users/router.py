from typing import List
import uuid
from fastapi import APIRouter,Depends, File, Query, Request, Response
from fastapi.responses import StreamingResponse
from sqlalchemy import insert
from app.auth.dependencies import get_current_user
from app.aws.client import StorageService
from app.database import async_session_maker
from sqlalchemy.sql import text
from app.exceptions import ActionAddExecption, AwsException, AwsNoSuchKeyException, QuestionnairesIsOverException
from app.users.dao import UsersDAO
from app.users.dependencies import validate_action
from botocore.exceptions import ClientError
from app.users.models import Users
from app.users.schemas import ResponseList, SAnceta, SAncetaResponse, SLike, SLikeResponse, SLiker, SUserData
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_dbapi
from sqlalchemy.exc import IntegrityError
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me",response_model=SUserData)
async def get_me(user : Users = Depends(get_current_user)):
    return user


@router.get("/my_photo")
async def get_photo(user : Users = Depends(get_current_user)):
    user_photo = await UsersDAO.get_user_photo(user.user_id)

    file = await StorageService.async_download_fileobj(user_photo.photo_path)
    return Response(content=file, media_type="image/png")


@router.get("/accounts",response_model=List[SAncetaResponse])
async def get_ancetas(
        request:Request,
        user : Users = Depends(get_current_user),
        limit : int = Query(ge=1,le=30)):
    
    resp = []
    generated = await UsersDAO.get_ancetas_for_user(user.user_id,limit)
    for i in generated:
        photo_path_url = request.url_for("get_specifically_photo",photo_path=i.photo_path)
        resp.append(SAncetaResponse(
            action_id=i.action_id,
            photo_id=i.photo_id,
            owner_id=i.owner_id,
            email=i.email,
            photo_url=(photo_path_url._url).replace('http','https' if '127.0.0.1' not in photo_path_url._url else 'http')
        ))

    if len(resp): # more than 0
        return resp
    else:
        raise QuestionnairesIsOverException


@router.get("/photo/{photo_path}")
async def get_specifically_photo(photo_path : str,user : Users = Depends(get_current_user)):
    try:
        file = await StorageService.async_download_fileobj(photo_path)
        return Response(content=file, media_type="image/png")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise AwsNoSuchKeyException
        else:
            raise AwsException

    

@router.put("/action",status_code=204)
async def update_action(
        action_id:uuid.UUID,
        action:str = Depends(validate_action),
        user : Users = Depends(get_current_user)
    ):
    
    await UsersDAO.update_action(
        action_id=action_id,
        action=action
    )



@router.get("/likes",response_model=List[SLikeResponse])
async def update_action(
        limit:int,
        request:Request,
        page : int = 0,
        user : Users = Depends(get_current_user)
    ):
    
    resp = []
    likes = await UsersDAO.get_likes(user.user_id,limit=limit,offset=limit*page)
    for like in likes:
        photo_path_url = request.url_for("get_specifically_photo",photo_path=like.photo_path)
        resp.append(SLikeResponse(
            action_id=like.action_id,
            valuer_id=like.valuer_id,
            email=like.email,
            photo_url=str(photo_path_url).replace('http','https' if '127.0.0.1' not in photo_path_url._url else 'http')
        )
        )
    
    return resp

    
@router.put("/likes",status_code=204)
async def update_action(
        action_id:uuid.UUID,
        seen:bool=True,
        user : Users = Depends(get_current_user),
    ):
    await UsersDAO.update_action_seen(
        action_id=action_id,
        seen=seen
    )
    
