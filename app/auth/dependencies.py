



from typing import Annotated, List
import uuid
from fastapi import Depends, File, Form, Header, Request, UploadFile, WebSocket
from app.JWTHandler import TokensData

from app.auth.enums import Gender
import filetype
from app.exceptions import EntityFormatException, InvalidGenderException, CredentialException
from fastapi.security import OAuth2PasswordBearer
from app.auth.utils import jwtHandler
from app.users.dao import UsersDAO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def validate_gender(gender: str = Form(..., description=f"Aviables values for gender: {Gender.list()}")):
    if gender not in Gender.list():
        raise InvalidGenderException
    return gender


def validate_photo(photo:UploadFile = File(...)) -> UploadFile:
    is_image = filetype.is_image(photo.file)
    if not is_image:
        raise EntityFormatException
    return photo
    

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwtHandler.verify_access_token(token)
    user_id: str = payload.user_id
    
    user = await UsersDAO.get_user_by_id(user_id)
    if user is None:
        raise CredentialException
    return user

async def ws_get_current_user(token:str):
    try:
        payload = jwtHandler.verify_access_token(token)
    except Exception:
        raise CredentialException
    user_id: str = payload.user_id
    
    user = await UsersDAO.get_user_by_id(user_id)
    if user is None:
        raise CredentialException
    return user

async def ws_authorization_header(authorization:str = Header(...)):
    authorization = authorization.replace('Bearer ', '')
    return authorization



async def get_new_tokens(token: Annotated[str, Depends(oauth2_scheme)]) -> TokensData:
    tokens_data = jwtHandler.refresh_tokens(token)
    if tokens_data is None:
        raise CredentialException
    
    return tokens_data