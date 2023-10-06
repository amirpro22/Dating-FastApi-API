
import time
from typing import Optional
from fastapi import Depends
import jwt
from jwt import exceptions
from pydantic import BaseModel
from fastapi.security import HTTPBearer
from enum import Enum

from app.exceptions import CredentialException, TokenExpiredException


class PayloadSchema(BaseModel):
    user_id : str
    exp : int

class TokensData(BaseModel):
    access_token : str
    refresh_token: str
    token_type: str




class JwtHandler:
        
    __algorithm = None
    __access_secret_key = None
    __refresh_secret_key = None
    expire_access_token_minutes = None
    expire_refresh_token_minutes = None
    token_type = None
    bearer = HTTPBearer()
    
    def __init__(self,access_secret_key:str,refresh_secret_key:str,algorithm:str='HS256',expire_access_token_minutes:int=60*60,expire_refresh_token_minutes:int=60*60*24*14,token_type="Bearer"):
        self.__algorithm = algorithm
        self.__access_secret_key = access_secret_key
        self.__refresh_secret_key = refresh_secret_key
        self.expire_access_token_minutes = expire_access_token_minutes
        self.expire_refresh_token_minutes = expire_refresh_token_minutes
        self.token_type = token_type

    @property
    def get_token_type(self) -> str:
        return self.token_type

    def create_access_token(self, user_id:int):
        payload = PayloadSchema(
            user_id=str(user_id),
            exp=int(time.time()) + self.expire_access_token_minutes,
        )
        payload = payload.dict()
        print(payload)
        token = jwt.encode(payload, self.__access_secret_key, algorithm=self.__algorithm)
        print(token)
        return token
    
    def create_refresh_token(self, user_id:int):
        payload = PayloadSchema(
            user_id=str(user_id),
            exp=int(time.time()) + self.expire_refresh_token_minutes,
        )
        payload = payload.dict()
        token = jwt.encode(payload, self.__refresh_secret_key, algorithm=self.__algorithm)
        return token
    
    def verify_access_token(self, token: str = Depends(bearer)) -> PayloadSchema:
        try:
            data = jwt.decode(token, self.__access_secret_key, algorithms=[self.__algorithm])
            payload = PayloadSchema.parse_obj(data)
            return payload
        except exceptions.ExpiredSignatureError:
            raise TokenExpiredException
        except exceptions.InvalidSignatureError:
            raise CredentialException
    
    def verify_refresh_token(self, token: str = Depends(bearer)) -> PayloadSchema: # ?
        try:
            data = jwt.decode(token, self.__refresh_secret_key, algorithms=[self.__algorithm])
            payload = PayloadSchema.parse_obj(data)
            return payload
        except exceptions.ExpiredSignatureError:
            raise TokenExpiredException
        except exceptions.InvalidSignatureError:
            raise CredentialException
        
    def refresh_tokens(self,refresh_token:str) -> TokensData:
        try:
            payload = self.verify_refresh_token(refresh_token)

            new_access_token = self.create_access_token(payload.user_id)
            new_refresh_token = self.create_refresh_token(payload.user_id)
            return TokensData(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                token_type=self.token_type
            )
        except Exception as e:
            print(e)
            raise CredentialException

    