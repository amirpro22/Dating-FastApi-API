import time
import uuid
from fastapi import APIRouter, Depends,status
from sqlalchemy import insert
from app.JWTHandler import TokensData
from app.auth.dependencies import get_new_tokens
from app.auth.utils import jwtHandler
from app.auth.dao import AuthDAO
from app.auth.enums import Gender
from app.auth.schemas import SAuthRegistrationParams, SLoginRequest, SLoginResponse, SRegisteredResponse
from app.auth.utils import check_password, hash_password
from app.aws.client import StorageService
from app.database import async_session_maker
from sqlalchemy.sql import text
from app.exceptions import UserAlreadyExistsException, UserIsNotFoundException, InvalidUserPassowrdException
from app.users.dao import UsersDAO

from app.users.models import Users

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/resigter",status_code=status.HTTP_201_CREATED,response_model=SRegisteredResponse)
async def register_user(
    reg_params: SAuthRegistrationParams = Depends(SAuthRegistrationParams)):
    
    user = await UsersDAO.get_user_by_email(email=reg_params.email)
    if not user:
        await AuthDAO.register_user(reg_params)
        return SRegisteredResponse(status="OK")
    else:
        raise UserAlreadyExistsException
    


@router.post("/login",status_code=status.HTTP_200_OK,response_model=SLoginResponse)
async def register_user(
    user_data : SLoginRequest):
    user = await UsersDAO.get_user_by_email(email=user_data.email)
    if user:
        is_password_right = check_password(user.password,user_data.password)
        if is_password_right:
            access_token = jwtHandler.create_access_token(user.user_id)
            refresh_token = jwtHandler.create_refresh_token(user.user_id)
            return SLoginResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type=jwtHandler.get_token_type
            )
        else:
            raise InvalidUserPassowrdException
    else:
        raise UserIsNotFoundException
    

    
@router.post("/refresh",status_code=status.HTTP_200_OK,response_model=SLoginResponse)
async def register_user(
    tokens_data: TokensData = Depends(get_new_tokens)):
    return tokens_data
    