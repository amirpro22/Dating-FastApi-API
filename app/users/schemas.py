
import datetime
from typing import List
import uuid
from pydantic import BaseModel,EmailStr, validator

from app.exceptions import LikesIsOverException


class SUserAuth(BaseModel):
    email : EmailStr
    password : str



class SUserData(BaseModel):
    user_id : uuid.UUID
    email : str
    gender : str
    likes : int
    dislikes : int 
    last_seen : datetime.datetime
    registered_at : datetime.datetime
    class Config:
        orm_mode = True


class SAncetaProcessing(BaseModel):
    photo_id : uuid.UUID
    owner_id : uuid.UUID
    email : str
    photo_path : str
    class Config:
        orm_mode = True

class SAnceta(BaseModel):
    action_id : uuid.UUID
    photo_id : uuid.UUID
    owner_id : uuid.UUID
    email : str
    photo_path : str
    class Config:
        orm_mode = True


class SAncetaResponse(BaseModel):
    action_id : uuid.UUID
    photo_id : uuid.UUID
    owner_id : uuid.UUID
    email : str
    photo_url : str
    class Config:
        orm_mode = True


class SLiker(BaseModel):
    valuer_id : uuid.UUID
    class Config:
        orm_mode = True


class SLike(BaseModel):
    action_id: uuid.UUID
    valuer_id : uuid.UUID
    email : str
    photo_path: str
    class Config:
        orm_mode = True


class SLikeResponse(BaseModel):
    action_id : uuid.UUID
    valuer_id : uuid.UUID
    email : str
    photo_url: str
    class Config:
        orm_mode = True


class ResponseList(BaseModel):
    response: List[SLikeResponse]
    @validator("response")
    def check_data_length(cls, v):
        if len(v) < 1:
            raise LikesIsOverException
        return v